import pandas as pd
import os

DATA_DIR = "data"

def load_all_data():
    files = [
        "indeed_jobs_with_expanded_domains.csv",
        "LinkedIn_Jobs_20251025_1427.csv",
        "RemoteOK_AllDomains_Last2Months.csv",
        "Remotive_Jobs_All_Domains-Faizu.csv",
        "WeWorkRemotely_Jobs_20251024_1734.csv"
    ]
    datasets = []
    for f in files:
        path = os.path.join(DATA_DIR, f)
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
            df['platform'] = f.split('_')[0]
            datasets.append(df)
    return datasets


def extract_role_domains(datasets):
    possible_cols = ['role_domain', 'domain', 'category', 'job_domain', 'job_category', 'specialization']
    domains = set()

    for df in datasets:
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        found = None
        for col in possible_cols:
            if col in df.columns:
                found = col
                break
        if found:
            domains.update(df[found].dropna().unique())
    return sorted(list(domains))


def load_login_data():
    path = os.path.join(DATA_DIR, "per_day_login.csv")
    if not os.path.exists(path):
        return pd.DataFrame(columns=['platform', 'logins_per_day'])

    df = pd.read_csv(path)
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

    # Handle your actual columns: "Portal", "Estimated Daily Visitors"
    if 'portal' in df.columns and 'estimated_daily_visitors' in df.columns:
        df = df.rename(columns={
            'portal': 'platform',
            'estimated_daily_visitors': 'logins_per_day'
        })
    else:
        # fallback detection
        platform_col = None
        login_col = None
        for c in df.columns:
            if 'platform' in c or 'portal' in c or 'site' in c:
                platform_col = c
            if 'login' in c or 'visitor' in c:
                login_col = c
        if platform_col and login_col:
            df = df.rename(columns={platform_col: 'platform', login_col: 'logins_per_day'})
        else:
            raise ValueError("⚠️ Could not detect platform or login columns in per_day_login.csv")

    return df[['platform', 'logins_per_day']]
