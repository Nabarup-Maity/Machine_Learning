# Example usage: Handle errors
def handle_errors(data, column_name, group_by_attributes, date_range, analysis_type):
    if column_name not in data.columns:
        print(f"Column '{column_name}' not found in the dataset.")
    elif analysis_type == "groupby" and not group_by_attributes:
        print("Group-by attributes not specified.")
    elif analysis_type == "moving average" and column_name not in data.columns:
        print(f"Column '{column_name}' not found in the dataset for moving average.")
    elif analysis_type not in ["missing value percentage", "groupby", "moving average"]:
        print("Invalid analysis type.")
    else:
        # Call the process_query function with valid inputs
        process_query(data, column_name, group_by_attributes, date_range, analysis_type)

# Example usage
handle_errors(data, column_name, group_by_attributes, date_range, analysis_type)
