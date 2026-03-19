# Paper: Interpretable Readmission Risk Scoring with Shapley Values

## Citation
Scott, M.G., Halpert, J., & Beesly, P. (2023). "Interpretable Readmission Risk Scoring with Shapley Values in Clinical Settings." *Journal of Biomedical Informatics*, 142, 104378.

## My Contributions
- Led model development: XGBoost classifier trained on 50M+ patient records
- Designed the SHAP-based interpretation framework that clinicians use to understand individual risk scores
- First-authored the paper; presented at 2 internal medical conferences

## Technical Approach
- XGBoost with careful feature engineering from EHR data (labs, vitals, diagnoses, medications, social determinants)
- SHAP values computed per-prediction to generate patient-level risk explanations
- Validated across 4 hospital systems with different patient populations
- Calibration analysis ensuring predicted probabilities match observed rates

## Key Results
- 0.82 AUC on held-out test set across all sites
- 12% reduction in 30-day readmissions when model was used to prioritize follow-up care
- Clinician trust study: 85% of surveyed MDs said SHAP explanations increased their confidence in model recommendations

## Skills Demonstrated
- Production ML (XGBoost, feature engineering at scale)
- Model interpretability (SHAP)
- Healthcare domain expertise
- Scientific writing and peer review
- Cross-functional collaboration with clinical teams
