# American Bankruptcy EDA

Exploratory Data Analysis of the American Bankruptcy dataset for Business Analytics.

## Overview

This project performs comprehensive exploratory data analysis (EDA) on the American Bankruptcy dataset, examining company financial metrics and their relationship to bankruptcy status.

## Dataset Structure

- **company_name**: Name of the company
- **year**: Year of the record
- **status_label**: Company status ("alive" or "failed")
- **X1 to X64**: Financial ratio features

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Place `american_bankruptcy.csv` in the project directory, then run:

```bash
python American_Bankruptcy_EDA.py
```

## Output

The script generates:

1. **Visualizations** (PNG files):
   - `01_status_distribution.png` - Distribution of company status
   - `02_yearly_status_trend.png` - Status trends over time
   - `03_failure_percentage_by_year.png` - Failure rates by year
   - `04_numeric_distributions.png` - Distributions of all numeric features
   - `05_correlation_heatmap.png` - Correlation matrix heatmap
   - `boxplot_*.png` - Boxplots for each feature by status

2. **Summary Reports** (CSV files):
   - `outlier_summary.csv` - Outlier detection results
   - `median_by_status.csv` - Median values by company status
   - `top_10_correlations.csv` - Top 10 feature correlations

## Key Insights

- Dataset composition and balance analysis
- Temporal trends in company status
- Feature distributions and outliers
- Correlation analysis among financial ratios
- Status-wise statistical comparisons

## Author

Created as part of the Introduction to Business Analytics course (2026)
