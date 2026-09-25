import pytest
from app.main import get_platform_info, calculate_discount

def test_get_platform_info():
    info = get_platform_info()
    assert info["status"] == "online"
    assert info["service"] == "cinepass-ticket-processor"
    assert "version" in info
    assert "python_version" in info

def test_calculate_discount_vip():
    assert calculate_discount(100.0, "VIP") == 80.0

def test_calculate_discount_premium():
    assert calculate_discount(100.0, "PREMIUM") == 90.0

def test_calculate_discount_standard():
    assert calculate_discount(100.0, "STANDARD") == 95.0

def test_calculate_discount_unknown_tier():
    assert calculate_discount(100.0, "UNKNOWN") == 100.0
