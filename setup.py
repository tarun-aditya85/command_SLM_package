#!/usr/bin/env python3
"""
Setup configuration for command-slm CLI package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="command-slm",
    version="0.1.0",
    description="AI-powered CLI for natural language to shell commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lalitha M V",
    author_email="",
    url="https://github.com/lmv/command-slm",
    packages=find_packages(),
    install_requires=[
        "llama-cpp-python>=0.2.0",
        "huggingface-hub>=0.20.0",
        "rich>=13.0.0",
        "prompt-toolkit>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "command-slm=command_slm.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    keywords="cli bash shell commands ai llm nlp command-line",
)
