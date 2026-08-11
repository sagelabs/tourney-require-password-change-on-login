# Let admins force a user to change their password on next login

## Background

Admins manage accounts from the admin panel (create user, edit user). When an
admin resets someone's password, or onboards an account with a temporary one,
there is no way to require that the user set a new password: they can keep
using the admin-assigned one indefinitely.

The intended flow, end to end:

1. An admin creates or edits a user and ticks a "require password change"
   checkbox.
2. The user logs in with the admin-assigned password.
3. Every page the user opens redirects them into the existing self-service
   password reset flow (`/reset_password`) until they set a new password.
4. After the reset, the flag is cleared and the user browses normally.

## What to build

Give admins a per-user "force password change" flag, and enforce it:

- **Data:** users gain a boolean attribute marking them as needing to change
  their password. A schema change to the `users` table implies a database
  migration; add one, mirroring the existing migrations under
  `migrations/versions/`.
- **Admin UI and API:** admins can set the flag when creating a user and when
  editing one, from the admin panel forms and through the users API.
- **Enforcement:** while a flagged user is logged in, every request redirects
  them into the password reset flow until they complete it. Once they set a
  new password, the flag clears and they can use the site normally.

## Current behaviour

To see it in the running app, follow "Running the app locally" in
`_ORIENTATION.md`, then:

1. Start the app, complete `/setup` with user mode `users`, and stay logged
   in as the admin.
2. Open `/admin/users` and click the plus icon next to the "Users" heading.
   The create-user form has name, email, and password fields and a row of
   checkboxes: Verified, Hidden, Banned. Nothing lets the admin require a
   password change.
3. Open any user from the list and click the "Edit User" icon. The
   edit form has the same checkbox row and a password field: this is the
   admin-assigns-a-password scenario from the Background, and today the user
   can keep that password forever.
4. Log out and click "Forgot your password?" on the login page. On a local
   instance with no mail settings the page shows an error saying the
   instance is not configured to send email (the request-reset email form
   still renders), and any `/reset_password/...` URL shows the same error
   instead of the set-new-password form, valid token or not. This is the
   flow the redirect will send flagged users into, and the mail check
   described in the acceptance criteria.
5. Register a player account in a private window and browse the site.
   Nothing ever pushes a logged-in account into the reset flow. That is the
   behaviour you are adding.

## Getting started

- For the data half, an existing boolean user flag such as `verified`,
  `hidden`, or `banned` already travels the full path you need: admin form,
  users API schema, model column. Trace one of them end to end and give
  `change_password` the same treatment, plus the migration.
- The enforcement half applies to every logged-in request. The Request
  lifecycle section of `_ORIENTATION.md` describes where per-request
  behaviour is implemented and why ordering matters there. Think early about
  which
  requests must be exempt from the redirect, or a flagged user can never
  escape it.
- `tests/users/test_auth.py` shows login and password-reset flows driven
  from tests, including how reset tokens are issued and consumed.

## Acceptance criteria

Use exactly the identifier **`change_password`** everywhere the flag
surfaces.

**Data and migration**

- A boolean column `change_password` on the `users` table, defaulting to
  false. Put the default on the model column itself: a freshly created,
  never-flagged user stores false, not NULL (the test suite builds its
  schema from the models, not the migration).
- An Alembic migration under `migrations/versions/` that adds the
  `change_password` column, written with `op.add_column` as the existing
  migrations are. The test suite builds its schema from the models, but the
  migration is still required.

**API**

- The user schema exposes a settable `change_password` field: an admin can
  set it when creating a user through the API and change it with
  `PATCH /api/v1/users/<id>`.
- A non-admin user cannot set or change `change_password` through the API.
  A self-update (`PATCH /api/v1/users/me`) that includes `change_password`
  still succeeds (HTTP 200); the field is ignored and the stored value is
  unchanged. Do not reject the request. (`PATCH /api/v1/users/<id>` for
  another user is already admin-only and rejects non-admins with 403; keep
  that. The case that needs care is the self-update.)

**Admin forms**

- The admin create-user and edit-user forms expose the flag with the field
  name `change_password`; the rendered pages contain
  `name="change_password"`.

**Enforcement**

- A logged-in user whose flag is set is redirected (HTTP 302) on any normal
  request, API requests under `/api/v1` included, to a `/reset_password/...`
  URL carrying a valid reset token, so that opening the redirect target
  shows the set-new-password form and submitting it completes the reset.
  This covers session-authenticated (browser) requests; token-authenticated
  API requests are out of scope, so if you treat them differently, note your
  reasoning in `_THINKING.md`.
- The redirect must not trap the user. At minimum, these must keep working
  for a flagged user: the reset-password pages themselves, logging out, and
  static theme assets (without the asset exemption, the reset page renders
  without its CSS and JS).
- Completing the reset flow clears the flag: after the user sets a new
  password, `change_password` is false and later requests are not
  redirected. Only submitting a new password clears it; merely opening the
  reset page leaves the flag set and the user still redirected.
- Completing the reset works without outgoing mail configured. Requesting a
  reset email may keep requiring a mail server, but opening a valid
  `/reset_password/...` URL and submitting a new password must succeed on an
  instance with no mail settings. The reset view starts with a
  mail-configuration check; it must not block completing the reset.
- Unflagged users are unaffected.

**General**

- The existing test suite still passes.

---

See [README.md](./README.md) for how to work this task: the process, the no-AI rule, keeping _THINKING.md, and how your work is evaluated.
