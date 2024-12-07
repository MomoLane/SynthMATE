import time
from threading import Thread


class ReactionController:
    def __init__(self, arduino, log_callback):
        self.arduino = arduino
        self.log_callback = log_callback
        self.running = False
        self.paused = False

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def start_reactions(self, reaction_data):
        self.reaction_thread = Thread(target=self._run_reactions, args=(reaction_data,))
        self.running = True
        self.paused = False
        self.reaction_thread.start()

    def pause_reactions(self):
        self.paused = True
        self._log("Reaction paused.")

    def resume_reactions(self):
        self.paused = False
        self._log("Reaction resumed.")

    def stop_reactions(self):
        self.running = False
        self._log("Reaction stopped.")

    def _run_reactions(self, reaction_data):
        for reaction in reaction_data:
            if not self.running:
                break

            while self.paused:
                time.sleep(0.5)

            self._log(f"Running reaction {reaction['Reaction #']}")
            self._execute_reaction(reaction)
            time.sleep(2)

        self._log("All reactions completed.")

    def _execute_reaction(self, reaction):
        self._log(f"Executing: {reaction}")
        time.sleep(2)