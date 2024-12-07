import pandas as pd


def load_reaction_data(file_path):
    try:
        df = pd.read_excel(file_path)
        reaction_data = df.to_dict("records")
        return reaction_data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
