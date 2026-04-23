import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import generate_insights

st.set_page_config(page_title="Data Insight Engine", layout="wide")

st.title("📊 Data Insight Engine")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Sidebar
    st.sidebar.title("⚙️ Controls")
    selected_columns = st.sidebar.multiselect(
        "Select columns",
        df.columns,
        default=df.columns
    )

    df = df[selected_columns]

    # Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # Basic Info
    st.subheader("📊 Basic Statistics")
    st.write(df.describe())

    # Missing Values
    st.subheader("⚠️ Missing Values")
    st.write(df.isnull().sum())
    # 🧹 Handle Missing Values
st.subheader("🧹 Data Cleaning")

option = st.selectbox(
    "Choose method to handle missing values",
    ["None", "Drop Rows", "Fill with Mean"]
)

if option == "Drop Rows":
    df = df.dropna()
    st.success("Missing rows dropped!")

elif option == "Fill with Mean":
    df = df.fillna(df.mean(numeric_only=True))
    st.success("Missing values filled with mean!")

    # Visualization
    st.subheader("📈 Visualization")
    column = st.selectbox("Select column", df.columns)

    fig, ax = plt.subplots()

    if df[column].dtype != 'object':
        ax.hist(df[column], bins=20)
        ax.set_title(f"Distribution of {column}")
    else:
        df[column].value_counts().plot(kind='bar', ax=ax)
        ax.set_title(f"Count of {column}")

    st.pyplot(fig)

    # 🔥 Correlation Heatmap
    st.subheader("🔥 Correlation Heatmap")

    numeric_df = df.select_dtypes(include=['number'])

    if not numeric_df.empty:
        corr = numeric_df.corr()

        fig2, ax2 = plt.subplots()
        cax = ax2.matshow(corr)
        plt.colorbar(cax)

        ax2.set_xticks(range(len(corr.columns)))
        ax2.set_yticks(range(len(corr.columns)))

        ax2.set_xticklabels(corr.columns, rotation=90)
        ax2.set_yticklabels(corr.columns)

        st.pyplot(fig2)
    else:
        st.write("No numeric columns available for correlation.")

    # 🧠 Insights
    st.subheader("🧠 Insights")

    insights = generate_insights(df)
    for i in insights:
        st.write("- " + i)

    # 📥 Download Report
    st.subheader("📥 Download Processed Data")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="processed_data.csv",
        mime="text/csv",
    )

else:
    st.info("👆 Upload a CSV file to start")
