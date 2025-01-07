from config import CONFIG  # Import the config.py file
import cv2
import time
import pandas as pd
from pyfirmata import Arduino, util
from datetime import datetime


class AzoDyeSynthesis:
    def __init__(self, board):
        self.board = board
        self.pump_pins = CONFIG["pump_pins"]  # Use pump pins from CONFIG
        

    def load_reaction_data(self, file_path):
        """
        Load the reaction data from an Excel or CSV file.
        """
        try:
            if file_path.endswith('.xlsx'):
                self.data = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)

            required_columns = ['Reaction #', 'Aniline derivative 1', 'Aniline derivative 2', 'Sodium Nitrite', 'Total Volume']
            if not all(col in self.data.columns for col in required_columns):
                raise ValueError("Missing required columns in the data.")
        except Exception as e:
            raise RuntimeError(f"Failed to load reaction data: {str(e)}")

    def run_synthesis(self):
        """
        Execute the synthesis process for each reaction.
        """
        if self.data is None:
            raise RuntimeError("No reaction data loaded.")

        for index, reaction in self.data.iterrows():
            print(f"Starting Reaction {reaction['Reaction #']}...")
            self.perform_diazotization(reaction)
            self.perform_coupling(reaction)
            self.capture_reaction_image(reaction['Reaction #'])
            self.clean_vial()

    def perform_diazotization(self, reaction):
        """
        Perform the diazotization step.
        """
        self.pump_liquid(self.pump_pins['Aniline derivative 1'], reaction['Aniline derivative 1'])
        self.pump_liquid(self.pump_pins['Sodium Nitrite'], reaction['Sodium Nitrite'])
        time.sleep(120)

    def perform_coupling(self, reaction):
        """
        Perform the coupling step.
        """
        self.pump_liquid(self.pump_pins['Aniline derivative 2'], reaction['Aniline derivative 2'])
        time.sleep(1800)

    def pump_liquid(self, pump_pin, volume):
        calibration = self.pump_pins.get(pump_pin, 1)  # Default to 1 if missing
        duration = volume / calibration
        print(f"Pumping {volume} mL from Pump {pump_pin} (duration: {duration}s)...")
        self.board.digital[pump_pin].write(1)
        time.sleep(duration)
        self.board.digital[pump_pin].write(0)
        

    def capture_reaction_image(self, reaction_number):
        """
        Capture a reaction photo and extract the color hex code.
        """
        print(f"Capturing image for Reaction {reaction_number}...")
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            file_name = f"reaction_{reaction_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(file_name, frame)
            print(f"Image saved as {file_name}.")
            hex_code = self.extract_color_hex(frame)
            print(f"Color Hex Code: {hex_code}")
        cam.release()

    def extract_color_hex(self, image):
        """
        Extract the predominant color from an image and return its hex code.
        """
        avg_color = image.mean(axis=0).mean(axis=0)
        hex_code = "#{:02x}{:02x}{:02x}".format(int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
        return hex_code

    def clean_vial(self):
        """
        Clean the reaction vial with deionized water.
        """
        print("Cleaning vial...")
        self.pump_liquid(self.pump_pins['Wash'], 10)
        self.pump_liquid(self.pump_pins['Waste'], 10)
