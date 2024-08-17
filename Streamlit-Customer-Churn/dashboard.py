import os
import pandas as pd
import streamlit as st
import io
import matplotlib.pyplot as plt

def load_data():
    # Construct file path relative to script
    file_path = os.path.join(os.path.dirname(__file__), 'churn.csv')
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    return df

def about_df(df):
    df_sample = df.sample(10)
    size = df.shape[0]
    buffer = io.StringIO()
    df.info(buf=buffer)
    info = buffer.getvalue()
    columns = df.dtypes
    missing_values = df.isnull().sum()
    stats = df.describe(include='all')

    return df_sample, size, info, columns, missing_values, stats

def customer_statistics(df):
    average_age = df['Age'].mean()
    average_tenure = df['Tenure'].mean()
    total_spend = df['Total Spend'].sum()
    average_support_calls = df['Support Calls'].mean()
    churn_rate = df['Churn'].mean() * 100
    payment_delay_std_dev = df['Payment Delay'].std()

    statistics = {
        'Average Age': average_age,
        'Average Tenure': average_tenure,
        'Total Spend': total_spend,
        'Average Support Calls': average_support_calls,
        'Churn Rate (%)': churn_rate,
        'Payment Delay Std Dev': payment_delay_std_dev
    }

    return statistics

def future_insights(df):
    if df['Churn'].dtype == 'object':
        df['Churn'] = df['Churn'].astype('category').cat.codes
    
    df['Total Spend'] = pd.to_numeric(df['Total Spend'], errors='coerce')
    df['Payment Delay'] = pd.to_numeric(df['Payment Delay'], errors='coerce')

    df = df.dropna(subset=['Churn', 'Total Spend', 'Payment Delay'])
    
    if 'Churn' not in df.columns or df['Churn'].empty:
        st.error("Churn column is missing or empty in the dataset.")
        return
    
    numeric_cols = df.select_dtypes(include='number').columns
    if 'Churn' not in numeric_cols:
        numeric_cols = numeric_cols.append(pd.Index(['Churn']))
    
    churn_prediction = df.groupby('Churn')[numeric_cols].mean()
    st.subheader('Churn Prediction Insights:')
    st.write(churn_prediction)

    st.subheader('Churn vs. Total Spend:')
    fig, ax = plt.subplots()
    try:
        df.boxplot(column='Total Spend', by='Churn', ax=ax)
        plt.title('Churn vs. Total Spend')
        plt.suptitle('')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred during the Total Spend boxplot: {e}")

    st.subheader('Churn vs. Payment Delay:')
    fig, ax = plt.subplots()
    try:
        df.groupby('Churn')['Payment Delay'].mean().plot(kind='bar', ax=ax)
        ax.set_ylabel('Average Payment Delay')
        plt.title('Churn vs. Payment Delay')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred during the Payment Delay bar chart: {e}")

def customer_segmentation(df):
    df['Tenure'] = pd.to_numeric(df['Tenure'], errors='coerce')
    df['Subscription Type'] = df['Subscription Type'].astype('category').cat.codes
    df = df.dropna(subset=['Tenure', 'Subscription Type'])
    numeric_cols = df.select_dtypes(include='number').columns
    if 'Subscription Type' not in numeric_cols or 'Tenure' not in numeric_cols:
        numeric_cols = numeric_cols.append(pd.Index(['Subscription Type', 'Tenure']))

    try:
        segmentation = df.groupby(['Subscription Type', 'Tenure'])[numeric_cols].mean()
        st.subheader('Customer Segmentation Based on Subscription Type and Tenure:')
        st.write(segmentation)
    except Exception as e:
        st.error(f"An error occurred during segmentation: {e}")

    st.subheader('Subscription Type Distribution:')
    fig, ax = plt.subplots()
    try:
        df['Subscription Type'].value_counts().plot(kind='bar', ax=ax)
        plt.title('Subscription Type Distribution')
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred during the Subscription Type Distribution plot: {e}")

if __name__ == "__main__":
    st.title("Customer Churn Dashboard")
    st.subheader("Data Analysis and Customer Insights")
    st.write("----------------------------------------------------------------------------------------")

    # Load dataset
    try:
        df = load_data()
        st.success("Dataset successfully loaded!")
    except FileNotFoundError as e:
        st.error(f"Error loading dataset: {e}")
        df = None

    if df is not None and not df.empty:
        if st.sidebar.button("About Dataset"):
            st.subheader("About Dataset")
            df_sample, size, info, columns, missing_values, stats = about_df(df)

            st.subheader('DataFrame Sample:')
            st.write(df_sample)

            st.subheader('DataFrame Size:')
            st.write(size)

            st.subheader('DataFrame Info:')
            st.text(info)

            st.subheader('Column Names and Types:')
            st.write(columns)

            st.subheader('Missing Values:')
            st.write(missing_values)

            st.subheader('Statistics:')
            st.write(stats)

        if st.sidebar.button("Customer Statistics"):
            st.subheader("Customer Statistics")
            customer_stats = customer_statistics(df)
            for key, value in customer_stats.items():
                st.write(f'{key}: {round(value, 2)}')

        if st.sidebar.button("Future Insights"):
            st.subheader("Future Insights Based on Existing Data")
            future_insights(df)

        if st.sidebar.button("Customer Segmentation"):
            st.subheader("Customer Segmentation Insights")
            customer_segmentation(df)
    else:
        st.warning("Please upload a dataset to proceed.")
