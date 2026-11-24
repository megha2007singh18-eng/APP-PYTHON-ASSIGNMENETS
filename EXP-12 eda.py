import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore


np.random.seed(42)
n_samples = 1000

data = {
    'customer_id': range(1, n_samples + 1),
    'age': np.random.normal(40, 12, n_samples).astype(int),
    'tenure': np.random.exponential(24, n_samples).astype(int),
    'monthly_charges': np.random.normal(65, 20, n_samples),
    'total_charges': np.random.normal(2000, 1500, n_samples),
    'num_services': np.random.randint(1, 8, n_samples),
    'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples, p=[0.5, 0.3, 0.2]),
    'payment_method': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n_samples),
    'churn': np.random.choice([0, 1], n_samples, p=[0.73, 0.27])
}

df = pd.DataFrame(data)

missing_indices = np.random.choice(n_samples, 50, replace=False)
df.loc[missing_indices[:25], 'monthly_charges'] = np.nan
df.loc[missing_indices[25:], 'total_charges'] = np.nan

outlier_indices = np.random.choice(n_samples, 20, replace=False)
df.loc[outlier_indices[:10], 'monthly_charges'] = np.random.uniform(200, 500, 10)
df.loc[outlier_indices[10:], 'total_charges'] = np.random.uniform(10000, 20000, 10)

df.to_csv('customer_churn.csv', index=False)
print("Original dataset saved as 'customer_churn.csv'")


df = pd.read_csv('customer_churn.csv')


print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print("\nFirst 5 records:")
print(df.head())
print("\nDataset information:")
print(df.info())
print("\nColumn names:")
print(df.columns.tolist())
print("\nShape:", df.shape)


