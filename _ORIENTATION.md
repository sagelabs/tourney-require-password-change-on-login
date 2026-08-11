# Tourney codebase orientation

How the codebase is organised, how to set it up, and how to work with the
test suite.

## Product overview

Tourney hosts scoring-based competitions:

- An **organiser** stands up an instance, configures the event, and publishes
  **challenges**.
- **Players** register and submit answers to challenges. A correct answer is
  recorded as a **solve** and earns points; an incorrect one as a **fail**.
  Players compete as individuals or as teams, depending on the configured
  mode.
- A live **scoreboard** ranks the competitors. Visibility settings control
  who can see challenges, scores, and accounts, and scores can be frozen at a
  cut-off time.
- **Admins** run the event from an admin panel: challenges, users and teams,
  submissions, settings. The same operations are exposed through the REST
  API.

## Architecture

Tourney is a Flask monolith: one Python package (`Tourney/`) serving both
server-rendered pages and a REST API over a single relational database.

A request passes through:

1. A chain of `@app.before_request` handlers.
2. A view function (server-rendered page) or an API resource (`/api/v1`).
3. SQLAlchemy models for reads and writes.
4. A Jinja template (pages) or a Marshmallow schema (API JSON) for the
   response.

Pinned stack: Flask 2.1, SQLAlchemy 1.4, Marshmallow 2.x, Python 3.11 only.
The code targets these exact pinned versions; match the surrounding code.

## Request lifecycle

`create_app()` in `Tourney/__init__.py` is the application factory. It wires
config, the cache, the Jinja loader chain, the database, and the blueprints
(page views, admin panel, `/api/v1`).

Every request then runs the `@app.before_request` chain defined in
`Tourney/utils/initialization/__init__.py`, in a fixed order: subdirectory
redirect, setup gate (is the instance configured yet), IP tracking, ban
check, token authentication, CSRF. A handler's position in the chain
determines what it can assume about the request, so order matters when adding
to it.

Two details to know:

- Request handlers read a **cached snapshot of the current user**, not a
  fresh row: `get_current_user_attrs()` and the team/config equivalents in
  `Tourney/utils/user/` are memoized. A change made to a user during a
  request is not visible to before-request checks in the same cycle.
- Session-based requests carry a CSRF token. Token-authenticated requests
  (`Authorization` header) skip CSRF.

Views live in the top-level blueprint modules (`auth.py`, `challenges.py`,
`teams.py`, `users.py`, `scoreboard.py`, `views.py`) and in `admin/`. The API
lives under `api/v1/`.

## Data model

All models are in `Tourney/models/__init__.py`. The schema relies heavily on
single-table polymorphism:

- **Challenges** are polymorphic on a `type` column; each type is supplied by
  a plugin.
- **Submissions** are polymorphic too: a correct submission is recorded as a
  **Solve**, an incorrect one as a **Fail**.

**Accounts.** The runtime `user_mode` config switches the platform between
individual play (`users`) and team play (`teams`). Scoring, solves, and most
ownership logic key on an *account*: a user in users mode, a team in teams
mode, exposed through hybrid properties such as `account_id` rather than a
raw `user_id`. Code that deals with who solved what must work in both modes.

`Configs` is a key/value table holding all runtime configuration (next
section).

## Configuration

Two separate systems:

| | File / environment config | Runtime config |
|---|---|---|
| Storage | `config.ini` (env-var overridable) | `Configs` table |
| Written by | operator, at deploy time | admin panel / `set_config` |
| Read with | `get_app_config("KEY")` | `get_config("key", default)` |
| Holds | database URL, secret key, mail, S3, OAuth | `ctf_name`, `challenge_visibility`, `freeze`, `user_mode`, ... |

`get_config` is cached. `set_config` invalidates the cache. A direct write to
the `Configs` table is not visible until the cache clears.

## Plugins

`Tourney/plugins/` is scanned at startup and each subpackage's `load(app)`
runs. Challenge types and flag types are plugins: `CHALLENGE_CLASSES` and
`FLAG_CLASSES` are registries keyed by a type string. `BaseChallenge` (in
`Tourney/plugins/challenges/`) defines the `attempt` / `solve` / `fail`
contract that every challenge type implements. This is the main extension
point.

## API and serialization

The API is flask-restx under `/api/v1`, one module per resource in
`Tourney/api/v1/`. Marshmallow schemas in `Tourney/schemas/` handle API input
and output. WTForms in `Tourney/forms/` back the server-rendered forms. Enums
and default values are in `Tourney/constants/`.

## Repository layout

