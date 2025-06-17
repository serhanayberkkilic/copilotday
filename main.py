import random
import re
import uuid
from datetime import datetime, timedelta
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("TravelAssistant", version="1.0.0", description="A travel assistant for hotel and flight suggestions")

# Custom data sets to replace Faker
STREET_NAMES = [
    "Main Street", "Oak Avenue", "Park Boulevard", "First Street", "Second Street",
    "Elm Street", "Washington Avenue", "Lincoln Boulevard", "Central Avenue", "Broadway",
    "Fifth Avenue", "Sunset Boulevard", "Market Street", "Church Street", "School Street",
    "Maple Avenue", "Pine Street", "Cedar Avenue", "Walnut Street", "Chestnut Street"
]

STREET_NUMBERS = list(range(100, 9999))

def generate_fake_address():
    """Generate a fake street address"""
    number = random.choice(STREET_NUMBERS)
    street = random.choice(STREET_NAMES)
    return f"{number} {street}"

def validate_iso_date(date_str: str, param_name: str) -> datetime.date:
    """
    Validates that a string is in ISO format (YYYY-MM-DD) and returns the parsed date.

    Args:
        date_str: The date string to validate
        param_name: Name of the parameter for error messages

    Returns:
        The parsed date object

    Raises:
        ValueError: If the date is not in ISO format or is invalid
    """
    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not iso_pattern.match(date_str):
        raise ValueError(f"{param_name} must be in ISO format (YYYY-MM-DD), got: {date_str}")

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid {param_name}: {e}")


@mcp.tool()
async def suggest_hotels(
    location: Annotated[str, Field(description="Location (city or area) to search for hotels")],
    check_in: Annotated[str, Field(description="Check-in date in ISO format (YYYY-MM-DD)")],
    check_out: Annotated[str, Field(description="Check-out date in ISO format (YYYY-MM-DD)")],
) -> str:
    """
    Suggest hotels based on location and dates.
    """
    try:
        # Validate dates
        check_in_date = validate_iso_date(check_in, "check_in")
        check_out_date = validate_iso_date(check_out, "check_out")

        # Ensure check_out is after check_in
        if check_out_date <= check_in_date:
            raise ValueError("check_out date must be after check_in date")

        # Hotel data
        hotel_types = ["Luxury", "Boutique", "Budget", "Business", "Resort"]
        hotel_suffixes = ["Hotel", "Inn", "Suites", "Resort", "Plaza", "Lodge", "Manor", "Palace"]
        amenities = [
            "Free WiFi", "Swimming Pool", "Spa & Wellness Center", "Fitness Center", 
            "Restaurant", "Bar & Lounge", "Room Service", "Free Parking", 
            "Business Center", "Conference Rooms", "Concierge Service", "Airport Shuttle",
            "Pet Friendly", "Laundry Service", "24/7 Front Desk", "Complimentary Breakfast"
        ]

        neighborhoods = [
            "Downtown", "Historic District", "Waterfront", "Business District", 
            "Arts District", "University Area", "Old Town", "City Center",
            "Harbor District", "Financial District", "Cultural Quarter", "Shopping District"
        ]

        # Hotel name prefixes to make them more realistic
        hotel_prefixes = [
            "Grand", "Royal", "Imperial", "Golden", "Silver", "Crown", "Elite",
            "Premier", "Superior", "Deluxe", "Executive", "Metropolitan", "Continental",
            "International", "Central", "Park", "Garden", "Harbor", "Riverside"
        ]

        # Generate a rating between 3.0 and 5.0
        def generate_rating():
            return round(random.uniform(3.0, 5.0), 1)

        # Generate a price based on hotel type
        def generate_price(hotel_type):
            price_ranges = {
                "Luxury": (250, 600),
                "Boutique": (180, 350),
                "Budget": (80, 150),
                "Resort": (200, 500),
                "Business": (150, 300),
            }
            min_price, max_price = price_ranges.get(hotel_type, (100, 300))
            return round(random.uniform(min_price, max_price))

        # Generate between 3 and 8 hotels
        num_hotels = random.randint(3, 8)
        hotels = []

        for i in range(num_hotels):
            hotel_type = random.choice(hotel_types)
            hotel_amenities = random.sample(amenities, random.randint(4, 8))
            neighborhood = random.choice(neighborhoods)
            
            # Generate hotel name
            if random.random() < 0.7:  # 70% chance of having a prefix
                prefix = random.choice(hotel_prefixes)
                suffix = random.choice(hotel_suffixes)
                hotel_name = f"{prefix} {suffix}"
            else:
                hotel_name = f"{hotel_type} {random.choice(hotel_suffixes)}"

            hotel = {
                "name": hotel_name,
                "address": generate_fake_address(),
                "location": f"{neighborhood}, {location}",
                "rating": generate_rating(),
                "price_per_night": generate_price(hotel_type),
                "hotel_type": hotel_type,
                "amenities": hotel_amenities,
                "available_rooms": random.randint(1, 15),
                "phone": f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
                "check_in_time": "15:00",
                "check_out_time": "11:00"
            }
            hotels.append(hotel)

        # Sort by rating to show best hotels first
        hotels.sort(key=lambda x: x["rating"], reverse=True)
        return {"hotels": hotels, "total_found": len(hotels)}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


