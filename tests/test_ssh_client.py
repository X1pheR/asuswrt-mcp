from __future__ import annotations

import paramiko

from asuswrt_mcp.clients.ssh import AsusRouterSshClient, CommandResult
from asuswrt_mcp.config import Settings


def test_connect_rejects_unknown_host_keys(monkeypatch) -> None:
    observed: dict[str, object] = {}

    class FakeSshClient:
        def load_system_host_keys(self) -> None:
            observed["loaded_system_host_keys"] = True

        def set_missing_host_key_policy(self, policy: object) -> None:
            observed["policy"] = policy

        def connect(self, **kwargs: object) -> None:
            observed["connect_kwargs"] = kwargs

    monkeypatch.setattr(paramiko, "SSHClient", FakeSshClient)

    client = AsusRouterSshClient(Settings(host="192.168.1.1", ssh_username="admin"))
    client.connect()

    assert observed["loaded_system_host_keys"] is True
    assert isinstance(observed["policy"], paramiko.RejectPolicy)


def test_get_nvram_many_separates_empty_values_without_router_newline(monkeypatch) -> None:
    client = AsusRouterSshClient(Settings(host="192.168.1.1", ssh_username="admin"))

    def fake_run(command: str) -> CommandResult:
        # ASUSWRT may emit no newline at all for an empty/missing nvram key.
        # A caller-provided record separator must prevent the next key from
        # becoming the previous key's value.
        if "printf '\\n'" in command:
            stdout = "first=\n\nsecond=value\n"
        else:
            stdout = "first=second=value"
        return CommandResult(command=command, stdout=stdout, stderr="", exit_status=0)

    monkeypatch.setattr(client, "_run_shell", fake_run)

    assert client.get_nvram_many(["first", "second"]) == {
        "first": "",
        "second": "value",
    }


def test_command_deadline_closes_channel_without_retry(monkeypatch) -> None:
    import pytest
    from types import SimpleNamespace
    from asuswrt_mcp.errors import RouterOperationError
    from asuswrt_mcp.clients import ssh as module
    observed = {"closed": False, "calls": 0}
    class Channel:
        def recv_ready(self): return False
        def recv_stderr_ready(self): return False
        def exit_status_ready(self): return False
        def close(self): observed["closed"] = True
    channel = Channel()
    class Transport:
        def exec_command(self, *args, **kwargs):
            observed["calls"] += 1
            return None, SimpleNamespace(channel=channel), None
    client = AsusRouterSshClient(Settings(host="192.168.1.1", ssh_username="admin", timeout_seconds=1))
    client._client = Transport()
    ticks = iter([0.0, 2.0])
    monkeypatch.setattr(module.time, "monotonic", lambda: next(ticks))
    with pytest.raises(RouterOperationError) as error:
        client.run_command("service restart_logger")
    assert error.value.code == "ssh_command_timeout"
    assert observed == {"closed": True, "calls": 1}


def test_command_drains_output_before_waiting_for_exit() -> None:
    from types import SimpleNamespace
    class Channel:
        output = [b"state=ready\n"]
        errors = [b"diagnostic\n"]
        def recv_ready(self): return bool(self.output)
        def recv_stderr_ready(self): return bool(self.errors)
        def recv(self, _size): return self.output.pop(0)
        def recv_stderr(self, _size): return self.errors.pop(0)
        def exit_status_ready(self): return not self.output and not self.errors
        def recv_exit_status(self):
            assert self.exit_status_ready()
            return 0
    channel = Channel()
    class Transport:
        def exec_command(self, *args, **kwargs):
            return None, SimpleNamespace(channel=channel), None
    client = AsusRouterSshClient(Settings(host="192.168.1.1", ssh_username="admin"))
    client._client = Transport()
    result = client.run_command("bounded read")
    assert result.stdout == "state=ready"
    assert result.stderr == "diagnostic"
