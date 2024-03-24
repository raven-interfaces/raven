import streamlit as st
import time
import os

# Function to read content from file and format it into Markdown
def read_and_format_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

def main():
    st.markdown("# Flight Log")
    content_placeholder = st.empty()  # Create a placeholder for content

    while True:
        content_placeholder.empty()

        image_path = os.path.join('trip/', "picture_copy.jpg")
        file_path = os.path.join('trip/', "notes.txt")

        if os.path.exists(file_path) and os.path.exists(image_path):
            content = read_and_format_content(file_path)
            # Display formatted content as Markdown and image

            print(content)
            content_placeholder.markdown(content)
            # content_placeholder.image(image_path)
        else:
            # Clear the content if the file or image doesn't exist
            content_placeholder.empty()

        # Wait for 5 seconds before updating again
        time.sleep(5)  # Adjusted to 5 seconds as per original comment

if __name__ == "__main__":
    main()
