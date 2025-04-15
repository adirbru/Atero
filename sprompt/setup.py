# setup.py

from setuptools import setup, find_packages

setup(
    name="sprompt",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    description="A Python library for security verification of model prompts with slow policy generation to challenge monkey-patching.",
    entry_points={
        "console_scripts": [
            "prompt_security_client=client.main:main",
        ],
    },
)
