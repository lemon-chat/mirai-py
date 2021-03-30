
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mirai-py", # Replace with your own username
    version="0.1a1.dev1",
    author="Jun Wang",
    author_email="jstzwj@aliyun.com",
    description="Mirai python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lemon-chat/mirai-py",
    project_urls={
        "Bug Tracker": "https://github.com/lemon-chat/mirai-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7'
)