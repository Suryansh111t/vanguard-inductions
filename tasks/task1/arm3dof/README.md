# arm3dof — 3-DOF Arm & Inverse Kinematics (Task 1)

A 3-joint robotic arm that computes the joint angles needed to touch a target
point in 3D, then smoothly moves there. Built for ROS 2 Humble, shown in RViz2
(primary) or Gazebo Classic (optional bonus).

---

## 1. What each joint does

```
base_link                      the pedestal (reference frame, 0,0,0)
   │  base_yaw        (Z axis)  turn the whole arm left / right
link1                          rotating hub
   │  shoulder_pitch  (Y axis)  tip the arm forward / back
link2  (upper arm, 0.25 m)
   │  elbow_pitch     (Y axis)  bend the elbow
link3  (forearm, 0.25 m)
   │  tip_joint       (fixed)
tip_link                       the gripper point (end-effector)
```

At all-zero angles the arm points straight up. Link geometry (`D1=0.10`,
`L2=0.25`, `L3=0.25` metres) lives in **both** `urdf/arm3dof.urdf` and
`arm3dof/ik.py` — they must always agree.

## 2. How the pieces fit together (the ROS 2 mental model)

- **URDF** (`urdf/arm3dof.urdf`) — a description of links + joints. It is just
  data; on its own it does nothing.
- **robot_state_publisher** — a node that reads the URDF and listens on the
  `/joint_states` **topic**. Every time it hears a new set of joint angles it
  computes where each link is and publishes the **TF** (transform) tree.
- **/joint_states** — the topic carrying the three joint angles. Something has
  to publish it: either our `move_arm` node, or the slider GUI.
- **move_arm** (`arm3dof/move_arm.py`) — our node. It solves IK, then publishes
  `/joint_states` many times a second, interpolating from Home to the target so
  the arm *animates* instead of teleporting.
- **RViz2** — subscribes to TF + the URDF and draws the arm in 3D.

That chain — *node → `/joint_states` topic → robot_state_publisher → TF → RViz*
— is the thing worth understanding. Nodes never talk to each other directly;
they publish/subscribe to named topics.

## 3. The inverse kinematics (`arm3dof/ik.py`)

Forward kinematics = "given angles, where is the tip?". **Inverse** kinematics
is the reverse and is what we need. The trick is to split it into two easy
sub-problems:

1. **Base yaw** aims the arm at the target: `t1 = atan2(y, x)`.
2. That leaves a flat **2-link problem** in the vertical plane. Using the
   distance `d` from shoulder to target:
   - Elbow (law of cosines): `t3 = acos((d² − L2² − L3²) / (2·L2·L3))`
   - Shoulder: `t2 = atan2(r, s) − atan2(L3·sin t3, L2 + L3·cos t3)`

`ik.py` self-tests itself — run `python3 arm3dof/ik.py` and it solves several
targets and confirms forward kinematics lands back on each one (error ≈ 1e-16).

---

## 4. Run it (inside the container)

Open a terminal in the container (noVNC desktop terminal, or
`docker compose exec vanguard-sim /bin/bash`). Then:

```bash
cd ~/vanguard_ws

# build just this package and make it findable
colcon build --packages-select arm3dof
source install/setup.bash

# quick math check (no simulator needed)
python3 src/task1/arm3dof/arm3dof/ik.py

# ---- MAIN DEMO: RViz ----
ros2 launch arm3dof display.launch.py
```

RViz opens and the arm swings from pointing-up (Home) to the target. The
terminal prints the IK solution and an FK check, e.g.:

```
Target (x,y,z) = (0.300, 0.150, 0.200) m
IK solution (deg): base_yaw=26.6, shoulder_pitch=27.8, elbow_pitch=91.1
FK check: tip lands at (0.300, 0.150, 0.200) m  ->  error 0.000 mm
```

### Try other targets
```bash
ros2 launch arm3dof display.launch.py target_x:=0.25 target_y:=-0.10 target_z:=0.30
ros2 launch arm3dof display.launch.py elbow_up:=false        # other elbow solution
```

### Move the joints by hand (understanding forward kinematics)
```bash
ros2 launch arm3dof display.launch.py use_gui:=true
```
Three sliders appear — drag them and watch the arm move.

> **After editing any file** run `colcon build --packages-select arm3dof` and
> `source install/setup.bash` again in that terminal.

---

## 5. Optional bonus: Gazebo Classic (physics)

More moving parts (needs ros2_control controllers). The RViz demo already
satisfies the task; do this only if you want a Gazebo recording.

```bash
cd ~/vanguard_ws
colcon build --packages-select arm3dof
source install/setup.bash
ros2 launch arm3dof gazebo.launch.py
```
Gazebo opens, the arm spawns, controllers load, and after a few seconds the arm
drives to the target under simulated physics. If Gazebo renders black, run
`export LIBGL_ALWAYS_SOFTWARE=1` before launching.

---

## 6. Files

| File | What it is |
|------|------------|
| `urdf/arm3dof.urdf`            | The robot: links, joints, colours (+ Gazebo extras) |
| `arm3dof/ik.py`               | Forward + inverse kinematics (self-testing) |
| `arm3dof/move_arm.py`         | Node: solve IK, animate Home → Target |
| `launch/display.launch.py`    | RViz demo (main) |
| `launch/gazebo.launch.py`     | Gazebo demo (bonus) |
| `config/arm_controllers.yaml` | ros2_control controllers (Gazebo only) |
| `rviz/arm.rviz`               | RViz view preset |
