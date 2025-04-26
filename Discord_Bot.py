# === DISCORD VIDEO UPLOAD FUNCTION ===
# This script sends a video to my Discord channel using the official HTTP API
# It uses the built-in 'requests' library to create an HTTP POST request

import requests


def send_video_to_discord(video_path, bot_token, channel_id, video_data):
    message= f"Captured Movement on {video_data}" # Message includes the datetime the video was captured
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    with open(video_path, "rb") as f:
        files = {
            "file": (video_path, f),
        }
        data = {
            "content": message
        }

        response = requests.post(url, headers=headers, data=data, files=files)

    # Check if the message was sent successfully
    if response.status_code == 200 or response.status_code == 201:
        print("Video sent successfully!")
    else:       # Print an Error
        print(f"Failed to send video. Status: {response.status_code}")
        print(response.text)
