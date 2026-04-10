# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:30:00 2026

@author: Naveen
"""


import pandas as pd          
import numpy as np           
import os                    

# ------------------------------
# 1 — Load and Explore
# ------------------------------
# Location where the cleaned CSV file is stored
path = r"C:\Users\Naveen\OneDrive - Patracorp\Formula\Python in Excel\mini project"

# Read the previously cleaned Hacker News dataset
df = pd.read_csv(os.path.join(path, "data/trends_clean.csv"))

# Display basic dataset shape (rows, columns)
print(f"Loaded data: {df.shape}\n")

# Show a preview of the first 5 rows
print(f"First 5 rows:\n{df.head(5)}")

# Calculate and display average score
print(f"Average score: {df['score'].mean():.2f}")

# Calculate and display average number of comments
print(f"Average comments: {df['num_comments'].mean():.2f}")

# ------------------------------
# 2 — Basic Analysis with NumPy
# ------------------------------
print("--- Numpy Stats ---\n")

# Compute mean score using NumPy
print(f"Mean score\t\t: {np.mean(df['score']):.2f}")

# Compute median score
print(f"Median score\t: {np.median(df['score']):.2f}")

# Compute standard deviation of score
print(f"Std deviation\t: {np.std(df['score']):.2f}")

# Compute maximum score
print(f"Max score\t\t: {np.max(df['score']):.2f}")

# Compute minimum score
print(f"Min score\t\t: {np.min(df['score']):.2f}\n")

# Determine which category has the most stories
highest_category = df['category'].value_counts().sort_values(ascending=False).index[0]
highest_number_of_stories = df['category'].value_counts().sort_values(ascending=False).iloc[0]

print(f"Most stories in: {highest_category} ({highest_number_of_stories} stories)\n")

# Group by title and sum comments to find most commented story
pivot = df.groupby("title")['num_comments'].sum().sort_values(ascending=False)

most_commented_story = pivot.index[0]
most_number_of_comments = pivot.iloc[0]

print(f'Most commented story: "{most_commented_story}" - {most_number_of_comments} comments\n')

# ------------------------------
# 3 — Add New Columns
# ------------------------------
# Create engagement metric (comments relative to score)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Flag stories as popular if score is above average
df["is_popular"] = [
    True if score > df["score"].mean() else False
    for score in df["score"]
]

# ------------------------------
# 4 — Save the Result
# ------------------------------
df.to_csv(os.path.join(path, "data/trends_analysed.csv"), index=False)

print("Saved to data/trends_analysed.csv")

