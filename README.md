# Payroll Notification Project

## Overview
This project provides an API endpoint to process payroll notifications by uploading a CSV file with payroll data. The application is designed to run exclusively via Docker.

## Setup
1. **Environment Variables**  
   Create a `.env` file based on the provided `env.example` file. The following environment variables must be defined:
   - API_USER
   - API_PASSWORD
   - SMTP_SERVER
   - SMTP_PORT
   - SMTP_USER
   - SMTP_PASSWORD

2. **Docker Deployment**  
   Build and run the project using Docker:
   ```
   docker-compose up --build
   ```

## API Usage

### Endpoint
- `/process`
- Method: POST

### Authentication
Use the credentials query parameter with the following format.

### Required Query Parameters
- `company`: The name of the company.
- `country`: (Optional, defaults to "do".)

### File Upload
The API accepts a single CSV file upload. Make sure that:
- The file has a .csv extension.
- The MIME type is text/csv.

## CSV Format
The CSV file must include the following headers exactly:
- full_name
- email
- position
- health_discount_amount
- social_discount_amount
- taxes_discount_amount
- other_discount
- gross_salary
- gross_payment
- net_payment
- period

### Example CSV:
```
full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period,other_discount
Juan Pérez,aefhoagheigue7@yopmail.com,Desarrollador,100.00,200.00,150.00,50.00,5000.00,4500.00,4000.00,2023-10-01,5
otro nombre,aegaegee3553ss@yopmail.com,Desarrollador,100.00,200.00,150.00,50.00,5000.00,4500.00,4000.00,2023-10-01,6
```
