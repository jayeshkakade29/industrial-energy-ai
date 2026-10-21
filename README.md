# ⚡ Industrial Energy AI — Energy Analytics & Forecasting Dashboard

<p align="center">
  <strong>Turn industrial energy data into actionable insights.</strong>
</p>

<p align="center">
  <a href="https://industrial-energy-ai-jftbz5kt6c8ahdhxxiajfm.streamlit.app/">
    <strong>🚀 Live Demo</strong>
  </a>
  &nbsp; • &nbsp;
  <a href="https://github.com/jayeshkakade29/industrial-energy-ai">
    <strong>📂 GitHub Repository</strong>
  </a>
</p>

---

## 📌 Project Overview

**Industrial Energy AI** is a Python-based industrial energy analytics and forecasting application built to explore machine-level energy consumption, identify unusual consumption patterns, estimate next-day energy usage, and support data-driven energy management.

The application combines data cleaning, exploratory analysis, machine-level comparisons, machine learning, and an interactive Streamlit dashboard in one workflow.

It uses a synthetic industrial energy dataset to demonstrate how data engineering and machine learning techniques can help identify potential energy inefficiencies and support operational decision-making.

## 🎯 Project Objectives

- Analyze industrial energy consumption across multiple machines and shifts.
- Clean missing values and remove duplicate records.
- Compare recent machine energy usage against historical baselines.
- Calculate energy consumption per production unit.
- Forecast next-day total energy consumption using machine learning.
- Visualize energy trends and machine-level insights.
- Generate a structured JSON analysis report.
- Provide actionable recommendations for further investigation.

## 🚀 Live Application

**Try the deployed dashboard:**

