from fastapi import FastAPI, HTTPException, Response
import csv
import requests
import pandas as pd
from datetime import datetime

app = FastAPI()

def get_vehicle_info(access_token):
    vehicle_url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    vehicle_headers = {"Authorization": f"Bearer {access_token}"}
    vehicle_response = requests.get(vehicle_url, headers=vehicle_headers)
    
    if vehicle_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch vehicle information")
    
    return vehicle_response.json()

def convert_to_excel(vehicle_info):
    df = pd.DataFrame(vehicle_info)
    current_date_iso_formatted = datetime.now().strftime("%Y-%m-%d")
    filename = f'vehicles_{current_date_iso_formatted}.xlsx'
    df.to_excel(filename, index=False)
    return filename

@app.get("/vehicle_info/")
async def get_vehicle_info_data():
    url = "https://api.baubuddy.de/index.php/login"
    payload = {
        "username": "365",
        "password": "1"
    }
    headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to authenticate")
    
    access_token = response.json().get("oauth", {}).get("access_token")
    
    vehicle_info = get_vehicle_info(access_token)
    excel_file = convert_to_excel(vehicle_info)
    
    try:
        with open(excel_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read Excel file: {str(e)}")
    #Failed to read Excel file: 'utf-8' codec can't decode byte 0xf8 in position 14: invalid start byte"
    return {
        "excel_file": Response(content=file_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={excel_file}"}),
        "json_data": vehicle_info
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



######TO GET TOKEN 
# url = "https://api.baubuddy.de/index.php/login"
# payload = {
#     "username": "",
#     "password": ""
# }
# headers = {
#     "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
#     "Content-Type": "application/json"
# }
# response = requests.request("POST", url, json=payload, headers=headers)
# print(response.text)