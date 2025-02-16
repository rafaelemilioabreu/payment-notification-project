import os
import smtplib
from email.message import EmailMessage
from Models.payroll_dto import PayRollDto
from Services.translation_service import get_translation

def send_email(recipient: PayRollDto, country: str = "do", attachment=None):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    email_user = os.getenv('SMTP_USER')
    email_password = os.getenv('SMTP_PASSWORD')

    msg = EmailMessage()
    msg['Subject'] = get_translation("email_subject", country)
    msg['From'] = email_user
    msg['To'] = recipient.email
    
    email_content = f"""{get_translation('email_greeting', country)} {recipient.full_name},

{get_translation('email_body', country)}

{get_translation('email_farewell', country)}
{get_translation('email_department', country)}"""

    msg.set_content(email_content)

    if attachment:
        file_data = attachment
        file_name = get_translation("file_name_payroll", country).format(name=recipient.full_name)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
    except Exception as e:
        error_msg = get_translation("error_sending_email", country).format(error=str(e))
        print(error_msg)
        return e
