from setuptools import setup, find_packages

setup(
    name="uzix",
    version="0.3.0",
    description="Multilingual prompt injection detector — English, Hindi, Hinglish",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Uzix Contributors",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "flask>=2.3.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "python-dotenv>=1.0.1",
        "waitress>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "uzix=uzix.__main__:main",
            "uzix-serve=uzix.server:main",
            "uzix-train=uzix.train:main",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
