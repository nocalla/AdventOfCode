"""
Find the Elf carrying the most Calories.
How many total Calories is that Elf carrying?
"""

import numpy as np
import pandas as pd

df = pd.read_csv(
    r"2022\01_counting_calories\input.txt",
    header=None,
    names=["A"],
    low_memory=True,
    skip_blank_lines=False,
)

print(df.head(20))
print(df.shape)

df_list = np.split(df, df[df.isnull().all(1)].index)  # type: ignore

combined_df = pd.concat(df_list, axis="columns", ignore_index=True)

for col in combined_df:
    combined_df[col] = combined_df[col].sort_values(ignore_index=True)

print(combined_df.head(20))

sums = combined_df.sum()

largest = sums.nlargest(n=3, keep="first")
sum_largest = largest.sum()

print(f"Top 3: {largest.tolist()}.\nTotal Calories: {sum_largest}")
