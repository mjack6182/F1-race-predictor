# Predicting Formula 1 Podium Finishes

A data science project for CIS 710. The goal is to predict whether a driver will finish on the podium (top 3) using only information available before the race, such as grid position, qualifying results, and driver and constructor form going into the race. The model is a random forest classifier trained on historical race results from 1950 onward. Recent seasons are added from the FastF1 library so the model reflects the current grid.

## Data Sources

- **Kaggle:** [Formula 1 World Championship (1950 - 2024)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020) by Rohan Rao
- **FastF1:** the [FastF1](https://docs.fastf1.dev/) Python library, for 2025 and later seasons

## Project Structure

```
data/raw/        Kaggle CSVs (committed)
data/recent/     FastF1 export for 2025+
data/processed/  Cleaned, model-ready data
notebooks/       01_eda, 02_preprocessing, 03_model
src/             Reusable Python code
reports/         Proposal, slides, and figures
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name f1-podium
```

Then launch Jupyter with `jupyter notebook` (or `jupyter lab`) and select the `f1-podium` kernel.

## Data Placement

The Kaggle CSVs are already committed in `data/raw/`. To refresh them, download the dataset from the Kaggle link above and replace the CSVs in `data/raw/` (`races.csv`, `results.csv`, `qualifying.csv`, `drivers.csv`, etc.). FastF1 exports go in `data/recent/`. The FastF1 cache folder is git-ignored.

## Deliverables

| Deliverable        | Due          |
|--------------------|--------------|
| Proposal           | Nov 13, 2026 |
| Presentation       | Dec 4, 2026  |
| Final submission   | Dec 7, 2026  |
