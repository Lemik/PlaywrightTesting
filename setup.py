from setuptools import setup, find_packages

setup(
    name="playwright-testing",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "pytest-playwright",
        "playwright",
        "python-dotenv",
        "pytest-html",
        "pytest-xdist"
    ],
) 