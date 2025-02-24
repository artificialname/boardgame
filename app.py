from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQbXNvjqouvsgiidt7Ra2CvWotrQA_0iDoSiWfhNDews05Afp3bjNlOcfvh-9Hv9dPFp0L4f7QZR-Ah/pub?output=csv"

def fetch_data():
    df = pd.read_csv(GOOGLE_SHEET_URL)
    
    # Ensure there are enough rows to avoid out-of-bounds errors
    if df.shape[0] < 3:
        return [], []  # Return empty data if there aren't enough rows
    
    # Extract headers from B2:I2 (row index 1, columns B to I)
    column_headers = df.iloc[0, 1:9].tolist()
    
    # Extract cards dynamically based on available rows
    cards = []
    for i in range(1, len(df)):  # Start from index 1 instead of 2
        if i >= len(df):  # Avoid index errors
            break
        card = {
            "title": df.iloc[i, 0],  # Column A (Title)
            "data": df.iloc[i, 1:9].tolist()  # Columns B to I (Data)
        }
        cards.append(card)
    
    return column_headers, cards

@app.route("/")
def home():
    column_headers, cards = fetch_data()
    return render_template("index.html", column_headers=column_headers, cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
