# TravelAssistant

## Overview
TravelAssistant is a Python-based application that provides hotel and flight suggestions for travel planning. It uses the `FastMCP` framework to create a service that generates realistic, mock travel data based on user inputs such as location, check-in/check-out dates for hotels, and departure/return dates for flights. The application is designed to simulate a travel assistant service, generating fake but plausible hotel and flight information for demonstration purposes.

## Features
- **Hotel Suggestions**: Provides a list of hotels in a specified location with details such as name, address, rating, price per night, amenities, and availability.
- **Flight Suggestions**: Generates flight options between two locations, including details like airline, flight number, departure/arrival times, duration, price, and cabin class.
- **Input Validation**: Validates date inputs in ISO format (YYYY-MM-DD) and ensures logical constraints (e.g., check-out date must be after check-in date).
- **Randomized Data**: Uses predefined datasets and randomization to create realistic hotel names, addresses, airport codes, and flight details.
- **Error Handling**: Returns meaningful error messages for invalid inputs or unexpected issues.

## Requirements
- Python 3.8+
- Dependencies:
  - `pydantic` for data validation
  - `FastMCP` (custom framework for creating the service)
- Standard Python libraries: `random`, `re`, `uuid`, `datetime`, `typing`

## Installation
1. Clone the repository or download the source code:
   ```bash
   git clone <repository-url>
   cd travel-assistant
   ```
2. Install the required dependencies:
   ```bash
   pip install pydantic
   ```
   Note: `FastMCP` is assumed to be a custom or external dependency. Ensure it is available in your environment or install it as per its documentation.
3. Run the application:
   ```bash
   python travel_assistant.py
   ```

## Usage
The application exposes two main tools via the `FastMCP` framework:

### 1. `suggest_hotels`
Suggests hotels based on the provided location and check-in/check-out dates.

**Parameters**:
- `location` (str): City or area to search for hotels (e.g., "New York").
- `check_in` (str): Check-in date in ISO format (YYYY-MM-DD).
- `check_out` (str): Check-out date in ISO format (YYYY-MM-DD).

**Example Call**:
```python
result = await suggest_hotels(location="New York", check_in="2025-07-01", check_out="2025-07-05")
```

**Example Response**:
```json
{
  "hotels": [
    {
      "name": "Grand Hotel",
      "address": "1234 Main Street",
      "location": "Downtown, New York",
      "rating": 4.8,
      "price_per_night": 320,
      "hotel_type": "Luxury",
      "amenities": ["Free WiFi", "Spa & Wellness Center", "Restaurant", "Concierge Service"],
      "available_rooms": 5,
      "phone": "+1-555-123-4567",
      "check_in_time": "15:00",
      "check_out_time": "11:00"
    },
    ...
  ],
  "total_found": 4
}
```

### 2. `suggest_flights`
Suggests flights based on departure and destination locations, departure date, and an optional return date.

**Parameters**:
- `from_location` (str): Departure city or airport (e.g., "New York").
- `to_location` (str): Destination city or airport (e.g., "Los Angeles").
- `departure_date` (str): Departure date in ISO format (YYYY-MM-DD).
- `return_date` (str, optional): Return date in ISO format (YYYY-MM-DD) for round-trip flights.

**Example Call**:
```python
result = await suggest_flights(
    from_location="New York",
    to_location="Los Angeles",
    departure_date="2025-07-01",
    return_date="2025-07-07"
)
```

**Example Response**:
```json
{
  "departure_flights": [
    {
      "flight_id": "A1B2C3D4",
      "airline": "SkyWings Airlines",
      "flight_number": "AA1234",
      "aircraft": "Boeing 737-800",
      "from_airport": {"code": "NYC", "name": "New York International Airport", "city": "New York"},
      "to_airport": {"code": "LAX", "name": "Los Angeles International Airport", "city": "Los Angeles"},
      "departure": "2025-07-01T08:30:00",
      "arrival": "2025-07-01T11:45:00",
      "duration_minutes": 195,
      "duration_formatted": "3h 15m",
      "is_direct": true,
      "price": 245.67,
      "currency": "USD",
      "available_seats": 12,
      "cabin_class": "Economy",
      "baggage_included": true,
      "meal_service": false
    },
    ...
  ],
  "return_flights": [...],
  "search_info": {
    "from_location": "New York",
    "to_location": "Los Angeles",
    "departure_date": "2025-07-01",
    "return_date": "2025-07-07",
    "total_departure_options": 5,
    "total_return_options": 4,
    "trip_type": "round_trip"
  }
}
```

## Code Structure
- **Main File**: `travel_assistant.py`
- **Key Functions**:
  - `generate_fake_address`: Generates realistic street addresses using predefined street names and numbers.
  - `validate_iso_date`: Validates and parses dates in ISO format (YYYY-MM-DD).
  - `suggest_hotels`: Generates a list of hotels with randomized attributes like name, price, rating, and amenities.
  - `suggest_flights`: Generates flight options with realistic details like airport codes, flight numbers, and durations.
- **Data Generation**:
  - Uses predefined lists for hotel names, amenities, airlines, aircraft types, and airport hubs.
  - Randomizes data to simulate real-world variability (e.g., prices, ratings, flight durations).
- **Error Handling**: Returns JSON-compatible error messages for invalid inputs or unexpected errors.

## Notes
- The application generates mock data and does not connect to real hotel or flight databases.
- Airport codes are generated based on city names and may not correspond to real-world IATA codes.
- The `FastMCP` framework is assumed to handle the service's API or interface layer. Ensure it is properly configured.
- The code avoids external file I/O and network calls, making it suitable for environments like Pyodide.

## Contributing
Contributions are welcome! Please submit pull requests or open issues for bugs, feature requests, or improvements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
