# Tool Setup — Quick-Start Guide

> **No prior Git experience needed.** This guide walks you through everything from installation to cloning the repository, step by step.

---

## What you need

| Tool | Purpose | Includes Git? |
|---|---|---|
| **GitHub Desktop** | Visual Git client — recommended for most users | ✅ Yes |
| **GitHub CLI** (`gh`) | Command-line alternative for advanced users | ❌ Requires separate Git install |

You only need **one** of the two. GitHub Desktop is recommended if you are new to Git.

---

## Option A — GitHub Desktop (recommended)

### 1. Download and install GitHub Desktop

1. Go to [desktop.github.com](https://desktop.github.com).
2. Click the **Download for [your OS]** button.

<!-- screenshot: GitHub Desktop download page with the Download button highlighted -->

3. Open the downloaded installer and follow the on-screen prompts.
   - On **Windows**: run the `.exe` file. GitHub Desktop installs automatically with no options to choose.
   - On **macOS**: open the `.dmg` file and drag **GitHub Desktop** into your Applications folder.

<!-- screenshot: macOS drag-to-Applications prompt -->

4. Launch **GitHub Desktop**.

---

### 2. Sign in to GitHub

1. On the welcome screen, click **Sign in to GitHub.com**.

<!-- screenshot: GitHub Desktop welcome screen with "Sign in to GitHub.com" button -->

2. Your browser opens. Sign in to your GitHub account (or create one at [github.com](https://github.com) if you do not have one).
3. Click **Authorize desktop** when prompted.
4. Switch back to GitHub Desktop — you should see your username in the top-left corner.

<!-- screenshot: GitHub Desktop after sign-in, showing username -->

---

### 3. Clone the repository

> **What is cloning?** Cloning downloads a full copy of the repository to your computer so you can work on files locally.

1. In GitHub Desktop, click **File → Clone repository…** (or press `Ctrl+Shift+O` / `⇧⌘O`).
2. Select the **GitHub.com** tab.
3. In the search box, type `hardware-features` and select `rockett90/hardware-features` from the list.

<!-- screenshot: Clone repository dialog with rockett90/hardware-features selected -->

4. Under **Local path**, choose a folder on your computer where the repository will be saved (e.g. `Documents/hardware-features`).
5. Expand **Advanced options** and tick **"Recurse submodules"** — this is essential. It downloads the shared component library at the same time.

<!-- screenshot: Advanced options panel with Recurse submodules ticked -->

6. Click the blue **Clone** button.

GitHub Desktop downloads the repository. This may take a minute or two depending on your internet connection.

> ⚠️ **If you accidentally cloned without submodules**, open a terminal in the repository folder and run:
> ```bash
> git submodule update --init
> ```

---

### 4. Verify the clone

1. In GitHub Desktop, click **Repository → Show in Explorer** (Windows) or **Repository → Show in Finder** (macOS).
2. Check that the `library/` folder is **not empty** — it should contain subfolders like `symbols/`.

If `library/` is empty, the submodule did not initialise. Re-run `git submodule update --init` in a terminal opened at the repository root.

---

### 5. Creating a branch

1. In GitHub Desktop, click **Current branch** (top centre of the window) to open the branch panel.
2. Click **New branch**.
3. Type the branch name — follow the naming convention in [CONTRIBUTING.md](../CONTRIBUTING.md#branch-naming). Example: `init/my-feature`.
4. Click **Create branch**.

<!-- screenshot: New branch dialog with branch name typed -->

---

### 6. Publishing your branch

After creating a branch, it exists only on your computer until you publish it.

1. Click the blue **Publish branch** button in the top-right corner of GitHub Desktop.

<!-- screenshot: GitHub Desktop toolbar with the Publish branch button highlighted -->

This pushes your branch to GitHub and triggers any CI workflows configured for that branch.

---

### 7. Committing and pushing changes

1. Make your changes in KiCad or a text editor.
2. Switch back to GitHub Desktop — changed files appear in the **Changes** panel on the left.
3. Tick the files you want to include in the commit (all are ticked by default).
4. In the **Summary** box at the bottom-left, type a short commit message.
5. Click the blue **Commit to `<branch-name>`** button.
6. Click **Push origin** in the top-right corner to send your commits to GitHub.

<!-- screenshot: GitHub Desktop Changes panel with commit summary and button highlighted -->

> **Tip:** Push at the end of every working session so your work is backed up and CI can run.

---

## Option B — GitHub CLI

> Use this option if you are comfortable with the command line or need to script repository interactions.

### 1. Install Git

GitHub CLI requires Git to be installed separately.

- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win). During installation, accept the defaults — pay attention to the "Adjusting your PATH" step and select **"Git from the command line and also from 3rd-party software"**.
- **macOS**: Git is included with Xcode Command Line Tools. Run `xcode-select --install` in Terminal, or install via [Homebrew](https://brew.sh): `brew install git`.
- **Linux**: `sudo apt install git` (Debian/Ubuntu) or equivalent for your distribution.

Verify: `git --version`

---

### 2. Install GitHub CLI

1. Go to [cli.github.com](https://cli.github.com) and download the installer for your OS.
   - **Windows**: download the `.msi` installer and run it.
   - **macOS**: `brew install gh`
   - **Linux**: follow the instructions at [cli.github.com/manual/installation](https://cli.github.com/manual/installation)

2. Verify: `gh --version`

---

### 3. Sign in

```bash
gh auth login
```

Follow the interactive prompts:

1. Select **GitHub.com**.
2. Select **HTTPS** as the preferred protocol.
3. Select **Login with a web browser** — a one-time code will appear in your terminal.
4. Open the URL shown, paste the code, and authorise the CLI.

Verify your login:

```bash
gh auth status
```

You should see `✓ Logged in to github.com as <your-username>`.

---

### 4. Clone the repository

```bash
git clone --recurse-submodules https://github.com/rockett90/hardware-features.git
cd hardware-features
```

The `--recurse-submodules` flag is essential — it clones the shared component library at the same time.

---

### 5. Creating a branch

```bash
git checkout main
git pull
git checkout -b init/my-feature
git push -u origin init/my-feature
```

Replace `init/my-feature` with the correct branch name for your task — see [CONTRIBUTING.md](../CONTRIBUTING.md#branch-naming) for the naming convention.

---

### 6. Basic daily workflow

```bash
# Get the latest changes from the team
git pull

# Stage changed files
git add features/my-feature/

# Commit
git commit -m "feat(my-feature): add initial schematic"

# Push to GitHub
git push
```

---

### 7. Common CLI commands

| What you want to do | Command |
|---|---|
| See changed files | `git status` |
| See commit history | `git log --oneline` |
| Switch to an existing branch | `git checkout branch-name` |
| Open a PR in the browser | `gh pr create --web` |
| View open PRs | `gh pr list` |
| Check CI status for current branch | `gh pr checks` |

---

## Further reading

- [docs/setup/kicad-setup.md](setup/kicad-setup.md) — KiCad installation and library configuration
- [docs/how-to/init-feature.md](how-to/init-feature.md) — how to initialise a new feature
- [docs/how-to/worked-example.md](how-to/worked-example.md) — full worked example from idea to release
- [CONTRIBUTING.md](../CONTRIBUTING.md) — branch naming, commit format, and PR guidelines
