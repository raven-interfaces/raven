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
    st.markdown("# Flight Log")
    content_placeholder = st.empty()  # Create a placeholder for content

    while True:
        # Clear the content of the app
        content_placeholder.empty()

        if os.path.exists("trip/picture.png"):
            content_placeholder.image("trip/picture.png")

        file_path = os.path.join('trip/', "notes.txt")
        if os.path.exists(file_path):
            content = read_and_format_content(file_path)
            # Display formatted content
            content_placeholder.markdown(content)

        # Wait for 1 second before updating again
        time.sleep(1)

if __name__ == "__main__":
    main()