import pytest
from app import app
import io
import os
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_query():
    return f"credentials={os.getenv('API_USER')} {os.getenv('API_PASSWORD')}"

@pytest.fixture
def sample_csv():
    return (
        "email,full_name,position,health_discount_amount,social_discount_amount,"
        "taxes_discount_amount,other_discount,gross_salary,gross_payment,net_payment,period\n"
        "test@email.com,John Doe,Developer,100.50,200.75,300.25,50.00,5000.00,4500.00,3848.50,2023-01"
    )

def test_process_payroll_success(client, auth_query, sample_csv):
    data = {'file': (io.BytesIO(sample_csv.encode()), 'test.csv', 'text/csv')}
    
    with patch('app.get_payroll_data_from_csv') as mock_csv_service, \
         patch('app.generate_pdf') as mock_pdf_service, \
         patch('app.send_email') as mock_email_service:
        
        mock_payroll = MagicMock(
            email="test@email.com",
            to_dict=lambda: {"email": "test@email.com"}
        )
        mock_csv_service.return_value = [mock_payroll]
        mock_pdf_service.return_value = b"fake pdf content"
        
        response = client.post(
            f'/process?company=test&country=do&{auth_query}',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert len(response.json['clients']) == 1
        
        mock_csv_service.assert_called_once()
        mock_pdf_service.assert_called_once()
        mock_email_service.assert_called_once()

def test_missing_auth(client):
    response = client.post('/process?company=test')
    assert response.status_code == 401

def test_invalid_auth(client):
    response = client.post('/process?company=test&credentials=invalid invalid')
    assert response.status_code == 401

def test_missing_company(client, auth_query):
    response = client.post(f'/process?{auth_query}')
    assert response.status_code == 400
    assert b"Company parameter is required" in response.data

def test_missing_file(client, auth_query):
    response = client.post(f'/process?company=test&{auth_query}')
    assert response.status_code == 400
    assert b"File parameter is required" in response.data

def test_multiple_files(client, auth_query):
    data = {
        'file1': (io.BytesIO(b'content1'), 'test1.csv', 'text/csv'),
        'file2': (io.BytesIO(b'content2'), 'test2.csv', 'text/csv')
    }
    response = client.post(
        f'/process?company=test&{auth_query}',
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    assert b"Only one file is allowed" in response.data

def test_invalid_file_extension(client, auth_query):
    data = {'file': (io.BytesIO(b'content'), 'test.txt', 'text/plain')}
    response = client.post(
        f'/process?company=test&{auth_query}',
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    assert b"Only CSV files are allowed" in response.data

def test_invalid_content_type(client, auth_query):
    data = {'file': (io.BytesIO(b'content'), 'test.csv', 'text/plain')}
    response = client.post(
        f'/process?company=test&{auth_query}',
        content_type='text/plain'
    )
    assert response.status_code == 400

@patch('app.get_payroll_data_from_csv')
def test_csv_service_error(mock_csv_service, client, auth_query, sample_csv):
    mock_csv_service.side_effect = ValueError("Invalid CSV format")
    data = {'file': (io.BytesIO(sample_csv.encode()), 'test.csv', 'text/csv')}
    
    response = client.post(
        f'/process?company=test&{auth_query}',
        data=data,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 400
    assert b"Invalid CSV format" in response.data