# pyrepo-copier

This is my personal python repository bootstrap.

Feel free to use it as a launching point for your next project!

## How to use it

### 1. Create a new repo

This template uses [copier](https://copier.readthedocs.io/) to
create a new repo from the template.  You can install copier with:

```sh
pip install copier
```

Then run `copier`, passing in the template url and the desired
output directory:

```sh
copier gh:tlambert03/pyrepo-copier your-package-name
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

Optionally, install [pre-commit](https://pre-commit.com/):

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

When I'm ready to deploy a version, I tag the commit with a version number and
push it to github.  This will trigger a github action that will build and deploy
to PyPI. (see the "deploy" step in `workflows/ci.yml`). The version number is determined by the git tag using
[hatch-vcs](https://github.com/ofek/hatch-vcs)... which wraps
[setuptools-scm](https://github.com/pypa/setuptools_scm/)

To auto-deploy to PyPI, you'll need to set a `TWINE_API_KEY` environment
variable in your github repo settings.  You can get this key from your [pypi
account](https://pypi.org/manage/account/token/).  Then add it to your github
repository settings as a secret named `TWINE_API_KEY`. (see [github
docs](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository))

(the name `TWINE_API_KEY` is specified in `workflows/ci.yml`)

```sh
git tag -a v0.1.0 -m v0.1.0
git push --follow-tags

# or, specify a remote:
# git push upstream --follow-tags
```

> *if you're curious, see also some thoughts on [semantic releases below](#semantic-versioning--release)*



## Conventional Commits

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) is a
specification for adding human and machine readable meaning to commit messages.
Using it faithfully will allow you to automate a lot of things (changelogs,
versioning, ...) at release time. To use it here:

- Use the `conventional-pre-commit` step in pre-commit. It will force you to use
  conventional commits locally.
- [VS Code]: Add the [Conventional
  Commits](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits)
  extension, making it easier to create conventional commits.
- This still doesn't protect GitHub PR commits, so add the [Semantic
  PRs](https://github.com/marketplace/semantic-prs) GitHub App to check that PR
  titles follow the Convention Commits Spec (and require squash commits)
- Protect the `main` branch:
  - use only PRs for `main`
  - use squash merge
  - require the `Semantic PRs` check to pass for merging
  - consider allowing only `semantic-release` to push to that branch.

- Future: use [frappucino](https://github.com/Carreau/frappuccino) or
  [griffe](https://github.com/mkdocstrings/griffe) to detect breaking API
  changes & add a GitHub action to enforce a `!` in the title or `BREAKING
  CHANGE` footer.

### Semantic Versioning & Release

I'm still not sure how I feel about [SemVer](https://semver.org/).  Seems better
than nothing, but also totally broken. I highly recommend these articles for
insight:

- [Semantic Versioning Will Not Save
  You](https://hynek.me/articles/semver-will-not-save-you/) - *Hynek Schlawack*
- [Version numbers: how to use
  them?](https://bernat.tech/posts/version-numbers/) - *Bernát Gábor*
- [Why I don't like SemVer anymore](https://snarky.ca/why-i-dont-like-semver/) -
  *Brett Cannon*
- [Should You Use Upper Bound Version
  Constraints?](https://iscinumpy.dev/post/bound-version-constraints/) - *Henry
  Schreiner*
- [Versioning Software](https://caremad.io/posts/2016/02/versioning-software/) -
  *Donald Stufft*

One of the biggest problems with SemVer is humans implementing it (see
[ZeroVer](https://0ver.org/) 😂). One approach is to use fully-automated version
& release management to take the human out of it.
[semantic-release](https://semantic-release.gitbook.io/semantic-release/) is
popular in the javascript world, and a
[`python-semantic-release`](https://python-semantic-release.readthedocs.io/)
variant exists. If you want to try it, this repo configures that in
`pyproject.toml`:

- Set up [`python-semantic-release` on GitHub
  Actions](https://python-semantic-release.readthedocs.io/en/latest/automatic-releases/github-actions.html)
  (see `ci.yml`)

## Update your repo (if you used `cruft`)

This template may change over time, bringing in new improvements, fixes, and
updates.  To update an existing project that was created from this template
using cruft, run `cruft update` in the root of the project.  See [cruft
docs](https://cruft.github.io/cruft/#updating-a-project) for details.

## Alternatives

- [cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python)
  (this one is a bit much for me but is an amazing reference for modern best
  practices in python repo maintenance)