print("\n" + "=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

numerical_cols = ['age', 'tenure', 'monthly_charges', 'total_charges', 'num_services']

print("\n--- Basic Statistics (describe) ---")
print(df[numerical_cols].describe())

print("\n--- Mean ---")
print(df[numerical_cols].mean())

print("\n--- Median ---")
print(df[numerical_cols].median())

print("\n--- Mode ---")
print(df[numerical_cols].mode().iloc[0])

print("\n--- Standard Deviation ---")
print(df[numerical_cols].std())

print("\n--- Variance ---")
print(df[numerical_cols].var())

print("\n--- Minimum ---")
print(df[numerical_cols].min())

print("\n--- Maximum ---")
print(df[numerical_cols].max())

print("\n--- Quantiles (25th, 50th, 75th) ---")
print(df[numerical_cols].quantile([0.25, 0.5, 0.75]))


print("\n" + "=" * 60)
print("DATA VISUALIZATION")
print("=" * 60)

sns.set_style("whitegrid")
plt.figure(figsize=(15, 10))

for i, col in enumerate(numerical_cols, 1):
    plt.subplot(2, 3, i)
    plt.hist(df[col].dropna(), bins=20, edgecolor='black', alpha=0.7)
    plt.title(f'{col} Distribution')
    plt.xlabel(col)
    plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('histograms.png')
plt.show()

plt.figure(figsize=(15, 5))
for i, col in enumerate(numerical_cols, 1):
    plt.subplot(1, 5, i)
    sns.boxplot(y=df[col])
    plt.title(f'Box Plot of {col}')

plt.tight_layout()
plt.savefig('boxplots.png')
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(df['monthly_charges'], df['total_charges'], alpha=0.5)
plt.title('Monthly Charges vs Total Charges')
plt.xlabel('Monthly Charges')
plt.ylabel('Total Charges')
plt.savefig('scatter_monthly_vs_total.png')
plt.show()

plt.figure(figsize=(8, 6))
scatter = plt.scatter(df['age'], df['monthly_charges'], c=df['churn'], alpha=0.5, cmap='coolwarm')
plt.title('Age vs Monthly Charges (colored by Churn)')
plt.xlabel('Age')
plt.ylabel('Monthly Charges')
plt.colorbar(scatter, label='Churn')
plt.savefig('scatter_age_vs_monthly.png')
plt.show()

plt.figure(figsize=(10, 8))
corr_matrix = df[numerical_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Matrix')
plt.savefig('correlation_matrix.png')
plt.show()


print("\n" + "=" * 60)
print("HANDLING MISSING DATA")
print("=" * 60)

print("\nMissing values per column:")
print(df.isnull().sum())

print("\nTotal missing values:", df.isnull().sum().sum())

df_filled = df.copy()
for col in numerical_cols:
    if df_filled[col].isnull().any():
        mean_val = df_filled[col].mean()
        df_filled[col] = df_filled[col].fillna(mean_val)
        print(f"Filled missing values in '{col}' with mean: {mean_val:.2f}")

print("\nMissing values after filling:")
print(df_filled.isnull().sum())


print("\n" + "=" * 60)
print("DETECTING AND HANDLING OUTLIERS")
print("=" * 60)

df_zscore = df_filled[numerical_cols].apply(zscore)
df_filled['age_zscore'] = df_zscore['age']
df_filled['tenure_zscore'] = df_zscore['tenure']
df_filled['monthly_charges_zscore'] = df_zscore['monthly_charges']
df_filled['total_charges_zscore'] = df_zscore['total_charges']
df_filled['num_services_zscore'] = df_zscore['num_services']

outlier_condition = (
    (df_filled['age_zscore'].abs() > 3) |
    (df_filled['tenure_zscore'].abs() > 3) |
    (df_filled['monthly_charges_zscore'].abs() > 3) |
    (df_filled['total_charges_zscore'].abs() > 3) |
    (df_filled['num_services_zscore'].abs() > 3)
)

outliers = df_filled[outlier_condition]
print(f"\nNumber of outliers detected: {len(outliers)}")
print("\nOutlier records:")
print(outliers[numerical_cols + [c for c in df_filled.columns if 'zscore' in c]])

df_no_outliers = df_filled[~outlier_condition].copy()
print(f"\nDataset shape after removing outliers: {df_no_outliers.shape}")

def cap_values(series):
    upper_limit = series.mean() + 3 * series.std()
    lower_limit = series.mean() - 3 * series.std()
    return series.clip(lower=lower_limit, upper=upper_limit)

df_capped = df_filled.copy()
for col in numerical_cols:
    df_capped[col + '_capped'] = cap_values(df_capped[col])
    print(f"Capped '{col}': lower={df_capped[col + '_capped'].min():.2f}, upper={df_capped[col + '_capped'].max():.2f}")

print("\nCapped columns created:", [c for c in df_capped.columns if 'capped' in c])


print("\n" + "=" * 60)
print("VERIFICATION OF CLEANED DATASET")
print("=" * 60)

print("\nMissing values in df_no_outliers:")
print(df_no_outliers.isnull().sum())

zscore_cols = [c for c in df_no_outliers.columns if 'zscore' in c]
if zscore_cols:
    remaining_outliers = df_no_outliers[
        (df_no_outliers[zscore_cols].abs() > 3).any(axis=1)
    ]
    print(f"\nRemaining outliers in df_no_outliers: {len(remaining_outliers)}")

zscore_cols_capped = [c for c in df_capped.columns if 'zscore' in c]
if zscore_cols_capped:
    remaining_outliers_capped = df_capped[
        (df_capped[zscore_cols_capped].abs() > 3).any(axis=1)
    ]
    print(f"Remaining outliers in df_capped: {len(remaining_outliers_capped)}")

print("\nFinal dataset (df_no_outliers) shape:", df_no_outliers.shape)
print("Columns:", df_no_outliers.columns.tolist())


print("\n" + "=" * 60)
print("SAVING CLEANED DATASETS")
print("=" * 60)

df_no_outliers.to_csv('customer_churn_cleaned_no_outliers.csv', index=False)
print("Saved: customer_churn_cleaned_no_outliers.csv")

df_capped.to_csv('customer_churn_cleaned_capped.csv', index=False)
print("Saved: customer_churn_cleaned_capped.csv")

df_filled.to_csv('customer_churn_filled.csv', index=False)
print("Saved: customer_churn_filled.csv")

print("\n" + "=" * 60)
print("EDA COMPLETE")
print("=" * 60)
