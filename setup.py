from setuptools import find_packages, setup

setup(
    name="imkernel",
    version="0.1.0",
    author="ermeng",
    author_email="ermeng@ermeng.fun",
    description="A brief description of IMKernel",
    long_description="A long description of IMKernel",
    url="https://github.com/MermengM/im_kernel_python",
    packages=find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[],
    license="GNU General Public License v3 or later (GPLv3+)",
    keywords="IMKernel kernel image processing",
    project_urls={
        "Bug Tracker": "https://github.com/MermengM/im_kernel_python/issues",
    },
)