@mcp.tool()
async def suggest_flights(
    from_location: Annotated[str, Field(description="Departure location (city or airport)")],
    to_location: Annotated[str, Field(description="Destination location (city or airport)")],
    departure_date: Annotated[str, Field(description="Departure date in ISO format (YYYY-MM-DD)")],
    return_date: Annotated[str | None, Field(description="Return date in ISO format (YYYY-MM-DD)")] = None,
) -> str:
    """
    Suggest flights based on locations and dates.
    """
    try:
        # Validate dates
        dep_date = validate_iso_date(departure_date, "departure_date")
        ret_date = None
        if return_date:
            ret_date = validate_iso_date(return_date, "return_date")
            # Ensure return date is after departure date
            if ret_date <= dep_date:
                raise ValueError("return_date must be after departure_date")

        # Flight data
        airlines = [
            "SkyWings Airlines", "Global Air Express", "Atlantic Airways", "Pacific Express",
            "Mountain Jets", "Stellar Airlines", "Sunshine Airways", "Northern Flights",
            "Oceanic Air", "Continental Airways", "Liberty Airlines", "Eagle Express",
            "Horizon Air", "Blue Sky Airlines", "Golden Wings", "Silver Airways"
        ]

        aircraft_types = [
            "Boeing 737-800", "Airbus A320", "Boeing 787-9", "Airbus A350-900", 
            "Embraer E190", "Bombardier CRJ900", "Boeing 777-300", "Airbus A330-200",
            "Boeing 737 MAX 8", "Airbus A321", "Boeing 757-200", "Embraer E175"
        ]

        cabin_classes = ["Economy", "Premium Economy", "Business", "First Class"]

        # Generate airport codes based on locations
        def generate_airport_code(city):
            """Generate a realistic 3-letter airport code"""
            # Common airport code patterns
            city_clean = re.sub(r'[^A-Za-z]', '', city.upper())
            
            if len(city_clean) >= 3:
                # Use first 3 letters of city
                code = city_clean[:3]
            else:
                # Generate based on first letter + random
                vowels = "AEIOU"
                consonants = "BCDFGHJKLMNPQRSTVWXYZ"
                
                first_char = city_clean[0] if city_clean else random.choice(consonants)
                code = first_char
                
                # Add two more characters
                for _ in range(2):
                    if random.random() < 0.6:  # 60% chance of consonant
                        code += random.choice(consonants)
                    else:
                        code += random.choice(vowels)
            
            return code

        from_code = generate_airport_code(from_location)
        to_code = generate_airport_code(to_location)

        # Major hub airports for connections
        major_hubs = [
            {"code": "ATL", "name": "Hartsfield-Jackson Atlanta International", "city": "Atlanta"},
            {"code": "ORD", "name": "O'Hare International Airport", "city": "Chicago"},
            {"code": "DFW", "name": "Dallas/Fort Worth International", "city": "Dallas"},
            {"code": "LHR", "name": "London Heathrow Airport", "city": "London"},
            {"code": "CDG", "name": "Charles de Gaulle Airport", "city": "Paris"},
            {"code": "DXB", "name": "Dubai International Airport", "city": "Dubai"},
            {"code": "AMS", "name": "Amsterdam Airport Schiphol", "city": "Amsterdam"},
            {"code": "FRA", "name": "Frankfurt Airport", "city": "Frankfurt"}
        ]

        def generate_flight_number():
            """Generate a realistic flight number"""
            airline_code = random.choice(["AA", "UA", "DL", "SW", "BA", "LH", "AF", "KL", "EK", "QR"])
            number = random.randint(100, 9999)
            return f"{airline_code}{number}"

        def create_flight(from_airport, to_airport, dep_date, base_price_multiplier=1.0):
            """Create a single flight object"""
            # Generate departure time (between 5 AM and 11 PM)
            hour = random.randint(5, 23)
            minute = random.choice([0, 15, 30, 45])
            dep_time = datetime.combine(dep_date, datetime.min.time()).replace(hour=hour, minute=minute)

            # Flight duration based on rough distance estimation
            # This is simplified - in reality would use actual distance calculations
            flight_minutes = random.randint(90, 600)  # 1.5 to 10 hours
            arr_time = dep_time + timedelta(minutes=flight_minutes)

            # Determine if this is a direct or connecting flight
            is_direct = random.random() < 0.65  # 65% chance of direct flight

            # Base price calculation
            base_price = random.uniform(150, 800) * base_price_multiplier
            
            flight = {
                "flight_id": str(uuid.uuid4())[:8].upper(),
                "airline": random.choice(airlines),
                "flight_number": generate_flight_number(),
                "aircraft": random.choice(aircraft_types),
                "from_airport": from_airport,
                "to_airport": to_airport,
                "departure": dep_time.strftime("%Y-%m-%dT%H:%M:00"),
                "arrival": arr_time.strftime("%Y-%m-%dT%H:%M:00"),
                "duration_minutes": flight_minutes,
                "duration_formatted": f"{flight_minutes // 60}h {flight_minutes % 60}m",
                "is_direct": is_direct,
                "price": round(base_price, 2),
                "currency": "USD",
                "available_seats": random.randint(1, 35),
                "cabin_class": random.choice(cabin_classes),
                "baggage_included": random.choice([True, False]),
                "meal_service": random.choice([True, False]) if flight_minutes > 180 else False
            }

            # Add connection info for non-direct flights
            if not is_direct:
                connection_hub = random.choice(major_hubs)
                
                # Split the flight into segments
                segment1_duration = round(flight_minutes * random.uniform(0.4, 0.6))
                segment2_duration = flight_minutes - segment1_duration
                connection_time = random.randint(60, 240)  # 1-4 hours connection

                segment1_arrival = dep_time + timedelta(minutes=segment1_duration)
                segment2_departure = segment1_arrival + timedelta(minutes=connection_time)

                flight["segments"] = [
                    {
                        "flight_number": generate_flight_number(),
                        "from_airport": from_airport,
                        "to_airport": connection_hub,
                        "departure": dep_time.strftime("%Y-%m-%dT%H:%M:00"),
                        "arrival": segment1_arrival.strftime("%Y-%m-%dT%H:%M:00"),
                        "duration_minutes": segment1_duration,
                        "aircraft": random.choice(aircraft_types)
                    },
                    {
                        "flight_number": generate_flight_number(),
                        "from_airport": connection_hub,
                        "to_airport": to_airport,
                        "departure": segment2_departure.strftime("%Y-%m-%dT%H:%M:00"),
                        "arrival": arr_time.strftime("%Y-%m-%dT%H:%M:00"),
                        "duration_minutes": segment2_duration,
                        "aircraft": random.choice(aircraft_types)
                    }
                ]
                flight["connection_airport"] = connection_hub["code"]
                flight["connection_duration_minutes"] = connection_time
                flight["total_duration_minutes"] = flight_minutes + connection_time

            return flight

        # Create airport objects
        from_airport = {
            "code": from_code,
            "name": f"{from_location} International Airport",
            "city": from_location,
        }
        to_airport = {
            "code": to_code,
            "name": f"{to_location} International Airport",
            "city": to_location,
        }

        # Generate departure flights
        departure_flights = []
        num_dep_flights = random.randint(4, 8)

        for _ in range(num_dep_flights):
            flight = create_flight(from_airport, to_airport, dep_date)
            departure_flights.append(flight)

        # Sort by price
        departure_flights.sort(key=lambda x: x["price"])

        # Generate return flights if return_date is provided
        return_flights = []
        if ret_date:
            num_ret_flights = random.randint(4, 8)
            
            for _ in range(num_ret_flights):
                flight = create_flight(to_airport, from_airport, ret_date, base_price_multiplier=0.9)
                return_flights.append(flight)
            
            # Sort by price
            return_flights.sort(key=lambda x: x["price"])

        # Prepare response
        response = {
            "departure_flights": departure_flights,
            "return_flights": return_flights,
            "search_info": {
                "from_location": from_location,
                "to_location": to_location,
                "departure_date": departure_date,
                "return_date": return_date,
                "total_departure_options": len(departure_flights),
                "total_return_options": len(return_flights) if return_flights else 0,
                "trip_type": "round_trip" if return_date else "one_way"
            }
        }

        return response

    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()