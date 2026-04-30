# SourceTree Setup Guide

## Installation

1. Download SourceTree from [sourcetreeapp.com](https://www.sourcetreeapp.com)
2. Install and sign in with an Atlassian account (free)
3. During setup, connect your GitHub account: Preferences → Accounts → Add → GitHub → Connect

---

## Cloning the repository

1. File → New → **Clone from URL**
2. Source URL: `https://github.com/rockett90/hardware-features.git`
3. Destination path: choose a local folder
4. ⚠️ Tick **"Recurse submodules"** — this is essential. It clones the component library at the same time.
5. Click **Clone**

---

## Creating a branch

1. Repository → **Branch**
2. Type a name following the naming convention (see CONTRIBUTING.md section 3)
   - Examples: `artifact/my-first-feature/initial-schematic`, `chore/update-readme`
3. Tick **"Checkout new branch"**
4. Click **Create Branch**

---

## Making commits

1. Make your changes in KiCad or a text editor
2. In SourceTree, go to the **File Status** view
3. Tick the files you want to include in the commit ("Stage" them)
4. Type a freeform commit message in the box at the bottom
5. Click **Commit**

> Note: commit messages are freeform. Only the **PR title** needs to follow `type(scope): description` format.

---

## Pushing to GitHub

1. Click **Push** in the toolbar
2. Select your branch
3. Click **Push**

Do this at the end of every working session.

---

## Opening a Draft PR

After your first push, GitHub will show a yellow banner on the repository page.

1. Click **"Compare & pull request"**
2. Click the **dropdown arrow** on the green button
3. Select **"Create draft pull request"**
4. Set the PR title to `type(scope): description` format (e.g. `feat(my-first-feature): add initial schematic`)
5. Click **Create draft pull request**

---

## Updating from main before marking Ready for Review

Before marking your PR ready, bring in the latest changes from main:

1. Click **Fetch** in the toolbar
2. In the left sidebar under **Remotes → origin**, right-click **main**
3. Select **"Merge origin/main into current branch"**

> ⚠️ If KiCad file conflicts appear (`.kicad_sch` or `.kicad_pcb`), **stop immediately** and speak to the lead. Do not attempt to resolve these conflicts manually — the files will be silently corrupted.

---

## Viewing history

Click **History** in the left sidebar to see the full commit history of the repository.
