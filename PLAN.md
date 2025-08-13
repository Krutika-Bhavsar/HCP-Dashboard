# HCP Targeting Optimization MVP - Plan

## Goal
Identify and rank high-value healthcare professionals (HCPs) for marketing/sales reps using synthetic data.

## Inputs
- Synthetic HCP data (generated via Synthea-like logic)
- Columns: NPI Id, speciality, rx value, state code, writing behavior for rx of NPI

## Outputs
- HCP segmentation
- Priority list
- Channel affinity (email vs in-person)

## Implementation Steps
1. Generate synthetic HCP data in `hcp_utils.py`.
2. Implement ranking, segmentation, and channel affinity logic in `hcp_utils.py`.
3. Build Streamlit UI in `app.py` to:
   - Display segmentation, priority list, and channel affinity
   - Allow filtering by state and specialty
4. Document plan and usage in `PLAN.md`.

## File Structure
- app.py (Streamlit UI)
- hcp_utils.py (data & logic)
- PLAN.md (this plan)
