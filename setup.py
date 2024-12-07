from setuptools import setup, find_packages

setup(
    name="SynthMATE",
    version="1.0",
    description="Automated Azo Dye Synthesis using Raspberry Pi, Python and Arduino to control peristaltic pumps",
    author="Collen Skhosana",
    author_email="amykelani.skhosana@yahoo.com",
    role="Research Associate (Developer)",
    affiliation="University of Johannesburg",
    packages=find_packages(),
    include_package_data=True,
    Install_requires=[
        "tkinter",
        "openpyxl",
        "pyfirmata",
        "opencv-python",
        "pillow",
        "numpy",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "synthmate=app.gui:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
