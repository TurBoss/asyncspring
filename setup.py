import setuptools

setuptools.setup(
    name="asyncspring",
    version="0.1.0",
    url="https://github.com/turboss/asyncspring",

    author="TurBoss",
    author_email="tutboss@mail.com",

    description="Asyncio python library for the SpringLobby protocol",
    long_description=open("README.md").read(),

    packages=setuptools.find_packages(),

    install_requires=[
        "asyncblink",
        "ruamel.yaml"
    ],

    classifiers=[
        "Development Status :: 1 - Beta",
        'License :: MIT License (MIT)',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires="~=3.6",
)
