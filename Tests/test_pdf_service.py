import pytest
from datetime import datetime
from Models.payroll_dto import PayRollDto
from Services.pdf_service import generate_pdf
from Services.translation_service import get_translation
import re
from pypdf import PdfReader  # Updated import
from io import BytesIO

@pytest.fixture
def sample_payroll():
    return PayRollDto(
        email="test@example.com",
        full_name="John Doe",
        position="Developer",
        health_discount_amount=100.50,
        social_discount_amount=200.75,
        taxes_discount_amount=300.25,
        other_discount=50.00,
        gross_salary=5000.00,
        gross_payment=4500.00,
        net_payment=3848.50,
        period="2023-01",
        read_date=datetime.now()
    )

def extract_pdf_text(pdf_content: bytes) -> str:
    pdf = PdfReader(BytesIO(pdf_content))
    return " ".join(page.extract_text() for page in pdf.pages)

def test_generate_pdf_content(sample_payroll):
    pdf_content = generate_pdf(sample_payroll)
    
    assert pdf_content is not None
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 0
    assert pdf_content.startswith(b'%PDF')

def test_generate_pdf_data_validation(sample_payroll):
    pdf_content = generate_pdf(sample_payroll)
    pdf_text = extract_pdf_text(pdf_content)
    
    assert sample_payroll.full_name in pdf_text
    assert sample_payroll.position in pdf_text
    assert f"${sample_payroll.gross_salary:,.2f}" in pdf_text
    assert f"${sample_payroll.net_payment:,.2f}" in pdf_text
    assert sample_payroll.period in pdf_text

def test_generate_pdf_number_formatting(sample_payroll):
    pdf_content = generate_pdf(sample_payroll)
    pdf_text = extract_pdf_text(pdf_content)
    
    amount_pattern = r'\$\d{1,3}(?:,\d{3})*\.\d{2}'
    assert re.search(amount_pattern, pdf_text) is not None

@pytest.mark.parametrize("invalid_payroll", [
    None,
    "invalid_data",
    {},
])
def test_generate_pdf_invalid_input(invalid_payroll):
    with pytest.raises(AttributeError):
        generate_pdf(invalid_payroll)


