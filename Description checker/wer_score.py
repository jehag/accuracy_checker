import os
import base64
from PIL import Image
import requests
import jiwer

# Read the server URL from the text file
with open('Server_URL.txt', 'r') as f:
    server_url = f.read().strip()

# Read the descriptions from 30k_captions.txt into a dictionary
descriptions = {}
with open('30k_captions.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            descriptions[parts[0]] = parts[1]

# Initialize a list to store the WER scores
wer_scores = []

# Iterate over all files in the images folder
for filename in os.listdir('images'):
    # Check if the file is an image
    if not filename.endswith(('.jpg', '.jpeg', '.png')):
        continue

    # Read the image file and convert it to base64 encoding
    with open(f'images/{filename}', 'rb') as f:
        image_bytes = f.read()
        base64_bytes = base64.b64encode(image_bytes)
        base64_string = base64_bytes.decode('utf-8')

    # Send a POST request to the server URL with the base64-encoded image as a parameter
    data = {"image": base64_string}
    response = requests.get(server_url, json=data)

    if response.status_code == 200:
        print("Request was successful!")
    else:
        raise (f"Request failed with status code {response.status_code} : {response.text}")
    # Extract the first caption from the response JSON object
    caption = response.json()['captionRes']['captions'][0]

    # Get the corresponding description from 30k_captions.txt
    key = f'{filename}#0'
    description = descriptions.get(key)

    # Calculate the WER score between the caption and the description
    wer_score = jiwer.wer(description, caption)
    print(wer_score)
    wer_scores.append(wer_score)

# Calculate the average WER score
avg_wer_score = sum(wer_scores) / len(wer_scores)

print(f'Average WER score: {avg_wer_score:.4f}')
