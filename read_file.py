import pandas as pd
from os import path


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


def main():
    excel_data = load_excel_file()

    if excel_data:
        # organise_data(data=excel_data)

        department_dict = convert_pd_to_dict(excel_data.get("departments", pd.DataFrame()), "department_id")
        workers_dict = convert_pd_to_dict(excel_data.get("workers", pd.DataFrame()), "worker_id")
        candidates_dict = convert_pd_to_dict(excel_data.get("candidates", pd.DataFrame()), "candidate_id")
        candidate_enrollment_dict = convert_pd_to_dict(excel_data.get("candidate_enrollment", pd.DataFrame()),
                                                       "candidates_id")

        candidates_merged = {
            key: {**candidates_dict[key], **candidate_enrollment_dict[key]}
            for key in candidates_dict if key in candidate_enrollment_dict
        }

        print(department_dict)


def organise_data(data: dict):
    for sheet, df in data.items():
        ...


if __name__ == "__main__":
    main()
