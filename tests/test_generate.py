from __future__ import annotations

import os
import shutil
import sys
import tempfile
from collections.abc import Callable, Iterator
from pathlib import Path
from subprocess import run
from typing import Any

import pytest
import tomli

TEMPLATE = Path(__file__).parent.parent
# environment for subprocesses run inside generated projects:
# - copier's tasks (`git commit`) need a git identity; don't rely on the machine's
# - UV_PYTHON/VIRTUAL_ENV from the outer test environment must not leak into the
#   generated project's `uv sync`, which has its own `requires-python`
ENV = {
    **{k: v for k, v in os.environ.items() if k not in ("UV_PYTHON", "VIRTUAL_ENV")},
    "GIT_AUTHOR_NAME": "Name",
    "GIT_AUTHOR_EMAIL": "email@wp.p",
    "GIT_COMMITTER_NAME": "Name",
    "GIT_COMMITTER_EMAIL": "email@wp.p",
}


@pytest.fixture(scope="session")
def template() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(TEMPLATE, td, dirs_exist_ok=True)
        run(["git", "-C", td, "add", ".", "-A"])
        run(["git", "-C", td, "commit", "-m", "test"], env=ENV)
        run(["git", "-C", td, "tag", "99.99.99"])
        yield Path(td)


@pytest.fixture
def run_copier(tmp_path: Path) -> Callable[..., Path]:
    def _copier(template: Path, dest: Path = tmp_path, **kwargs: Any) -> Path:
        # --trust runs the post-copy tasks (git init, uv sync, commit, prek install)
        cmd = ["copier", "copy", "--force", "--trust"]
        for k, v in kwargs.items():
            cmd.extend(["-d", f"{k}={v}"])
        cmd.extend([str(template), str(dest)])
        run(cmd, check=True, env=ENV)
        return dest

    return _copier


def test_copier(template: Path, run_copier: Callable[..., Path]) -> None:
    NAME = "some-project"
    output = run_copier(
        template,
        author_name="Test Name",
        author_email="test@example.com",
        project_name=NAME,
    )
    prj = tomli.loads((output / "pyproject.toml").read_text())["project"]
    assert prj["name"] == NAME
    assert prj["authors"] == [{"email": "test@example.com", "name": "Test Name"}]
    assert prj["license"] == "BSD-3-Clause"
    assert not any(c.startswith("License ::") for c in prj["classifiers"])
    # tasks ran
    assert (output / ".git").is_dir()
    assert (output / ".venv").is_dir()
    assert (
        not (output / "uv.lock").exists()
        or "uv.lock" in (output / ".gitignore").read_text()
    )


def test_bake_and_test(template: Path, run_copier: Callable[..., Path]) -> None:
    output = run_copier(
        template,
        project_name="some-project",
        minimum_python=sys.version_info.minor,  # use current minor version for CI
    )
    run(["uv", "run", "pytest"], check=True, cwd=output, env=ENV)


def test_bake_and_build(template: Path, run_copier: Callable[..., Path]) -> None:
    output = run_copier(template, minimum_python=sys.version_info.minor)
    run(["uv", "build"], check=True, cwd=output, env=ENV)
    assert len(list((output / "dist").iterdir())) >= 2


@pytest.mark.parametrize("type_checker", ["ty", "mypy"])
def test_bake_and_prek(
    template: Path, run_copier: Callable[..., Path], type_checker: str
) -> None:
    output = run_copier(template, mode="customize", type_checker=type_checker)
    config = (output / ".pre-commit-config.yaml").read_text()
    assert (type_checker in config) and ("zizmor" in config)
    # tasks already ran `prek install`
    assert (output / ".git" / "hooks" / "pre-commit").exists()
    run(["uv", "run", "prek", "run", "--all-files"], check=True, cwd=output, env=ENV)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"mode": "simple"},
        {"mode": "tooling"},
        {
            "mode": "customize",
            "minimum_python": 10,
            "test_lowest_pinned_dependencies": True,
            "test_pre_release": True,
        },
        {"mode": "customize", "minimum_python": 15},
    ],
    ids=lambda d: "-".join(f"{k}={v}" for k, v in d.items()),
)
def test_rendered_workflow(
    template: Path, run_copier: Callable[..., Path], kwargs: dict[str, Any]
) -> None:
    """The rendered CI workflow passes actionlint and zizmor."""
    output = run_copier(template, **kwargs)
    ci_file = output / ".github" / "workflows" / "ci.yml"
    assert ci_file.exists()

    run(["actionlint", str(ci_file)], check=True)
    run(["zizmor", "--offline", str(output / ".github")], check=True)

    ci_content = ci_file.read_text(encoding="utf-8")
    is_lowest = kwargs.get("test_lowest_pinned_dependencies", False)
    assert ("resolution:" in ci_content) is is_lowest
    assert ("[${{ matrix.resolution }}]" in ci_content) is is_lowest
    # the test matrix covers every version from the minimum to the latest
    min_py = kwargs.get("minimum_python", 11)
    expected = ", ".join(f'"3.{v}"' for v in range(min_py, 16))
    assert f"python-version: [{expected}]" in ci_content


def test_simple_mode_has_pytest_config(
    template: Path, run_copier: Callable[..., Path]
) -> None:
    output = run_copier(template, mode="simple")
    tool = tomli.loads((output / "pyproject.toml").read_text())["tool"]
    assert "pytest" in tool
    assert "ty" not in tool and "mypy" not in tool and "ruff" not in tool
    assert not (output / ".pre-commit-config.yaml").exists()
