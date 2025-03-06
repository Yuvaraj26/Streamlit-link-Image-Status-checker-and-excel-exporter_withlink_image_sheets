# Link and Image Status Checker

A Streamlit-based web application that checks the status of links and images across multiple URLs, with support for canonical URL verification and detailed reporting.

## Features

- **URL Processing**: Upload Excel files containing URLs to process
- **Link Checking**: Verifies the status of all links on each webpage
- **Image Validation**: Checks if images load properly and validates their formats
- **Canonical URL Detection**: Identifies canonical URLs for each webpage
- **Detailed Reporting**: Generates comprehensive Excel reports with separate sheets for:
  - Links status
  - Images status
  - Summary statistics
- **Real-time Progress**: Shows processing status and metrics in real-time
- **Error Tracking**: Captures and reports various types of errors encountered

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd Streamlit_Linkstatus_Imagestatus_canonicalurlcheck_withseperateimagesheet_Webscraping
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. In the web interface:
   - Enter the base URL (default: https://www.walmartconnect.ca)
   - Upload an Excel file containing URLs to check
   - Enter the desired output Excel file name
   - Click "Process" to start the analysis

3. The application will:
   - Process each URL
   - Check all links and images
   - Display real-time progress
   - Generate a detailed Excel report

## Input Excel File Format

The input Excel file should contain:
- A column named "URL" with the URLs to check
- One URL per row

## Output Excel File Format

The generated Excel file contains three sheets:

1. **Links Sheet**:
   - Source URL
   - Link URL
   - Link Text
   - Status
   - Status Code
   - Canonical URL
   - Timestamp (IST)

2. **Images Sheet**:
   - Source URL
   - Link URL
   - Alt Text
   - Status
   - Status Code
   - Canonical URL
   - Timestamp (IST)

3. **Summary Sheet**:
   - Total Links
   - Total Images
   - Total Errors
   - Error Rate

## Supported Image Formats

The application supports various image formats including:
- JPEG/JPG
- PNG
- GIF
- BMP
- WebP
- SVG
- ICO

## Error Handling

The application handles various types of errors:
- Invalid URLs
- Network connectivity issues
- Missing images
- Broken links
- Invalid image formats

## Dependencies

- streamlit
- pandas
- requests
- beautifulsoup4
- pytz
- openpyxl

## Notes

- The application uses IST (Indian Standard Time) for timestamps
- Progress updates are shown in real-time
- Large files may take longer to process
- Network connectivity is required for URL checking

## Contributing

Feel free to submit issues and enhancement requests! 