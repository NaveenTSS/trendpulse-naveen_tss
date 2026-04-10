
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 21:38:41 2026

@author: Naveen


This script:
- Fetches top Hacker News stories
- Categorizes stories using keyword matching
- Collects up to 125 stories in total
- Limits each category to a maximum of 25 stories
- Saves the collected data as a JSON file

"""

# ------------------------------
# Imports
# ------------------------------
import requests      # Used to call the Hacker News API
import json          # Used to serialize Python objects into JSON
import time          # Used for rate-limiting API calls
import os            # Used for file and directory operations

# ------------------------------
# Base output path (local folder)
# ------------------------------
# All generated data will be saved relative to this directory
path = r"C:\Users\Naveen\OneDrive - Patracorp\Formula\Python in Excel\mini project"

# ------------------------------
# Hacker News API endpoint
# ------------------------------
# Endpoint that returns a list of top story IDs
url = "https://hacker-news.firebaseio.com/v0/topstories.json"

# Fetch the top 500 story IDs to work with a larger pool
story_ids = requests.get(url=url).json()[:500]

# ------------------------------
# Category definitions and keywords
# ------------------------------
# Each category is associated with keywords used for classification
categories = [
    {
        "Category": "technology",
        "Keywords": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"]
    },
    {
        "Category": "worldnews",
        "Keywords": ["war", "government", "country", "president", "election", "climate", "attack", "global"]
    },
    {
        "Category": "sports",
        "Keywords": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"]
    },
    {
        "Category": "science",
        "Keywords": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"]
    },
    {
        "Category": "entertainment",
        "Keywords": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
    }
]

# ------------------------------
# Fetch a single story by ID
# ------------------------------
def get_stories(story_id):
    """
    Fetches full story details from Hacker News
    using the provided story ID.
    """
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    headers = {"User-Agent": "TrendPulse/1.0"}
    return requests.get(url=story_url, headers=headers).json()

# ------------------------------
# Determine category based on title keywords
# ------------------------------
def get_category(title):
    """
    Determines the category of a story by checking
    if any predefined keywords appear in the title.
    """
    if not title:
        return None

    for category in categories:
        for keyword in category["Keywords"]:
            # Perform case-insensitive word-level matching
            if keyword.lower() in title.lower().split(" "):
                return category["Category"]

    # Return None if no category matches
    return None

# ------------------------------
# Storage for collected stories
# ------------------------------
stories = []  # Final list of collected stories

# Track how many stories have been collected per category
counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}

# Track categories that have reached the 25-story limit
restricted_categories = set()

# ------------------------------
# Main story collection loop
# ------------------------------
for each_id in story_ids:

    # Fetch individual story data
    story = get_stories(each_id)
    if not story:
        continue

    title = story.get("title")

    # Determine the story category
    bin_item = get_category(title)

    # Skip stories with categories we do not track
    if bin_item not in counts:
        continue

    # Skip categories that have reached their limit
    if bin_item in restricted_categories:
        continue

    # Enforce maximum of 25 stories per category
    if counts.get(bin_item, 0) >= 25:
        restricted_categories.add(bin_item)
        continue

    # Build the final story record
    fill = {
        "post_id": story.get("id"),
        "title": title,
        "category": bin_item,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": time.time()
    }

    # Add story to results
    stories.append(fill)

    # Update category count
    counts[bin_item] += 1

    # Pause to avoid hammering the API
    time.sleep(0.3)

# ------------------------------
# Convert collected data to JSON
# ------------------------------
json_data = json.dumps(stories, indent=2)

# ------------------------------
# Write output file
# ------------------------------
# Change working directory to project path
os.chdir(path)

# Create output directory if it does not exist
os.makedirs("data", exist_ok=True)

# Construct full file path safely
new_path = os.path.join(path, r"data\trends_20240115.json")

# Write JSON data to file
with open(new_path, "w") as f:
    f.write(json_data)

# Final status message
print(f"Collected {len(stories)} stories. saved to data\\trends_20240115.json")
