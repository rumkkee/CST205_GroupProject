import requests

data = requests.get("/api/alt-fuel-stations/v1/nearest.json?api_key=DEMO_KEY&location=1617+Cole+Blvd+Golden+CO&fuel_type=ELEC&limit=1")
print(data)

data = data.json()
print(data)