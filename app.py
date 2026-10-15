from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="NHANES Health Correlation Explorer",
    page_icon="🩺",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "nhanes_health.csv"
NUMERIC_COLUMNS = [
    "age",
    "bmi",
    "waist_cm",
    "systolic_bp",
    "diastolic_bp",
    "hba1c",
    "total_chol",
    "hdl_chol",
    "sleep_hours",
    "sedentary_minutes",
]
LABELS = {
    "age": "Age (years)",
    "bmi": "BMI (kg/m²)",
    "waist_cm": "Waist circumference (cm)",
    "systolic_bp": "Systolic blood pressure (mmHg)",
    "diastolic_bp": "Diastolic blood pressure (mmHg)",
    "hba1c": "HbA1c (%)",
    "total_chol": "Total cholesterol (mg/dL)",
    "hdl_chol": "HDL cholesterol (mg/dL)",
    "sleep_hours": "Sleep (hours) ",
    "sedentary_minutes": "Sedentary time (minutes/day)",
}
THRESHOLDS = {
    "Systolic BP ≥ 130 mmHg": ("systolic_bp", 130),
    "BMI ≥ 30 kg/m²": ("bmi", 30),
    "HbA1c ≥ 6.5%": ("hba1c", 6.5),
}


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["sex"] = data["sex"].astype("category")
    return data


def pretty_name(column):
    return LABELS.get(column, column.replace("_", " ").title())


def correlation_stats(data, x, y, method):
    pair = pd.DataFrame({"x": data[x], "y": data[y]}).dropna()
    if len(pair) < 2 or pair["x"].nunique() < 2 or pair["y"].nunique() < 2:
        return np.nan, len(pair)
    if method == "Spearman":
        # Ranking first computes Spearman's rho without pandas' optional SciPy dependency.
        value = pair["x"].rank(method="average").corr(pair["y"].rank(method="average"))
    else:
        value = pair["x"].corr(pair["y"])
    return value, len(pair)


def correlation_matrix(data, columns, method):
    """Build pairwise correlations without requiring SciPy for Spearman."""
    result = pd.DataFrame(index=columns, columns=columns, dtype=float)
    for x in columns:
        for y in columns:
            pair = pd.DataFrame({"x": data[x], "y": data[y]}).dropna()
            if len(pair) < 2 or pair["x"].nunique() < 2 or pair["y"].nunique() < 2:
                result.loc[x, y] = np.nan
            elif method == "Spearman":
                result.loc[x, y] = pair["x"].rank(method="average").corr(
                    pair["y"].rank(method="average")
                )
            else:
                result.loc[x, y] = pair["x"].corr(pair["y"])
    return result


try:
    df = load_data()
except FileNotFoundError:
    st.error(f"Could not find the dataset at `{DATA_PATH}`. Keep nhanes_health.csv beside app.py.")
    st.stop()

