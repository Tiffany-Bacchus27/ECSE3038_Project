from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests
import re

app = FastAPI()

settings = {}
sensor_data = []

class Settings(BaseModel):
    user_temp: float
    user_light: str
    light_duration: str

class SensorData(BaseModel):
    temperature: float
    presence: bool

regex = re.compile(r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')

def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return None
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

def get_sunset_time():
    response = requests.get("https://api.sunrise-sunset.org/json?lat=40.7128&lng=-74.0060&date=today")
    data = response.json()
    return data["results"]["sunset"]

@app.put("/settings")
async def update_settings(settings_data: Settings):
    user_light = settings_data.user_light
    if user_light == "sunset":
        user_light = get_sunset_time()

    duration = parse_time(settings_data.light_duration)
    if not duration:
        return {"error": "Invalid duration format"}

    light_time = datetime.strptime(user_light, "%H:%M:%S")
    light_time_off = (light_time + duration).strftime("%H:%M:%S")

    settings.update({
        "_id": "1",
        "user_temp": settings_data.user_temp,
        "user_light": user_light,
        "light_time_off": light_time_off
    })
    return settings

@app.post("/sensors")
async def receive_sensor_data(data: SensorData):
    sensor_entry = {
        "temperature": data.temperature,
        "presence": data.presence,
        "datetime": datetime.now().isoformat()
    }
    sensor_data.append(sensor_entry)

    current_time = datetime.now().time().strftime("%H:%M:%S")
    fan_on = False
    light_on = False

    if settings:
        if data.temperature > settings["user_temp"] and data.presence:
            fan_on = True
        light_start = datetime.strptime(settings["user_light"], "%H:%M:%S").time()
        light_end = datetime.strptime(settings["light_time_off"], "%H:%M:%S").time()
        current = datetime.strptime(current_time, "%H:%M:%S").time()
        if light_start <= current <= light_end and data.presence:
            light_on = True

    return {"fan": fan_on, "light": light_on}

@app.get("/graph")
async def get_graph_data(size: int = Query(...)):
    return sensor_data[-size:] if size <= len(sensor_data) else sensor_data