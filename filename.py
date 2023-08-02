# Import necessary libraries
import re
import streamlit as st
import pandas as pd
from transformers import pipeline

# Define the rules and synonyms
rules = {
    'columns': ['column', 'attribute', 'feature'],
    'missing_value': ['missing value percentage', 'incomplete', 'missing data', 'NaN values', 'empty values'],
    'groupby': ['group by', 'grouped by', 'categorized by', 'aggregated by'],
    'trends_charts': ['trend', 'trend analysis', 'trend chart', 'pattern', 'pattern analysis'],
    'moving_average': ['moving average', 'smoothed average', 'rolling average'],
    'max': ['most frequent', 'max', 'maximum', 'most common', 'top'],
    'min': ['least frequent', 'min', 'minimum', 'least common', 'lowest'],
    'average': ['average', 'mean', 'average value', 'mean value', 'typical value'],
    'sum': ['sum', 'total', 'summation', 'add up'],
    'summary': ['describe', 'summary', 'overview', 'summary statistics'],
    # Add more rules and synonyms here
}

# Load the CSV or Excel file
def load_data(file_path):
    data = pd.read_csv(file_path, )  # or pd.read_excel(file_path) for Excel
    return data

# Get a sample overview of the dataset
def get_sample_overview(data):
    sample = data.head(5)  # Change the number to adjust the sample size
    return sample

def parse_query(query):
    analysis = None
    columns = []

    for rule, synonyms in rules.items():
        for synonym in synonyms:
            if synonym in query:
                analysis = rule
                break

    # Extract column names using regex
    columns_match = re.findall(r'\b(?:column|attribute|feature)\s+(\w+)\b', query)
    columns.extend(columns_match)

    return analysis, columns


# Get a list of columns from the dataset
def get_column_list(data):
    return data.columns.tolist()

# Filter data by city name
def filter_data_by_column_value(data, column_name, value):
    return data[data[column_name] == value]

# Calculate the average salary
def calculate_average(data, column_name):
    return data[column_name].mean()

# Calculate the sum of a column
def calculate_sum(data, column_name):
    return data[column_name].sum()

# Generate a histogram of a column
def generate_histogram(data, column_name):
    plt.figure(figsize=(8, 6))
    plt.hist(data[column_name], bins=20, edgecolor='k')
    plt.xlabel(column_name)
    plt.ylabel('Count')
    plt.title(f'Histogram of {column_name}')
    st.pyplot(plt)


# Functions for each analysis type
def analyze_missing_value(df, columns):
    for column in columns:
        missing_percentage = (df[column].isnull().sum() / len(df)) * 100
        print(f"Missing value percentage for {column}: {missing_percentage:.2f}%")
        st.text(f"Missing value percentage for {column}: {missing_percentage:.2f}%")




# Streamlit web application
def main():
    st.title("CSV/Excel Data Analyzer")

    # File upload
    file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if file is not None:
        data = load_data(file)
        # Sidebar to show list of columns
        st.sidebar.title("List of Columns")
        column_list = get_column_list(data)
        selected_column = st.sidebar.selectbox("Select a column", column_list)

        st.write("Sample Overview:")
        sample_overview = get_sample_overview(data)
        st.write(sample_overview)

        query_text = st.text_input("Enter your analysis request:")

        # Parse the query
        analysis, columns = parse_query(query_text)
        st.text(analysis)
        st.text(columns)
        
        # Perform the requested analysis
        if analysis == 'missing_value':
            analyze_missing_value(data, columns)
        elif analysis == 'groupby':
            analyze_groupby_trends(data, columns)
        elif analysis == 'moving_average':
            analyze_moving_average(data, columns)
        elif analysis == 'max':
            analyze_most_frequent(data, columns)
        elif analysis == 'summary':
            analyze_summary(data, columns)

if __name__ == "__main__":
    main()
