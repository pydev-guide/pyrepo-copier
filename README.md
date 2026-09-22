# Python Package Template

This is a [copier](https://copier.readthedocs.io/) template for a python package.

Feel free to use it as a launching point for your next project!

## How to use it

### 1. Create a new repo

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and
[git](https://git-scm.com/) installed.  Then run `copier`, passing in the
template url and the desired output directory (usually the name of your new
package):

```sh
uvx copier copy --trust gh:pydev-guide/pyrepo-copier your-package-name
```

> `--trust` is required because the template runs a few
> [tasks](https://copier.readthedocs.io/en/stable/configuring/#tasks) after
> generating the project: `git init`, `uv sync`, an initial commit, and
> `prek install`.  Omit it if you'd rather do those yourself (copier will error;
> see the `_tasks` section in `copier.yml` for exactly what they do).

### 2. Run the tests

```sh
cd <your-package-name>
uv run pytest
```

### 3. Lint

If you selected pre-commit (or used the "full-featured" default), hooks are
installed via [prek](https://prek.j178.dev/) (a fast, drop-in replacement for
[pre-commit](https://pre-commit.com/)) and run on every commit.  To run them
manually:

```sh
uv run prek run --all-files
```

### 4. Upload to GitHub

If you have the [GitHub CLI](https://cli.github.com/) installed, and would like
to create a GitHub repository for your new package:

```sh
gh repo create --source=. --public --remote=origin --push
```

> alternatively, you can follow github's guide for
> [adding a local repository to github](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github#adding-a-local-repository-to-github-using-git)

## Next Steps

- Enable [Dependabot](https://docs.github.com/en/code-security/dependabot) on
  the repo: it keeps both GitHub Actions and pre-commit hook versions up to
  date (see `.github/dependabot.yml`).
- Follow links below for more info on the included tools (pay particular
  attention to [hatch](https://hatch.pypa.io/) and
  [ruff](https://docs.astral.sh/ruff/)).
- See how to [Deploy to PyPI](#deploying-to-pypi) below.

## Stuff included

- [PEP 517](https://peps.python.org/pep-0517/) build system with [hatch
  backend](https://hatch.pypa.io/)
  - build with `uv build`, [*not* `python
    setup.py`](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html)!
- [PEP 621](https://peps.python.org/pep-0621/) metadata and [PEP
  639](https://peps.python.org/pep-0639/) license expression in
  `pyproject.toml`
  - *all* additional configurables are also in `pyproject.toml`, with
  links to documentation
- [PEP 735](https://peps.python.org/pep-0735/) dependency groups (`test`,
  `dev`), installed with `uv sync`
- uses `src` layout ([How come?](https://hynek.me/articles/testing-packaging/))
- git tag-based versioning with [hatch-vcs](https://github.com/ofek/hatch-vcs)
- autodeploy to PyPI on tagged commit via [trusted
  publishing](https://docs.pypi.org/trusted-publishers/). See [Deploying to
  PyPI](#deploying-to-pypi) below.
- Testing with [pytest](https://docs.pytest.org/)
- CI & testing with [github actions](https://docs.github.com/en/actions)
  - actions are pinned to commit SHAs and updated by dependabot
  - minimal `permissions` per job
- GitHub action
  [cron-job](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
  running tests against dependency pre-releases (using `--pre` to install
  dependencies).
- pre-commit hooks, run with [prek](https://prek.j178.dev/) locally and via
  [prek-action](https://github.com/j178/prek-action) in CI:
  - [ruff](https://docs.astral.sh/ruff/) - amazing linter and
    formatter. Takes the place of `flake8`, `autoflake`, `isort`, `pyupgrade`,
    `black`, and more...
  - [ty](https://docs.astral.sh/ty/) - fast static type checker (default), or
    [mypy](https://github.com/python/mypy) (strict mode) if you prefer.
  - [typos](https://github.com/crate-ci/typos) - spell checker
  - [actionlint](https://github.com/rhysd/actionlint) and
    [zizmor](https://docs.zizmor.sh/) - lint & audit GitHub workflows
  - [validate-pyproject](https://github.com/abravalheri/validate-pyproject)

## Deploying to PyPI

When you're ready to deploy a version of your package, tag the commit with a
version number and push it to github.  This will trigger a github action that
will build and deploy to PyPI. (see the "upload-to-pypi" job in
`workflows/ci.yml`). The version number is determined by the git tag using
[hatch-vcs](https://github.com/ofek/hatch-vcs)... which wraps
[setuptools-scm](https://github.com/pypa/setuptools_scm/)

```sh
git tag -a v0.1.0 -m v0.1.0
git push --follow-tags

# or, specify a remote:
# git push upstream --follow-tags
```

To auto-deploy to PyPI, you will need to create a trusted publisher on PyPi:

- Connect to PyPi (you need an account)
- Go to your projects and click on "Publishing" (last item on the left menu)
- In the section "Add a new pending publisher"
- Enter the project name (as in your `pyproject.toml`), the organization or username of the repository owner (on Github) and the repository name
- Next, enter `ci.yml` as "Workflow name" and leave the environment blank
- Add the publisher and you are good to go!

## Update your repo

This template may change over time, bringing in new improvements, fixes, and
updates.  To update an existing project that was created from this template
using copier, just enter the root of the project, make sure `git status` shows
the working directory is clean, and run: `uvx copier update --trust`.  See
[copier docs](https://copier.readthedocs.io/en/stable/updating/) for details.
