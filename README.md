# Link Checker and Excel Exporter

This project is a Streamlit application that reads an Excel file containing URLs, checks each URL (and its links and images) for their status, and exports the collected data into a new Excel file. The project is modularized into several Python files for better maintainability and extensibility.

## Features

- **Excel URL Import:** Reads URLs from an Excel file (expects a column named `URL`).
- **Link Checking:** Fetches each URL, parses the HTML for all anchor tags, and checks the status of each link.
- **Image Checking:** Extracts and verifies all images on the page.
- **Canonical URL Extraction:** Extracts the canonical URL from each page, if available.
- **Timestamp Logging:** Adds an IST timestamp to each record.
- **Error Summary:** Displays an error summary for easy analysis.
- **Excel Export:** Exports the collected link and image data into an Excel file for further analysis.
- **Modular Design:** Code is split into separate modules to handle reading, link checking, image checking, and data processing.

## File Structure

```
.
├── app.py              # Main Streamlit application
├── excel_reader.py     # Module to read URLs from Excel files
├── link_checker.py     # Module to fetch URLs, check links, and validate images
├── data_processor.py   # Module to process each URL and aggregate data
└── requirements.txt    # Project dependencies
```

## Setup and Installation

### 1. Create and Activate a Virtual Environment

- **macOS/Linux:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

- **Windows (Command Prompt):**
  ```bash
  python -m venv venv
  venv\Scripts\activate.bat
  ```

- **Windows (PowerShell):**
  ```bash
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

### 2. Install Dependencies

With your virtual environment activated, run:

```bash
pip install -r requirements.txt
```

The **requirements.txt** file includes:
```txt
streamlit
requests
beautifulsoup4
pandas
pytz
openpyxl
```

## Running the Application

After installing the dependencies, start the Streamlit app by running:

```bash
streamlit run app.py
```

The application will launch in your default browser. Follow the on-screen instructions to:

1. Input a base URL for relative links.
2. Upload an Excel file containing a column named `URL`.
3. Specify the desired output file name (e.g., `output.xlsx`).
4. Click the **Process** button to check the links and images and generate the Excel report.

## How It Works

- **Excel Reader:** The `excel_reader.py` module reads URLs from the uploaded Excel file.
- **Link & Image Checker:** The `link_checker.py` module fetches each URL, parses the HTML using BeautifulSoup, checks the status of each link and image, and records relevant data.
- **Data Processor:** The `data_processor.py` module iterates over the list of URLs and aggregates the link and image check results.
- **Main App:** The `app.py` file ties all modules together using Streamlit, and provides a user interface to upload files, process data, and download results.

## Error Handling & Summary

- The application detects broken links (status codes 400-599) and lists them under an error summary.
- Images that fail to load or are not valid images are flagged for review.
- The error rate percentage is displayed for quick analysis.

