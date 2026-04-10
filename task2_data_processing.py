import pandas as pd
from datetime import datetime

# Load JSON file
# Get today's date in YYYYMMDD format (same format used while saving the file)
date_str = datetime.now().strftime("%Y%m%d")

# Create file path using today's date
file_path = f"/Users/shivani/MINI PROJECT/data/trends_20260407.json"

# Read JSON file into a Pandas DataFrame
df = pd.read_json(file_path)

# Print how many rows (stories) were loaded
print(f"Loaded {len(df)} stories from {file_path}\n")


# Remove duplicates
# Remove duplicate rows based on 'post_id' (same story repeated)
df = df.drop_duplicates(subset=["post_id"])

# Print remaining rows after removing duplicates
print(f"After removing duplicates: {len(df)}")


# Remove missing values

# Remove rows where important fields are missing (post_id, title, score)
df = df.dropna(subset=["post_id", "title", "score"])

# Print remaining rows after removing missing values
print(f"After removing nulls: {len(df)}")


# Fix data types

# Convert 'score' and 'num_comments' to numbers (in case they are strings)
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Remove rows where conversion failed (became NaN)
df = df.dropna(subset=["score", "num_comments"])

# Convert them to integer type
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# Remove low-quality stories

# Keep only stories where score is 5 or more
df = df[df["score"] >= 5]

# Print remaining rows after filtering low scores
print(f"After removing low scores: {len(df)}\n")

# Clean title whitespace

# Remove extra spaces from beginning and end of titles
df["title"] = df["title"].str.strip()


# Step 7: Save cleaned data

# Define output file path
output_path = "data/trends_clean.csv"

# Save cleaned DataFrame as CSV file
df.to_csv(output_path, index=False)

# Print confirmation message
print(f"Saved {len(df)} rows to {output_path}\n")


# Step 8: Category summary

print("Stories per category:")

# Count how many stories are in each category
category_summary = df["category"].value_counts()

# Print count for each category (in fixed order)
for category in ["technology", "worldnews", "sports", "science", "entertainment"]:
    print(f"  {category:<15} {category_summary.get(category, 0)}")