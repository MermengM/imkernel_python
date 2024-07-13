from setuptools import find_packages, setup

setup(
    name="imkernel",
    version="0.1.0",
    author="ermeng",
    author_email="ermeng@ermeng.fun",
    description="imkernel for python",
    long_description="imkernel是基于三维四层统一模型（IM)理念以及工业语言(IL)构建的python类库",
    url="https://github.com/MermengM/imkernel_python",
    packages=find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[],
    license="GNU General Public License v3 or later (GPLv3+)",
    keywords="IMKernel kernel IM IL",
    project_urls={
        "Bug Tracker": "https://github.com/MermengM/imkernel_python/issues",
    },
)
