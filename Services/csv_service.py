import pandas as pd
from datetime import datetime
from Models.payroll_dto import PayRollDto
from typing import List
import re
from Services.translation_service import get_translation

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_numeric(value: any) -> float:
    try:
        return float(value) if pd.notna(value) else 0.0
    except (ValueError, TypeError):
        return 0.0

def get_payroll_data_from_csv(file: str, country: str = "do") -> List[PayRollDto]:
    df = pd.read_csv(file)

    required_columns = [
        'email', 'full_name', 'position', 'health_discount_amount',
        'social_discount_amount', 'taxes_discount_amount', 'other_discount',
        'gross_salary', 'gross_payment', 'net_payment', 'period'
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(get_translation("error_missing_columns", country).format(
            columns=', '.join(missing_columns)))
    
    payrolls_dtos = []
    
    for _, row in df.iterrows():
        if not is_valid_email(row['email']):
            continue
            
        try:
            payroll = PayRollDto(
                email=row['email'],
                read_date=datetime.now(),
                full_name=row['full_name'],
                position=row['position'],
                health_discount_amount=validate_numeric(row['health_discount_amount']),
                social_discount_amount=validate_numeric(row['social_discount_amount']),
                taxes_discount_amount=validate_numeric(row['taxes_discount_amount']),
                other_discount=validate_numeric(row['other_discount']),
                gross_salary=validate_numeric(row['gross_salary']),
                gross_payment=validate_numeric(row['gross_payment']),
                net_payment=validate_numeric(row['net_payment']),
                period=str(row['period'])
            )
            payrolls_dtos.append(payroll)
        except Exception as e:
            print(get_translation("error_processing_row", country).format(
                email=row['email'], error=str(e)))
            continue
    
    return payrolls_dtos