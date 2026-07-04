# Task 2: Taming the Noise (1D Kalman Filter)

## The Problem

Our rover is traversing rough, rocky terrain. The vibrations are intense, and our raw
Inertial Measurement Unit (IMU) readings are completely erratic. If the navigation system
blindly trusts this noisy telemetry, the rover will think it is jumping back and forth
uncontrollably! We need a way to look past the noise and find the true path.

## Your Mission

Build a **1D Discrete Kalman Filter** from scratch in Python to smooth out this erratic
data. By balancing our mathematical model of the rover's motion against the noisy sensor
updates (the Predict–Update cycle), you will extract a clean, stable state estimate from
the chaos.

## What You Need To Do

* **Simulate the Chaos** — Use `numpy` to generate a 1D dataset of constant motion, then
  inject it with heavy Gaussian noise 𝒩(μ, σ²) to mimic our broken IMU.
* **Filter the Truth** — Implement a 1D Kalman filter loop (Predict & Update) to
  dynamically smooth the dataset.
* **Show Your Work** — Use `matplotlib` to plot a comparison graph showing three things:
  the true path, the noisy raw data, and your smoothed Kalman Filter estimate.
* **Know Your Math** — Add brief comments explaining the key variables (State Estimate,
  Error Covariance, Process/Measurement Noise). Show us you understand *why* the math
  works.

## Helpful Resources

* [kalmanfilter.net — 1D Kalman Filter walkthrough](https://www.kalmanfilter.net/kalman1d.html)
* [How a Kalman Filter Works, in Pictures](https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/)

## Working in Docker

This task is plain Python — it doesn't need ROS or Gazebo at all. You can run it directly
on your host machine, **or** inside the container for a consistent environment (it already
has `numpy`, `scipy`, and `matplotlib` installed). See
[`docs/GETTING_STARTED.md`](../../docs/GETTING_STARTED.md) either way.

If you use the container, work inside `vanguard_ws/src/task2` — it's mounted straight to
this `tasks/task2/` folder, so your files are already in the right place to commit.

## Deliverables

Place everything below directly in this folder (`tasks/task2/`):

1. A self-contained `kalman_filter.py` script.
2. A screenshot of your generated matplotlib comparison plot.
