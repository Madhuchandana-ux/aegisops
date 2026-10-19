import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedGroupKFold

folder = Path("data/processed/external")
df = pd.read_csv(folder / "aegisops_train_final.csv")

df["_group_text"] = (
    df["description"].fillna("").astype(str).str.strip().str.lower()
)

if df["_group_text"].eq("").any():
    raise ValueError("Blank descriptions found.")

all_categories = set(df["category"].dropna())
splitter = StratifiedGroupKFold(
    n_splits=5, shuffle=True, random_state=42
)

candidates = []

for fold, (train_idx, val_idx) in enumerate(
    splitter.split(df, y=df["category"], groups=df["_group_text"]),
    start=1
):
    train = df.iloc[train_idx]
    val = df.iloc[val_idx]

    train_categories = set(train["category"].dropna())
    val_categories = set(val["category"].dropna())

    train_text = set(train["_group_text"])
    val_text = set(val["_group_text"])
    overlap = train_text & val_text

    print(
        f"Fold {fold}: train={len(train)}, validation={len(val)}, "
        f"validation categories={len(val_categories)}/{len(all_categories)}, "
        f"text overlap={len(overlap)}"
    )

    if (
        not overlap
        and train_categories == all_categories
        and val_categories == all_categories
    ):
        candidates.append(
            (abs(len(val) - 0.20 * len(df)), fold, train_idx, val_idx)
        )

if not candidates:
    print("\nNo fold contains all categories while keeping descriptions grouped.")
    print("No files were changed. We need to inspect the category groups.")
    raise SystemExit(1)

_, chosen_fold, train_idx, val_idx = min(candidates, key=lambda x: x[0])

train = df.iloc[train_idx].drop(columns=["_group_text"]).copy()
val = df.iloc[val_idx].drop(columns=["_group_text"]).copy()

train.to_csv(folder / "aegisops_train_grouped.csv", index=False)
val.to_csv(folder / "aegisops_validation_grouped.csv", index=False)

print(f"\nSelected fold: {chosen_fold}")
print("Training shape:", train.shape)
print("Validation shape:", val.shape)
print("Shared descriptions:", len(
    set(train["description"].str.strip().str.lower()) &
    set(val["description"].str.strip().str.lower())
))
print("\nValidation category counts:")
print(val["category"].value_counts().sort_index().to_string())
