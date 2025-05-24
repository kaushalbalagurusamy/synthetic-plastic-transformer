from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="synthetic-plastic-transformer",
    version="0.1.0",
    author="Your Name",
    author_email="your-email@example.com",
    description="A materials discovery engine for replacing synthetic polymers with organic natural fibers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/synthetic-plastic-transformer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.3.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spt-train=synthetic_plastic_transformer.cli:train",
            "spt-predict=synthetic_plastic_transformer.cli:predict",
            "spt-evaluate=synthetic_plastic_transformer.cli:evaluate",
        ],
    },
    include_package_data=True,
    package_data={
        "synthetic_plastic_transformer": ["data/*.json", "configs/*.yaml"],
    },
) 