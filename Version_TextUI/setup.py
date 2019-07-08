from setuptools import setup, find_packages

setup(
    name="timetablebuilder",
    packages=find_packages("src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["bs4", "lxml"],
    entry_points={"console_scripts": ["timetablebuilder = timetablebuilder.main"]},
)
