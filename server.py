import csv
import json
from fastapi import FastAPI, Response, UploadFile, File, HTTPException, Query
import requests
import pandas as pd
import uvicorn

app = FastAPI()

def get_vehicle_info(access_token):
    vehicle_url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    vehicle_headers = {"Authorization": f"Bearer {access_token}"}
    vehicle_response = requests.get(vehicle_url, headers=vehicle_headers)
    
    if vehicle_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch vehicle information")
    
    return vehicle_response.json()

def resolve_color_code(label_id):
    label_url = f"https://api.baubuddy.de/dev/index.php/v1/labels/{label_id}"
    label_response = requests.get(label_url)
    
    if label_response.status_code != 200:
        return "blue"
    
    label_info = label_response.json()
    return label_info.get("colorCode", "blue")  # return colorCode as default


@app.post("/vehicle_info/")
async def post_vehicle_info(csv_file: UploadFile = File(...)):
   # read file content
    csv_content = await csv_file.read()
    csv_reader = csv.DictReader(csv_content.decode("utf-8").splitlines())

    # Filter out any resources that do not have a value set for hu field
    vehicle_info = [row for row in csv_reader if row.get("hu") is None]

    return {
        "original_data": vehicle_info,
    }



@app.get("/vehicle_info/")
async def get_vehicle_info_data(colored: bool = Query(True, description="Flag to resolve color codes for labelIds")):
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
    
    if colored:
        # For each labelId in the vehicle's JSON array labelIds resolve its colorCode
        for vehicle in vehicle_info:
            label_ids = vehicle.get("labelIds")
            if label_ids is not None:
                vehicle.setdefault("labelColors", [])
                for label_id in label_ids:
                    color_code = resolve_color_code(label_id)
                    vehicle["labelColors"].append(color_code)


    # Filter out any resources that do not have a value set for hu field
    #filtered_vehicle_info = [vehicle for vehicle in vehicle_info if vehicle.get("hu") is None]
                    

    # return data in JSON format
    return {
        "original_data2": vehicle_info,
        #"filtered-data":filtered_vehicle_info
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
