import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="argcompile",
    version="0.0.1",
    author="Arthur Henrique Della Fraga",
    author_email="Arthur.Henrique.Della.Fraga@gmail.com",
    description="An argparse extension to manage process multiple input arguments in several goals.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/artu-hnrq/argcompile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
