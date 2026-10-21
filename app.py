
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. Create project folders
Path("data").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

DATA_FILE = Path("data/energy_data.csv")

st.set_page_config(
    page_title="Industrial Energy AI",
    page_icon="⚡",
    layout="wide",
)


# 2. Generate sample industrial energy data
def generate_data():
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=90)
    rows = []

    for day, date in enumerate(dates):
        for machine, base in [
            ("M01", 120),
            ("M02", 145),
            ("M03", 100),
        ]:
            for shift in ["Morning", "Evening", "Night"]:
                production = max(20, 100 + rng.normal(0, 12))
                energy = base + production * 0.65 + rng.normal(0, 8)

                # Simulated energy spike for M02 in the final week
                if machine == "M02" and day >= 83:
                    energy += 55

                rows.append({
                    "date": date,
                    "machine": machine,
                    "shift": shift,
                    "production_units": round(production, 2),
                    "energy_kwh": round(energy, 2),
                })

    df = pd.DataFrame(rows)
    df.loc[5, "energy_kwh"] = np.nan
    df.loc[15, "production_units"] = np.nan
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


# 3. Load and clean data
def load_data():
    if not DATA_FILE.exists():
        generate_data()

    df = pd.read_csv(DATA_FILE)
    rows_before = len(df)
    missing_before = int(df.isna().sum().sum())

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for col in ["energy_kwh", "production_units"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.drop_duplicates()
    df = df.dropna(subset=["date", "machine", "shift"])

    for col in ["energy_kwh", "production_units"]:
        df[col] = df.groupby("machine")[col].transform(
            lambda s: s.fillna(s.median())
        )
        df[col] = df[col].fillna(df[col].median())

    df = df[
        (df["energy_kwh"] >= 0)
        & (df["production_units"] >= 0)
    ].copy()

    quality = {
        "rows_before": rows_before,
        "rows_after": len(df),
        "missing_before": missing_before,
        "missing_after": int(df.isna().sum().sum()),
    }

    return df, quality


# 4. Compare latest energy with previous 28-day baseline
def analyze_machines(df):
    daily = (
        df.groupby(["date", "machine"], as_index=False)
        .agg(
            energy_kwh=("energy_kwh", "sum"),
            production_units=("production_units", "sum"),
        )
    )

    latest_date = daily["date"].max()
    latest = daily[daily["date"] == latest_date].copy()

    baseline_data = daily[
        (daily["date"] < latest_date)
        & (daily["date"] >= latest_date - pd.Timedelta(days=28))
    ]

    baseline = (
        baseline_data.groupby("machine")["energy_kwh"]
        .mean()
        .rename("baseline_kwh")
    )

    latest = latest.join(baseline, on="machine")
    latest["baseline_kwh"] = latest["baseline_kwh"].fillna(
        latest["energy_kwh"]
    )

    latest["change_kwh"] = (
        latest["energy_kwh"] - latest["baseline_kwh"]
    )

    latest["change_pct"] = np.where(
        latest["baseline_kwh"] > 0,
        latest["change_kwh"] / latest["baseline_kwh"] * 100,
        0,
    )

    latest["kwh_per_unit"] = np.where(
        latest["production_units"] > 0,
        latest["energy_kwh"] / latest["production_units"],
        np.nan,
    )

    return daily, latest.sort_values("change_kwh", ascending=False), latest_date


# 5. Forecast total energy for tomorrow
def forecast_energy(daily):
    total = (
        daily.groupby("date", as_index=False)["energy_kwh"]
        .sum()
        .sort_values("date")
    )

    total["day_number"] = np.arange(len(total))
    total["day_of_week"] = total["date"].dt.dayofweek
    features = ["day_number", "day_of_week"]

    train = total.iloc[:-7]
    test = total.iloc[-7:]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        min_samples_leaf=2,
    )

    model.fit(train[features], train["energy_kwh"])
    predictions = model.predict(test[features])
    mae = mean_absolute_error(test["energy_kwh"], predictions)

    model.fit(total[features], total["energy_kwh"])

    tomorrow = total["date"].max() + pd.Timedelta(days=1)
    next_day = pd.DataFrame({
        "day_number": [len(total)],
        "day_of_week": [tomorrow.dayofweek],
    })

    prediction = float(model.predict(next_day[features])[0])

    return tomorrow, max(0, prediction), float(mae)


# 6. Display application
st.title("⚡ Industrial Energy Intelligence")
st.write(
    "Clean energy data, identify unusual machine consumption "
    "and estimate tomorrow's energy requirement."
)

prompt = st.text_area(
    "Your analysis request",
    "Find unusual energy consumption, forecast tomorrow, and suggest a target."
)

if st.button("Run Energy Analysis", type="primary"):
    with st.spinner("Analyzing energy data..."):
        df, quality = load_data()
        daily, machines, latest_date = analyze_machines(df)
        tomorrow, forecast, mae = forecast_energy(daily)

        target = forecast * 0.97

        st.subheader("1. Data Quality")
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows before cleaning", quality["rows_before"])
        c2.metric("Rows after cleaning", quality["rows_after"])
        c3.metric("Missing cells after cleaning", quality["missing_after"])

        st.subheader("2. Energy Forecast")
        c1, c2, c3 = st.columns(3)
        c1.metric("Latest data date", str(latest_date.date()))
        c2.metric("Tomorrow's forecast", f"{forecast:,.1f} kWh")
        c3.metric("Proposed target", f"{target:,.1f} kWh")

        st.caption(
            f"Forecast evaluation MAE on a 7-day holdout: {mae:.1f} kWh. "
            "This is a baseline model, not a guaranteed prediction."
        )

        st.subheader("3. Machine Consumption Analysis")
        st.dataframe(machines.round(2), use_container_width=True)

        st.subheader("4. Energy Trend")
        chart = daily.pivot(
            index="date",
            columns="machine",
            values="energy_kwh",
        )
        st.line_chart(chart)

        st.subheader("5. Findings")
        top = machines.iloc[0]

        if top["change_kwh"] > 0:
            st.write(
                f"**Investigation lead:** {top['machine']} has the largest "
                f"positive deviation: +{top['change_kwh']:.1f} kWh "
                f"({top['change_pct']:.1f}%) versus its baseline."
            )
        else:
            st.write("No machine is above its calculated baseline today.")

        st.write(
            "A consumption spike does not prove a mechanical fault. "
            "Check machine runtime, production levels, idle periods, "
            "maintenance records, and meter readings."
        )

        st.subheader("6. Recommended Actions")
        st.write("1. Inspect the machine with the largest energy increase.")
        st.write("2. Compare energy per unit of production.")
        st.write("3. Check shift-wise runtime and idle energy usage.")
        st.write("4. Validate the proposed target against tomorrow's production plan.")

        report = {
            "prompt": prompt,
            "latest_data_date": str(latest_date.date()),
            "forecast_date": str(tomorrow.date()),
            "forecast_kwh": round(forecast, 2),
            "proposed_target_kwh": round(target, 2),
            "data_quality": quality,
            "machine_analysis": machines.round(2).to_dict(orient="records"),
        }

        report_path = Path("reports/latest_report.json")
        report_path.write_text(
            pd.Series(report).to_json(indent=2, force_ascii=False),
            encoding="utf-8",
        )

        st.success("Analysis complete! Report saved in reports/latest_report.json")

        st.download_button(
            "Download Analysis Report",
            data=pd.Series(report).to_json(indent=2, force_ascii=False),
            file_name="energy_report.json",
            mime="application/json",
        )
else:
    st.info("Enter your request and click Run Energy Analysis.")
