import setuptools

with open('DESCRIPTION.md') as description:
	long_description = description.read()

setuptools.setup(
    name="argcompile",
    version="0.0.4",
    author="Arthur Henrique Della Fraga",
    author_email="Arthur.Henrique.Della.Fraga@gmail.com",
    description="An argparse extension to easily manage post-processing of multiple parsed arguments",
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
