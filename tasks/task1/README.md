# Task 1: The Art of Reach (3DOF Arm & Inverse Kinematics)

## The Problem

Our rover has finally arrived at the target extraction site, and the high-priority
geological sample is sitting just 40 centimeters away. There is just one massive problem:
the rover's chassis is stuck in the sand. Our only hope of retrieving the sample is to use
the onboard 3-Degree-of-Freedom (3DOF) manipulator arm. However, the targeting software was
corrupted during descent. The arm doesn't know how to bend its joints to reach the rock!

## Your Mission

Build the digital twin of this robotic arm and write the software that tells it how to
move. Inside your Docker environment, you will design a 3DOF arm, load it into a
simulation, and use **Inverse Kinematics (IK)** to calculate exactly how each joint must
rotate to move the gripper from its resting position to a specific (X, Y, Z) coordinate.

## What You Need To Do

* **Build the Blueprint** — Write a URDF or Xacro file to construct a 3DOF robotic arm:
  a base, three distinct links, and three rotating joints.
* **Bring it to Life** — Launch your robotic arm inside Gazebo Classic or RViz2 so we can
  see it in 3D space.
* **Solve the Puzzle (Inverse Kinematics)** — Given the 3D coordinates of the target rock,
  calculate the required joint angles to reach that exact spot. You may write the Python
  math yourself, or use MoveIt 2.
* **Make the Move** — Write a ROS 2 node that publishes the calculated joint trajectories,
  moving the arm from Point A (Home) to Point B (Target).

## Helpful Resources

* [URDF Tutorials (ROS 2 docs)](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html)
* [Xacro basics](http://wiki.ros.org/xacro)
* [MoveIt 2 Getting Started](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html)
* [Inverse Kinematics — concept primer](https://en.wikipedia.org/wiki/Inverse_kinematics)

## Working in Docker

This task needs the full simulation stack. Do your work **inside the container**, in the
`vanguard_ws/src/task1` workspace — see [`docs/GETTING_STARTED.md`](../../docs/GETTING_STARTED.md)
if you haven't set up the container yet.

Anything you build inside `vanguard_ws/src/task1` in the container appears automatically in
this `tasks/task1/` folder on your host machine (they're the same folder, just mounted into
the container) — so there's nothing extra to copy over before you commit.

## Deliverables

Place everything below directly in this folder (`tasks/task1/`):

1. A complete ROS 2 package containing your URDF/Xacro files, launch files, and movement
   script.
2. A short screen recording (or a few clear screenshots) of your simulated arm
   successfully moving to the target point inside your noVNC browser window.
