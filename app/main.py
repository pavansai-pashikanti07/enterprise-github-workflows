"""
Enterprise Demo Microservice Application
A lightweight Python service used to demonstrate CI/CD pipelines,
Composite Actions, and Matrix Testing in GitHub Actions.
"""
import os
import sys

def get_platform_info():
    return {
        "status": "online",
        "service": "cinepass-ticket-processor",
        "version": "1.0.0",
        "python_version": sys.version.split()[0],
        "os": os.name
    }

def calculate_discount(price: float, tier: str) -> float:
    discounts = {
        "VIP": 0.20,
        "PREMIUM": 0.10,
        "STANDARD": 0.05
    }
    rate = discounts.get(tier.upper(), 0.0)
    return round(price * (1 - rate), 2)

if __name__ == "__main__":
    print("Starting Ticket Processing Microservice...")
    info = get_platform_info()
    print(f"Service Info: {info}")
    sample_price = calculate_discount(100.0, "VIP")
    print(f"Sample VIP ticket price (base 100): {sample_price}")
