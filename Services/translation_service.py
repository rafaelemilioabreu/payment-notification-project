from typing import Dict

translations: Dict[str, Dict[str, str]] = {
    "do": {
        "payment_information": "Información de Pago",
        "gross_salary": "Salario Bruto",
        "gross_payment": "Pago Bruto",
        "net_payment": "Pago Neto",
        "health_insurance": "SFS",
        "social_security": "AFP",
        "taxes": "ISR",
        "employee_information": "Información del Empleado",
        "paystub_payment": "Comprobante de Pago",
        "name": "Nombre",
        "title": "Cargo",
        "discounts": "Descuentos",
        "others": "Otros",
        "total": "Total",
        "company": "Empresa",
        "email_subject": "Notificación de Nómina",
        "email_greeting": "Estimado/a",
        "email_body": "Adjunto encontrará su comprobante de pago para este período.",
        "email_farewell": "Saludos cordiales,",
        "email_department": "Departamento de Nómina",
        "error_missing_columns": "El archivo CSV no contiene las columnas requeridas: {columns}",
        "error_processing_row": "Error procesando fila para {email}: {error}",
        "error_sending_email": "Error enviando correo: {error}",
        "error_loading_image": "Error cargando imagen: {error}",
        "period": "Período",
        "currency_symbol": "$",
        "file_name_payroll": "nomina_{name}.pdf",
        "sfs": "SFS",
        "afp": "AFP",
        "isr": "ISR"
    },
    "usa": {
        "payment_information": "Payment Information",
        "gross_salary": "Gross Salary",
        "gross_payment": "Gross Payment",
        "net_payment": "Net Payment",
        "health_insurance": "Health Insurance",
        "social_security": "Social Security",
        "taxes": "Taxes",
        "employee_information": "Employee Information",
        "paystub_payment": "Paystub Payment",
        "name": "Name",
        "title": "Title",
        "discounts": "Deductions",
        "others": "Others",
        "total": "Total",
        "company": "Company",
        "email_subject": "Payroll Notification",
        "email_greeting": "Dear",
        "email_body": "Please find attached your payroll for this period.",
        "email_farewell": "Best regards,",
        "email_department": "Payroll Department",
        "error_missing_columns": "The CSV file is missing required columns: {columns}",
        "error_processing_row": "Error processing row for {email}: {error}",
        "error_sending_email": "Error sending email: {error}",
        "error_loading_image": "Error loading image: {error}",
        "period": "Period",
        "currency_symbol": "$",
        "file_name_payroll": "payroll_{name}.pdf",
        "sfs": "Health Insurance",
        "afp": "Social Security",
        "isr": "Taxes"
    }
}

def get_translation(key: str, country: str = "do") -> str:
    country = country.lower()
    if country not in translations:
        country = "do"
    
    return translations[country].get(key, key)