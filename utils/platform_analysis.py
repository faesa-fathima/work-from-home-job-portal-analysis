import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def best_platform_for_recruiter(role_domain, job_mode, job_datasets, login_data):
    combined = pd.concat(job_datasets, ignore_index=True)

    combined.columns = combined.columns.str.lower().str.strip().str.replace(' ', '_')
    if 'role_domain' not in combined.columns or 'job_mode' not in combined.columns:
        return "Data Missing Columns"

    filtered = combined[
        (combined['job_mode'].str.lower() == job_mode.lower()) &
        (combined['role_domain'].str.contains(role_domain, case=False, na=False))
    ]

    if filtered.empty:
        return "No Best Fit"

    job_counts = filtered['platform'].value_counts().reset_index()
    job_counts.columns = ['platform', 'job_count']

    login_data.columns = login_data.columns.str.lower().str.strip()
    if 'platform' not in login_data.columns:
        return "Login data missing platform info"

    merged = pd.merge(job_counts, login_data, on='platform', how='left').fillna(0)

    scaler = MinMaxScaler()
    merged[['job_score', 'login_score']] = scaler.fit_transform(
        merged[['job_count', 'logins_per_day']]
    )

    merged['final_score'] = 0.6 * merged['job_score'] + 0.4 * merged['login_score']

    return merged.loc[merged['final_score'].idxmax(), 'platform']


def best_platform_for_job_seeker(role_domain, job_mode, job_datasets):
    combined = pd.concat(job_datasets, ignore_index=True)
    combined.columns = combined.columns.str.lower().str.strip().str.replace(' ', '_')

    if 'role_domain' not in combined.columns or 'job_mode' not in combined.columns:
        return "Data Missing Columns"

    filtered = combined[
        (combined['job_mode'].str.lower() == job_mode.lower()) &
        (combined['role_domain'].str.contains(role_domain, case=False, na=False))
    ]

    if filtered.empty:
        return "No Best Fit"

    platform_counts = filtered['platform'].value_counts()
    return platform_counts.idxmax()
