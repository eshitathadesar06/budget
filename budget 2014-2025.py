import streamlit as st
import pandas as pd

# ----------------------------------------------------
# Page Settings
# ----------------------------------------------------
st.set_page_config(page_title="Budget Analysis Dashboard", layout="wide")

# ----------------------------------------------------
# Custom CSS for Beautiful UI/UX
# ----------------------------------------------------
st.markdown("""
    <style>
        .card {
            padding: 20px;
            border-radius: 18px;
            background-color: #f7f7f9;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
            text-align: center;
            font-weight: 600;
            font-size: 18px;
        }
        .metric-value {
            font-size: 26px;
            font-weight: 700;
            color: #4b8ef5;
        }
        .section-title {
            font-size: 26px !important;
            font-weight: 700 !important;
            color: #333 !important;
            padding-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Title & Instructions
# ----------------------------------------------------
st.title("📊 Premium Budget Analysis Dashboard")
st.write("Upload your **Budget CSV** and explore a clean, modern analysis dashboard.")

# ----------------------------------------------------
# File Upload
# ----------------------------------------------------
uploaded_file = st.file_uploader("📂 Upload Your Budget CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ----------------------------------------------------
    # Data Preview
    # ----------------------------------------------------
    st.markdown("<div class='section-title'>📌 Data Preview</div>", unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    # ----------------------------------------------------
    # Auto Detect Columns
    # ----------------------------------------------------
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    all_columns = df.columns.tolist()

    year_candidates = [c for c in all_columns if "year" in c.lower() or "fy" in c.lower()]
    category_candidates = [
        c for c in all_columns
        if any(word in c.lower() for word in ["category", "sector", "department", "head"])
    ]

    st.sidebar.header("⚙️ Settings")

    year_col = st.sidebar.selectbox("Select Year Column", [None] + year_candidates)
    amount_col = st.sidebar.selectbox("Select Amount Column", numeric_cols)
    category_col = st.sidebar.selectbox("Select Category Column", [None] + category_candidates)

    if not amount_col:
        st.error("❌ No numeric amount column found. Cannot continue.")
        st.stop()

    # ----------------------------------------------------
    # Summary Metrics (Cards)
    # ----------------------------------------------------
    st.markdown("<div class='section-title'>📈 Summary Metrics</div>", unsafe_allow_html=True)

    total_budget = df[amount_col].sum()
    avg_budget = df[amount_col].mean()
    max_budget = df[amount_col].max()
    min_budget = df[amount_col].min()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"<div class='card'>Total Budget<br><span class='metric-value'>{total_budget:,.2f}</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card'>Average Budget<br><span class='metric-value'>{avg_budget:,.2f}</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card'>Highest Value<br><span class='metric-value'>{max_budget:,.2f}</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='card'>Lowest Value<br><span class='metric-value'>{min_budget:,.2f}</span></div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # Year-wise Trend (Streamlit Built-in Chart)
    # ----------------------------------------------------
    if year_col:
        st.markdown("<div class='section-title'>📉 Year-wise Analysis</div>", unsafe_allow_html=True)
        year_df = df.groupby(year_col)[amount_col].sum().reset_index()
        year_df = year_df.sort_values(year_col)
        st.line_chart(year_df, x=year_col, y=amount_col, height=350)
    else:
        st.info("👉 Select a Year Column from sidebar to see trend.")

    # ----------------------------------------------------
    # Category-wise Chart
    # ----------------------------------------------------
    if category_col:
        st.markdown("<div class='section-title'>📊 Category-wise Distribution</div>", unsafe_allow_html=True)
        cat_df = df.groupby(category_col)[amount_col].sum().reset_index()
        cat_df = cat_df.sort_values(amount_col, ascending=False)
        st.bar_chart(cat_df, x=category_col, y=amount_col, height=400)
    else:
        st.info("👉 Select a Category Column from sidebar to see category breakdown.")

    # ----------------------------------------------------
    # Download Cleaned CSV
    # ----------------------------------------------------
    st.markdown("<div class='section-title'>📥 Download Processed Data</div>", unsafe_allow_html=True)

    st.download_button(
        label="📌 Download Cleaned CSV",
        data=df.to_csv(index=False),
        file_name="Processed_Budget_Data.csv",
        mime="text/csv"
    )

else:
    st.info("⬆ Upload a CSV file to begin.")
