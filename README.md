SynthMATE 

SynthMATE is an automated synthesis platform designed to conduct azo dye reactions and can be modified for other chemical synthesis as per user requirements. Utilizing Python and OpenCV, SynthMATE provides users with a flexible interface to control peristaltic pumps, take real-time reaction photos, and monitor each step of the chemical reaction process.

Overview

SynthMATE automates the synthesis of azo dyes, replicating advanced methodologies with simplified yet effective processes. 

The project involves:

Pump Assignments for chemical handling

Automated Reaction Steps including diazotization, coupling, dilution, and washing

Hexadecimal Color Analysis for visual product analysis

SynthMATE is built with Python's tkinter library for Graphical User Interface (GUI), pyFirmata for pump control via Arduino, and OpenCV for image processing using a Raspberry Pi computer and camera.

Features

Automated Chemical Reaction Steps: Controls pumps for a sequence of reactions.

Pause and Resume: Allows users to pause and resume reactions.

Hexadecimal Color Analysis: Records colors from product images to streamline analysis.

Data Export and Reporting: Saves results in Excel format for further data analysis.

Setup and Installation

Prerequisites

1. Hardware: Arduino, peristaltic pumps, Raspberry Pi (optional), camera.

2. Python: Python 3.9

3. Python Libraries: Install required libraries using the command line: pip install -r requirements.txt

Installation Steps

1. Clone this repository: 
   
   
      git clone https://github.com/MomoLane/SynthMATE.git


2. Unzip the folder in your home directory.
   

3. Navigate to the SynthMATE-main unzipped folder using the command line: 
   
   
      cd SynthMATE-main

4.Connect Arduino microcontroller board to the Raspberry Pi computer using a USB serial communication cable

5.Configure the GUI by editing config.py file in the app directory to change Arduino port and other variables.

Usage

Launching the Application

Run the GUI using the following command:

python gui.py

Importing Reaction Data

1. Use File > Import Excel to load an Excel sheet containing reaction volumes and combinations.


2. A summary will be displayed before the reaction starts for user confirmation.

Running the Reaction Process

1. Start the process by pressing "Start".
2. Pause or Resume as needed.
3. At each step, the GUI will display logs, and a camera image will capture key reaction phases.
4. Results are saved in an Excel file, including color analysis in hexadecimal format.

Detailed Functionality
Pump Assignments
The pumps have the following assignments:

Pump 1: Aniline derivative 1
Pump 2: Aniline derivative 2
Pump 3: Aniline derivative 3
Pump 4: Sodium nitrite
Pump 5: Sodium hydroxide
Pump 6: Deionized water
Pump 7: Waste
Pump 8: Wash

Reaction Workflow

The software controls each pump and follows this synthesis process:

1. Diazotization: Sodium nitrite and aniline derivative mix.
2. Coupling Reaction: A second aniline derivative is added.
3. Dilution and Neutralization: Sodium hydroxide is added after dilution.
4. Washing and Repetition: The solution is removed to waste, and the vial is washed.

Logging

All key events and errors are logged in the GUI log panel. The log panel also includes timestamps for easy reference.

Pause and Resume Functionality

The Pause function allows the user to halt the process at any point and resume seamlessly by presssing the Start function:

Pause: Temporarily stops the process.

Start: Continues the process from where it left off.

This feature is critical for manually intervening in case of unexpected issues.

Image Analysis and Color Extraction

Images captured during the reaction process are analyzed using OpenCV. The GUI converts the image to hexadecimal color values to record color changes and aid in reaction monitoring.

Configuration

To adjust settings, such as pump delay times or camera settings, edit the relevant scripts. Ensure to follow the format provided and document any changes made.

Contributing

1. Fork the repository.

2. Create a new branch for your feature (git checkout -b feature-name).
Commit your changes (git commit -am 'Add new feature').
3. Push the branch (git push origin feature-name).
4. Create a Pull Request to merge your changes.

I welcome contributions of bug fixes, feature improvements, or documentation enhancements.

License

This project is licensed under the GNU General Public License. See the LICENSE file for details.

References

Use the UJ Harvard referencing system for citing this software in academic publications. Refer to the University of Johannesburg’s guidelines for correct citation format.
