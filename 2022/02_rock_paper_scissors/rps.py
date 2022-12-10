import pandas as pd

choice_map = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}

outcome_map = {
    -1: 6,  # win AY BZ
    2: 6,  # win CX
    0: 3,  # draw AX, BY, CZ
    -2: 0,  # loss AZ
    1: 0,  # loss BX, CY
}

target_outcome_map = {"X": 0, "Y": 3, "Z": 6}

matchups = {
    "A0": "C",
    "B0": "A",
    "C0": "B",
    "A3": "A",
    "B3": "B",
    "C3": "C",
    "A6": "B",
    "B6": "C",
    "C6": "A",
}

df = pd.read_csv(
    r"02_rock_paper_scissors\input.txt",
    sep=" ",
    header=None,
    names=[
        "Col 1",
        "Col 2",
        "Choice Col1",
        "Choice Col2",
        "Diff",
        "Outcome",
        "Target Outcome",
        "Target Choice",
        "Choice Num",
        "Final Score 1",
        "Final Score 2",
    ],
)

df["Choice Col1"] = df["Col 1"].map(choice_map)
df["Choice Col2"] = df["Col 2"].map(choice_map)
df["Diff"] = df["Choice Col1"] - df["Choice Col2"]
df["Outcome"] = df["Diff"].map(outcome_map)
df["Target Outcome"] = df["Col 2"].map(target_outcome_map)
df["Target Choice"] = (df["Col 1"] + df["Target Outcome"].astype(str)).map(
    matchups
)

df["Choice Num"] = df["Target Choice"].map(choice_map)


df["Final Score 1"] = df["Choice Col2"] + df["Outcome"]
df["Final Score 2"] = df["Choice Num"] + df["Target Outcome"]

total_points_1 = df["Final Score 1"].sum()
total_points_2 = df["Final Score 2"].sum()

print(df.head())

print(
    f"\nPart 1 Total Points: {total_points_1}\nPart 2 Total Points:"
    f" {total_points_2}\n"
)
