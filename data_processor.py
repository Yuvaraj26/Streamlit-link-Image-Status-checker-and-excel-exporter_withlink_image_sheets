# This module iterates over URLs and uses the link-checking functionality.

import streamlit as st
from link_checker import fetch_and_check_links
import time

def process_data(urls, base_url):
    """Process each URL and collect data."""
    all_data = []
    total_urls = len(urls)
    
    for index, url in enumerate(urls, 1):
        try:
            # Process the URL and get data
            url_data = fetch_and_check_links(url, base_url)
            all_data.extend(url_data)
            
            # Calculate progress (as a value between 0 and 1)
            progress = index / total_urls
            
            # Return both the data and progress information
            yield {
                'data': url_data,
                'progress': progress,
                'progress_percentage': int(progress * 100),  # For display purposes
                'current_url': url,
                'links_found': len([d for d in url_data if d['Type'] == 'Link']),
                'images_found': len([d for d in url_data if d['Type'] == 'Image']),
                'errors_found': len([d for d in url_data if d['Status'] == 'Error'])
            }
            
        except Exception as e:
            yield {
                'data': [],
                'progress': index / total_urls,
                'progress_percentage': int((index / total_urls) * 100),
                'current_url': url,
                'error': str(e)
            }
    
    return all_data
