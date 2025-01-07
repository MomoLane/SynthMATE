from config import CONFIG  # Import the config.py file
import time
import pandas as pd
from pyfirmata import Arduino, util


class AgNPsynthesis:
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

            required_columns = ['Deionized Water', 'AgNO3 Solution', 'NaOH Solution']
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
            print("Starting AgNP Reaction")
            self.arduino.dispense("Deionized Water", reaction['Deionized Water'])
            print("Manually add DBSA and aniline now.")
            time.sleep(300)
            self.arduino.dispense("AgNO3 Solution", reaction['AgNO3 Solution'])
            print("Stirring for 15 minutes...")
            time.sleep(900)  # Allow Stirring for 15 minutes
            self.arduino.dispense("NaOH Solution", reaction['NaOH Solution'])
            print("Heating and stirring at 90°C for 2 minutes...")
            time.sleep(120) # Simulate 2 minute reaction time
            print("Checking reaction completion...")
            time.sleep(5)  # Simulate completion check
            print("Reaction Complete")
            

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


