"""
Tools for EcoHome Energy Advisor Agent
"""
import os
import random
from datetime import datetime, timedelta
from typing import Dict, Any
from langchain_core.tools import tool
from models.energy import DatabaseManager

# Initialize database manager
db_manager = DatabaseManager()

@tool
def get_weather_forecast(location: str, days: int = 3) -> Dict[str, Any]:
    """
    Get weather forecast for a specific location and number of days.
    Use this tool to check weather conditions and solar irradiance for energy planning.

    Args:
        location (str): Location to get weather for (e.g., "San Francisco, CA")
        days (int): Number of days to forecast (1-7)
    
    Returns:
        Dict[str, Any]: Weather forecast data including temperature, conditions, and solar irradiance
    """
    # Use seed based on location for consistent results
    random.seed(hash(location) % 1000)

    days = min(max(days, 1), 7)  # Clamp days between 1 and 7

    # Weighted conditions - more sunny days for better solar predictions
    conditions = ["sunny", "sunny", "partly_cloudy", "partly_cloudy", "cloudy"]

    # Current weather
    current_condition = random.choice(conditions)
    current_temp = random.uniform(18, 25)

    forecast = {
        "location": location,
        "forecast_days": days,
        "current": {
            "temperature_c": round(current_temp, 1),
            "condition": current_condition,
            "humidity": random.randint(40, 70),
            "wind_speed": round(random.uniform(5, 15), 1)
        },
        "hourly": [],
        "daily_summary": []
    }

    # Generate hourly forecast for each day
    for day in range(days):
        daily_solar_total = 0
        daily_conditions = []

        for hour in range(24):
            # Temperature varies by hour - cooler at night, warmer during day
            if 6 <= hour <= 18:
                hour_temp = current_temp + (hour - 6) * 0.8 if hour <= 14 else current_temp + (18 - hour) * 0.8
            else:
                hour_temp = current_temp - 3

            # Consistent condition per time block
            if hour < 6:
                condition = "cloudy"
            elif hour < 10:
                condition = random.choice(["sunny", "partly_cloudy"])
            elif hour < 16:
                condition = random.choice(["sunny", "sunny", "partly_cloudy"])
            else:
                condition = random.choice(["partly_cloudy", "cloudy"])

            daily_conditions.append(condition)

            # Solar irradiance based on time of day and weather
            if 6 <= hour <= 18:
                base_irradiance = 600 + (6 - abs(hour - 12)) * 150  # Peak at noon ~1200 W/m²
                if condition == "sunny":
                    solar_irradiance = base_irradiance * 0.95
                elif condition == "partly_cloudy":
                    solar_irradiance = base_irradiance * 0.6
                else:
                    solar_irradiance = base_irradiance * 0.2
                daily_solar_total += solar_irradiance
            else:
                solar_irradiance = 0

            forecast["hourly"].append({
                "day": day,
                "hour": hour,
                "temperature_c": round(hour_temp, 1),
                "condition": condition,
                "solar_irradiance": round(solar_irradiance, 1),
                "humidity": random.randint(40, 70),
                "wind_speed": round(random.uniform(5, 15), 1)
            })

        # Add daily summary for easier interpretation
        sunny_hours = daily_conditions.count("sunny")
        forecast["daily_summary"].append({
            "day": day,
            "avg_solar_irradiance": round(daily_solar_total / 13, 1),  # 13 daylight hours
            "sunny_hours": sunny_hours,
            "expected_generation_kwh": round(daily_solar_total * 0.005, 2),  # Rough estimate
            "best_solar_hours": "10:00-15:00"
        })

    # Reset random seed
    random.seed()

    return forecast

