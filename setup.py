from pathlib import Path
from setuptools import setup, find_packages

server = Path(__file__).parent / "chbs" / "server.py"
with server.open("r") as f:
    for line in f:
        if line.startswith("__version__"):
            __version__ = line.partition("=")[-1].strip().strip('"').strip("'")
            break

changelog = (Path(__file__).parent / "CHANGELOG.txt").read_text()
readme = (Path(__file__).parent / "README.md").read_text()
long_desc = readme + "\n\n---\n\n" + changelog

tests_require = ["pytest"]
setup(
    name="chbs",
    version=__version__,
    author="Wayne Werner",
    author_email="wayne@waynewerner.com",
    url="https://github.com/waynew/correcthorsebatterystaple",
    packages=find_packages(),
    data_files=["chbs/adjectives.txt", "chbs/nouns.txt"],
    entry_points="""
    [console_scripts]
    chbs=chbs.server:do_it
    """,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    tests_require=tests_require,
    extras_require={"test": tests_require, "build": ["wheel"]},
    classifiers=["License :: OSI Approved :: MIT License"],
)
