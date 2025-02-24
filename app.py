from flask import Flask, render_template
import requests
import pandas as pd
import io  # Import io for StringIO

app = Flask(__name__)

# Replace this with your Google Sheet URL (CSV format )
SHEET_URL = "https://docs.google.com/spreadsheets/d/your_sheet_id/pub?output=csv"

def fetch_data():
    response = requests.get(SHEET_URL)
    data = response.content.decode("utf-8")
    df = pd.read_csv(io.StringIO(data))

    # Extract column headers from the second row (B2:I2)
    column_headers = df.iloc[0, 1:9].tolist()

    # Remove the first row (headers) and reset the index
    df = df.iloc[1:].reset_index(drop=True)

    # Rename the first column (A) to "Title"
    df.rename(columns={df.columns[0]: "Title"}, inplace=True)

    # Convert to list of dictionaries
    cards = []
    for _, row in df.iterrows():
        card = {
            "Title": row["Title"],
            "Headers": column_headers,
            "Values": row.iloc[1:9].tolist()  # Use `.iloc` for better indexing
        }
        cards.append(card)

    return cards

@app.route("/")
def home():
    cards = fetch_data()
    return render_template("index.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
