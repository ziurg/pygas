from setuptools import find_packages, setup

# pip install --editable .
setup(
    name="pygas",
    description="Calcul de réseaux de gaz.",
    url="https://github.com/ziurg/pygas",
    license="MIT",
    classifiers=[
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=["click", "numpy", "scipy", "matplotlib", "pandas", "pyvis"],
    extras_require={
        "test": ["coverage", "pytest", "pytest-cov"],
    },
    entry_points={
        "console_scripts": [
            "pygas=app.entrypoints.cli:main",
        ],
    },
)
