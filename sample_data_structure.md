# American Bankruptcy Dataset - Sample Structure

## Data Format

The `american_bankruptcy.csv` file should have the following structure:

```
company_name,year,status_label,X1,X2,X3,...,X64
Company_A,2019,alive,0.5,0.8,0.3,...,0.6
Company_B,2019,failed,0.2,0.1,0.9,...,0.1
Company_C,2020,alive,0.6,0.7,0.4,...,0.5
...
```

## Columns

### Metadata Columns
- **company_name** (string): Name/identifier of the company
- **year** (integer): Year of the observation (e.g., 2015-2022)
- **status_label** (string): Target variable - either "alive" or "failed"

### Feature Columns
- **X1 to X64** (float): Financial ratios and metrics
  - These typically represent normalized financial indicators
  - May include liquidity, profitability, solvency, and efficiency ratios

## Sample Data Specifications

- **Total Records**: 5,910 observations
- **Unique Companies**: 1,000 companies
- **Time Period**: 2015-2022 (8 years)
- **Status Distribution**:
  - Alive: ~88% of records
  - Failed: ~12% of records
- **Feature Range**: Typically 0-1 or normalized values
- **Missing Values**: Generally clean dataset with minimal missing data

## Data Characteristics

- Right-skewed distributions for many financial ratios
- Strong positive correlations between some features
- Several features with high outlier percentages (X15, X6, X12)
- Temporal pattern: failure rates vary by year
- Class imbalance: More "alive" than "failed" companies
