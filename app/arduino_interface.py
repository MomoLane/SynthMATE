import pyfirmata


class ArduinoInterface:
    def __init__(self, port):
        self.board = pyfirmata.Arduino(port)
        self.pumps = {
            "Aniline 1": 2,
            "Aniline 2": 3,
            "Sodium Nitrite": 4,
            "Sodium Hydroxide": 5,
            "Deionized Water": 6,
            "Waste": 7,
            "Wash": 8
        }

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

    def dispense(self, pump, volume):
        """Simulate dispensing of volume through the specified pump."""
        print(f"Dispensing {volume} mL via pump {pump}...")
        self.board.digital[pump].write(1)

    def stop_all(self):
        """Stop all pumps immediately."""
        print("Stopping all pumps.")

    def close(self):
        """Release Arduino resources."""
        self.board.exit()
        print("Arduino connection closed")