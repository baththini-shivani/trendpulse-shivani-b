import requests
import time
import os
import json
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"} # This header helps the API know who is making the request

# Define categories and related keywords
# These keywords will help us decide which story belongs to which category
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Get top story IDs from Hacker News API
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
ids = requests.get(url, headers=headers).json() # returns a list of story IDs

# Function to assign a category based on title
def assign_category(title):
    title = title.lower() # convert title to lowercase for easy matching
    
    # Check each category and its keywords
    for category, keywords in categories.items():
        for word in keywords:
            if word in title:      # If any keyword is found in title, return that category
                return category
    # If no keyword matches, return None        
    return None

# Prepare storage
# this will store all selected stories
final_data = []

# This keeps count of how many stories we collected per category
category_count = {cat: 0 for cat in categories}

# Loop through each category
for category in categories:

    # Loop through all story IDs
    for sid in ids:
        if category_count[category] >= 25:   # Stop when we have collected 25 stories for this category
            break

        # Create URL for each story using its ID
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
        
        # Fetch story details
        res = requests.get(item_url, headers=headers)
        
        # Skip if request failed
        if res.status_code != 200:
            continue

        data = res.json()

        # Skip if data is empty or not a story (could be comment/job etc.)
        if not data or data.get("type") != "story":
            continue

        # Get story title
        title = data.get("title", "")

        # Check if this story belongs to current category
        if assign_category(title) == category:
            
            # Create a dictionary with required fields
            story = {
                "post_id": data.get("id"),
                "title": title,
                "category": category,
                "score": data.get("score"),
                "num_comments": data.get("descendants"),
                "author": data.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Add story to final list
            final_data.append(story)
            
            # Increase count for this category
            category_count[category] += 1

    # Print how many stories collected for this category
    print(f"{category}: {category_count[category]} stories collected")
    
    # Wait for 2 seconds before moving to next category
    #sleep per category
    time.sleep(2)  

# Create "data" folder if it does not exist
folder_name = "data"
os.makedirs(folder_name, exist_ok=True)

# Create file name with today’s date
date_str = datetime.now().strftime("%Y%m%d")
file_path = f"{folder_name}/trends_{date_str}.json"

# Save all collected stories into JSON file
with open(file_path, "w") as f:
    json.dump(final_data, f, indent=4)

# Print Final result
print(f"\nCollected {len(final_data)} stories. Saved to {file_path}")
