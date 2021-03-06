from fpdf import FPDF
from datetime import datetime


def create_invoice_pdf(INVOICE, DETAILS, FILEPATH, SETTINGS):

    NAME = str(SETTINGS["pdf_title"])
    ADDRESS = str(SETTINGS["pdf_address"])
    GST_NO = str(SETTINGS["pdf_gst_no"])

    pdf = FPDF('P', 'mm', 'A4')
    FILENAME = "Invoice" + "_" + \
        INVOICE['name'] + '_id_' + str(INVOICE['invoice_no']) + '_' +\
        datetime.now().strftime('%d-%m-%Y%H%S') + '_' + ".pdf"

    # Add new page. Without this you cannot create the document.
    pdf.add_page()

    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(200, 6, txt=NAME, align='C', fill=False)
    pdf.ln(2)

    pdf.set_font('Arial', '', 10.0)
    pdf.text(
        x=50, y=22, txt=ADDRESS)

    pdf.set_font('Arial', 'B', 10.0)
    pdf.text(x=78, y=30, txt=f'GST No. : {GST_NO}')

    pdf.line(10, 35, 200, 35)

    pdf.set_font('Arial', 'B', 12.0)
    pdf.text(x=90, y=43, txt='TAX INVOICE')

    pdf.line(10, 48, 200, 48)
    pdf.line(105, 58, 200, 58)

    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=15, y=64, txt='Invoice Number: ')
    pdf.text(x=60, y=64, txt=str(INVOICE["invoice_no"]))

    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=15, y=72, txt='Invoice Date:')
    pdf.text(x=60, y=72, txt=str(INVOICE["invoice_date"].strftime("%d/%m/%Y")))

    pdf.set_font('Arial', 'B', 9.0)
    reverse_charges = 'Yes' if INVOICE["reverse_charges"] else "No"
    pdf.text(x=15, y=80, txt='Reverse Charges (Y/N): ')
    pdf.text(x=60, y=80, txt=str(reverse_charges))

    pdf.set_font('Arial', 'B', 9.0)
    state = INVOICE['state']
    pdf.text(x=15, y=88, txt='State: ')
    pdf.text(x=30, y=88, txt=str(state))

    pdf.set_font('Arial', 'B', 9.0)
    code = INVOICE['state_code']
    pdf.text(x=60, y=88, txt='Code: ')
    pdf.text(x=75, y=88, txt=str(code))

    # Vertical Line
    pdf.line(105, 48, 105, 94)
    pdf.line(10, 48, 10, 94)
    pdf.line(200, 48, 200, 94)

    ''' Right side bill to party '''
    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=143, y=54, txt='BILL TO PARTY')

    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=115, y=64, txt='Name: ')
    pdf.set_font('Arial', '', 9.0)
    pdf.text(x=130, y=64, txt=str(INVOICE["name"]))

    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=115, y=70, txt='Address:')  # Address
    pdf.ln(56)
    pdf.cell(120, 6, "")
    pdf.set_font('Arial', '', 9.0)
    pdf.multi_cell(w=70, h=2, txt=str(INVOICE['address']),
                   align="L", fill=False, border=0)

    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=115, y=82, txt='GSTIN No: ')
    pdf.set_font('Arial', '', 9.0)
    pdf.text(x=160, y=82, txt=str(INVOICE["gst"]))

    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=115, y=88, txt='State: ')
    pdf.set_font('Arial', '', 9.0)
    pdf.text(x=130, y=88, txt=str(INVOICE["party_state"]))

    pdf.set_font('Arial', 'B', 9.0)
    pdf.text(x=160, y=88, txt='Code: ')
    pdf.set_font('Arial', '', 9.0)
    pdf.text(x=175, y=88, txt=str(INVOICE["party_code"]))

    pdf.ln(24)
    pdf.cell(190, 6, "", border="T", fill=None)

    ''' Table '''
    deets_w = {'Sr_No': 5.5, 'hsn': 8, 'prod': 20, 'batch_no': 8, 'mfg_date': 9, 'qty': 9, 'size': 8,
               'rate': 7, 'mrp': 7, 'taxable_amt': 14}
    pdf.ln(6)
    pdf.set_font('Times', 'IB', 9.0)
    for ii in deets_w:
        pdf.cell(deets_w[ii] * 2, 6, str(ii).replace("_",
                                                     " ").title(), border=1, align='C', fill=False)
    pdf.ln(2)

    pdf.set_font('Arial', '', 9.0)
    for row in DETAILS:  # sets no. of rows
        pdf.ln(4)
        for field in deets_w:  # sets no. of cols
            pdf.cell(deets_w[field] * 2, 6, str(row[field]),
                     border=1, align='C', fill=False)
        pdf.ln(2)

    pdf.ln(10)

    pdf.set_font('Times', 'B', 9.0)
    pdf.multi_cell(90, 6, 'Total Rs. in Words: ' +
                   str(INVOICE["rupees_in_words"]), border=0, align='L', fill=False)
    pdf.cell(20, 6, '', border=0, align='L', fill=False)

    pdf.set_font('Times', '', 9.0)
    pdf.ln(6)

    pdf.cell(90, 6, 'AYURVEDIC PROP. MEDICINE',
             border="BT", align='C', fill=False)
    pdf.cell(20, 6, '', border=0, align='L', fill=False)
    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(40, 6, 'Total before Tax:', border=1, align='L', fill=False)
    pdf.set_font('Arial', '', 9.0)
    pdf.cell(40, 6, str(INVOICE["total_before_tax"]),
             border=1, align='C', fill=False)

    pdf.ln(6)

    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(90, 6, "Bank Name: " +
             str(INVOICE["bank_name"]), border=0, align='L', fill=False)
    pdf.cell(20, 6, '', border=0, align='L', fill=False)
    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(40, 6, 'CGST', border=1, align='L', fill=False)
    pdf.set_font('Arial', '', 9.0)
    pdf.cell(40, 6, str(INVOICE["total_cgst"]),
             border=1, align='C', fill=False)

    pdf.ln(6)

    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(90, 6, "Account No.:: " +
             str(INVOICE["account_no"]), border=0, align='L', fill=False)
    pdf.cell(20, 6, '', border=0, align='L', fill=False)
    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(40, 6, 'SGST', border=1, align='L', fill=False)
    pdf.set_font('Arial', '', 9.0)
    pdf.cell(40, 6, str(INVOICE["total_sgst"]),
             border=1, align='C', fill=False)

    pdf.ln(6)

    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(90, 6, "IFSC Code:" +
             str(INVOICE["ifsc"]), border=0, align='L', fill=False)
    pdf.cell(20, 6, '', border=0, align='L', fill=False)
    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(40, 6, 'IGST', border=1, align='L', fill=False)
    pdf.set_font('Arial', '', 9.0)
    pdf.cell(40, 6, str(INVOICE["total_igst"]),
             border=1, align='C', fill=False)

    pdf.ln(6)

    pdf.set_font('Times', 'IB', 9.0)
    pdf.cell(90, 6, "Goods once sold cannot be returned or replaced",
             border="T", align='C', fill=False)
    pdf.cell(20, 6, '', border=0, align='L', fill=False)

    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(40, 6, 'Total Tax Amount:', border=1, align='L', fill=False)
    pdf.set_font('Arial', '', 9.0)
    pdf.cell(40, 6, str(INVOICE["total_tax_amt"]),
             border=1, align='C', fill=False)

    pdf.ln(6)

    pdf.cell(90, 6, "", border=0, align='C', fill=False)
    pdf.cell(20, 6, '', border=0, align='L', fill=False)

    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(40, 6, 'Total after Tax:', border=1, align='L', fill=False)
    pdf.set_font('Arial', '', 9.0)
    pdf.cell(40, 6, str(INVOICE["total_after_tax"]),
             border=1, align='C', fill=False)

    pdf.ln(6)

    pdf.cell(90, 6, "", border=0, align='C', fill=False)
    pdf.cell(20, 6, '', border=0, align='L', fill=False)

    pdf.set_font('Arial', 'B', 9.0)
    pdf.cell(40, 6, 'GST Reverse Charges:', border=1, align='L', fill=False)
    pdf.set_font('Arial', '', 9.0)
    pdf.cell(40, 6, str(INVOICE["gst_reverse_charge"]),
             border=1, align='C', fill=False)

    pdf.ln(12)

    pdf.set_font('Times', 'IB', 9.0)
    sign_text = f'For {NAME.title()}'
    pdf.cell(190, 6, sign_text, align="R", fill=False)

    pdf.ln(18)

    pdf.set_font('Times', 'B', 8.0)
    pdf.cell(130, 6, 'E & O.E.', align="R", fill=False)

    pdf.cell(60, 6, 'Authorized Signature', align="R", fill=False)

    pdf.ln(6)
    pdf.cell(190, 6, "", align="C", border="T", fill=False)

    try:
        pdf.output(FILEPATH + "/" + FILENAME, 'F')
        print("Created PDF.")
        return True
    except Exception as e:
        print(e)
        return False
