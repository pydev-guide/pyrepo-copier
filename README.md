# Python Package Template

This is a template for a python package.

Feel free to use it as a launching point for your next project!

## How to use it

### 1. Create a new repo

This template uses [copier](https://copier.readthedocs.io/) to
create a new repo from the template.

```sh
pip install "copier"
```

Then run `copier`, passing in the template url and the desired
output directory (usually the name of your new package):

```sh
copier copy gh:pydev-guide/pyrepo-copier your-package-name
```

### 2. Run `git init` and install `pre-commit`

After creating the repo, you'll want to initialize a git repo.

> *This is important: you won't be able to `run pip install -e .`
without running `git init`*

```sh
cd <your-package-name>
git init
git add .
git commit -m 'build: Initial Commit'
```

If you selected pre-commit (or used the "full-featured" default),
install [pre-commit](https://pre-commit.com/), run `pre-commit autoupdate`,
and then install the git commit hook with `pre-commit install`:

```sh
pip install pre-commit
pre-commit autoupdate
pre-commit install
git add .
git commit -m 'chore: update pre-commit'
```

### 3. Install Locally and Run Tests

To run tests locally, you'll need to install the package in editable mode. 

I like to first create a new environment dedicated to my package:

```sh
mamba create -n <your-package-name> python
mamba activate <your-package-name>
```

Then install the package in editable mode:

```sh
pip install -e .[test]
```

*if you run into problems here, make sure that you ran git init above!*

Finally, run the tests:

```sh
pytest
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

- If you'd like: setup the [pre-commit.ci](https://pre-commit.ci/) service to
  run all pre-commit checks on every PR (in case contributors aren't running it
  locally).  Note that you can always run checks locally with `pre-commit run
  -a`
- Follow links below for more info on the included tools (pay particular
  attention to [hatch](https://hatch.pypa.io/) and
  [ruff](https://beta.ruff.rs/docs/)).
- See how to [Deploy to PyPI](#deploying-to-pypi) below.

## Stuff included

- [PEP 517](https://peps.python.org/pep-0517/) build system with [hatch
  backend](https://hatch.pypa.io/)
  - build with `python -m build`, [*not* `python
    setup.py`](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html)!
- [PEP 621](https://peps.python.org/pep-0621/) metadata in `pyproject.toml`
  - *all* additional configurables are also in `pyproject.toml`, with
  links to documentation
- uses `src` layout ([How come?](https://hynek.me/articles/testing-packaging/))
- git tag-based versioning with [hatch-vcs](https://github.com/ofek/hatch-vcs)
- autodeploy to PyPI on tagged commit (set `TWINE_API_KEY` env var on github). See [Deploying to PyPI](#deploying-to-pypi) below.
- Testing with [pytest](https://docs.pytest.org/en/7.1.x/)
- CI & testing with [github actions](https://docs.github.com/en/actions)
- GitHub action
  [cron-job](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
  running tests against dependency pre-releases (using `--pre` to install
  dependencies).
- [pre-commit](https://pre-commit.com/) with
  - [ruff](https://github.com/charliermarsh/ruff) - amazing linter and
    formatter. Takes the place of `flake8`, `autoflake`, `isort`, `pyupgrade`,
    and more...
  - [black](https://github.com/psf/black) - opinionated code formatter
  - [mypy](https://github.com/python/mypy) - static type hint checker (defaults
    to `strict` mode)
  - [conventional-pre-commit](https://github.com/compilerla/conventional-pre-commit) - enforce good commit messages (this is commented out by default). See [Conventional Commits](#thoughts-on-conventional-commits) below.
- [`check-manifest`](https://github.com/mgedmin/check-manifest) test to check
  completeness of files in your release.
- I use and include [github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator) to automate changelog generation... but there are probably better options now (this is a hot topic).

## Deploying to PyPI

When you're ready to deploy a version of your package, tag the commit with a version number and
push it to github.  This will trigger a github action that will build and deploy
to PyPI. (see the "deploy" step in `workflows/ci.yml`). The version number is determined by the git tag using
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
the working directory is clean, and run: `copier update`.  See [copier
docs](https://copier.readthedocs.io/en/stable/updating/) for details.
