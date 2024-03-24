import streamlit as st
import time
import os

# Function to read content from file and format it into Markdown
def read_and_format_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    # You can format the content as per your requirement here
    # For simplicity, let's assume the content is already in Markdown format
    return content


def main():
    # Path to the folder where the content is being written
    # Placeholder to display content
    content_placeholder = st.empty()

    while True:
        # Read content from file
        file_path = os.path.join('trip/', "notes.txt")
        if os.path.exists(file_path):
            content = read_and_format_content(file_path)
            # Display formatted content
            content_placeholder.markdown(content)

        st.image('test_files/palm.jpeg')

        # Wait for 2 seconds before updating again
        time.sleep(0.5)

if __name__ == "__main__":
    main()