from setuptools import setup
from glob import glob

package_name = "arm3dof"

setup(
    name=package_name,
    version="1.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        # install our data folders so `ros2 launch`/`$(find arm3dof)` can find them
        ("share/" + package_name + "/urdf", glob("urdf/*")),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/config", glob("config/*")),
        ("share/" + package_name + "/rviz", glob("rviz/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Suryansh",
    maintainer_email="suryansh111t@gmail.com",
    description="Task 1: 3-DOF robotic arm with inverse kinematics.",
    license="MIT",
    entry_points={
        "console_scripts": [
            # `ros2 run arm3dof move_arm`
            "move_arm = arm3dof.move_arm:main",
        ],
    },
)
