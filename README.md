# Weather App

## Overview
This is a Full Stack Weather Application that accepts user location input to retrieve real-time weather data, a 5-day forecast, and interactive map data. It also features a backend that handles data persistence with full CRUD capabilities and data export.

## Technologies Used
* **Backend:** Python, FastAPI, SQLite
* **Frontend:** HTML, CSS, Vanilla JavaScript
* **APIs:** OpenWeatherMap API, Google Maps Embed API

## Features Implemented
* **Core Requirements:**
  * Real-time location-based weather retrieval.
  * Backend data persistence using an SQLite database.
  * Full CRUD (Create, Read, Update, Delete) endpoints via FastAPI.
  * Graceful frontend and backend error handling for invalid locations.
  * Adaptable, responsive design for desktop and mobile.
* **"Stand Apart" Features:**
  * 5-Day Forecast displayed in a clean, organized horizontal grid.
  * Additional API Integration: Interactive Google Maps embed based on user location.
  * Data Export: Endpoint to export database records to a CSV file.

## Setup & Run Instructions
1. Clone this repository to your local machine.
2. Ensure you have Python installed. Install the backend dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
3. API Key Setup: This project uses environment variables to secure API keys.
  - Create a file named `.env` in the root directory of the project.
  - Add your OpenWeatherMap API key to the file like this:
    ```bash
    WEATHER_API_KEY=your_actual_api_key_here
    ```
4. Start the backend server by running:
   ```bash
   uvicorn main:app --reload
   ```
5. Open `index.html` in any modern web browser to view and interact with the application.
