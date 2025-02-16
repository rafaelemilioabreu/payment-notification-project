import pytest
import pandas as pd
from datetime import datetime
from Services.csv_service import get_payroll_data_from_csv, is_valid_email, validate_numeric
from Services.translation_service import get_translation
import os

@pytest.fixture
def sample_csv(tmp_path):
    csv_content = """email,full_name,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount,gross_salary,gross_payment,net_payment,period
test@email.com,John Doe,Developer,100.50,200.75,300.25,50.00,5000.00,4500.00,3848.50,2023-01
invalid.email,Jane Doe,Manager,150.25,250.50,350.75,75.00,6000.00,5500.00,4673.50,2023-01"""
    
    csv_file = tmp_path / "test_payroll.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)

def test_is_valid_email():
    assert is_valid_email("test@example.com") == True
    assert is_valid_email("invalid.email") == False
    assert is_valid_email("test@.com") == False
    assert is_valid_email("@example.com") == False

def test_validate_numeric():
    assert validate_numeric("100.50") == 100.50
    assert validate_numeric("invalid") == 0.0
    assert validate_numeric(None) == 0.0
    assert validate_numeric(pd.NA) == 0.0

def test_get_payroll_data_from_csv(sample_csv):
    payrolls = get_payroll_data_from_csv(sample_csv)
    
    assert len(payrolls) == 1  # Only valid email should be processed
    payroll = payrolls[0]
    
    assert payroll.email == "test@email.com"
    assert payroll.full_name == "John Doe"
    assert payroll.position == "Developer"
    assert payroll.health_discount_amount == 100.50
    assert payroll.social_discount_amount == 200.75
    assert payroll.taxes_discount_amount == 300.25
    assert payroll.other_discount == 50.00
    assert payroll.gross_salary == 5000.00
    assert payroll.gross_payment == 4500.00
    assert payroll.net_payment == 3848.50
    assert payroll.period == "2023-01"
    assert isinstance(payroll.read_date, datetime)

def test_get_payroll_data_missing_columns(tmp_path):
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("email,full_name\ntest@email.com,John Doe")
    
    with pytest.raises(ValueError) as exc_info:
        get_payroll_data_from_csv(str(invalid_csv))
    
    expected_missing_columns = "position, health_discount_amount, social_discount_amount, taxes_discount_amount, other_discount, gross_salary, gross_payment, net_payment, period"
    expected_message = get_translation("error_missing_columns").format(columns=expected_missing_columns)
    
    error_message = str(exc_info.value)
    assert error_message == expected_message