```
Tourney/
  __init__.py        create_app() application factory
  auth.py            login / register / logout / reset, OAuth
  api/v1/            REST API, one module per resource
  models/__init__.py all SQLAlchemy models (one file)
  schemas/           Marshmallow (de)serialization
  forms/             WTForms definitions
  constants/         enums and default values
  plugins/           challenge and flag types (auto-discovered)
  utils/             config, scoring, email, uploads, security, initialization
  themes/            Jinja themes (prebuilt assets committed)
  admin/             admin panel blueprint
migrations/versions/ Alembic revisions
tests/               pytest suite, mirrors the app layout
```

To find code:

- Find a behaviour by its URL: grep for the route in `api/v1/` or the
  blueprint modules.
- Find everywhere a model is used: grep for the model name.
- The tests are documentation: the test for a feature shows how it is
  exercised end to end.

## Setup

Python 3.11 is required. With [uv](https://docs.astral.sh/uv/), which
downloads it for you:

```bash
uv venv --python 3.11 .venv && source .venv/bin/activate
uv pip install -r requirements.txt -r development.txt
```

Without uv, `python3.11 -m venv .venv` and
`pip install -r requirements.txt -r development.txt` also work.

## Running the app locally

Use this to check behaviour in the browser rather than through a test:

```bash
python serve.py              # dev server with auto-reload on http://127.0.0.1:4000
python serve.py --port 8000  # different port
```

- With no database configured, the app creates a local SQLite file at
  `Tourney/tourney.db` on first start.
- The first visit redirects to `/setup`, a short wizard that names the event
  and creates the admin account. After setup you are logged in as that admin;
  the admin panel is at `/admin`.
- In the wizard, user mode `users` is the simplest for manual testing. In
  `teams` mode every account, including the admin, must create or join a team
  before the participation pages load; until then, logging in redirects to
  the team page.
- To test as a player, register a second account in a private browser window.
- To start over with a clean instance, stop the server and delete **both**
  `Tourney/tourney.db` and the `.data/` directory in the repo root. The
  config cache lives in `.data/filesystem_cache` and survives a database
  reset; deleting only the database leaves the app convinced it is already
  set up.

## Running tests

The suite runs fully offline against in-memory SQLite. The only required
environment variable is `TESTING_DATABASE_URL`; no `config.ini` or `/setup`
step is needed.

```bash
TESTING_DATABASE_URL='sqlite://' pytest -n auto \
  -W ignore::sqlalchemy.exc.SADeprecationWarning \
  -W ignore::sqlalchemy.exc.SAWarning
```

The full suite takes about **4 to 6 minutes** even in parallel: every test
builds a full app and a fresh database through the real `/setup` flow. It is
not stuck.

Do not run the whole suite on every change. A single test takes about 1 to 3
seconds. Run the file or test you are working on, and run the full suite once
before you finish:

```bash
pytest tests/api/v1/test_challenges.py            # one file
pytest tests/api/v1/test_challenges.py::test_x    # one test
pytest -k "some_keyword"                          # by name
# useful flags: -x (stop at first failure), --lf (rerun last failures),
#               -p no:randomly (deterministic order)
```

## Writing tests

Use `tests/helpers.py` instead of writing your own setup code:

- `create_tourney(...)` builds a full app and a fresh database and runs the
  real `/setup`; `destroy_tourney(app)` tears it down. Most tests wrap their
  body in `with app.app_context():`.
- The `gen_*` factories (`gen_challenge`, `gen_flag`, `gen_solve`,
  `gen_fail`, `gen_team`, `gen_user`, `gen_hint`, `gen_award`, and about
  twenty more) create model rows directly. Use them instead of driving the UI
  to reach a state.
- `register_user(app, ...)` and `login_as_user(app, ...)` return a test
  client that is already registered or authenticated. The client injects the
  CSRF token for JSON requests automatically.
- Time is controlled with `freezegun` (the `ctftime` / freeze helpers). For
  time-dependent behaviour, freeze time instead of sleeping.
- External services are mocked: SMTP and Mailgun via patched transports, S3
  via `moto`, the OAuth provider via `login_with_mlc`. Tests never touch the
  network; assert against the mock.

The fastest way to write a test is to copy the nearest existing one: the
`tests/` tree mirrors the app layout (`tests/api/v1/...` mirrors
`Tourney/api/v1/...`).

## Known issues

- **SQLite skips migrations.** In development and tests the app calls
  `create_all()` and stamps the latest revision; Alembic never runs. A model
  change therefore works in the test suite without a migration. Production
  (MySQL or PostgreSQL) does run migrations, so a schema change needs a
  matching revision under `migrations/versions/`.
- **Request handlers see a cached user snapshot** (memoized
  `get_current_user_attrs`), not a live query. See Request lifecycle above.
- **`get_config` is cached.** Change values through `set_config`; direct
  `Configs` writes are invisible until the cache clears.
- **One test builds one full app plus database.** This is why the suite is
  slow and why scoping test runs matters.
- **Do not upgrade pinned dependencies.** The code targets the exact pinned
  versions.