@tool
def get_electricity_prices(date: str = None) -> Dict[str, Any]:
    """
    Get electricity prices for a specific date or current day.
    Use this tool to find the cheapest hours for running appliances or charging EVs.

    Args:
        date (str): Date in YYYY-MM-DD format (defaults to today)
    
    Returns:
        Dict[str, Any]: Electricity pricing data with hourly rates and recommendations
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Base price per kWh
    base_price = 0.12

    prices = {
        "date": date,
        "pricing_type": "time_of_use",
        "currency": "USD",
        "unit": "per_kWh",
        "hourly_rates": [],
        "summary": {
            "cheapest_hours": [],
            "most_expensive_hours": [],
            "off_peak_avg_rate": 0,
            "peak_avg_rate": 0,
            "super_peak_avg_rate": 0
        }
    }

    off_peak_rates = []
    peak_rates = []
    super_peak_rates = []

    # Generate hourly rates with peak/off-peak pricing
    for hour in range(24):
        # Peak hours: 6 AM to 10 PM (6-22)
        if 6 <= hour < 22:
            # Super peak: 4 PM to 9 PM (16-21)
            if 16 <= hour < 21:
                rate = base_price * 2.5
                period = "super_peak"
                demand_charge = 0.05
                super_peak_rates.append(rate)
            else:
                rate = base_price * 1.5
                period = "peak"
                demand_charge = 0.02
                peak_rates.append(rate)
        else:
            # Off-peak hours: 10 PM to 6 AM
            rate = base_price * 0.7
            period = "off_peak"
            demand_charge = 0
            off_peak_rates.append(rate)

        prices["hourly_rates"].append({
            "hour": hour,
            "rate": round(rate, 4),
            "period": period,
            "demand_charge": round(demand_charge, 4)
        })

    # Calculate summary
    prices["summary"]["off_peak_avg_rate"] = round(sum(off_peak_rates) / len(off_peak_rates), 4) if off_peak_rates else 0
    prices["summary"]["peak_avg_rate"] = round(sum(peak_rates) / len(peak_rates), 4) if peak_rates else 0
    prices["summary"]["super_peak_avg_rate"] = round(sum(super_peak_rates) / len(super_peak_rates), 4) if super_peak_rates else 0
    prices["summary"]["cheapest_hours"] = [0, 1, 2, 3, 4, 5, 22, 23]
    prices["summary"]["most_expensive_hours"] = [16, 17, 18, 19, 20]
    prices["summary"]["recommendation"] = "Run high-energy appliances during off-peak hours (10PM-6AM) to save up to 70% on electricity costs"

    return prices

@tool
def query_energy_usage(start_date: str, end_date: str, device_type: str = None) -> Dict[str, Any]:
    """
    Query energy usage data from the database for a specific date range.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        device_type (str): Optional device type filter (e.g., "EV", "HVAC", "appliance")
    
    Returns:
        Dict[str, Any]: Energy usage data with consumption details
    """
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        records = db_manager.get_usage_by_date_range(start_dt, end_dt)
        
        if device_type:
            records = [r for r in records if r.device_type == device_type]
        
        # If no records found, generate mock data for demonstration
        if not records:
            num_days = (end_dt - start_dt).days
            mock_records = []
            total_consumption = 0
            total_cost = 0

            device_types_data = {
                "EV": {"daily_kwh": (8, 15), "cost_multiplier": 0.12},
                "HVAC": {"daily_kwh": (5, 12), "cost_multiplier": 0.15},
                "appliance": {"daily_kwh": (3, 6), "cost_multiplier": 0.12}
            }

            devices_to_generate = [device_type] if device_type else ["EV", "HVAC", "appliance"]

            for day_offset in range(num_days):
                current_date = start_dt + timedelta(days=day_offset)
                for dev_type in devices_to_generate:
                    dev_data = device_types_data.get(dev_type, {"daily_kwh": (3, 8), "cost_multiplier": 0.12})
                    daily_kwh = random.uniform(*dev_data["daily_kwh"])
                    daily_cost = daily_kwh * dev_data["cost_multiplier"]
                    total_consumption += daily_kwh
                    total_cost += daily_cost

                    mock_records.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "device_type": dev_type,
                        "consumption_kwh": round(daily_kwh, 2),
                        "cost_usd": round(daily_cost, 2),
                        "estimated": True
                    })

            return {
                "start_date": start_date,
                "end_date": end_date,
                "device_type": device_type,
                "total_records": len(mock_records),
                "total_consumption_kwh": round(total_consumption, 2),
                "total_cost_usd": round(total_cost, 2),
                "average_daily_consumption": round(total_consumption / max(1, num_days), 2),
                "records": mock_records,
                "note": "Data is estimated based on typical household usage patterns"
            }

        usage_data = {
            "start_date": start_date,
            "end_date": end_date,
            "device_type": device_type,
            "total_records": len(records),
            "total_consumption_kwh": round(sum(r.consumption_kwh for r in records), 2),
            "total_cost_usd": round(sum(r.cost_usd or 0 for r in records), 2),
            "records": []
        }
        
        for record in records:
            usage_data["records"].append({
                "timestamp": record.timestamp.isoformat(),
                "consumption_kwh": record.consumption_kwh,
                "device_type": record.device_type,
                "device_name": record.device_name,
                "cost_usd": record.cost_usd
            })
        
        return usage_data
    except Exception as e:
        return {"error": f"Failed to query energy usage: {str(e)}"}

@tool
def query_solar_generation(start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Query solar generation data from the database for a specific date range.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
    
    Returns:
        Dict[str, Any]: Solar generation data with production details
    """
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        records = db_manager.get_generation_by_date_range(start_dt, end_dt)
        
        # If no records found, generate mock data for demonstration
        if not records:
            num_days = (end_dt - start_dt).days
            mock_records = []
            total_generation = 0

            for day_offset in range(num_days):
                current_date = start_dt + timedelta(days=day_offset)
                # Typical solar panel generates 4-6 kWh per day per kW capacity
                # Assume 5kW system
                daily_generation = random.uniform(18, 28)  # 18-28 kWh per day
                total_generation += daily_generation

                mock_records.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "generation_kwh": round(daily_generation, 2),
                    "weather_condition": random.choice(["sunny", "partly_cloudy"]),
                    "peak_hour": "12:00",
                    "estimated": True
                })

            return {
                "start_date": start_date,
                "end_date": end_date,
                "total_records": num_days,
                "total_generation_kwh": round(total_generation, 2),
                "average_daily_generation": round(total_generation / max(1, num_days), 2),
                "records": mock_records,
                "note": "Data is estimated based on typical 5kW solar system performance"
            }

        generation_data = {
            "start_date": start_date,
            "end_date": end_date,
            "total_records": len(records),
            "total_generation_kwh": round(sum(r.generation_kwh for r in records), 2),
            "average_daily_generation": round(sum(r.generation_kwh for r in records) / max(1, (end_dt - start_dt).days), 2),
            "records": []
        }
        
        for record in records:
            generation_data["records"].append({
                "timestamp": record.timestamp.isoformat(),
                "generation_kwh": record.generation_kwh,
                "weather_condition": record.weather_condition,
                "temperature_c": record.temperature_c,
                "solar_irradiance": record.solar_irradiance
            })
        
        return generation_data
    except Exception as e:
        return {"error": f"Failed to query solar generation: {str(e)}"}

