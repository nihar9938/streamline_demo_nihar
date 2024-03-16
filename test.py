import streamlit as st
import pandas as pd
import json

def csv_to_json_html(csv_file):
    """Reads a CSV file, converts it to JSON, and creates an HTML file with the JSON data."""

    df = pd.read_csv(csv_file)
    json_data = df.to_json(orient="records")

    with open("data.html", "w") as f:
        f.write("<h1>CSV Data as JSON</h1>")
        f.write("<pre>")
        json.dump(json_data, f, indent=4)
        f.write("</pre>")

    return "data.html"

def download_html_file(file_path):
    """Downloads the specified HTML file."""

    with open(file_path, "rb") as f:
        content = f.read()

    st.download_button(
        label="Download JSON as HTML",
        data=content,
        file_name=file_path,
        mime="text/html",
    )

if __name__ == "__main__":  # Only run for Streamlit execution
    st.title("CSV to JSON HTML Generator Demo by Nihar")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        try:
            html_file = csv_to_json_html(uploaded_file)
            st.write(f"Generated HTML file: [{html_file}](data.html)")
            download_html_file(html_file)  # Add the download button here
        except Exception as e:
            st.error(f"Error processing CSV: {e}")
