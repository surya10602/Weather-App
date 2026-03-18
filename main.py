from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import requests
import csv
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv # Add this import

# Load environment variables from the .env file
load_dotenv() 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "weather_app.db"

# Pull the API key securely from the environment
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_records
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, location TEXT, temperature REAL, date_logged TEXT)''')
    conn.commit()
    conn.close()

init_db()

# CREATE & READ API Call (Current Weather)
@app.post("/weather/")
def create_weather_record(location: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")
        
    data = response.json()
    temp = data['main']['temp']
    icon_code = data['weather'][0]['icon']
    description = data['weather'][0]['description'].title()
    
    # Store information into the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weather_records (location, temperature, date_logged) VALUES (?, ?, date('now'))", (location, temp))
    conn.commit()
    conn.close()
    
    return {
        "location": location, 
        "temperature": temp, 
        "description": description,
        "icon": icon_code,
        "message": "Record created"
    }

# GET 5-Day Forecast
@app.get("/forecast/")
def get_forecast(location: str):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Forecast not found")
        
    data = response.json()
    daily_forecasts = []
    
    # Filter for 1 reading per day (at noon)
    for item in data['list']:
        if "12:00:00" in item['dt_txt']:
            daily_forecasts.append({
                "date": item['dt_txt'].split(" ")[0],
                "temperature": item['main']['temp'],
                "description": item['weather'][0]['description'].title(),
                "icon": item['weather'][0]['icon']
            })
            
    return {"location": location, "forecast": daily_forecasts}

# READ All Database Records
@app.get("/records/")
def read_records():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_records")
    records = cursor.fetchall()
    conn.close()
    return records

# UPDATE Database Record
@app.put("/records/{record_id}")
def update_record(record_id: int, new_temp: float):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE weather_records SET temperature = ? WHERE id = ?", (new_temp, record_id))
    conn.commit()
    conn.close()
    return {"message": "Record updated"}

# DELETE Database Record
@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather_records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return {"message": "Record deleted"}

# EXPORT Data to CSV
@app.get("/export/csv")
def export_csv():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_records")
    records = cursor.fetchall()
    conn.close()
    
    with open("export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Location", "Temperature", "Date"])
        writer.writerows(records)
        
    return FileResponse("export.csv", media_type="text/csv", filename="weather_data.csv")