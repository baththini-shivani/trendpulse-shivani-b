import requests
import time
import os
import json
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"}

# Step 1: Category keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Step 2: Fetch IDs
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
ids = requests.get(url, headers=headers).json()

# Step 3: Category function
def assign_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category
    return None

# Step 4: Prepare storage
final_data = []
category_count = {cat: 0 for cat in categories}

# Step 5: Loop category-wise
for category in categories:

    for sid in ids:
        if category_count[category] >= 25:
            break

        item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
        res = requests.get(item_url, headers=headers)

        if res.status_code != 200:
            continue

        data = res.json()

        if not data or data.get("type") != "story":
            continue

        title = data.get("title", "")

        if assign_category(title) == category:
            story = {
                "post_id": data.get("id"),
                "title": title,
                "category": category,
                "score": data.get("score"),
                "num_comments": data.get("descendants"),
                "author": data.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            final_data.append(story)
            category_count[category] += 1

    print(f"{category}: {category_count[category]} stories collected")
    time.sleep(2)  #sleep per category

# Step 6: Create folder if not exists
folder_name = "data"
os.makedirs(folder_name, exist_ok=True)

# Step 7: Create filename with date
date_str = datetime.now().strftime("%Y%m%d")
file_path = f"{folder_name}/trends_{date_str}.json"

# Step 8: Save JSON file
with open(file_path, "w") as f:
    json.dump(final_data, f, indent=4)

# Step 9: Final output
print(f"\nCollected {len(final_data)} stories. Saved to {file_path}")