st.markdown(
    """
    <style>
      .stApp { background: #f5f7fb; }
      [data-testid="stMain"] { color: #243247; }
      [data-testid="stMain"] h1,
      [data-testid="stMain"] h2,
      [data-testid="stMain"] h3,
      [data-testid="stMain"] p,
      [data-testid="stMain"] li,
      [data-testid="stMain"] [data-testid="stMarkdownContainer"] {
        color: #243247 !important;
      }
      [data-testid="stMain"] [data-testid="stCaptionContainer"] {
        color: #5b6680 !important;
      }
      [data-testid="stMain"] [data-testid="stMetricValue"] {
        color: #172033 !important;
      }
      [data-testid="stMain"] .eyebrow { color: #2363eb !important; }
      [data-testid="stMain"] [data-testid="stExpander"] summary {
        background: #1a1d25;
        color: #f8fafc !important;
      }
      [data-testid="stMain"] [data-testid="stExpander"] summary * {
        color: #f8fafc !important;
      }
      .block-container { padding-top: 4rem; padding-bottom: 3rem; max-width: 1500px; }
      [data-testid="stMetric"] { background: white; border: 1px solid #e4e9f1;
        padding: 1rem 1.15rem; border-radius: 14px; box-shadow: 0 2px 10px #1725540a; }
      [data-testid="stMetricLabel"] { color: #5b6680; }
      .eyebrow { color: #2363eb; font-size: .78rem; font-weight: 700;
        letter-spacing: .12em; text-transform: uppercase; margin-bottom: .25rem; }
      .muted { color: #5b6680; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">Data exploration · NHANES 2017–2018</div>', unsafe_allow_html=True)
st.title("Health Correlation Explorer")
st.markdown(
    "Explore how health measures move together across **4,433 adults**. "
    "Use the sidebar to filter the sample; every view below uses the same filtered participants."
)

with st.sidebar:
    st.header("Study filters")
    sex_options = ["All"] + sorted(df["sex"].dropna().astype(str).unique().tolist())
    selected_sex = st.selectbox("Sex", sex_options)
    age_min, age_max = int(df["age"].min()), int(df["age"].max())
    selected_ages = st.slider("Age range (years)", age_min, age_max, (age_min, age_max))
    st.divider()
    method_label = st.radio("Correlation method", ["Pearson", "Spearman"], horizontal=True)
    st.caption(
        "Pearson measures linear association. Spearman measures rank based, monotonic association."
    )

filtered = df[df["age"].between(*selected_ages)].copy()
if selected_sex != "All":
    filtered = filtered[filtered["sex"].astype(str) == selected_sex]

st.markdown("### Dataset at a glance")
st.markdown(
    "Each row represents one adult participant in the 2017–2018 National Health and Nutrition "
    "Examination Survey. Measures include body composition, blood pressure, blood lipids, "
    "HbA1c, sleep, and sedentary time. NHANES oversamples some groups, so these correlations "
    "describe this sample rather than the whole U.S. population."
)
metric1, metric2, metric3 = st.columns(3)
metric1.metric("Participants in current sample", f"{len(filtered):,}")
metric2.metric("Numeric measures", len(NUMERIC_COLUMNS))
metric3.metric("Missing values in source", f"{int(df[NUMERIC_COLUMNS].isna().sum().sum()):,}")

with st.expander("Preview filtered participant rows", expanded=True):
    st.dataframe(filtered, width="stretch", hide_index=True, height=260)

st.markdown("## Pairwise relationship")
pair_controls = st.columns([1, 1, 1.4])
x_col = pair_controls[0].selectbox(
    "X variable", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index("bmi"), format_func=pretty_name
)
y_default = "systolic_bp"
y_col = pair_controls[1].selectbox(
    "Y variable", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index(y_default), format_func=pretty_name
)
color_threshold = pair_controls[2].selectbox("Color points by", ["No threshold"] + list(THRESHOLDS))

pair = pd.DataFrame({"x": filtered[x_col], "y": filtered[y_col]}).dropna()
r_value, n_value = correlation_stats(filtered, x_col, y_col, method_label)
stat1, stat2, stat3 = st.columns([1, 1, 3])
stat1.metric(f"{method_label} correlation (r)", "—" if pd.isna(r_value) else f"{r_value:.3f}")
stat2.metric("Participants (n)", f"{n_value:,}")
if pd.isna(r_value):
    stat3.info("Correlation needs at least two complete observations with variation in both variables.")

fig, ax = plt.subplots(figsize=(10, 5.2))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
if not pair.empty:
    def add_trendline(plot_data, color="#e47b45"):
        usable = plot_data[["x", "y"]].dropna()
        if len(usable) > 1 and usable["x"].nunique() > 1:
            slope, intercept = np.polyfit(usable["x"], usable["y"], 1)
            line_x = np.linspace(usable["x"].min(), usable["x"].max(), 100)
            ax.plot(line_x, slope * line_x + intercept, color=color, linewidth=2.5)

    if color_threshold == "No threshold":
        ax.scatter(pair["x"], pair["y"], alpha=0.48, s=28, color="#3974d8", edgecolor="white", linewidth=0.35)
        add_trendline(pair)
    else:
        threshold_col, cutoff = THRESHOLDS[color_threshold]
        plot_data = pd.DataFrame({
            "x": filtered[x_col], "y": filtered[y_col], "threshold": filtered[threshold_col]
        }).dropna()
        plot_data["Threshold group"] = np.where(
            plot_data["threshold"] >= cutoff, f"At/above {cutoff:g}", f"Below {cutoff:g}"
        )
        for group, color in [(f"Below {cutoff:g}", "#5a8dee"), (f"At/above {cutoff:g}", "#e47b45")]:
            group_data = plot_data[plot_data["Threshold group"] == group]
            if not group_data.empty:
                ax.scatter(group_data["x"], group_data["y"], label=group, color=color,
                           alpha=0.68, s=38, edgecolor="white", linewidth=0.35)
        add_trendline(pair, color="#26344d")
        ax.legend(title=color_threshold, frameon=False)
    ax.set_xlabel(pretty_name(x_col))
    ax.set_ylabel(pretty_name(y_col))
    ax.grid(True, color="#e8edf5", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#d5dce8")
else:
    ax.text(0.5, 0.5, "No complete observations for this pair", ha="center", va="center", transform=ax.transAxes)
    ax.set_axis_off()
st.pyplot(fig, width="stretch")
plt.close(fig)
if color_threshold != "No threshold":
    st.caption("The threshold colors and fitted line are descriptive; r and n use all complete X/Y pairs in the filtered sample.")

st.markdown("## Correlation heatmap")
st.caption(f"Method: {method_label}. Each cell shows the coefficient and pairwise participant count. Colors always span −1 to 1.")
heatmap_vars = st.multiselect(
    "Numeric variables to include",
    NUMERIC_COLUMNS,
    default=["age", "bmi", "waist_cm", "systolic_bp", "hba1c", "hdl_chol", "sleep_hours"],
    format_func=pretty_name,
)

if len(heatmap_vars) < 2:
    st.info("Choose at least two numeric variables to draw the heatmap.")
else:
    heat_data = filtered[heatmap_vars]
    corr = correlation_matrix(heat_data, heatmap_vars, method_label)
    counts = heat_data.notna().astype(int).T.dot(heat_data.notna().astype(int))
    annotations = corr.copy().astype(object)
    for row in heatmap_vars:
        for col in heatmap_vars:
            value = corr.loc[row, col]
            annotations.loc[row, col] = "—" if pd.isna(value) else f"{value:.2f}\nn={int(counts.loc[row, col]):,}"
    fig, ax = plt.subplots(figsize=(max(8, len(heatmap_vars) * 1.15), max(6, len(heatmap_vars) * 0.82)))
    image = ax.imshow(corr.to_numpy(dtype=float), cmap="coolwarm", vmin=-1, vmax=1)
    colorbar = fig.colorbar(image, ax=ax, shrink=0.8)
    colorbar.set_label(f"{method_label} r")
    positions = np.arange(len(heatmap_vars))
    ax.set_xticks(positions, [pretty_name(v) for v in heatmap_vars], rotation=35, ha="right")
    ax.set_yticks(positions, [pretty_name(v) for v in heatmap_vars])
    ax.set_xticks(np.arange(-0.5, len(heatmap_vars), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(heatmap_vars), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for i, row in enumerate(heatmap_vars):
        for j, col in enumerate(heatmap_vars):
            value = corr.loc[row, col]
            label = "—" if pd.isna(value) else f"{value:.2f}\nn={int(counts.loc[row, col]):,}"
            ax.text(j, i, label, ha="center", va="center", fontsize=9, color="#172033")
    ax.set_xlim(-0.5, len(heatmap_vars) - 0.5)
    ax.set_ylim(len(heatmap_vars) - 0.5, -0.5)
    ax.set_xlabel("")
    ax.set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

st.caption("A correlation near zero does not rule out a nonlinear pattern (for example, a U-shaped relationship).")
