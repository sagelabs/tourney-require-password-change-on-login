Welcome. You have been invited to do a paid coding task for Enki's **AI
training data program**. Read this whole file before you start.

---

## What you will do

[`_TASK.md`](./_TASK.md) describes one small change to this codebase: a bug fix
or a small feature. You make the change, write tests for it, and keep the
existing test suite passing.

What we pay for is the record of **how you worked**. In order of importance,
the deliverables are:

1. **`_THINKING.md`**: your working notes, written while you work.
2. **Your commits**: frequent, with messages that explain why.
3. **Your code**: correct, tested, with the existing suite still passing.

Rough but honest notes with a working fix are worth more to us than a perfect
fix with no notes.

---

## No AI assistance

**Do not use Claude, ChatGPT, Copilot, Cursor, Cody, Windsurf, Gemini, or any
other AI coding tool while working on this task.** This applies to the code,
the tests, `_THINKING.md`, and your commit messages.

The value of this work is that it records how a person reasons through a
problem. AI-generated content makes the result useless to us. If you normally
work with AI and working without it feels slow, write that in `_THINKING.md`;
that is useful information too.

You can use: your editor's language server and standard autocomplete, linters,
formatters, test runners, documentation, and search engines.

---

## Time

Each task takes about 3 to 8 hours. We pay hourly, so work at your normal
pace: do not rush, and do not pad. If you are heading past 10 hours, email
us (addresses below) so we can help with whatever is blocking you, instead
of losing time on it alone.

You do not need to track time precisely. The timestamps in `_THINKING.md` are
enough; tell us the approximate total when you submit.

---

## Getting started

Follow these steps in order.

1. **Make your own copy of this repository.** Click **"Use this template"** on
   GitHub and create a **private** repository. Do all your work in your copy.
2. **Clone your copy** to your machine.
3. **Log your start time.** Open [`_THINKING.md`](./_THINKING.md) and replace
   the `[HH:MM]` next to "Starting" with the current time. Commit that change;
   it is your first commit and marks when you started. Keep the file open and
   keep adding to it through every step below.
4. **Read [`_ORIENTATION.md`](./_ORIENTATION.md), then [`_TASK.md`](./_TASK.md),
   end to end.** Take notes in the "Reading notes" section of `_THINKING.md`
   while you read. Do not start coding yet.
5. **Set up the environment** by following the setup steps in
   [`_ORIENTATION.md`](./_ORIENTATION.md). You need Python 3.11; `uv` will
   install it for you.
6. **Run the test suite once** to confirm your setup works. It takes about 4
   to 6 minutes; it is not stuck. The exact command is in `_ORIENTATION.md`.
   When it finishes, add a note to `_THINKING.md`: did setup work on the first
   try, what (if anything) went wrong, and roughly how long the suite took.
7. **Write your plan in `_THINKING.md`, then start.** If the task is a bug fix,
   reproduce the bug before you fix it.

---

## How to complete the task

### _THINKING.md

`_THINKING.md` is the main deliverable. It is a log of what you did and thought
while working, not a report written afterwards. Write it as you go.

The template in the repo explains each section at the top of the section. In
summary:

| Section | When to write it | What to record |
|---|---|---|
| Before reading anything | First, right after cloning | Your start time (replace the placeholder and commit); optionally what you expect the task to involve |
| Reading notes | While reading `_ORIENTATION.md`, `_TASK.md`, and the code | What you read and opened, what you learned, where you expect the change to go |
| Plan | After reading, before changing code | The task in your own words; intended changes in order; approaches you rejected |
| Progress log | While you work | Timestamped entries: what you searched for, files you opened and changed, results, dead ends, decisions |
| Retrospective | At the end (required) | Weakest parts of the solution, what you did not cover, what you would do with more time |

Rules that matter:

- Write entries at the time things happen. Do not reconstruct the log at the
  end from memory.
- Do not clean up or rewrite earlier entries. Wrong guesses and corrections
  are some of the most valuable content.
- Name the files you opened, searched, and changed in each entry.
- Short, rough sentences are fine. Clean writing is not the goal; an accurate
  record is.

### Commits

Commit often, and treat commit messages as part of the deliverable: we read
them. A good message says what you decided and why, not only what changed.

- Good: `moved the redirect ahead of the CSRF handler so a flagged user is not
  logged out before the reset runs`
- Not useful: `update auth`

Good moments to commit: plan written, bug reproduced, first test passing,
direction changed, change complete, tests written.

### When you are done

Check that:

- [ ] The requirements in [`_TASK.md`](./_TASK.md) are met, or `_THINKING.md`
      explains what you did not complete and why.
- [ ] You wrote tests for the behaviour you changed.
- [ ] The full existing test suite still passes.
- [ ] `_THINKING.md` is filled in for every section, including the
      Retrospective.
- [ ] Your commit history shows the steps of the work, not one final commit.

---

## The codebase

**Tourney** is a competition platform: challenges, teams, users, a live
scoreboard, an admin panel, and a REST API. Your task is a change to existing
code, so part of the work is finding your way around a codebase you did not
write, and your notes on how you do that are part of what we pay for.

[`_ORIENTATION.md`](./_ORIENTATION.md) covers how the code is organised, how to
set up and run the tests, and known issues that would otherwise cost you time.
Read it before you write code.

---

## Submitting

1. Push your final commit to your copy of the repository.
2. Email **kirill@enki.com** and **catalin@enki.com** with:
   - a link to your repository (add us as collaborators if it is private),
   - roughly how long you spent,
   - anything you want us to know: a caveat, a question, something you are
     proud of.
3. We review, confirm receipt, and arrange payment.

---

## Questions

If anything in this file or in [`_TASK.md`](./_TASK.md) is unclear, or you hit a
blocker you cannot reasonably work around, email **kirill@enki.com** and
**catalin@enki.com**. Do not stay stuck in silence; we would rather answer a
question than have you guess.

Some details in `_TASK.md` are left open on purpose: how you interpret an
underspecified requirement is part of what we want to see. When in doubt, make
a decision, write in `_THINKING.md` why you made it, and keep going.
