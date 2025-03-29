"""

"""

# setup.py
from setuptools import setup, find_packages

setup(
    name="stayforge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "pathspec",
        "tomli", "tomli_w",
        "requests", "urllib3"
                    "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "stayforge=scripts.cil:main",
        ],
    },
)
