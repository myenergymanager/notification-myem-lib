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
    install_requires=[
        "requests==2.28.1",
    ],
    extras_require={
        "dev": [
            # this depdency should be present in the client, we only used it here for test.
            "pytest==7.2.0",
            "coverage==6.5.0",
            "flake8==6.0.0",
            "pytest-dotenv==0.5.2",
            "pre-commit==2.20.0",
            "pydocstyle==6.1.1",
            "pylint==2.15.8",
            "mypy==0.991",
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
