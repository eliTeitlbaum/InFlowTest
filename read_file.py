import pandas as pd
from os import path
from data_validator import *


def load_excel_file():
    while True:
        file_path = input("please enter the file path (with .xlsx extension): ")
        file_path = file_path.replace('"', "").replace("'", "")

        if not path.isfile(file_path):
            print("file not found. please try again: ")
            continue

        try:
            excel_data = pd.read_excel(file_path, sheet_name=None)

            return excel_data

        except Exception as e:
            print("invalid file. please try again:")
            print("Error : ", e)


def convert_pd_to_dict(df, index_col):

    return df.set_index(index_col).to_dict(orient="index")


def insert_and_check_data(sheet, data: dict):
    for key, data_sheet in data.items():
        if validate_id(key) and check_data(data_sheet):

            ...
        else:
            print(f"Error check in {key} - {data}")


def organise_data(data: dict):
    sheet_dict = {
        "departments": "department_id",
        "workers": "worker_id",
        "candidates": "candidate_id",
        "candidate_enrollment": "candidates_id"
    }

    iterator = iter(sheet_dict.items())

    for sheet, index in iterator:
        data_sheet = convert_pd_to_dict(data.get(sheet, pd.DataFrame()), index)

        if sheet == "candidates":
            sheet2, index = next(iterator, (None, None))
            data_sheet_2 = convert_pd_to_dict(data.get(sheet2, pd.DataFrame()), index)

            data_sheet = {
                key: {**data_sheet[key], **data_sheet_2[key]}
                for key in data_sheet if key in data_sheet_2
            }

        insert_and_check_data(sheet=sheet, data=data_sheet)


def main():
    excel_data = load_excel_file()

    if excel_data:
        organise_data(data=excel_data)


if __name__ == "__main__":
    main()
