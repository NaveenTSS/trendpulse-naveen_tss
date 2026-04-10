# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 07:54:42 2026

@author: Naveen
"""


import pandas as pd
import os

# ------------------------------
# Base project path
# ------------------------------
# This is where input JSON and output CSV files are stored
path = r"C:\Users\Naveen\OneDrive - Patracorp\Formula\Python in Excel\mini project"

print("Adding json data into a dataframe\n")

# ------------------------------
# Load JSON data into a DataFrame
# ------------------------------
# Reads the cleaned story JSON file generated earlier
df = pd.read_json(os.path.join(path, "data\\trends_20240115.json"))

print(f"Loaded {len(df)} stories from data/trends_20240115.json\n")

# ------------------------------
# Remove duplicate stories
# ------------------------------
# Ensures each post_id appears only once
df.drop_duplicates(subset='post_id', inplace=True)

print(f"After removing duplicates: {len(df)}")

# ------------------------------
# Remove rows with critical missing values
# ------------------------------
# post_id, title, and score are essential fields
df.dropna(subset=['post_id', 'title', 'score'], inplace=True)

print(f"After removing nulls: {len(df)}")

# ------------------------------
# Ensure numeric columns have correct data types
# ------------------------------
# Convert score column to integer if needed
if df['score'].dtype != 'int64':
    df['score'] = df['score'].astype('int64')

# Convert num_comments column to integer if needed
if df['num_comments'].dtype != 'int64':
    df['num_comments'] = df['num_comments'].astype('int64')

# ------------------------------
# Remove low-quality stories
# ------------------------------
# Drop stories with score less than 5
to_drop = df[df['score'] < 5].index
df.drop(to_drop, inplace=True)

print(f"After removing low scores: {len(df)}\n")

# ------------------------------
# Clean title text
# ------------------------------
# Remove leading/trailing whitespace from titles
df['title'] = df['title'].str.strip()

# ------------------------------
# Save cleaned dataset to CSV
# ------------------------------
output_path = os.path.join(path, "data\\trends_clean.csv")
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to data/trends_clean.csv\n")

# ------------------------------
# Summary statistics
# ------------------------------
# Display how many stories exist in each category
print("Stories per category:")
print(df['category'].value_counts())

