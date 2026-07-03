"""
Task 1: Data Cleaning and Preprocessing
Dataset: marketing_campaign.csv (Customer Personality Analysis - Kaggle)
Follows the mini-guide steps from the internship task PDF.
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------
# 0. LOAD RAW DATA
# ---------------------------------------------------------------
df = pd.read_csv('/home/claude/marketing_campaign.csv', sep='\t')
raw_shape = df.shape
raw_dupe_full = df.duplicated().sum()
raw_dupe_id = df['ID'].duplicated().sum()
raw_nulls = df.isnull().sum()
raw_nulls = raw_nulls[raw_nulls > 0]

log = []
log.append(f"RAW DATA: {raw_shape[0]} rows x {raw_shape[1]} columns")
log.append(f"Full-row duplicates found: {raw_dupe_full}")
log.append(f"Duplicate IDs found: {raw_dupe_id}")
log.append(f"Missing values found:\n{raw_nulls.to_string()}")

# ---------------------------------------------------------------
# 1. RENAME COLUMN HEADERS -> clean, uniform, lowercase, no spaces
# ---------------------------------------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_', regex=False)
)

# ---------------------------------------------------------------
# 2. IDENTIFY & HANDLE MISSING VALUES (.isnull())
#    income has 24 nulls -> impute with median (robust to outliers)
# ---------------------------------------------------------------
income_median = df['income'].median()
n_missing_income = df['income'].isnull().sum()
df['income'] = df['income'].fillna(income_median)

# ---------------------------------------------------------------
# 3. REMOVE DUPLICATE ROWS (.drop_duplicates())
# ---------------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
df = df.drop_duplicates(subset='id')
after = len(df)
dupes_removed = before - after

# ---------------------------------------------------------------
# 4. STANDARDIZE TEXT VALUES (education, marital_status)
# ---------------------------------------------------------------
df['education'] = df['education'].str.strip().str.title()
df['education'] = df['education'].replace({'2N Cycle': '2nd Cycle'})

df['marital_status'] = df['marital_status'].str.strip().str.title()
# Collapse non-standard / placeholder categories into "Other"
invalid_marital = ['Absurd', 'Yolo', 'Alone']
n_invalid_marital = df['marital_status'].isin(invalid_marital).sum()
df['marital_status'] = df['marital_status'].replace(
    {v: 'Other' for v in invalid_marital}
)

# ---------------------------------------------------------------
# 5. CONVERT DATE FORMATS TO CONSISTENT TYPE (dd-mm-yyyy -> datetime)
# ---------------------------------------------------------------
df['dt_customer'] = pd.to_datetime(df['dt_customer'], format='%d-%m-%Y')
# Standardize displayed format to dd-mm-yyyy text, per the PDF's hint
df['dt_customer'] = df['dt_customer'].dt.strftime('%d-%m-%Y')

# ---------------------------------------------------------------
# 6. CHECK & FIX DATA TYPES
# ---------------------------------------------------------------
int_cols = ['id', 'year_birth', 'kidhome', 'teenhome', 'recency',
            'mntwines', 'mntfruits', 'mntmeatproducts', 'mntfishproducts',
            'mntsweetproducts', 'mntgoldprods', 'numdealspurchases',
            'numwebpurchases', 'numcatalogpurchases', 'numstorepurchases',
            'numwebvisitsmonth', 'acceptedcmp3', 'acceptedcmp4', 'acceptedcmp5',
            'acceptedcmp1', 'acceptedcmp2', 'complain', 'z_costcontact',
            'z_revenue', 'response']
for c in int_cols:
    df[c] = df[c].astype('int64')
df['income'] = df['income'].astype('float64')

# ---------------------------------------------------------------
# 7. OUTLIER TREATMENT
#    a) year_birth: ages > ~100 in 2014 are clearly data-entry errors
#    b) income: extreme value (666666) is an obvious outlier
# ---------------------------------------------------------------
n_age_outliers = (df['year_birth'] < 1940).sum()
df = df[df['year_birth'] >= 1940]

n_income_outliers = (df['income'] > 200000).sum()
df = df[df['income'] <= 200000]

# ---------------------------------------------------------------
# 8. DERIVED / HELPER COLUMNS (useful, common in this dataset's cleaning)
# ---------------------------------------------------------------
df['age'] = 2014 - df['year_birth']
df['total_spending'] = (df['mntwines'] + df['mntfruits'] + df['mntmeatproducts']
                         + df['mntfishproducts'] + df['mntsweetproducts'] + df['mntgoldprods'])
df['total_children'] = df['kidhome'] + df['teenhome']

# ---------------------------------------------------------------
# 9. DROP CONSTANT / NON-INFORMATIVE COLUMNS
#    z_costcontact and z_revenue have a single constant value for every row
# ---------------------------------------------------------------
df = df.drop(columns=['z_costcontact', 'z_revenue'])

# ---------------------------------------------------------------
# 10. RESET INDEX & SAVE
# ---------------------------------------------------------------
df = df.reset_index(drop=True)
df.to_csv('/home/claude/work/marketing_campaign_cleaned.csv', index=False)

clean_shape = df.shape
log.append(f"\nMissing income values imputed with median ({income_median}): {n_missing_income} rows")
log.append(f"Duplicate rows removed: {dupes_removed}")
log.append(f"Invalid marital_status values relabeled to 'Other': {n_invalid_marital}")
log.append(f"Age outliers removed (year_birth < 1940): {n_age_outliers}")
log.append(f"Income outliers removed (income > 200000): {n_income_outliers}")
log.append(f"Constant columns dropped: z_costcontact, z_revenue")
log.append(f"\nCLEANED DATA: {clean_shape[0]} rows x {clean_shape[1]} columns")
log.append(f"Remaining nulls: {df.isnull().sum().sum()}")
log.append(f"Remaining full-row duplicates: {df.duplicated().sum()}")

with open('/home/claude/work/cleaning_log.txt', 'w') as f:
    f.write('\n'.join(log))

print('\n'.join(log))
print("\nFinal dtypes:\n", df.dtypes)
