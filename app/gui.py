import tkinter as tk
from tkinter import filedialog, messagebox
from app.controller import ReactionController
from app.arduino_interface import ArduinoInterface
from app.logger import setup_logging
from app.data_loader import load_reaction_data
from app.synthesis import AzoDyeSynthesis
from app.image_processing import capture_image, analyze_color
from app.config import CONFIG
import logging


class SynthMATEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SynthMATE - Automated Azo Dye Synthesis")
        self.root.geometry("800x600")

        self.arduino = ArduinoInterface(CONFIG["arduino_port"])

        self.controller = ReactionController(self.arduino, self.log_message)

        self._setup_gui()

        self.reaction_data = []

    def _setup_gui(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        load_button = tk.Button(button_frame, text="Load Reaction Data", command=self.load_data)
        load_button.grid(row=0, column=1, padx=5)

        start_button = tk.Button(button_frame, text="Start Reaction", command=self.start_reaction)
        start_button.grid(row=0, column=2,padx=5)

        pause_button = tk.Button(button_frame, text="Pause Reaction", command=self.pause_reaction)
        pause_button.grid(row=0, column=3,padx=5)

        stop_button = tk.Button(button_frame, text="Stop Reaction", command=self.stop_reaction)
        stop_button.grid(row=0, column=4,padx=5)

        self.log_panel = tk.Text(self.root, width=80, height=20)
        self.log_panel.pack()

        self.log_panel.config(state=tk.DISABLED)

        self.logger = setup_logging(self.log_panel)

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.reaction_data = load_reaction_data(file_path)
            if self.reaction_data:
                self.logger.info(f"Loaded reaction data from {file_path}")
                self.display_summary()

    def load_reaction_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        try:
            self.synthesis = AzoDyeSynthesis(self.board, self.pump_pins)
            self.synthesis.load_reaction_data(file_path)
            messagebox.showinfo("Success", "Reaction data loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def display_summary(self):
        summary = f"Loaded {len(self.reaction_data)} reactions.\n"
        for i, reaction in enumerate(self.reaction_data, start=1):
            summary += f"Reaction {i}: {reaction}\n"
        if messagebox.askokcancel("Confirm Reactions", summary):
            self.logger.info("Reaction parameters confirmed by the user.")
        else:
            self.logger.info("Reaction parameters not confirmed by the user.")

    def start_reaction(self):
        if not self.reaction_data:
            self.logger.warning("No reaction data loaded.")
            return
        self.controller.start_reactions(self.reaction_data)

    def start_azo_synthesis():
        try:
            app = AzoDyeSynthesis(board, pump_pins={
                'Aniline 1': 2, 'Aniline 2': 3, 'Sodium Nitrite': 4, 'Sodium Hydroxide': 5,
                'Deionized Water': 6, 'Waste': 7, 'Wash': 8
            })
            file_path = filedialog.askopenfilename()
            app.load_reaction_data(file_path)
            app.run_synthesis()
            messagebox.showinfo("Success", "Synthesis completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_reaction(self):
        self.controller.pause_reactions()

    def stop_reaction(self):
        self.controller.stop_reactions()

    def log_message(self, message):
        self.logger.info(message)

    def capture_image_and_analyze(self):
        image_path = capture_image(CONFIG["camera_index"], CONFIG["image_save_path"])
        hex_color = analyze_color(image_path)
        self.logger.info(f"Image captured at {image_path}, Color: {hex_color}")


def main():
    root = tk.Tk()
    app = SynthMATEApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
