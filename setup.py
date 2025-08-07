from setuptools import setup, find_packages


setup(
    name="django-sightline",
    version="0.1.0",
    description="Smart, privacy-friendly site analytics for Django. Track visits, popular pages, referrers, and more — directly from the admin dashboard.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Francesco Ridolfi",
    author_email="francesco.ridolfi.02@gmail.com",
    url="https://github.com/francescoridolfi/django-sightline",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Django>=3.2",
        "user-agents>=2.2.0"
    ],
)