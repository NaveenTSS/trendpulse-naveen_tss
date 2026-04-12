# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 11:39:37 2026

@author: Naveen
"""


# Import pandas for data loading and manipulation
import pandas as pd
# Import os for directory and file path operations
import os
# Import matplotlib for creating plots
import matplotlib.pyplot as plt
# Import seaborn for statistical visualizations
import seaborn as sns

# ------------------------------------------------------------------
# Task 1 — Setup
# ------------------------------------------------------------------

# Define the base path of the project
path = r"C:\Users\Naveen\OneDrive - Patracorp\Formula\Python in Excel\mini project"

# Change working directory to project path
os.chdir(path)

# Create outputs folder if it does not exist
os.makedirs("outputs", exist_ok=True)

# Change working directory to outputs folder
os.chdir(os.path.join(path, "outputs"))

# Load the CSV data into a DataFrame
df = pd.read_csv(os.path.join(path, "data\\trends_analysed.csv"))

# ------------------------------------------------------------------
# Task 2 — Chart 1: Top 10 Stories by Score
# ------------------------------------------------------------------

# Get top 10 stories by score
top_10_stories = df[['post_id','score']].sort_values(by='score', ascending=False)[:10]
# Create a new figure with specific dimensions
plt.figure(figsize=(15,6))
# Create a bar chart. Convert post_id to string so it is treated as categorical data
plt.bar(top_10_stories['post_id'].astype('str'), top_10_stories['score'])
# Set chart title
plt.title("Top 10 Stories by Score")
# Set x-axis label
plt.xlabel("Stories")
# Set y-axis label
plt.ylabel("Score")
# Save the plot to a PNG file
plt.savefig("chart1_top_stories.png")
# Display the plot
plt.show()

# ------------------------------------------------------------------
# Task 3 — Chart 2: Stories per Category
# ------------------------------------------------------------------

# Count the number of stories in each category
stories_per_category = df['category'].value_counts()
# Create a color palette with one color per category
colors = plt.cm.Set1(range(len(stories_per_category)))
# Create a new figure and axis
fig, ax = plt.subplots()
# Set figure height
fig.set_figheight(6)
# Set figure width
fig.set_figwidth(10)
# Create a bar plot for category counts
ax.bar(stories_per_category.index, stories_per_category, color=colors)
# Set chart title
ax.set_title("Stories per Category")
# Set x-axis label
ax.set_xlabel("Category")
# Set y-axis label
ax.set_ylabel("Number of Stories")
# Save the plot
plt.savefig("chart2_categories.png")
# Display the plot
plt.show()

# ------------------------------------------------------------------
# Task 4 — Chart 3: Score vs Comments
# ------------------------------------------------------------------

# Create a scatter plot using seaborn. Points are colored based on is_popular.
sns.scatterplot(data=df, x='score', y='num_comments', hue='is_popular')
# Set x-axis label
plt.xlabel("Score")
# Set y-axis label
plt.ylabel("Number of Comments")
# Set plot title
plt.title("Score vs Comments")
# Save the scatter plot
plt.savefig("chart3_scatter.png")
# Display the plot
plt.show()

# ------------------------------------------------------------------
# DASHBOARD: COMBINED VIEW
# ------------------------------------------------------------------

# Create a figure for the dashboard layout
fig = plt.figure(figsize=(12,8))
# Define a GridSpec layout with 2 rows, 2 columns. # Top row is taller than the bottom row
gs = fig.add_gridspec(nrows=2, ncols=2, height_ratios=[2,1])

# Create a subplot that spans the full top row
ax_top = fig.add_subplot(gs[0,:])
# Plot the top 10 stories bar chart
ax_top.bar(top_10_stories['post_id'].astype('str'), top_10_stories['score'])
# Set title
ax_top.set_title("Top 10 Stories by Score")
# Set axis labels
ax_top.set_xlabel("Stories")
ax_top.set_ylabel("Score")

# Bottom left panel: STORIES PER CATEGORY

# Create subplot in bottom-left position
ax_bl = fig.add_subplot(gs[1,0])
# Create the category bar chart
ax_bl.bar(stories_per_category.index, stories_per_category, color=colors)
# Set title and axis labels
ax_bl.set_title("Stories per Category")
ax_bl.set_xlabel("Category")
ax_bl.set_ylabel("Number of Stories")

# Bottom right panel: SCATTER PLOT

# Create subplot in bottom-right position
ax_br = fig.add_subplot(gs[1,1])
# Draw seaborn scatter plot inside this axis
sns.scatterplot(data=df, x='score', y='num_comments', hue='is_popular', ax=ax_br)
# Set title and axis labels
ax_br.set_title("Score vs Comments")
ax_br.set_xlabel("Score")
ax_br.set_ylabel("Number of Comments")

# Save and show dashboard

# Save the entire dashboard as one image
plt.tight_layout()
# Automatically adjust spacing to avoid overlap
plt.savefig("dashboard.png")
# Display the dashboard
plt.show()


