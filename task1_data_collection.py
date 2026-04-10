
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 21:38:41 2026

@author: Naveen

This script:
- Fetches top Hacker News stories
- Categorizes them by keywords
- Collects up to 125 stories total
- Limits each category to a maximum of 25 stories
- Saves the final result as a JSON file
"""

# ------------------------------
# Imports
# ------------------------------
import requests      # For making HTTP API calls
import json          # For JSON serialization
import time          # For rate limiting (sleep)
import os            # For file and folder operations

# ------------------------------
# Base output path (local folder)
# ------------------------------
path = r"C:\Naveen\Formula\Python in Excel\mini project"

# ------------------------------
# Hacker News API endpoint
# ------------------------------
url = "https://hacker-news.firebaseio.com/v0/topstories.json"

# Fetch the top 500 story IDs from Hacker News
story_ids = requests.get(url=url).json()[:500]

# ------------------------------
# Category definitions and keywords
# ------------------------------
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
    Given a story ID, fetch the full story details
    from the Hacker News API.
    """
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    headers = {"User-Agent": "TrendPulse/1.0"}
    return requests.get(url=story_url, headers=headers).json()

# ------------------------------
# Determine category based on title keywords
# ------------------------------
def get_category(title):
    """
    Match words in the title against predefined
    keyword lists to assign a category.
    """
    if not title:
        return None

    for category in categories:
        for keyword in category["Keywords"]:
            # Case-insensitive keyword match
            if keyword.lower() in title.lower().split(" "):
                return category["Category"]

    # If no keyword matches
    return None

# ------------------------------
# Storage for collected stories
# ------------------------------
stories = []

# Count how many stories per category have been collected
counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}

# Track categories that have reached their limit
restricted_categories = set()

# ------------------------------
# Main story collection loop
# ------------------------------
for each_id in story_ids:

    # Stop once we collect 125 stories total
    if len(stories) == 125:
        break

    story = get_stories(each_id)
    if not story:
        continue

    title = story.get("title")

    # Determine category of the story
    bin_item = get_category(title)

    # Skip categories already marked as full
    if bin_item in restricted_categories:
        continue

    # Enforce max 25 stories per category
    if counts.get(bin_item, 0) >= 25:
        restricted_categories.add(bin_item)
        continue

    # Build final record
    fill = {
        "post_id": story.get("id"),
        "title": title,
        "category": bin_item,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": time.time()
    }

    # Store the story
    stories.append(fill)

    # Increment category counter if tracked
    if bin_item in counts:
        counts[bin_item] += 1

    # Rate limit API requests
    time.sleep(0.3)

# ------------------------------
# Convert collected data to JSON
# ------------------------------
json_data = json.dumps(stories, indent=2)

# ------------------------------
# Write output file
# ------------------------------
os.chdir(path)

# Create output folder (will fail if it already exists)
os.mkdir("data")

# Build full file path safely
new_path = os.path.join(path, r"data\trends_20240115.json")

# Write JSON to file
with open(new_path, "w") as f:
    f.write(json_data)

# Final status message
print(f"Collected {len(stories)} stories. saved to data\\trends_20240115.json")
