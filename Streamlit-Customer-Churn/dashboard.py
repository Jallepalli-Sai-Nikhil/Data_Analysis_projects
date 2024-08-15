import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Custom functions===========================================================================
def about_df(df):
    # Ensure that we don't sample more rows than are available in the DataFrame
    sample_size = min(len(df), 10)
    
    # Sample view
    df_sample = df.sample(sample_size)
    
    # Get size
    size = df.shape[0]
    
    # Get DataFrame info
    info = df.info()
    
    # Get column names
    columns = df.columns
    
    # Count missing values
    missing_values = df.isnull().sum()
    
    # Get basic statistics
    stats = df.describe()

    return df_sample, size, info, columns, missing_values, stats


# customer statistic function=========================================================================
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


# future insights===========================================================================
def future_insights(df):
    average_monthly_spend = df['Total Spend'].mean()
    projected_total_spend_next_year = average_monthly_spend * 12 * len(df)

    churn_rate = df['Churn'].mean()
    projected_churn_next_year = churn_rate * len(df)

    average_support_calls = df['Support Calls'].mean()
    projected_support_calls_increase = average_support_calls * 1.1  # Assuming a 10% increase

    average_payment_delay = df['Payment Delay'].mean()
    projected_payment_delay_increase = average_payment_delay * 1.05  # Assuming a 5% increase

    standard_and_basic_users = df[df['Subscription Type'].isin(['Standard', 'Basic'])]
    projected_upgrades = len(standard_and_basic_users) * 0.15  # Assuming 15% might upgrade

    average_tenure = df['Tenure'].mean()
    projected_tenure_growth = average_tenure * 1.2  # Assuming a 20% improvement in retention

    insights = {
        'Projected Total Spend Next Year': projected_total_spend_next_year,
        'Projected Churn Next Year': projected_churn_next_year,
        'Projected Support Calls Increase': projected_support_calls_increase,
        'Projected Payment Delay Increase': projected_payment_delay_increase,
        'Projected Subscription Upgrades': projected_upgrades,
        'Projected Tenure Growth': projected_tenure_growth
    }

    return insights


# Dashboard functions (graphs)=========================================================================
def age_distribution_graph(df):
    fig, ax = plt.subplots()
    df['Age'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title('Distribution of Age')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    return fig


def avg_total_spend_subscription_type(df):
    fig, ax = plt.subplots()
    df.groupby('Subscription Type')['Total Spend'].mean().plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title('Average Total Spend by Subscription Type')
    ax.set_xlabel('Subscription Type')
    ax.set_ylabel('Average Total Spend')
    return fig


def gender_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df['Gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Gender Distribution')
    ax.set_ylabel('')
    return fig


def total_spend_distribution_by_contract_length(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby('Contract Length')['Total Spend'].sum().plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'], ax=ax)
    ax.set_title('Total Spend Distribution by Contract Length')
    ax.set_ylabel('')
    return fig


def churn_rate_by_gender(df):
    fig, ax = plt.subplots()
    churn_rate_by_gender = df.groupby('Gender')['Churn'].mean() * 100
    churn_rate_by_gender.plot(kind='bar', color='coral', ax=ax)
    ax.set_title('Churn Rate by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Churn Rate (%)')
    return fig


def age_distribution_by_gender(df):
    fig, ax = plt.subplots()
    df[df['Gender'] == 'Male']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='blue', label='Male', ax=ax)
    df[df['Gender'] == 'Female']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='red', label='Female', ax=ax)
    ax.set_title('Age Distribution by Gender')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    ax.legend()
    return fig


# Main app===========================================================================
if __name__ == "__main__":
    # Set up the Streamlit page
    st.title("Customer Churn Dashboard")
    st.subheader("Data Analysis and Customer Insights")
    st.write("----------------------------------------------------------------------------------------")

    # Sidebar for data upload and dataset selection
    st.sidebar.title("Customer Analysis")

    # Download sample dataset button
    if st.sidebar.button("Download Sample Dataset"):
        # Create a sample dataset
        data = {
            'Age': [22, 45, 32, 41, 36],
            'Gender': ['Male', 'Female', 'Female', 'Male', 'Male'],
            'Tenure': [2, 5, 3, 7, 1],
            'Support Calls': [1, 2, 0, 3, 1],
            'Total Spend': [500, 1200, 700, 1500, 400],
            'Payment Delay': [5, 10, 0, 7, 3],
            'Subscription Type': ['Basic', 'Standard', 'Basic', 'Premium', 'Basic'],
            'Contract Length': [12, 24, 12, 36, 6],
            'Churn': [0, 0, 1, 0, 1]
        }
        sample_df = pd.DataFrame(data)
        
        # Allow the user to download the dataset as CSV
        csv = sample_df.to_csv(index=False)
        st.sidebar.download_button(label="Download CSV", data=csv, file_name='sample_dataset.csv', mime='text/csv')

    # File uploader for custom dataset
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

    df = pd.DataFrame()

    # Load dataset based on user input
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Dataset successfully loaded!")
    else:
        st.warning("Please upload a dataset or download the sample dataset to proceed.")
    
    # Data analysis options once the dataset is available
    if not df.empty:
        # About dataset
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

        # Customer statistics
        if st.sidebar.button("Customer Statistics"):
            st.subheader("Customer Statistics")
            customer_stats = customer_statistics(df)
            for key, value in customer_stats.items():
                st.write(f'{key}: {round(value, 2)}')

        # Future insights
        if st.sidebar.button("Future Insights"):
            st.subheader("Future Insights")
            future_stats = future_insights(df)
            for key, value in future_stats.items():
                st.write(f'{key}: {round(value, 2)}')

        # Dashboard with visualizations
        if st.sidebar.button("Dashboard"):
            st.subheader("Customer Dashboard")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Age Distribution")
                fig = age_distribution_graph(df)
                st.pyplot(fig)
            with col2:
                st.subheader("Avg Spend by Subscription Type")
                fig = avg_total_spend_subscription_type(df)
                st.pyplot(fig)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Gender Distribution")
                fig = gender_distribution(df)
                st.pyplot(fig)
            with col2:
                st.subheader("Total Spend by Contract Length")
                fig = total_spend_distribution_by_contract_length(df)
                st.pyplot(fig)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Churn Rate by Gender")
                fig = churn_rate_by_gender(df)
                st.pyplot(fig)
            with col2:
                st.subheader("Age Distribution by Gender")
                fig = age_distribution_by_gender(df)
                st.pyplot(fig)
