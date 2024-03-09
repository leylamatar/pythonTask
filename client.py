import io
import requests
import csv
import pandas as pd
from datetime import datetime, timedelta

def send_csv_to_server(csv_file, keys=None, colored=True):
    with open(csv_file, 'rb') as file:
        csv_content = file.read().decode("utf-8")

    params = {"colored": colored}
    if keys:
        params["keys"] = keys

    response = requests.post("http://127.0.0.1:8000/vehicle_info/", params=params, files={"csv_file": io.StringIO(csv_content)})

    if response.status_code == 200:
        #save the CSV content
        csv_content = response.text.splitlines()
        df = pd.read_csv(io.StringIO("\n".join(csv_content)), header=None)  

        # Rows are sorted by response field 
        df = df.sort_values(by=0) 
        # Columns always contain rnr field
        if 'rnr' not in df.columns:
            df.insert(0, 'rnr', None)
        # Save as Excel file
        current_date_iso_formatted = datetime.now().strftime("%Y-%m-%d")
        excel_filename = f'vehicles_{current_date_iso_formatted}.xlsx'
        df.to_excel(excel_filename, index=False)

        return excel_filename
    else:
        print("Error:", response.text)
        return None
    


def color_dataframe(df):
    # 'hu' color
    today = datetime.now()
    three_months_ago = today - timedelta(days=3*30)
    twelve_months_ago = today - timedelta(days=12*30)

    df['color'] = ''
    df.loc[df['hu'] >= three_months_ago, 'color'] = '#007500'  # green
    df.loc[(df['hu'] >= twelve_months_ago) & (df['hu'] < three_months_ago), 'color'] = '#FFA500'  # orange
    df.loc[df['hu'] < twelve_months_ago, 'color'] = '#b30000'  # red

    return df


if __name__ == "__main__":
    #change the the file name and keys (optional)
    csv_file_path = "vehicles.csv"
    keys = ["kurzname", "info"]
    colored = True
    excel_filename = send_csv_to_server(csv_file_path, keys=keys, colored=colored)
    if excel_filename:
        print(f"Excel file created: {excel_filename}")
    else:
        print("Failed to generate Excel file.")
