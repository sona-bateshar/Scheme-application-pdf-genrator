from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor

def add_header_section(story, data):
    styles = getSampleStyleSheet()

    # ---------- Styles ----------
    company_style = ParagraphStyle(
        name="company",
        parent=styles["Normal"],
        fontSize=12,
        leading=14,
        textColor="#1f2937",  # dark grey
    )

    scheme_title_style = ParagraphStyle(
        name="scheme_title",
        parent=styles["Heading1"],
        fontSize=18,
        leading=20,
        textColor="#1f2937",
    )

    address_style = ParagraphStyle(
        name="address",
        parent=styles["Normal"],
        fontSize=10,
        leading=12,
        textColor="#374151",
    )

    right_label_style = ParagraphStyle(
        name="right_label",
        parent=styles["Normal"],
        fontSize=10,
        alignment=2,  # right align
        textColor="#1f2937",
    )

    # ---------- Left Section ----------
    left_column = [
        Paragraph(data["scheme_company"], company_style),
        Spacer(1, 4),
        Paragraph(data["scheme_name"], scheme_title_style),
        Spacer(1, 2),
        Paragraph(data["scheme_address"], address_style),
    ]

    # ---------- Right Section ----------
    right_column = [
        Paragraph(f"Date - {data['application_submission_date']}", right_label_style),
        Spacer(1, 4),
        Paragraph(f"Application ID - {data['application_number']}", right_label_style),
    ]

    # Combine into a 2-column table
    header_table = Table(
        [[left_column, right_column]],
        colWidths=[350, 150]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 12))

    # ---------- Bottom Separator Line ----------
    line = Table(
        [[""]],
        colWidths=[500],
        style=[
            ('LINEBELOW', (0, 0), (-1, -1), 1, HexColor("#1f2937"))
        ]
    )
    story.append(line)
    story.append(Spacer(1, 12))



def generate_acknowledgement_pdf(data: dict) -> bytes:
    """
    Generates a PDF acknowledgement slip using ReportLab based on the input data dictionary.

    Args:
        data: A dictionary containing all the necessary application and payment details.

    Returns:
        The raw bytes content of the generated PDF file.
    """
    # 1. Setup
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=40, rightMargin=40,
                            topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    story = []

    add_header_section(story, data)
    
    # Define a style for data labels (bold, smaller)
    label_style = styles['Code']
    label_style.fontSize = 8
    label_style.alignment = 0 # Left
    
    # Define a style for data values (regular, normal size)
    value_style = styles['Normal']
    value_style.fontSize = 10
    value_style.alignment = 0 # Left

    # Helper function to create a key-value row
    def create_data_row(label, value):
        return [
            Paragraph(label, label_style),
            Paragraph(str(value), value_style)
        ]

    # --- 3. Main Content Table Style (Used for all sections) ---
    section_style = TableStyle([
        # Grid lines
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        # Column 0 (Label) has light background
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        # Padding
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        # Alignment for labels
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        # Alignment for values
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ])

    # --- 4. Applicant Details Section ---
    story.append(Paragraph("<b>1. Applicant Details</b>", styles['Heading4']))
    story.append(Spacer(1, 6))

    applicant_data = [
        create_data_row("APPLICANT NAME", data['applicant_name']),
        create_data_row("FATHER/HUSBAND NAME", data['father_or_husband_name']),
        create_data_row("DATE OF BIRTH", data['dob']),
        create_data_row("MOBILE NUMBER", data['mobile_number']),
        create_data_row("ID TYPE", data['id_type']),
        create_data_row("ID NUMBER", data['id_number']),
        create_data_row("AADHAR NUMBER", data['aadhar_number']),
        create_data_row("POSTAL ADDRESS", f"{data['postal_address']}, {data['postal_address_pincode']}"),
        create_data_row("PERMANENT ADDRESS", f"{data['permanent_address']}, {data['permanent_address_pincode']}"),
    ]
    
    applicant_table = Table(applicant_data, colWidths=[doc.width * 0.35, doc.width * 0.65])
    applicant_table.setStyle(section_style)
    story.append(applicant_table)
    story.append(Spacer(1, 12))

    # --- 5. Income & Category Section ---
    story.append(Paragraph("<b>2. Income & Category</b>", styles['Heading4']))
    story.append(Spacer(1, 6))

    income_data = [
        create_data_row("ANNUAL INCOME RANGE", data['annual_income']),
        create_data_row("PLOT CATEGORY", data['plot_category']),
        create_data_row("REGISTRATION FEES", f"Rs. {data['registration_fees']:,.2f}"),
        create_data_row("PROCESSING FEES", f"Rs. {data['processing_fees']:,.2f}"),
        create_data_row("TOTAL PAYABLE AMOUNT", f"Rs. {data['total_payable_amount']:,.2f}"),
    ]

    income_table = Table(income_data, colWidths=[doc.width * 0.35, doc.width * 0.65])
    income_table.setStyle(section_style)
    story.append(income_table)
    story.append(Spacer(1, 12))

    # --- 6. Payment Details Section ---
    story.append(Paragraph("<b>3. Payment Details</b>", styles['Heading4']))
    story.append(Spacer(1, 6))

    payment_data = [
        create_data_row("PAYMENT MODE", data['payment_mode']),
        create_data_row("TRANSACTION/DD DATE", data['dd_date_or_transaction_date']),
        create_data_row("TRANSACTION/DD NUMBER", data['dd_id_or_transaction_id']),
        create_data_row("TRANSACTION/DD AMOUNT", f"Rs. {data['dd_amount_or_transaction_amount']:,.2f}"),
        create_data_row("ACCOUNT HOLDER NAME", data['payer_account_holder_name']),
        create_data_row("BANK NAME", data['payer_bank_name']),
    ]

    payment_table = Table(payment_data, colWidths=[doc.width * 0.35, doc.width * 0.65])
    payment_table.setStyle(section_style)
    story.append(payment_table)
    story.append(Spacer(1, 24))

    # --- 7. Footer ---
    footer_text = f"Printed: {data['print_date']}"
    story.append(Paragraph(footer_text, styles['Normal']))

    # 8. Build the document and return bytes
    doc.build(story)
    
    # Rewind the buffer and return its content
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content
