from setuptools import find_packages, setup


setup(
    name="Notification-Myem-Lib",
    version="1.0",
    url="",
    license="",
    author="",
    author_email="",
    description="",
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=["importlib-metadata==4.13.0", "typing_extensions==4.0.1", "requests==2.28.1"],
    extras_require={
        "dev": [
            # this depdency should be present in the client, we only used it here for test.
            "pytest==6.2.5",
            "coverage==6.2",
            "flake8==3.9.2",
            "pytest-dotenv==0.5.2",
            "pre-commit==2.17.0",
            "pydocstyle==6.1.1",
            "pylint==2.12.2",
            "mypy==0.910",
            "typed-ast==1.4.3",
        ],
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
