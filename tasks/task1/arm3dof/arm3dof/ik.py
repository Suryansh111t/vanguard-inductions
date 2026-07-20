"""
Inverse & forward kinematics for the 3-DOF arm defined in urdf/arm3dof.urdf.

The arm has three revolute joints:
    base_yaw       : rotation about vertical Z  (angle t1)
    shoulder_pitch : rotation about Y           (angle t2, measured from +Z)
    elbow_pitch    : rotation about Y           (angle t3, relative to link2)

At all-zero angles the arm points straight up (+Z). Positive t2/t3 tip the
arm forward, into +X.

These three link constants MUST match the URDF exactly, or the arm will not
land on the target:
    D1 = 0.10 m   base_link origin -> shoulder joint
    L2 = 0.25 m   shoulder -> elbow  (upper arm)
    L3 = 0.25 m   elbow -> tip       (forearm)

Run this file directly (`python3 ik.py`) to self-test: it solves IK for a few
targets and checks that forward kinematics lands back on them.
"""

import math

# ---- Geometry (keep in sync with urdf/arm3dof.urdf) ----
D1 = 0.10
L2 = 0.25
L3 = 0.25

# Reach limits, handy for sanity checks / error messages
REACH_MAX = L2 + L3          # arm fully extended
REACH_MIN = abs(L2 - L3)     # arm fully folded


def forward_kinematics(t1, t2, t3):
    """Joint angles (rad) -> tip position (x, y, z) in the base_link frame.

    Used both to *drive* the arm and to *verify* an IK solution."""
    # Reach in the vertical arm-plane (before the base yaw is applied):
    reach = L2 * math.sin(t2) + L3 * math.sin(t2 + t3)   # horizontal component
    height = D1 + L2 * math.cos(t2) + L3 * math.cos(t2 + t3)
    x = reach * math.cos(t1)
    y = reach * math.sin(t1)
    z = height
    return (x, y, z)


def inverse_kinematics(x, y, z, elbow_up=True):
    """Target (x, y, z) in the base_link frame -> joint angles (t1, t2, t3).

    Returns a tuple of three angles in radians, or raises ValueError if the
    point is outside the arm's reachable workspace.

    elbow_up selects between the two valid elbow configurations (the arm can
    reach most points with the elbow bent "up" or "down").
    """
    # 1) Base yaw: turn the whole arm so the target lies in its vertical plane.
    t1 = math.atan2(y, x)

    # 2) Reduce to a 2-link planar problem in that plane.
    r = math.hypot(x, y)     # forward distance from the base axis
    s = z - D1               # height of the target above the shoulder
    dist = math.hypot(r, s)  # straight-line shoulder-to-target distance

    if dist > REACH_MAX + 1e-9 or dist < REACH_MIN - 1e-9:
        raise ValueError(
            f"Target ({x:.3f}, {y:.3f}, {z:.3f}) is out of reach: "
            f"distance {dist:.3f} m not in [{REACH_MIN:.3f}, {REACH_MAX:.3f}] m."
        )

    # 3) Elbow angle via the law of cosines.
    cos_t3 = (dist * dist - L2 * L2 - L3 * L3) / (2 * L2 * L3)
    cos_t3 = max(-1.0, min(1.0, cos_t3))          # clamp tiny numeric overshoot
    t3 = math.acos(cos_t3)
    if not elbow_up:
        t3 = -t3

    # 4) Shoulder angle: aim at the target, then correct for the forearm.
    t2 = math.atan2(r, s) - math.atan2(L3 * math.sin(t3), L2 + L3 * math.cos(t3))

    return (t1, t2, t3)


def _self_test():
    targets = [
        (0.30, 0.15, 0.20),
        (0.40, 0.00, 0.10),
        (0.20, -0.20, 0.30),
        (0.00, 0.35, 0.15),
    ]
    print(f"D1={D1}  L2={L2}  L3={L3}  reach=[{REACH_MIN}, {REACH_MAX}] m\n")
    print(f"{'target':>22} | {'joint angles (deg)':>24} | {'FK error (m)':>12}")
    ok = True
    for tx, ty, tz in targets:
        q = inverse_kinematics(tx, ty, tz)
        px, py, pz = forward_kinematics(*q)
        err = math.dist((tx, ty, tz), (px, py, pz))
        ok = ok and err < 1e-9
        deg = [math.degrees(a) for a in q]
        print(f"({tx:5.2f},{ty:5.2f},{tz:5.2f}) | "
              f"[{deg[0]:6.1f} {deg[1]:6.1f} {deg[2]:6.1f}] | {err:.2e}")
    print("\nSELF-TEST", "PASSED" if ok else "FAILED")


if __name__ == "__main__":
    _self_test()
