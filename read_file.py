import pandas as pd
from os import path
from data_validator import *
from connectMySql import DbManager
import database_queries


# Function to load the Excel file
def load_excel_file():
    while True:
        # Prompt user for file path and clean it
        file_path = input("please enter the file path (with .xlsx extension): ")
        file_path = file_path.replace('"', "").replace("'", "")

        # Check if the file exists
        if not path.isfile(file_path):
            print("file not found. please try again: ")
            continue

        try:
            # Read the Excel file with multiple sheets
            excel_data = pd.read_excel(file_path, sheet_name=None)

            return excel_data

        except Exception as e:
            # If there's an error reading the file, prompt the user to try again
            print("invalid file. please try again:")
            print("Error : ", e)


# Convert pandas dataframe to dictionary with a specific index column
def convert_pd_to_dict(df, index_col):
    return df.set_index(index_col).to_dict(orient="index")


# Insert data into the database and perform validation
def insert_and_check_data(sheet, data: dict):
    db = DbManager()  # Initialize database connection

    try:
        # Iterate through the data dictionary
        for key, data_sheet in data.items():
            # Validate the data before inserting
            if validate_id(key) and check_data(data_sheet):

                # Insert data into appropriate table based on the sheet type
                if sheet == "departments":
                    database_queries.insert_new_departments(
                        insert=db.insert, name=data_sheet["department_name"], id_departments=key
                    )

                elif sheet == "workers":
                    database_queries.insert_new_worker(
                        insert=db.insert, fn=data_sheet["first_name"], ln=data_sheet["last_name"],
                        department_id=data_sheet["department_id"], worker_id=key
                    )

                elif sheet == "candidates":
                    database_queries.insert_new_candidates(
                        insert=db.insert, fn=data_sheet["first_name"], ln=data_sheet["last_name"],
                        enrollment_id=data_sheet["enrollment_id"], candidate_id=key,
                        enrolled_ts=data_sheet["enrolled_ts"], enrollment_ts=data_sheet["enrollment_ts"],
                        job_id=data_sheet["job_id"], worker_id=data_sheet["worker_id"]
                    )

            else:
                print(f"Error check in {key} - {data}")

    finally:
        # Close the database connection
        db.close()


# Organize and clean the data before inserting into the database
def organise_data(data: dict):
    # Define sheet names and corresponding index columns
    sheet_dict = {
        "departments": "department_id",
        "workers": "worker_id",
        "candidates": "candidate_id",
        "candidate_enrollment": "candidates_id"
    }

    iterator = iter(sheet_dict.items())  # Create an iterator for sheet names

    # Iterate through sheets and process them
    for sheet, index in iterator:
        # Get the sheet data and clean null values
        data_sheet2 = data.get(sheet, pd.DataFrame())
        data_sheet3 = data_sheet2.applymap(lambda x: None if (pd.isna(x) or pd.isnull(x)) else x)
        data_sheet = convert_pd_to_dict(data_sheet3, index)

        # If it's the candidates sheet, merge it with the next sheet (candidate_enrollment)
        if sheet == "candidates":
            sheet2, index = next(iterator, (None, None))
            data_sheet2 = data.get(sheet2, pd.DataFrame())
            data_sheet3 = data_sheet2.applymap(lambda x: None if (pd.isna(x) or pd.isnull(x)) else x)
            data_sheet_2 = convert_pd_to_dict(data_sheet3, index)

            # Merge data from both sheets
            data_sheet = {
                key: {**data_sheet[key], **data_sheet_2[key]}
                for key in data_sheet if key in data_sheet_2
            }

        # Insert the data into the database
        insert_and_check_data(sheet=sheet, data=data_sheet)


# Main function to drive the workflow
def main():
    # Load the Excel data
    excel_data = load_excel_file()

    # If data is loaded, process and insert it into the database
    if excel_data:
        organise_data(data=excel_data)


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
