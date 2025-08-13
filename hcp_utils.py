# hcp_utils.py
# Contains data generation, processing, and ranking functions for HCP dashboard
import pandas as pd
import numpy as np
import random

def synthea_simulator(num_patients=200):
    """
    Simulate Synthea-like provider and patient data and return HCP DataFrame.
    This is a placeholder for Synthea, generating realistic provider data.
    """
    np.random.seed(42)
    random.seed(42)
    npi_ids = [str(1000000000 + i) for i in range(num_patients)]
    specialties = random.choices([
        'Cardiology', 'Dermatology', 'Endocrinology', 'Family Medicine', 'Gastroenterology',
        'Internal Medicine', 'Neurology', 'Oncology', 'Pediatrics', 'Psychiatry', 'Surgery'
    ], k=num_patients)
    state_codes = random.choices([
        'CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI'
    ], k=num_patients)
    rx_values = np.random.lognormal(mean=9, sigma=0.7, size=num_patients).astype(int)
    writing_behavior = np.random.choice(['High', 'Medium', 'Low'], size=num_patients, p=[0.3, 0.5, 0.2])

    df = pd.DataFrame({
        'NPI Id': npi_ids,
        'speciality': specialties,
        'rx value': rx_values,
        'state_code': state_codes,
        'writing_behavior': writing_behavior
    })
    return df

def generate_hcp_data(num_hcps=200):
    """Generate synthetic HCP data using the Synthea simulator."""
    return synthea_simulator(num_hcps)

def save_hcp_data_to_excel(df, filename="hcp_data.xlsx"):
    """Save HCP DataFrame to an Excel file."""
    df.to_excel(filename, index=False)

def load_hcp_data_from_excel(filename="hcp_data.xlsx"):
    """Load HCP DataFrame from an Excel file."""
    return pd.read_excel(filename)

def rank_hcps(df):
    """Rank HCPs by rx value and writing behavior."""
    score_map = {'High': 3, 'Medium': 2, 'Low': 1}
    df['score'] = df['rx value'] * df['writing_behavior'].map(score_map)
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    df['priority_rank'] = df.index + 1
    return df

def segment_hcps(df):
    """Segment HCPs into tiers based on priority rank."""
    n = len(df)
    bins = [0, int(n*0.2), int(n*0.5), n]
    labels = ['Top 20%', 'Middle 30%', 'Bottom 50%']
    df['segment'] = pd.cut(df['priority_rank'], bins=bins, labels=labels, include_lowest=True)
    return df

def channel_affinity(df):
    """Assign channel affinity based on writing behavior and specialty."""
    affinity = []
    for _, row in df.iterrows():
        if row['writing_behavior'] == 'High' or row['speciality'] in ['Cardiology', 'Oncology']:
            affinity.append('In-person')
        else:
            affinity.append('Email')
    return pd.DataFrame({'NPI Id': df['NPI Id'], 'channel_affinity': affinity})
