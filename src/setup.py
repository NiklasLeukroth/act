import os

from setuptools import setup

package_name = "act"

share_dir = os.path.join("share", package_name)

setup(
    name=package_name,
    version="0.1.0",
    description="Digit Depth Reconstruction",
    url="https://github.com/vocdex/digit-depth",
    author="Shukrullo Nazirjonov",
    author_email="nazirjonovsh2000@gmail.com",
    license="MIT",
    install_requires=["numpy", "opencv-python", "torch"],
    packages=[package_name],
    data_files=[
        ("share/" + package_name, ["package.xml"]),
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "act_node = act.act_eval:main"
        ],
    },
)
