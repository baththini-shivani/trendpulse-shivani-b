import pandas as pd
import numpy as np


# Load cleaned data

df = pd.read_csv("/Users/shivani/MINI PROJECT/data/trends_clean.csv")

print(f"Loaded data: {df.shape}\n")


# Preview first 5 rows

print("First 5 rows:")
print(df.head(), "\n")


# Basic averages

avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"Average score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}\n")


# NumPy analysis

scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

print("--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores):,}")
print(f"Min score    : {np.min(scores)}\n")


# Category with most stories

categories, counts = np.unique(df["category"], return_counts=True)
max_index = np.argmax(counts)

print(f"Most stories in: {categories[max_index]} ({counts[max_index]} stories)\n")


# Most commented story

max_comment_index = np.argmax(comments)
top_story = df.iloc[max_comment_index]

print(f'Most commented story: "{top_story["title"]}"  — {top_story["num_comments"]:,} comments\n')


# Add new columns

df["engagement"] = df["num_comments"] / (df["score"] + 1)

avg_score = df["score"].mean()
df["is_popular"] = df["score"] > avg_score


# Save final file

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"Saved to {output_path}")