👉 [Industrial Energy AI — Open Live Dashboard](https://industrial-energy-ai-jftbz5kt6c8ahdhxxiajfm.streamlit.app/)

The application is deployed using Streamlit Community Cloud.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data processing and analysis |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and forecasting |
| Random Forest Regressor | Next-day energy consumption prediction |
| Streamlit | Interactive web dashboard |
| Matplotlib / Streamlit charts | Data visualization, where implemented |
| CSV | Input dataset storage |
| JSON | Structured analysis report |
| Git & GitHub | Version control and source code hosting |

## ✨ Current Features

### 1. Synthetic Industrial Dataset

The application generates a sample dataset containing approximately 90 days of industrial energy records for three machines:

- Machine M01
- Machine M02
- Machine M03

The sample data includes machine identifiers, shifts, energy consumption, production quantities, and dates.

The dataset also includes simulated data-quality issues and an artificial consumption spike to demonstrate the analysis workflow.

### 2. Data Cleaning

The application performs basic data-quality operations:

- Identifies and removes duplicate records.
- Handles missing numerical values using machine-level median values.
- Prepares the cleaned dataset for analysis and forecasting.

### 3. Machine-Level Energy Analysis

The dashboard analyzes machine consumption and compares the latest available day with a historical baseline based on the preceding 28 days.

It helps highlight machines that may require further investigation because of increased energy usage.

### 4. Energy Efficiency Analysis

The application calculates energy consumption per production unit.

This metric helps compare energy usage relative to output rather than looking only at total consumption.

### 5. Next-Day Energy Forecast

A Random Forest Regressor is used to estimate next-day total energy consumption.

The model uses date-related features, including the day number and day of the week.

The application also evaluates the model on a holdout period and calculates Mean Absolute Error (MAE).

**Important:** This is an initial forecasting model intended for learning and demonstration. It is not yet a production-grade industrial forecasting system.

### 6. Interactive Streamlit Dashboard

The dashboard brings the analysis together in one interface, including:

- Data-quality information
- Energy consumption insights
- Machine-level comparisons
- Historical energy trends
- Next-day energy forecast
- Suggested energy-saving target
- Recommended actions for investigation

### 7. JSON Report Generation

The application saves the latest analysis report to:

`reports/latest_report.json`

The report can be downloaded from the dashboard when the corresponding download option is available.

---

## 🔄 Application Workflow

```text
Synthetic Industrial Energy Data
              |
              v
        Load CSV Dataset
              |
              v
        Data Cleaning
   (Missing Values & Duplicates)
              |
              v
      Machine-Level Analysis
              |
              v
   Historical Baseline Comparison
              |
              v
     Energy Efficiency Metrics
              |
              v
   Random Forest Energy Forecast
              |
              v
      Streamlit Dashboard
              |
              v
       JSON Report Export
```

## 📁 Project Structure

```text
industrial-energy-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── energy_data.csv
│
└── reports/
    └── latest_report.json
```

**File and folder descriptions**

- `app.py` — Main application containing the data-processing, analysis, forecasting, and dashboard logic.
- `requirements.txt` — Python dependencies required to run the application.
- `README.md` — Project documentation.
- `.gitignore` — Specifies local files and folders that should not be committed.
- `data/energy_data.csv` — Generated industrial energy dataset.
- `reports/latest_report.json` — Latest generated analysis report.

The CSV and JSON files are generated by the application when the relevant workflow runs. Depending on your Git configuration, they may be generated locally rather than committed to the repository.

## ⚙️ Installation and Setup

Follow these steps to run the project on your local machine.

### Prerequisites

Install the following:

- Python 3.10 or a compatible version supported by the dependencies
- Git
- A code editor such as Visual Studio Code

### Step 1: Clone the Repository

```bash
git clone https://github.com/jayeshkakade29/industrial-energy-ai.git
```

### Step 2: Navigate to the Project

```bash
cd industrial-energy-ai
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

### Step 5: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

`http://localhost:8501`

Open that URL in your browser to use the dashboard.

## 📊 Machine Learning Approach

The current forecasting workflow uses a Random Forest Regressor.

**Model workflow:**

1. Prepare the energy consumption data.
2. Extract date-related features.
3. Split the data into training and holdout periods.
4. Train and evaluate the model.
5. Calculate Mean Absolute Error (MAE).
6. Retrain using the available dataset.
7. Predict the next day's total energy consumption.

### Evaluation Metric

**Mean Absolute Error (MAE)** measures the average absolute difference between actual and predicted energy consumption.

A lower MAE generally indicates smaller prediction errors on the evaluated data. Actual performance depends on the dataset and evaluation period.

## 🔍 Example Use Case

Imagine a manufacturing facility tracking the daily energy consumption of multiple machines.

The dashboard can help an analyst:

1. Examine historical energy usage.
2. Identify a machine with a recent increase in consumption.
3. Compare energy consumption against production output.
4. Review the next-day energy forecast.
5. Investigate possible operational causes.
6. Explore potential energy-saving opportunities.

The results provide **signals for investigation**, not proof of a mechanical fault or a confirmed root cause.

## 🔐 Data and Security

- The current project uses synthetic demonstration data.
- No real industrial sensor integration is currently required.
- Do not commit passwords, API keys, private configuration files, or other secrets to GitHub.
- Real industrial deployment would require appropriate data validation, access controls, monitoring, and security measures.

## 🚧 Current Limitations

This is an evolving portfolio project. Current limitations include:

- The dataset is synthetic rather than sourced from a live industrial system.
- The machine-level anomaly investigation is based on simple historical comparisons.
- The forecasting model uses a limited set of date-related features.
- Forecast accuracy may vary with the data and operating conditions.
- Suggested energy-saving targets are illustrative and are not guaranteed savings.
- The current application does not yet contain a fully implemented natural-language AI agent.

## 🗺️ Future Improvements

Planned improvements may include:

- [ ] Build a single-prompt AI agent for natural-language energy analysis.
- [ ] Add AI-generated explanations and evidence-based recommendations.
- [ ] Improve anomaly detection and root-cause investigation.
- [ ] Introduce richer forecasting features and time-series evaluation.
- [ ] Integrate real industrial energy datasets or sensor data.
- [ ] Add a proper data ingestion and transformation pipeline.
- [ ] Add historical report tracking and downloadable CSV exports.
- [ ] Evaluate deployment, monitoring, and data-quality improvements.

These items are planned enhancements and are not represented as completed features.

## 🎓 What This Project Demonstrates

This project demonstrates practical experience with:

- Python-based data analysis
- Data cleaning and preprocessing
- Exploratory data analysis
- Machine learning regression
- Forecast evaluation
- Industrial energy efficiency metrics
- Interactive dashboard development
- Structured report generation
- Git, GitHub, and application deployment

## 👨‍💻 Author

**Jayesh Kakade**

- GitHub: [@jayeshkakade29](https://github.com/jayeshkakade29)
- Project Repository: [industrial-energy-ai](https://github.com/jayeshkakade29/industrial-energy-ai)
- Live Demo: [Open Industrial Energy AI](https://industrial-energy-ai-jftbz5kt6c8ahdhxxiajfm.streamlit.app/)

---

⭐ If you find this project interesting, feel free to explore the repository and share feedback.

*Built as a learning-focused portfolio project exploring industrial energy analytics, machine learning, and interactive data applications.*