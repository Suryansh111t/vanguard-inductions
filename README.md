# Project Vanguard — Autonomous Subsystem Induction Tasks

Welcome to the Autonomous team induction program! This repo will walk you through **three
progressive tasks** covering robotic arm kinematics, sensor filtering, and computer vision —
the core building blocks of our rover's autonomy stack.

You are not expected to finish everything. Prioritize learning over completion — this
knowledge carries directly into later rounds.

---

## Start Here

New to Git or Docker? Read **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** first —
it's a complete, start-to-finish walkthrough: installing tools, forking this repo, running
the simulator, and submitting a Pull Request. Everything below assumes you've done that.

---

## The Tasks

| Task | What you'll build | Folder |
|---|---|---|
| **Task 1** — The Art of Reach | A 3DOF robotic arm + Inverse Kinematics in ROS 2/Gazebo | [`tasks/task1`](tasks/task1) |
| **Task 2** — Taming the Noise | A 1D Kalman Filter from scratch in Python | [`tasks/task2`](tasks/task2) |
| **Task 3** — Panorama or Bust | An image-stitching pipeline with OpenCV | [`tasks/task3`](tasks/task3) |

Each task folder has its own `README.md` with the full problem statement, requirements,
and deliverables. That's also exactly where you'll drop your submission — see below.

---

## How Submission Works

The Docker environment is wired so that whatever you build **inside the container** lands
**directly in the matching `tasks/taskN/` folder** on your machine — no manual copying.
Details are in [GETTING_STARTED.md](docs/GETTING_STARTED.md#35-where-your-files-actually-live).

1. **Fork this repository.**
   [How to fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

2. Complete whichever task(s) you're attempting, with your files inside the corresponding
   `tasks/taskN/` folder.

3. Commit and push:
   ```bash
   git add .
   git commit -m "task1: 3DOF arm IK solution"
   git push
   ```

4. **Open a Pull Request** back to this repository.

   **PR title format:**
   ```
   NAME [ID_NUMBER]
   ```
   Example: `Sparsh Bhutada [2024B4A30704H]`

   **PR description:** the template will auto-fill when you open the PR — just fill in
   your details and check off what you completed.

5. Wait for review and feedback.

---

## Environment Setup (Quick Reference)

```bash
git clone https://github.com/<your-username>/vanguard-inductions.git
cd vanguard-inductions
docker compose up -d --build
# then open http://localhost:6080 in your browser
```

Full instructions, including how the container connects to your files and what to do if
something breaks, are in [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).
