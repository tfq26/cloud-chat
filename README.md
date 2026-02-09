# Cloud Chat: Student Demo

Welcome to the Cloud Chat demo! This project illustrates how a **Thin Client** (your computer) can use a **Shared Cloud Document** (on AWS S3) to build a real-time communication system without a traditional database server. This is built for the Cloud Compute Club for the University of Texas at Dallas. This is not to be redistributed or used for any other purpose without consent or permission from the Cloud Compute Club.

## Setup Instructions

1.  **Extract the Files**: Unzip this folder to a location of your choice.
2.  **Install Dependencies**: Open your terminal/command prompt, navigate to this folder, and run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure AWS**: Depending on your instructor's setup:
    *   **Shared Demo**: Your instructor may have already filled in `config.py`. If so, skip to step 4!
    *   **Individual Project**: Open `config.py` in a text editor and enter your own credentials:
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

---

## 🛠️ Self-Hosting (Instructor Guide)

If you want to host this demo for your own class using your own AWS account, follow these steps to ensure it is secure:

### 1. Create an S3 Bucket
Create a standard S3 bucket (e.g., `cloud-chat-demo-shared`). Ensure it is **not** public; the Python script will use credentials to access it.

### 2. Create a Restricted IAM User
Do not use your root account or admin keys. Create a new IAM User (e.g., `chat-demo-bot`) and attach a **Directly Attached Inline Policy** like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/messages.json"
        }
    ]
}
```

### 3. Safety Best Practices
> [!IMPORTANT]
> **Key Rotation**: Only activate the Access Keys during the duration of your live demo.
> **Deactivate Immediately**: As soon as the class is over, go to the IAM Console and click **Deactivate** on the Access Keys. This instantly prevents any further unauthorized use, even if students still have the code.
> **Least Privilege**: The policy above ensures that even if the keys are leaked, the "attacker" can only read/write to that one specific JSON file and nothing else in your AWS account.
