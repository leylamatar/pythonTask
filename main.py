from fastapi import FastAPI, HTTPException, Response
import csv
import requests
from io import StringIO
import uvicorn

app = FastAPI()

def get_vehicle_info(access_token):
    vehicle_url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    vehicle_headers = {"Authorization": f"Bearer {access_token}"}
    vehicle_response = requests.get(vehicle_url, headers=vehicle_headers)
    
    if vehicle_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch vehicle information")
    
    return vehicle_response.json()

#return api data to csv file and downloads it
def convert_to_csv(vehicle_info):
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    
    csv_writer.writerow(vehicle_info[0].keys())
    for vehicle in vehicle_info:
        csv_writer.writerow(vehicle.values())
    

    return csv_data.getvalue()

@app.get("/vehicle_info/csv/")
async def get_vehicle_info_csv():
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
    csv_data = convert_to_csv(vehicle_info)
    
    # Return the CSV file as a downloadable attachment
    return Response(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=vehicle_info.csv"})

if __name__ == "__main__":
    
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