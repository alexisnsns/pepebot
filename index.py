import tweepy
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import random

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from environment variables
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate with Twitter API v1.1 and v2
def get_twitter_conn_v1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) -> tweepy.API:
    """Get Twitter connection for v1.1"""
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def get_twitter_conn_v2(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) -> tweepy.Client:
    """Get Twitter connection for v2"""
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )
    return client

# Create both v1.1 and v2 clients
client_v1 = get_twitter_conn_v1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
client_v2 = get_twitter_conn_v2(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Function to upload an image and post a tweet
def upload_and_post_image(image_url):
    try:
        # Fetch the image from the URL
        image_data = requests.get(image_url).content  # Get the image content
        
        # Save the image temporarily to upload to Twitter
        with open('temp_image.jpg', 'wb') as f:
            f.write(image_data)
        
        # Upload media with v1.1 client
        media = client_v1.media_upload(filename='temp_image.jpg')
        media_id = media.media_id

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create the tweet text with the timestamp and "Jones certified" with a checkmark
        tweet_text = f"{timestamp} - Jones certified ✅"

        # Post tweet with media using v2 client
        client_v2.create_tweet(text=tweet_text, media_ids=[media_id])
        print(f"Posted {image_url} with timestamp.")
        
        # Clean up the temporary file
        os.remove('temp_image.jpg')
    except Exception as e:
        print(f"Failed to post {image_url}: {e}")

# Load the last posted image index from a file (track the image that was last posted)
def load_last_posted_image():
    try:
        with open("last_posted_image.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        # If file doesn't exist, return 0 (start with the first image)
        return 0

# Save the index of the last posted image
def save_last_posted_image(index):
    with open("last_posted_image.txt", "w") as file:
        file.write(str(index))

# Get all image filenames (assumes images are named 1.jpg, 2.jpg, etc.)
image_files = [f"{i}.jpg" for i in range(0, 11)]  # Adjust the range if there are more images

# Load the last posted image index
last_posted_index = load_last_posted_image()

# Get the next image to post (ensure it's not the same one)
next_image_index = (last_posted_index + 1) % len(image_files)  # Cycles through the images

# Construct the S3 URL for the next image
image_url = f"https://pepebucketbot.s3.us-east-2.amazonaws.com/{image_files[next_image_index]}"

# Upload and post the image
upload_and_post_image(image_url)

# Save the index of the last posted image
save_last_posted_image(next_image_index)

