import pytest
from Services.translation_service import get_translation

def test_get_translation_spanish():
    assert get_translation("payment_information", "do") == "Información de Pago"
    assert get_translation("gross_salary", "do") == "Salario Bruto"
    assert get_translation("email_subject", "do") == "Notificación de Nómina"

def test_get_translation_english():
    assert get_translation("payment_information", "usa") == "Payment Information"
    assert get_translation("gross_salary", "usa") == "Gross Salary"
    assert get_translation("email_subject", "usa") == "Payroll Notification"

def test_get_translation_default_country():
    assert get_translation("payment_information") == "Información de Pago"
    assert get_translation("email_subject") == "Notificación de Nómina"

def test_get_translation_invalid_country():
    assert get_translation("payment_information", "fr") == "Información de Pago"
    assert get_translation("email_subject", "invalid") == "Notificación de Nómina"

def test_get_translation_case_insensitive():
    assert get_translation("payment_information", "DO") == "Información de Pago"
    assert get_translation("payment_information", "USA") == "Payment Information"

def test_get_translation_missing_key():
    non_existent_key = "non_existent_key"
    assert get_translation(non_existent_key, "do") == non_existent_key
    assert get_translation(non_existent_key, "usa") == non_existent_key

def test_get_translation_format_string():
    error_key = "error_missing_columns"
    columns = "col1, col2"
    
    es_translation = get_translation(error_key, "do").format(columns=columns)
    en_translation = get_translation(error_key, "usa").format(columns=columns)
    
    assert "col1, col2" in es_translation
    assert "col1, col2" in en_translation
    assert es_translation != en_translation

