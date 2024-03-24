import streamlit as st
import time
import os
from PIL import Image

# Function to read content from file and format it into Markdown
def read_and_format_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

def main():
    st.markdown("# Flight Log")
    content_placeholder = st.empty()  # Create a placeholder for content
    image_placeholder = st.empty()

    while True:
        content_placeholder.empty()
        image_placeholder.empty()

        image_path = os.path.join('trip/', "picture_copy.jpg")
        file_path = os.path.join('trip/', "notes.txt")

        if os.path.exists(file_path):
            content = read_and_format_content(file_path)
            # Display formatted content as Markdown and image
            print(content)
            content_placeholder.markdown(content)
            # content_placeholder.image(image_path)


            if os.path.exists(image_path):
                image = Image.open(image_path)
                image_placeholder.image(image)
            else:
                image_placeholder.warning("No Image")

        
        else:
            # Clear the content if the file or image doesn't exist
            content_placeholder.warning("Text file not found.")
            image_placeholder.empty()
            # content_placeholder.empty()

        # Wait for 5 seconds before updating again
        time.sleep(1)  # Adjusted to 5 seconds as per original comment

if __name__ == "__main__":
    main()
