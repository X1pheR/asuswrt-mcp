from __future__ import annotations

import ast
import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "src" / "asuswrt_mcp" / "server.py"
TOOLS_DOC = ROOT / "docs" / "tools.md"


def _registered_tools() -> set[str]:
    tree = ast.parse(SERVER.read_text(encoding="utf-8"))
    tools: set[str] = set()
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            target = decorator.func if isinstance(decorator, ast.Call) else decorator
            if isinstance(target, ast.Attribute) and target.attr == "tool":
                tools.add(node.name)
                break
    return tools


def test_release_metadata_uses_downstream_identity_consistently() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))

    assert project["name"] == "hypershell-asuswrt-mcp"
    assert server["name"] == "io.github.x1pher/asuswrt-mcp"
    assert server["repository"]["url"] == "https://github.com/X1pheR/asuswrt-mcp"
    assert server["version"] == project["version"]
    assert server["packages"][0]["identifier"] == project["name"]
    assert server["packages"][0]["version"] == project["version"]


def test_public_tool_reference_covers_every_registered_tool_once() -> None:
    registered = _registered_tools()
    text = TOOLS_DOC.read_text(encoding="utf-8")
    documented = re.findall(r"^\| `([^`]+)` \| (Read|Management) \|", text, flags=re.MULTILINE)
    names = [name for name, _ in documented]

    assert len(names) == len(set(names)), "duplicate tool rows in docs/tools.md"
    assert set(names) == registered
    assert len(registered) == 67


def test_readme_explains_downstream_purpose_near_the_top() -> None:
    opening = "\n".join((ROOT / "README.md").read_text(encoding="utf-8").splitlines()[:40])
    assert "Why this downstream exists" in opening
    assert "teefloo/asuswrt-mcp" in opening
    assert "47 to 67 tools" in opening
    assert "Correctness fixes" in opening
    assert "independent downstream" in opening.lower()

    provenance = (ROOT / "UPSTREAM.md").read_text(encoding="utf-8").lower()
    assert "independent downstream" in provenance
    assert "origin" in provenance
    assert "upstream" in provenance
    assert "github fork" not in provenance


def test_public_docs_do_not_embed_homelab_paths_or_runtime_secrets() -> None:
    public_docs = [
        ROOT / "README.md",
        ROOT / "UPSTREAM.md",
        ROOT / "SECURITY.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CHANGELOG.md",
        ROOT / "docs" / "tools.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in public_docs)
    forbidden = (
        "/srv/hypershell",
        "/mcp-data/docker",
        ".runtime-secrets",
        "192.168.18.",
    )
    for value in forbidden:
        assert value not in text


def test_server_manifest_allows_ssh_key_auth_without_password() -> None:
    server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    envs = {item["name"]: item for item in server["packages"][0]["environmentVariables"]}
    assert envs["ASUSWRT_HOST"]["isRequired"] is True
    assert envs["ASUSWRT_SSH_USERNAME"]["isRequired"] is True
    assert envs["ASUSWRT_SSH_PASSWORD"]["isRequired"] is False
    assert envs["ASUSWRT_SSH_PASSWORD"]["isSecret"] is True
    assert envs["ASUSWRT_SSH_KEY_FILE"]["isRequired"] is False


def test_paramiko_dependency_uses_supported_5x_release_line() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    paramiko = next(dep for dep in project["dependencies"] if dep.startswith("paramiko"))
    assert paramiko == "paramiko>=5,<6"
