from flask import Flask, render_template
import requests
import pandas as pd
import io

app = Flask(__name__)

# Replace this with your Google Sheet URL (CSV format)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQbXNvjqouvsgiidt7Ra2CvWotrQA_0iDoSiWfhNDews05Afp3bjNlOcfvh-9Hv9dPFp0L4f7QZR-Ah/pub?output=csv"

def fetch_data():
    response = requests.get(SHEET_URL)
    data = response.content.decode("utf-8")
    df = pd.read_csv(io.StringIO(data))

    # Extract column headers from B2:I2
    column_headers = df.iloc[0, 1:9].tolist()

    # Slice data correctly: Titles from A3:A14, values from B3:I14
    df = df.iloc[2:14].reset_index(drop=True)  # Rows 3-14 (zero-based index)
    df.rename(columns={df.columns[0]: "Title"}, inplace=True)

    # Convert to list of dictionaries
    cards = []
    for _, row in df.iterrows():
        card = {
            "Title": row["Title"],  # Title from column A
            "Headers": column_headers,  # Headers from B2:I2
            "Values": row.iloc[1:9].tolist()  # Data from B-I
        }
        cards.append(card)

    return cards

@app.route("/")
def home():
    cards = fetch_data()
    return render_template("index.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
