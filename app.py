from flask import Flask, render_template
import pandas as pd
import numpy as np  # Needed for handling NaN values

app = Flask(__name__)

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQbXNvjqouvsgiidt7Ra2CvWotrQA_0iDoSiWfhNDews05Afp3bjNlOcfvh-9Hv9dPFp0L4f7QZR-Ah/pub?output=csv"

def fetch_data():
    df = pd.read_csv(GOOGLE_SHEET_URL)

    # Ensure there are enough rows to avoid errors
    if df.shape[0] < 2:
        return [], []

    # Extract column headers from the actual column names (ignoring the first row)
    column_headers = df.columns[1:9].tolist()

    # Extract cards dynamically based on available rows
    cards = []
    for i in range(1, min(14, len(df))):  # Start at row 2 (index 1)
        card = {
            "title": df.iloc[i, 0] if pd.notna(df.iloc[i, 0]) else "",  # Handle NaN in title
            "data": df.iloc[i, 1:9].replace(np.nan, "").tolist()  # Replace NaN with empty strings in data
        }
        cards.append(card)

    return column_headers, cards

@app.route("/")
def home():
    column_headers, cards = fetch_data()
    return render_template("index.html", column_headers=column_headers, cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
