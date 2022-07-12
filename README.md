# pyrepo-cookiecutter

This is my personal python repository bootstrap.

Feel free to use it as a launching point for your next project!

## How to use it

I recommend using [`cruft`](https://github.com/cruft/cruft) instead of cookiecutter (this will let you [update it](#update-it) easily later)

```sh
cruft create https://github.com/tlambert03/pyrepo-cookiecutter
```

After creating the repo, you'll probably want to initialize a git repo, and install [pre-commit](https://pre-commit.com/):

```sh
cd <your-package-name>
git init
pre-commit autoupdate
pre-commit install
git add .
git commit -m 'build: Initial Commit'
```

If you have the [GitHub CLI](https://cli.github.com/) installed, and would like
to create a GitHub repository for your new package:

```sh
gh repo create --source=. --public --remote=origin --push
```

### next steps

- setup the [pre-commit.ci](https://pre-commit.ci/) service to run all pre-commit
  checks on every PR (in case contributors aren't running it locally).

## Update it

This template may change over time, bringing in new improvements, fixes, and
updates.  To update an existing project that was created from this template
using cruft, run `cruft update` in the root of the project.  See [cruft docs](https://cruft.github.io/cruft/#updating-a-project) for details.

## Stuff included

- [PEP 517](https://peps.python.org/pep-0517/) build system with [setuptools
  backend](https://setuptools.pypa.io/en/latest/build_meta.html)
  - build with `python -m build`, [*not* `python setup.py`](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html)!
- [PEP 621](https://peps.python.org/pep-0621/) metadata in `pyproject.toml`
  - *all* additional configurables are in `pyproject`, with the exception of `flake8`, which doesn't support it.
- uses `src` layout ([How come?](https://hynek.me/articles/testing-packaging/))
- git tag-based versioning with
  [setuptools-scm](https://github.com/pypa/setuptools_scm)
- autodeploy to PyPI on tagged commit (set `TWINE_API_KEY` env var on github).  (see also [semantic releases](#semantic-versioning--release))
- Testing with [tox](https://tox.wiki/en/latest/) &
  [pytest](https://docs.pytest.org/en/7.1.x/)
- CI & testing with [github actions](https://docs.github.com/en/actions) and
  [`tox-gh-actions`](https://github.com/ymyzk/tox-gh-actions)
- GitHub action cron-job running tests against dependency pre-releases
- [pre-commit](https://pre-commit.com/) with
  - [conventional-pre-commit](https://github.com/compilerla/conventional-pre-commit) - enforce good commit messages
  - [autoflake](https://github.com/PyCQA/autoflake) - auto-remove unused imports & variables
  - [isort](https://github.com/PyCQA/isort) - sort imports alphabetically, separated into sections by type
  - [pyupgrade](https://github.com/asottile/pyupgrade) - automatically upgrade syntax for newer python versions
  - [black](https://github.com/psf/black) - opinionated code formatter
  - [flake8](https://github.com/PyCQA/flake8) - checks source code for errors ([linter](https://en.wikipedia.org/wiki/Lint_(software)))
  - [mypy](https://github.com/python/mypy) - static type hint checker (defaults to `strict` mode)
- [`check-manifest`](https://github.com/mgedmin/check-manifest) test to check completeness of files in your release.

### Conventional Commits

[Conventional
Commits](https://www.conventionalcommits.org/en/v1.0.0/) is a specification for adding human and machine readable meaning to commit messages. Using it faithfully will allow you to automate a lot of things (changelogs, versioning, ...) at release time. To use it here:

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

I'm still not sure how I feel about [SemVer](https://semver.org/).  Seems better than nothing, but also totally broken. I highly recommend these articles for insight:

- [Semantic Versioning Will Not Save You](https://hynek.me/articles/semver-will-not-save-you/) - *Hynek Schlawack*
- [Version numbers: how to use them?](https://bernat.tech/posts/version-numbers/) - *Bernát Gábor*
- [Why I don't like SemVer anymore](https://snarky.ca/why-i-dont-like-semver/) - *Brett Cannon*
- [Should You Use Upper Bound Version Constraints?](https://iscinumpy.dev/post/bound-version-constraints/) - *Henry Schreiner*
- [Versioning Software](https://caremad.io/posts/2016/02/versioning-software/) - *Donald Stufft*

One of the biggest problems with SemVer is humans implementing it (see [ZeroVer](https://0ver.org/) 😂). One approach is to use fully-automated version & release management to take the human out of it. [semantic-release](https://semantic-release.gitbook.io/semantic-release/) is popular in the javascript world, and a [`python-semantic-release`](https://python-semantic-release.readthedocs.io/) variant exists. If you want to try it, this repo configures that in `pyproject.toml`:

- Set up [`python-semantic-release` on GitHub
  Actions](https://python-semantic-release.readthedocs.io/en/latest/automatic-releases/github-actions.html)
  (see `ci.yml`)

## See also

- [cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python) (this one is a bit much for me but is an amazing reference for modern best practices in python repo maintenance)
