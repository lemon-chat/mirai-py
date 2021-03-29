
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mirai-py", # Replace with your own username
    version="0.0.1",
    author="Jun Wang",
    author_email="jstzwj@aliyun.com",
    description="Mirai python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jstzwj/mirai-py",
    project_urls={
        "Bug Tracker": "https://github.com/jstzwj/mirai-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7'
)