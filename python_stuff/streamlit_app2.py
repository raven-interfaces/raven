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

        if os.path.exists(os.path.join("trip/", "picture.jpg")):
            content_placeholder.image("trip/picture.jpg")
        
        image_path = os.path.join('trip/', "picture.jpg")
        file_path = os.path.join('trip/', "notes.txt")


        if os.path.exists(file_path) and os.path.exists(image_path):
            content = read_and_format_content(file_path)
            # Display formatted content and image
            content_placeholder.markdown(content)
            content_placeholder.image(image_path)
        else:
            # Clear the content if the file or image doesn't exist
            content_placeholder.empty()

        # Wait for 5 seconds before updating again
        time.sleep(5)

if __name__ == "__main__":
    main()