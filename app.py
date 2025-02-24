from flask import Flask, render_template
import requests
import pandas as pd
import io  # Import io for StringIO

app = Flask(__name__)

# Replace this with your Google Sheet URL (CSV format)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQbXNvjqouvsgiidt7Ra2CvWotrQA_0iDoSiWfhNDews05Afp3bjNlOcfvh-9Hv9dPFp0L4f7QZR-Ah/pub?output=csv"

def fetch_data():
    response = requests.get(SHEET_URL)
    data = response.content.decode("utf-8")
    df = pd.read_csv(io.StringIO(data), skiprows=1)  # Skip row 1

    # Rename columns for easier access
    df.rename(columns={"Action card": "Title"}, inplace=True)

    # Convert to list of dictionaries
    cards = []
    for _, row in df.iterrows():
        card = {
            "Title": row["Title"],
            "Details": ", ".join([f"{col}: {row[col]}" for col in ["MOF", "MOE", "MOP", "MOI", "MOS", "MOT", "MOC", "MOD"]])
        }
        cards.append(card)

    return cards

@app.route("/")
def home():
    cards = fetch_data()
    return render_template("index.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
