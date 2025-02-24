from flask import Flask, render_template
import requests
import pandas as pd
import io

app = Flask(__name__)

# Replace with your Google Sheet CSV link
SHEET_URL = "https://docs.google.com/spreadsheets/d/your_sheet_id/pub?output=csv"

def fetch_data():
    try:
        response = requests.get(SHEET_URL)
        response.raise_for_status()  # Check if the request was successful
        data = response.content.decode("utf-8")
        df = pd.read_csv(io.StringIO(data), skiprows=1)  # Skip Row 1

        if df.empty:
            print("Error: Google Sheet is empty!")
            return []

        # Extract column headers from Row 2 (B2:I2)
        column_headers = df.iloc[0, 1:9].tolist()

        # Extract rows from A3:A14 (Titles) and B3:I14 (Data)
        df = df.iloc[1:12].reset_index(drop=True)  # Select rows 3-14 (1-based indexing)

        # Rename first column (A) to "Title"
        df.rename(columns={df.columns[0]: "Title"}, inplace=True)

        # Convert to list of dictionaries for HTML rendering
        cards = []
        for _, row in df.iterrows():
            card = {
                "Title": row["Title"],  # Card title from Column A
                "Headers": column_headers,  # Table headers (B2:I2)
                "Values": row.iloc[1:9].tolist()  # Row data (B3:I3 → B14:I14)
            }
            cards.append(card)

        return cards

    except Exception as e:
        print("Error fetching data:", e)
        return []

@app.route("/")
def home():
    cards = fetch_data()
    return render_template("index.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
