# Cloud Chat: Student Demo

Welcome to the Cloud Chat demo! This project illustrates how a **Thin Client** (your computer) can use a **Shared Cloud Document** (on AWS S3) to build a real-time communication system without a traditional database server. This is built for the Cloud Compute Club for the University of Texas at Dallas. This is not to be redistributed or used for any other purpose without consent or permission from the Cloud Compute Club.

## Setup Instructions

1.  **Extract the Files**: Unzip this folder to a location of your choice.
2.  **Install Dependencies**: Open your terminal/command prompt, navigate to this folder, and run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure AWS**: Open `config.py` in a text editor (like Notepad or VS Code) and enter the credentials provided by your instructor:
    *   `AWS_ACCESS_KEY`
    *   `AWS_SECRET_KEY`
    *   `S3_BUCKET_NAME`
4.  **Run the Chat**:
    ```bash
    python cloud_chat.py
    ```

## How it Works

*   **Shared State**: All chat messages are stored in a single `messages.json` file in the S3 bucket.
*   **Polling**: The app checks S3 every 5 seconds to see if anyone else has posted a message.
*   **Identity**: Your name and unique ID are stored locally in `identity.json`.

## Important Note
Keep your `config.py` private. Never share your AWS keys with anyone outside of this demo. This is not to be redistributed or used for any other purpose without consent or permission from the Cloud Compute Club.
