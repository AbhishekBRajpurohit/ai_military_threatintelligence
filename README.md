# GTD Analytics & Forecasting Dashboard

A Streamlit dashboard for exploring, visualizing, and forecasting trends in the
[Global Terrorism Database (GTD)](https://www.start.umd.edu/gtd/) — a public,
historical research dataset.

## ⚠️ Important Limitations

- **Not a live intelligence tool.** GTD is a static, historical dataset with no
  real-time feed. This project is for educational/portfolio purposes.
- **Attack Type Prediction** uses only pre-attack information (location, group,
  weapon/target choice) — casualty counts are intentionally excluded since they
  are outcomes, not predictors.
- **Threat Level Prediction** is a hand-tuned heuristic scoring system, not a
  validated statistical model.
- Model evaluation uses a **temporal split** (train on earlier years, test on
  later years) rather than a random split, since GTD is a time-series dataset
  and random splits would leak future information into training.

## Features

- 🌍 Global threat map with clustering for large result sets
- 🌍 Per-country incident analysis
- ⚖️ Multi-country comparison view
- 🤖 ML-based attack type prediction (RandomForest, temporal split)
- 🎯 Rule-based threat level scoring + ML casualty estimate
- 📈 Prophet-based trend forecasting
- 🧠 Auto-generated PDF/Word intelligence summary reports
- 📊 Filterable raw data explorer
- 🕵️ Group activity profiles

## Setup

```bash
pip install -r requirements.txt
python train_attack_model.py
python train_severity_model.py
```

Create `.streamlit/secrets.toml`:

```toml
APP_PASSWORD = "your-password-here"
```

Run:

```bash
streamlit run app.py
```

## Docker

```bash
docker compose up --build
```

## Data

Place `globalterrorism.csv` (GTD export) inside `data/`. Not included in this
repo due to size and licensing — download from the [START Consortium](https://www.start.umd.edu/gtd/contact/).

## Tech Stack

Python · Streamlit · scikit-learn · Prophet · Plotly · Folium · pandas