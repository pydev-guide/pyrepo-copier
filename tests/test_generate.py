import os
import shutil
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from subprocess import run
from typing import Any, Callable

import pytest
import tomli

TEMPLATE = Path(__file__).parent.parent


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@pytest.fixture(scope="session")
def template():
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(TEMPLATE, td, dirs_exist_ok=True)
        run(["git", "-C", td, "add", ".", "-A"])
        run(["git", "-C", td, "commit", "-m", "test"])
        run(["git", "-C", td, "tag", "99.99.99"])
        yield Path(td)


@pytest.fixture
def run_copier(tmp_path: Path):
    def _copier(
        template: Path, dest: Path = tmp_path, git_init: bool = False, **kwargs: Any
    ):
        cmd = ["copier", "copy", "--force"]
        for k, v in kwargs.items():
            cmd.extend(["-d", f"{k}={v}"])
        cmd.extend([str(template), str(dest)])

        run(cmd, check=True)
        if git_init:
            with inside_dir(str(tmp_path)):
                run(["git", "init", "-q"], check=True)
                gitcfg = tmp_path / ".git" / "config"
                gitcfg.touch()
                gitcfg.write_text("[user]\n\tname = Name\n\temail = email@wp.p\n")
                run(["git", "add", "."], check=True)
                run(["git", "commit", "-q", "-m", "init"], check=True)

        return tmp_path

    return _copier


def test_copier(template: Path, run_copier: Callable[..., Path]):
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


def test_bake_and_test(template: Path, run_copier: Callable[..., Path]):
    NAME = "some-project"
    output = run_copier(
        template,
        project_name=NAME,
        git_init=True,
        minimum_python=sys.version_info.minor,  # use current minor version for CI
    )
    with inside_dir(str(output)):
        run(["uv", "run", "pytest"], check=True)


def test_bake_and_build(template, run_copier: Callable[..., Path]):
    output = run_copier(template, git_init=True, minimum_python=sys.version_info.minor)

    with inside_dir(str(output)):
        run(["uv", "run", "check-manifest"], check=True)
        run(["uv", "build"], check=True)
        assert len(list((output / "dist").iterdir())) >= 2


def test_bake_and_pre_commit(template, run_copier: Callable[..., Path]):
    output = run_copier(template, git_init=True)

    assert (output / ".pre-commit-config.yaml").exists()

    with inside_dir(str(output)):
        run(["pre-commit", "autoupdate"], check=True)
        run(["pre-commit", "install"], check=True)
        run(["git", "add", "."], check=True)
        run(["pre-commit", "run", "--all-files"], check=True)


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
    ],
    ids=lambda d: d["mode"],
)
def test_actionlint_on_rendered_workflow(
    template: Path,
    run_copier: Callable[..., Path],
    kwargs: dict[str, Any],
    request: pytest.FixtureRequest,
):
    """Test that the rendered CI workflow passes actionlint validation."""
    # Test with default settings (should not have resolution matrix)
    output = run_copier(template, **kwargs)
    ci_file = output / ".github" / "workflows" / "ci.yml"
    assert ci_file.exists()

    # Run actionlint on default configuration
    run(["actionlint", str(ci_file)], check=True)

    # Verify no resolution matrix in default output
    ci_content = ci_file.read_text(encoding="utf-8")

    # if we're running pytest in verbose mode with -s, print the pyproject.toml content
    if request.config.getoption("-v") and request.config.getoption("-s"):
        print("\n" + ci_content)

    is_custom = kwargs["mode"] == "customize"
    assert ("resolution:" in ci_content) is is_custom
    assert ("[${{ matrix.resolution }}]" in ci_content) is is_custom


@pytest.mark.parametrize(
    "kwargs",
    [
        {"mode": "simple"},
        {"mode": "tooling"},
        {"mode": "customize"},
        {"mode": "customize", "use_mypy": False},
    ],
    ids=lambda d: ",".join(f"{k}={v}" for k, v in d.items()),
)
def test_validate_pyproject_on_rendered_pyproject(
    template: Path,
    run_copier: Callable[..., Path],
    kwargs: dict[str, Any],
    request: pytest.FixtureRequest,
):
    """Test that the rendered pyproject.toml passes validate-pyproject."""
    # Test with default settings (should not have resolution matrix)
    output = run_copier(template, **kwargs)
    pyproj = output / "pyproject.toml"
    assert pyproj.exists()

    # Run validate-pyproject on default configuration
    run(["validate-pyproject", str(pyproj)], check=True)

    # if we're running pytest in verbose mode with -s, print the pyproject.toml content
    content = pyproj.read_text(encoding="utf-8")
    if request.config.getoption("-v") and request.config.getoption("-s"):
        print("\n" + content)

    data = tomli.loads(content)
    tool = data.get("tool", {})
    project = data.get("project", {})
    assert "pytest" in tool
    if kwargs["mode"] == "simple":
        assert "version" in project
        assert "mypy" not in tool
        assert "ruff" not in tool
        assert "ty" not in tool
    elif kwargs["mode"] == "tooling":
        assert "version" not in project
        assert project.get("dynamic") == ["version"]
        assert "mypy" in tool
        assert "ruff" in tool
    elif kwargs["mode"] == "customize":
        assert "ruff" in tool
        if kwargs.get("use_mypy", True) is False:
            assert "mypy" not in tool
            assert "ty" in tool
        else:
            assert "mypy" in tool
            assert "ty" not in tool
