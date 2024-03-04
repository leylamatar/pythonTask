from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI()


access_token = ""

url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Request successful")
    data = response.json()
    print(data)
else:
    print("Request failed:", response.status_code)
    print(response.text)

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