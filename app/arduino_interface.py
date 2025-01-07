import pyfirmata
import time
from config import CONFIG  # Import the config.py file

class ArduinoInterface:
    def __init__(self, port):
        self.board = pyfirmata.Arduino(port)
        self.pump_pins = CONFIG["pump_pins"]  # Use pump pins from CONFIG
        self.iterator = pyfirmata.util.Iterator(self.board)
        self.iterator.start()
        print(f"Connected to Arduino on {port}")

        self.pumps = [self.board.get_pin(f'd:{i}:o') for i in range(2, 10)]

    def activate_pump(self, pump_index):
        """Activate a specific pump."""
        if 0 <= pump_index < len(self.pumps):
            self.pumps[pump_index].write(1)

    def deactivate_pump(self, pump_index):
        """Deactivate a specific pump."""
        if 0 <= pump_index < len(self.pumps):
            self.pumps[pump_index].write(0)

    def dispense(self, pump_pin, volume):
        calibration = self.pump_pins.get(pump_pin, 1)  # Default to 1 if missing
        duration = volume / calibration
        print(f"Dispensing {volume} mL via Pump {pump_pin} (duration: {duration}s)...")
        self.board.digital[pump_pin].write(1)
        time.sleep(duration)
        self.board.digital[pump_pin].write(0)

    def stop_all(self):
        """Stop all pumps immediately."""
        print("Stopping all pumps.")

    def close(self):
        """Release Arduino resources."""
        self.board.exit()
        print("Arduino connection closed")
