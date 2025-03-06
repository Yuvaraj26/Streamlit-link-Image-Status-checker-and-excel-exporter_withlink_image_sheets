# This module handles fetching a URL, parsing its links, and checking each link's status.

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from urllib.parse import urljoin, urlparse

def check_image_status(img_url, headers):
    """Check if an image loads properly."""
    try:
        response = requests.get(img_url, headers=headers, stream=True)
        if response.status_code == 200:
            # Get content type from headers
            content_type = response.headers.get('content-type', '').lower()
            
            # List of valid image content types including SVG
            valid_image_types = [
                'image/jpeg', 'image/png', 'image/gif', 'image/bmp',
                'image/webp', 'image/svg+xml', 'image/svg', 'image/x-icon',
                'application/xml',  # Some servers send SVG as application/xml
                'text/plain'  # Some servers send SVG as text/plain
            ]
            
            # Parse URL to handle query parameters
            parsed_url = urlparse(img_url)
            path = parsed_url.path.lower()
            
            # Check if URL ends with image extensions
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico']
            is_image_extension = any(path.endswith(ext) for ext in image_extensions)
            
            # Check if content type is valid or if URL has image extension
            if content_type in valid_image_types or is_image_extension:
                return 'OK', response.status_code
            return 'Not an Image', response.status_code
        return 'Error', response.status_code
    except Exception:
        return 'Error', 'Request Failed'

def fetch_and_check_links(url, base_url):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.110 Safari/537.3'
        )
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # If the URL is relative, prepend the base URL
    if not url.startswith('http'):
        url = base_url + url

    canonical_link_tag = soup.find("link", rel="canonical")
    canonical_url = canonical_link_tag['href'] if canonical_link_tag else 'Not Found'

    all_data = []

    # Check regular links
    for link in soup.find_all('a', href=True):
        link_url = link['href']
        if link_url.startswith('/'):
            link_url = base_url + link_url

        link_text = link.get_text(strip=True)
        status = 'OK'
        status_code = 0

        try:
            header = requests.get(link_url, headers=headers, allow_redirects=True)
            status_code = header.status_code
            if 400 <= header.status_code <= 599:
                status = 'Error'
        except Exception:
            status = 'Error'
            status_code = 'Request Failed'

        # Get current IST timestamp
        ist_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z')

        all_data.append({
            'Source URL': url,
            'Link URL': link_url,
            'Link Text': link_text,
            'Status': status,
            'Status Code': status_code,
            'Canonical URL': canonical_url,
            'Timestamp (IST)': ist_time,
            'Type': 'Link'
        })

    # Check images
    for img in soup.find_all('img', src=True):
        img_url = img['src']
        # Handle relative image URLs
        if not img_url.startswith(('http://', 'https://')):
            img_url = urljoin(base_url, img_url)

        alt_text = img.get('alt', 'No alt text')
        status, status_code = check_image_status(img_url, headers)

        # Get current IST timestamp
        ist_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S %Z')

        all_data.append({
            'Source URL': url,
            'Link URL': img_url,
            'Link Text': alt_text,
            'Status': status,
            'Status Code': status_code,
            'Canonical URL': canonical_url,
            'Timestamp (IST)': ist_time,
            'Type': 'Image'
        })

    return all_data
