from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

# Replace this with your Google Sheet URL (CSV format)
SHEET_URL = "https://docs.google.com/spreadsheets/d/your_sheet_id/pub?output=csv"

def fetch_data():
    response = requests.get(SHEET_URL)
    data = response.content.decode("utf-8")
    df = pd.read_csv(pd.compat.StringIO(data))  # Convert CSV to DataFrame
    return df.to_dict(orient="records")  # Convert to list of dictionaries

@app.route("/")
def home():
    cards = fetch_data()
    return render_template("index.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