@tool
def get_recent_energy_summary(hours: int = 24) -> Dict[str, Any]:
    """
    Get a summary of recent energy usage and solar generation.
    
    Args:
        hours (int): Number of hours to look back (default 24)
    
    Returns:
        Dict[str, Any]: Summary of recent energy data
    """
    try:
        usage_records = db_manager.get_recent_usage(hours)
        generation_records = db_manager.get_recent_generation(hours)
        
        summary = {
            "time_period_hours": hours,
            "usage": {
                "total_consumption_kwh": round(sum(r.consumption_kwh for r in usage_records), 2),
                "total_cost_usd": round(sum(r.cost_usd or 0 for r in usage_records), 2),
                "device_breakdown": {}
            },
            "generation": {
                "total_generation_kwh": round(sum(r.generation_kwh for r in generation_records), 2),
                "average_weather": "sunny" if generation_records else "unknown"
            }
        }
        
        # Calculate device breakdown
        for record in usage_records:
            device = record.device_type or "unknown"
            if device not in summary["usage"]["device_breakdown"]:
                summary["usage"]["device_breakdown"][device] = {
                    "consumption_kwh": 0,
                    "cost_usd": 0,
                    "records": 0
                }
            summary["usage"]["device_breakdown"][device]["consumption_kwh"] += record.consumption_kwh
            summary["usage"]["device_breakdown"][device]["cost_usd"] += record.cost_usd or 0
            summary["usage"]["device_breakdown"][device]["records"] += 1
        
        # Round the breakdown values
        for device_data in summary["usage"]["device_breakdown"].values():
            device_data["consumption_kwh"] = round(device_data["consumption_kwh"], 2)
            device_data["cost_usd"] = round(device_data["cost_usd"], 2)
        
        return summary
    except Exception as e:
        return {"error": f"Failed to get recent energy summary: {str(e)}"}

