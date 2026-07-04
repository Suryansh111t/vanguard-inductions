# Task 3: Panorama or Bust (The Wider Picture)

## The Problem

When our systems deploy in the field, documentation is everything. A single narrow photo
of a worksite is useless to the analysis team. We need expansive, highly accurate 1:3
panoramas with scale and directional data. The catch? The camera can only take small,
overlapping snapshots, and naive copy-pasting leaves ugly seams and distorted data.

## Your Mission

Build a custom image-stitching pipeline — essentially coding your phone's "Panorama Mode"
from scratch using Computer Vision. You need to detect overlapping features in a set of
photos, mathematically align them, and seamlessly blend them into a perfect, annotated
wide-angle shot.

## What You Need To Do

* **Gather Intel** — Go outside and shoot 5–8 overlapping images per site, for 2–3
  different sites.
* **Find the Commonalities** — Use feature detection algorithms (SIFT or ORB) to find
  matching points between your images. Justify your choice!
* **Align & Stitch** — Use RANSAC and Homography estimation to reject bad matches and
  mathematically glue the images together.
* **Polish & Annotate** — Blend the seams so they disappear. Crop the final image to a
  strict 1:3 (Height:Width) ratio, and overlay a manual scale bar and a cardinal direction
  arrow (N/E/S/W).

## Helpful Resources

* [OpenCV Feature Matching tutorial](https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html)
* [OpenCV Homography & RANSAC tutorial](https://docs.opencv.org/4.x/d9/dab/tutorial_homography.html)
* [SIFT vs ORB — feature detector overview](https://docs.opencv.org/4.x/db/d27/tutorial_py_table_of_contents_feature2d.html)

## Working in Docker

This task only needs Python + OpenCV — no ROS or Gazebo required. Run it on your host
machine directly, **or** inside the container, which already has
`opencv-contrib-python` installed (the `-contrib` build is required for SIFT). See
[`docs/GETTING_STARTED.md`](../../docs/GETTING_STARTED.md) either way.

If you use the container, work inside `vanguard_ws/src/task3` — it's mounted straight to
this `tasks/task3/` folder, so your files are already in the right place to commit.

## Deliverables

Place everything below directly in this folder (`tasks/task3/`):

1. Your complete Python stitching script.
2. 2–3 finished panoramas that meet the 1:3 ratio and annotation requirements.
3. A short, honest report: where did the stitching fail (e.g. repetitive textures, low
   overlap)? How did you fix or bypass these issues?
