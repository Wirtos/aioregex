import setuptools

setuptools.setup(
    name="aioregex",
    version="0.1",
    author="Wirtos_new",
    author_email="Wirtos.new@gmail.com",
    description="regex to allow both sync and async callables in the sub as repl",
    url="https://wirtos.github.io/aioregex/",
    packages=setuptools.find_packages(),
    project_urls={
        "Source Code": "https://github.com/Wirtos/aioregex",
    },
    install_requires=[],
    keywords="regex re asyncio aioregex",
    classifiers=[
        "Programming Language :: Python :: >=3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