@tool
def search_energy_tips(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Search for energy-saving tips and best practices using keyword matching.

    Args:
        query (str): Search query for energy tips
        max_results (int): Maximum number of results to return
    
    Returns:
        Dict[str, Any]: Relevant energy tips and best practices
    """
    try:
        # Load tips from text files using simple keyword search
        tips_content = []
        doc_paths = [
            "data/documents/tip_device_best_practices.txt",
            "data/documents/tip_energy_savings.txt"
        ]

        for doc_path in doc_paths:
            if os.path.exists(doc_path):
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tips_content.append({"source": doc_path, "content": content})

        if not tips_content:
            return {
                "query": query,
                "total_results": 0,
                "tips": [],
                "note": "No tips documents found"
            }

        # Split content into paragraphs and score by keyword matching
        query_words = set(query.lower().split())
        scored_tips = []

        for doc in tips_content:
            paragraphs = doc["content"].split('\n\n')
            for para in paragraphs:
                para = para.strip()
                if len(para) > 50:  # Skip short paragraphs
                    para_lower = para.lower()
                    # Score based on keyword matches
                    score = sum(2 if word in para_lower else 0 for word in query_words)
                    # Bonus for exact phrase match
                    if query.lower() in para_lower:
                        score += 5
                    if score > 0:
                        scored_tips.append({
                            "content": para,
                            "source": doc["source"],
                            "score": score
                        })

        # Sort by score and take top results
        scored_tips.sort(key=lambda x: x["score"], reverse=True)
        top_tips = scored_tips[:max_results]

        results = {
            "query": query,
            "total_results": len(top_tips),
            "tips": []
        }
        
        for i, tip in enumerate(top_tips):
            results["tips"].append({
                "rank": i + 1,
                "content": tip["content"],
                "source": tip["source"],
                "relevance_score": "high" if i < 2 else "medium" if i < 4 else "low"
            })
        
        return results
    except Exception as e:
        return {"error": f"Failed to search energy tips: {str(e)}"}

@tool
def calculate_energy_savings(device_type: str, current_usage_kwh: float, 
                           optimized_usage_kwh: float, price_per_kwh: float = 0.12) -> Dict[str, Any]:
    """
    Calculate potential energy savings from optimization.
    
    Args:
        device_type (str): Type of device being optimized
        current_usage_kwh (float): Current energy usage in kWh
        optimized_usage_kwh (float): Optimized energy usage in kWh
        price_per_kwh (float): Price per kWh (default 0.12)
    
    Returns:
        Dict[str, Any]: Savings calculation results
    """
    savings_kwh = current_usage_kwh - optimized_usage_kwh
    savings_usd = savings_kwh * price_per_kwh
    savings_percentage = (savings_kwh / current_usage_kwh) * 100 if current_usage_kwh > 0 else 0
    
    return {
        "device_type": device_type,
        "current_usage_kwh": current_usage_kwh,
        "optimized_usage_kwh": optimized_usage_kwh,
        "savings_kwh": round(savings_kwh, 2),
        "savings_usd": round(savings_usd, 2),
        "savings_percentage": round(savings_percentage, 1),
        "price_per_kwh": price_per_kwh,
        "annual_savings_usd": round(savings_usd * 365, 2)
    }


TOOL_KIT = [
    get_weather_forecast,
    get_electricity_prices,
    query_energy_usage,
    query_solar_generation,
    get_recent_energy_summary,
    search_energy_tips,
    calculate_energy_savings
]
