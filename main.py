from typing import List, Tuple
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from math import sin, cos, sqrt, atan2, radians
import sqlite3

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect("addresses.db")
c = conn.cursor()

# Create addresses table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS addresses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              street TEXT NOT NULL,
              city TEXT NOT NULL,
              state TEXT NOT NULL,
              zip TEXT NOT NULL,
              latitude REAL NOT NULL,
              longitude REAL NOT NULL)''')
conn.commit()

# Constants for calculating distances
EARTH_RADIUS = 6371  # km
MILES_TO_KM = 1.60934


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    latitude: float
    longitude: float

    @validator('zip')
    def validate_zip(cls, v):
        if len(v) != 5:
            raise ValueError('Zip code must be 5 digits')
        return v

    @validator('latitude', 'longitude')
    def validate_coordinates(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Invalid latitude or longitude')
        return v


@app.post("/addresses")
def create_address(address: Address):
    # Insert address into database
    c.execute("INSERT INTO addresses (street, city, state, zip, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
              (address.street, address.city, address.state, address.zip, address.latitude, address.longitude))
    conn.commit()
    return {'message': 'Address created successfully'}


@app.put("/addresses/{address_id}")
def update_address(address_id: int, address: Address):
    # Update address in database
    c.execute("UPDATE addresses SET street=?, city=?, state=?, zip=?, latitude=?, longitude=? WHERE id=?",
              (address.street, address.city, address.state, address.zip, address.latitude, address.longitude, address_id))
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    conn.commit()
    return {'message': 'Address updated successfully'}


@app.delete("/addresses/{address_id}")
def delete_address(address_id: int):
    # Delete address from database
    c.execute("DELETE FROM addresses WHERE id=?", (address_id,))
    if c.rowcount == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    conn.commit()
    return {'message': 'Address deleted successfully'}


@app.get("/addresses")
def get_addresses(latitude: float, longitude: float, radius: float) -> List[Tuple[int, str, str, str, str, float, float]]:
    # Retrieve addresses within given radius and location
    lat1 = radians(latitude)
    lon1 = radians(longitude)

    addresses = []
    for row in c.execute("SELECT * FROM addresses"):
        lat2 = radians(row[5])
        lon2 = radians(row[6])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = EARTH_RADIUS * c * MILES_TO_KM  # Convert to km
        if distance <= radius:
            addresses
