from config import CONFIG  # Import the config.py file
import time
import pandas as pd
from pyfirmata import Arduino, util



class HeckReaction:
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

            required_columns = ['DMF', 'Iodobenzene', 'Ethyl acrylate']
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
            print("Starting Heck Reaction")
            self.arduino.dispense("DMF", reaction['DMF'])
            time.sleep(60)
            self.arduino.dispense("Iodobenzene", reaction['Iodobenzene'])
            print("Stirring for 2 minutes...")
            time.sleep(120)  # Allow Stirring for 2 minutes
            self.arduino.dispense("Ethyl acrylate", reaction['Ethyl acrylate'])
            print("Stirring 2 minutes...")
            time.sleep(120) # Simulate 2 minute reaction time
            print("Add solid reagents + catalyst...")
            time.sleep(5)  # Simulate completion check
            print("Disconnect device and allow reaction to run overnight")



    def pump_liquid(self, pump_pin, volume):
        calibration = self.pump_pins.get(pump_pin, 1)  # Default to 1 if missing
        duration = volume / calibration
        print(f"Pumping {volume} mL from Pump {pump_pin} (duration: {duration}s)...")
        self.board.digital[pump_pin].write(1)
        time.sleep(duration)
        self.board.digital[pump_pin].write(0)
        

    def clean_vial(self):
        """
        Clean the reaction vial with deionized water.
        """
        print("Cleaning vial...")
        self.pump_liquid(self.pump_pins['Wash'], 10)
        self.pump_liquid(self.pump_pins['Waste'], 10)
    
