#Run the command to start the Streamlit app:streamlit run app.py

import streamlit as st
import pandas as pd
import io
import time

from excel_reader import read_urls_from_excel
from data_processor import process_data

st.title("Link and Image Checker")
st.write("Upload an Excel file containing a column named 'URL' to check both links and images.")

# User inputs
base_url = st.text_input("Enter the base URL (for relative URLs)", "https://www.walmartconnect.ca")
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
output_file_name = st.text_input("Enter the desired output Excel file name (e.g., output.xlsx)", "output.xlsx")

if st.button("Process"):
    if uploaded_file is not None:
        urls_to_process = read_urls_from_excel(uploaded_file)
        if urls_to_process:
            # Create a progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            details_container = st.empty()
            
            # Initialize counters
            total_links = 0
            total_images = 0
            total_errors = 0
            collected_data = []
            
            # Process URLs with detailed information
            for result in process_data(urls_to_process, base_url):
                # Update progress bar (using value between 0 and 1)
                progress_bar.progress(result['progress'])
                
                # Update status text (using percentage for display)
                status_text.text(f"Processing URL {result['progress_percentage']}% complete")
                
                # Display detailed information
                with details_container.container():
                    st.subheader(f"Current URL: {result['current_url']}")
                    
                    # Create columns for metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Links Found", result.get('links_found', 0))
                    with col2:
                        st.metric("Images Found", result.get('images_found', 0))
                    with col3:
                        st.metric("Errors Found", result.get('errors_found', 0))
                    
                    # Display any errors
                    if 'error' in result:
                        st.error(f"Error processing URL: {result['error']}")
                    
                    # Update totals
                    total_links += result.get('links_found', 0)
                    total_images += result.get('images_found', 0)
                    total_errors += result.get('errors_found', 0)
                
                # Add the data to our collection
                collected_data.extend(result.get('data', []))
                
                # Small delay to make the UI updates visible
                time.sleep(0.1)
            
            if collected_data:
                # Create separate DataFrames for links and images
                df = pd.DataFrame(collected_data)
                links_df = df[df['Type'] == 'Link']
                images_df = df[df['Type'] == 'Image']
                
                # Rename 'Link Text' to 'Alt Text' in the images DataFrame
                images_df = images_df.rename(columns={'Link Text': 'Alt Text'})
                
                # Display final summary statistics
                st.subheader("Final Summary Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Links", total_links)
                with col2:
                    st.metric("Total Images", total_images)
                with col3:
                    st.metric("Total Errors", total_errors)
                
                # Display error summary
                st.subheader("Error Summary")
                error_df = df[df['Status'] == 'Error']
                if not error_df.empty:
                    st.dataframe(error_df[['Source URL', 'Link URL', 'Type', 'Status Code']])
                else:
                    st.success("No errors found!")
                
                # Create an Excel file in memory with multiple sheets
                towrite = io.BytesIO()
                with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                    # Write links to the first sheet
                    links_df.to_excel(writer, sheet_name='Links', index=False)
                    # Write images to the second sheet
                    images_df.to_excel(writer, sheet_name='Images', index=False)
                    # Write summary statistics to the third sheet
                    summary_data = {
                        'Metric': ['Total Links', 'Total Images', 'Total Errors', 'Error Rate'],
                        'Value': [
                            total_links,
                            total_images,
                            total_errors,
                            f"{(total_errors / (total_links + total_images) * 100):.1f}%"
                        ]
                    }
                    pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                towrite.seek(0)
                
                st.download_button(
                    label="Download Result Excel File",
                    data=towrite,
                    file_name=output_file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("Processing completed!")
            else:
                st.error("No data was collected. Please check the input file and base URL.")
        else:
            st.error("No URLs found in the provided Excel file.")
    else:
        st.error("Please upload an Excel file.")
