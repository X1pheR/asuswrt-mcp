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
