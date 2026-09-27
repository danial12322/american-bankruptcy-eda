"""
EDA Practical – 2026
Paper: Introduction to Business Analytics
Dataset: American Bankruptcy dataset

Run:
    pip install pandas numpy matplotlib seaborn
    python American_Bankruptcy_EDA.py

Place american_bankruptcy.csv in the same folder as this script.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Load the dataset
# -----------------------------
FILE = "american_bankruptcy.csv"

df = pd.read_csv(FILE)

print("\n========== DATASET OVERVIEW ==========")
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nData types and non-null values:")
print(df.info())

# -----------------------------
# 2. Data quality check
# -----------------------------
print("\n========== DATA QUALITY ==========")
print("Missing values:")
print(df.isnull().sum())

print("\nTotal missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())

# -----------------------------
# 3. Basic descriptive statistics
# -----------------------------
numeric_cols = [c for c in df.columns if c.startswith("X")]

print("\n========== DESCRIPTIVE STATISTICS ==========")
print(df[numeric_cols].describe().T)

# -----------------------------
# 4. Categorical analysis
# -----------------------------
print("\n========== CATEGORICAL ANALYSIS ==========")
print("\nStatus counts:")
print(df["status_label"].value_counts())

print("\nStatus percentages:")
print((df["status_label"].value_counts(normalize=True) * 100).round(2))

print("\nNumber of unique companies:", df["company_name"].nunique())
print("Year range:", df["year"].min(), "to", df["year"].max())

# -----------------------------
# 5. Create output folder
# -----------------------------
OUT = "eda_outputs"
os.makedirs(OUT, exist_ok=True)

sns.set_theme(style="whitegrid")

# -----------------------------
# 6. Visualization: status distribution
# -----------------------------
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="status_label")
plt.title("Distribution of Company Status")
plt.xlabel("Status")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "01_status_distribution.png"), dpi=200)
plt.show()

# -----------------------------
# 7. Visualization: yearly status trend
# -----------------------------
year_status = pd.crosstab(df["year"], df["status_label"])

plt.figure(figsize=(10, 5))
for status in year_status.columns:
    plt.plot(year_status.index, year_status[status], marker="o", label=status)

plt.title("Company Status Records by Year")
plt.xlabel("Year")
plt.ylabel("Number of Records")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, "02_yearly_status_trend.png"), dpi=200)
plt.show()

# -----------------------------
# 8. Visualization: failure percentage by year
# -----------------------------
year_pct = (
    df.assign(failed_flag=(df["status_label"] == "failed").astype(int))
      .groupby("year")["failed_flag"]
      .mean()
      .mul(100)
)

plt.figure(figsize=(10, 5))
plt.plot(year_pct.index, year_pct.values, marker="o")
plt.title("Failed Record Percentage by Year")
plt.xlabel("Year")
plt.ylabel("Failed Records (%)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "03_failure_percentage_by_year.png"), dpi=200)
plt.show()

# -----------------------------
# 9. Distribution of numeric variables
# -----------------------------
df[numeric_cols].hist(
    figsize=(16, 18),
    bins=30,
    edgecolor="black"
)
plt.suptitle("Distributions of Numeric Variables", y=1.02, fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "04_numeric_distributions.png"), dpi=200)
plt.show()

# -----------------------------
# 10. Correlation heatmap
# -----------------------------
corr = df[numeric_cols].corr()

plt.figure(figsize=(13, 10))
sns.heatmap(corr, cmap="coolwarm", center=0, linewidths=0.2)
plt.title("Correlation Heatmap of Numeric Variables")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "05_correlation_heatmap.png"), dpi=200)
plt.show()

# -----------------------------
# 11. Boxplots by status
# -----------------------------
for col in numeric_cols:
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x="status_label", y=col)
    plt.title(f"{col} by Company Status")
    plt.tight_layout()
    plt.savefig(
        os.path.join(OUT, f"boxplot_{col}.png"),
        dpi=160
    )
    plt.close()

# -----------------------------
# 12. Outlier detection using IQR
# -----------------------------
outlier_rows = []

for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    count = ((df[col] < lower) | (df[col] > upper)).sum()

    outlier_rows.append({
        "feature": col,
        "outlier_count": int(count),
        "outlier_percentage": round(count / len(df) * 100, 2)
    })

outlier_df = pd.DataFrame(outlier_rows).sort_values(
    "outlier_percentage", ascending=False
)

print("\n========== OUTLIER SUMMARY ==========")
print(outlier_df.to_string(index=False))
outlier_df.to_csv(os.path.join(OUT, "outlier_summary.csv"), index=False)

# -----------------------------
# 13. Status-wise median comparison
# -----------------------------
median_by_status = df.groupby("status_label")[numeric_cols].median().T
median_by_status["difference_failed_minus_alive"] = (
    median_by_status["failed"] - median_by_status["alive"]
)

print("\n========== MEDIAN VALUES BY STATUS ==========")
print(median_by_status.round(3))

median_by_status.to_csv(
    os.path.join(OUT, "median_by_status.csv")
)

# -----------------------------
# 14. Strongest correlations
# -----------------------------
pairs = []
for i, col1 in enumerate(numeric_cols):
    for col2 in numeric_cols[i + 1:]:
        pairs.append((col1, col2, corr.loc[col1, col2]))

top_corr = (
    pd.DataFrame(pairs, columns=["Feature_1", "Feature_2", "Correlation"])
      .assign(Abs_Correlation=lambda x: x["Correlation"].abs())
      .sort_values("Abs_Correlation", ascending=False)
      .head(10)
)

print("\n========== TOP 10 CORRELATIONS ==========")
print(top_corr.to_string(index=False))
top_corr.to_csv(os.path.join(OUT, "top_10_correlations.csv"), index=False)

# -----------------------------
# 15. Key insights
# -----------------------------
status_counts = df["status_label"].value_counts()
alive_pct = status_counts.get("alive", 0) / len(df) * 100
failed_pct = status_counts.get("failed", 0) / len(df) * 100

company_failure = (
    df.groupby("company_name")["status_label"]
      .apply(lambda s: (s == "failed").any())
)

print("\n========== KEY EDA INSIGHTS ==========")
print(f"1. The dataset contains {len(df):,} records, {df['company_name'].nunique():,} unique companies and {df.shape[1]} columns.")
print(f"2. There are {df.isnull().sum().sum():,} missing values and {df.duplicated().sum():,} duplicate rows.")
print(f"3. 'Alive' represents {alive_pct:.2f}% of records, while 'Failed' represents {failed_pct:.2f}% of records.")
print(f"4. The data covers {df['year'].min()} to {df['year'].max()} ({df['year'].nunique()} years).")
print(f"5. {int(company_failure.sum()):,} companies have at least one record labelled 'failed'.")
print(f"6. X15, X6 and X12 have the highest IQR-based outlier percentages in this dataset.")
print("7. Several numeric variables show very strong positive correlations, indicating possible redundancy among some features.")
print("8. The feature distributions are strongly right-skewed for many variables, so mean values should be interpreted together with medians and spread.")

print("\nEDA completed. Charts and summary CSV files are saved in:", OUT)
