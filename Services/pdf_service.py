from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from Models.payroll_dto import PayRollDto
from io import BytesIO
import os
from Services.translation_service import get_translation  # Add this import

def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"

def get_company_logo(company: str) -> str:
    static_folder = "static"
    company_image = f"{static_folder}/{company.lower()}.png"
    default_image = f"{static_folder}/default.png"
    
    if os.path.exists(company_image):
        return company_image
    elif os.path.exists(default_image):
        return default_image
    return None

def generate_pdf(payroll_dto: PayRollDto, country: str = 'do', company: str ='default'):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Define column positions with balanced spacing
    left_col = 50
    middle_col = width/3 + 50    
    right_col = width - 150      

    # First Column - Logo and Payment Info
    logo_path = get_company_logo(company)
    start_y = height - 100

    if logo_path:
        try:
            img = ImageReader(logo_path)
            img_width = 150
            aspect = img.getSize()[1] / img.getSize()[0]
            img_height = img_width * aspect
            c.drawImage(img, left_col, start_y - img_height + 30, width=img_width, height=img_height)
            start_y = start_y - img_height
        except Exception as e:
            print(get_translation("error_loading_image", country).format(error=str(e)))
            c.setFont("Helvetica-Bold", 16)
            c.drawString(left_col, start_y, f"{get_translation('company', country)}: {company}")
            start_y -= 30

    # Payment Information in left column
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_col, start_y - 20, get_translation("payment_information", country))
    c.setFont("Helvetica", 12)
    c.drawString(left_col, start_y - 40, f"{get_translation('gross_salary', country)}: {format_currency(payroll_dto.gross_salary)}")
    c.drawString(left_col, start_y - 60, f"{get_translation('gross_payment', country)}: {format_currency(payroll_dto.gross_payment)}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_col, start_y - 80, f"{get_translation('net_payment', country)}: {format_currency(payroll_dto.net_payment)}")

    # Middle Column - Employee Information
    top_y = height - 100
    c.setFont("Helvetica-Bold", 14)
    c.drawString(middle_col, top_y, get_translation("employee_information", country))
    c.setFont("Helvetica", 12)
    c.drawString(middle_col, top_y - 20, f"{get_translation('paystub_payment', country)}: {payroll_dto.period}")
    c.drawString(middle_col, top_y - 40, f"{get_translation('name', country)}: {payroll_dto.full_name}")
    c.drawString(middle_col, top_y - 60, f"{get_translation('title', country)}: {payroll_dto.position}")

    # Right Column - Deductions
    c.setFont("Helvetica-Bold", 14)
    c.drawString(right_col, top_y, get_translation("discounts", country))
    c.setFont("Helvetica", 12)
    c.drawString(right_col, top_y - 20, f"{get_translation('sfs', country)}: {format_currency(payroll_dto.social_discount_amount)}")
    c.drawString(right_col, top_y - 40, f"{get_translation('afp', country)}: {format_currency(payroll_dto.health_discount_amount)}")
    c.drawString(right_col, top_y - 60, f"{get_translation('isr', country)}: {format_currency(payroll_dto.taxes_discount_amount)}")
    c.drawString(right_col, top_y - 80, f"{get_translation('others', country)}: {format_currency(payroll_dto.other_discount)}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(right_col, top_y - 100, f"Total: {format_currency(payroll_dto.total)}")

    c.save()
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value
