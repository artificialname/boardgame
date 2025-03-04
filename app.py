from flask import Flask, jsonify, send_from_directory
import requests
import csv
import os

app = Flask(__name__, static_folder="static")

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQbXNvjqouvsgiidt7Ra2CvWotrQA_0iDoSiWfhNDews05Afp3bjNlOcfvh-9Hv9dPFp0L4f7QZR-Ah/pub?output=csv"

def fetch_google_sheet():
    try:
        response = requests.get(GOOGLE_SHEET_URL)
        response.raise_for_status()
        lines = response.text.splitlines()
        reader = csv.reader(lines)
        return list(reader)
    except Exception as e:
        print("Error fetching sheet:", str(e))
        return []

@app.route("/")
def serve_index():
    return send_from_directory(os.path.join(app.root_path, "static"), "index.html")

@app.route("/get_grid_data")
def get_grid_data():
    sheet_data = fetch_google_sheet()

    if not sheet_data or len(sheet_data) < 2:
        return jsonify({"headers": [], "titles": [], "rows": []})
    
    headers = sheet_data[0][1:9]  # Extract B to I from row 1
    titles = [row[0] for row in sheet_data[1:101] if len(row) >= 9]  # Extract A for row titles
    rows = [row[1:9] for row in sheet_data[1:101] if len(row) >= 9]  # Extract B to I for rows 2-101
    
    return jsonify({"headers": headers, "titles": titles, "rows": rows})


if __name__ == "__main__":
    app.run(debug=True)
