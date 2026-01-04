#!/usr/bin/env python3
"""
Setup script for SmartConnect Contact Management System
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    """Read README.md for long description."""
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "SmartConnect Contact Management System - A modern, secure desktop contact manager"

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt."""
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return ["customtkinter>=5.2.0", "bcrypt>=4.0.0"]

setup(
    name="smartconnect",
    version="1.0.0",
    author="SmartConnect Team",
    author_email="contact@smartconnect.com",
    description="A modern, secure desktop contact management system with user authentication",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smartconnect",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/smartconnect/issues",
        "Source": "https://github.com/yourusername/smartconnect",
        "Documentation": "https://github.com/yourusername/smartconnect/blob/main/README.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Groupware",
        "Topic :: Database :: Front-Ends",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Natural Language :: English",
        "Topic :: Communications :: Email :: Address Book",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "hypothesis>=6.82.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "build": [
            "pyinstaller>=5.0.0",
            "setuptools>=65.0.0",
            "wheel>=0.37.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smartconnect=run:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.rst"],
    },
    keywords=[
        "contact management",
        "address book",
        "desktop application",
        "gui",
        "customtkinter",
        "sqlite",
        "authentication",
        "user management",
        "contacts",
        "crm",
    ],
    zip_safe=False,
)