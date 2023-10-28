import os
import pandas as pd

def convert_to_csv(filename, data_list):
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    file_name = os.path.join(download_path, f"{filename}.csv")

    df = pd.DataFrame(data_list)

    # Save the DataFrame to a CSV file
    df.to_csv(file_name, index=False)

    return file_name
