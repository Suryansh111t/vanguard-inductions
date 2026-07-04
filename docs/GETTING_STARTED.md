# Getting Started — Git & Docker, Start to Finish

This is the only setup doc you need to read before starting any task. It walks through
everything from forking this repo to running the simulator and submitting your work.

---

## Part 1 — Install the tools

You need three things on your machine:

1. **Git** — [install instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. **Docker** — [install instructions](https://docs.docker.com/get-docker/) (Docker Desktop
   includes Docker Compose already, on Windows/Mac. On Linux, also install the
   [Compose plugin](https://docs.docker.com/compose/install/).)
3. A terminal you're comfortable typing in. If you've never used one:
   [Linux command line basics](https://ubuntu.com/tutorials/command-line-for-beginners#1-overview).

To check everything installed correctly:

```bash
git --version
docker --version
docker compose version
```

If any of these error out, fix that before continuing — nothing else will work otherwise.

---

## Part 2 — Get the repo onto your machine (Git)

### 2.1 Fork it

Go to this repository on GitHub and click **Fork** (top right). This creates your own
copy under your GitHub account. **Work on your fork, not the original** — you don't have
permission to push to the original, and you shouldn't need it.

Reference: [How to fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

### 2.2 Clone your fork

```bash
git clone https://github.com/<your-username>/vanguard-inductions.git
cd vanguard-inductions
```

Note: this URL should point to **your fork**, not the original repo. You can copy the
exact URL from the green "Code" button on your fork's GitHub page.

### 2.3 The Git commands you'll actually use

You only need a handful of commands for this whole induction:

```bash
git status                  # what's changed?
git add .                   # stage everything you changed
git commit -m "message"     # save a snapshot with a description
git push                    # send it to your fork on GitHub
```

Run `git add`, `git commit`, and `git push` every time you finish a chunk of work you don't
want to lose — don't wait until the very end to commit for the first time.

---

## Part 3 — Run the simulator (Docker)

### 3.1 What Docker is actually doing here

Instead of installing ROS 2, Gazebo, and a dozen libraries directly on your laptop (which
takes hours and breaks differently on every OS), Docker runs all of that inside an isolated
container — a lightweight virtual environment — with everything pre-installed. You interact
with it through a browser tab showing a full Linux desktop.

### 3.2 Build and start the container

From inside the `vanguard-inductions` folder:

```bash
docker compose up -d --build
```

* `--build` compiles the image the first time (or after you pull Dockerfile changes) — this
  can take several minutes the first time, then it's cached and fast.
* `-d` runs it in the background so your terminal stays free.

### 3.3 Open the desktop

Go to **http://localhost:6080** in your browser. You should see a Linux desktop. This is
your ROS 2 environment — Gazebo, RViz, and a terminal all live here.

### 3.4 Open a terminal inside the container

You can either open a terminal from within the noVNC desktop itself, or from your host
machine's terminal:

```bash
docker compose exec vanguard-sim /bin/bash
```

Either way, you're now inside the container and can run `ros2`, `colcon build`, etc.

### 3.5 Where your files actually live

This is the important part: the `tasks/task1`, `tasks/task2`, and `tasks/task3` folders on
your **host machine** are directly connected (bind-mounted) to
`vanguard_ws/src/task1`, `task2`, `task3` **inside the container**. They are the same
files, viewed from two places.

That means:
- You can write code with your normal editor (VS Code, etc.) on your host machine, in
  `tasks/task1/`.
- Build and run it inside the container, from `vanguard_ws/src/task1`.
- There's no copying, uploading, or syncing step — saving a file in one place instantly
  shows up in the other.

### 3.6 Stopping the container

```bash
docker compose down
```

Your files in `tasks/` are untouched — they live on your host machine, not inside the
container, so stopping or even deleting the container never deletes your work.

---

## Part 4 — Submit your work

1. Make sure your work is inside the correct folder: `tasks/task1/`, `tasks/task2/`,
   and/or `tasks/task3/`.
2. Commit and push:
   ```bash
   git add .
   git commit -m "task1: 3DOF arm IK solution"
   git push
   ```
3. Open a Pull Request from your fork back to the original repository.
   * **PR title:** `NAME [ID_NUMBER]`
   * **PR description:** use the template that auto-fills when you open the PR.
4. Wait for review — we may leave comments asking for changes or clarification.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `docker: command not found` | Docker isn't installed, or your terminal needs a restart after installing it. |
| Blank/black screen at `localhost:6080` | Wait ~10 seconds after `docker compose up`, then refresh. |
| `Bad exit status: seccomp` on container start | Confirm `security_opt: seccomp:unconfined` is present in `docker-compose.yml` (it is, by default — check you didn't edit it out). |
| Gazebo won't launch, or renders solid black | Give Docker more resources: Docker Desktop → Settings → Resources → at least 4 GB RAM, 2 CPUs. If it still fails, try `export LIBGL_ALWAYS_SOFTWARE=1` inside the container before launching Gazebo. |
| Files I changed aren't showing up in the container (or vice versa) | Make sure you're editing files inside `tasks/task1` (etc.), not somewhere else in the repo — only those three folders are bind-mounted. |
| `Package '<name>' not found` after creating a new ROS 2 package | You need to `colcon build` and then `source install/setup.bash` again inside the container after creating or editing a package. |
| `git push` asks for a password and rejects it | GitHub no longer accepts account passwords for `git push`. Set up a [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) or [SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) instead. |
