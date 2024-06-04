
import subprocess
try:
    import inquirer
except ImportError:
    subprocess.run(["pip", "install", "inquirer"])
    import inquirer

try:
    import reportlab
except ImportError:
    subprocess.run(["pip", "install", "reportlab"])
    import reportlab

try:
    import pymongo
    #print("Pymongo is there")
except ImportError:
    subprocess.run(["pip", "install", "pymongo"])
    import pymongo


# Now you can import and use the installed packages
from pymongo import MongoClient

from inquirer import questions, Text, List
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors




from reportlab.lib.colors import Color
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from input_module import collect_input
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['KEPL']
collection = db['Interns']

def insert_data_to_mongodb(answers):
    try:
        document_count = collection.count_documents({})
        file_number = document_count + 1
        answers['File'] = f"{file_number:03d}"
        collection.insert_one(answers)
        return file_number
    
    except Exception as e:
        print(f"Error inserting data to MongoDB: {e}")
        return None




def generate_offer_letter(answers):

    #declaring variables
    res = {"Enterprise Applications":"To develop enterprise tools for the company",
           "UI/UX":"To develop the user interface for company products",
           "DevOps":"To build and maintain CI/CD infrastructure"}
    filename = f"offerletter_{file_number}.pdf" 
    title = 'Internship Offer Letter'
    salutation = 'Dear'
    letterBody1 = f"In response to your application referenced above, after verifying your academic credentials, I am\npleased to offer you an internship opportunity in the {answers['Practice']} practice at Koyya\nEnterprises Private Limited, Bengaluru. Below is your internship schedule."
    letterBody2 = """Please mail us your acceptance of this offer before the start date of the internship without which this offer will be null and void. We will be sending the induction instructions once we receive your acceptance mail."""
    closing = 'For Koyya Enterprises Private Limited'
    signature1 = 'Krishna Mohan Koyya'
    signature2 = 'Managing Director'
    logo = 'logo.png'
    sign = 'signature.png'
   
    # Creating a canvas
    w, h = A4
    pdf = canvas.Canvas(filename, pagesize=A4)
    pdf.setTitle(title)
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawCentredString(w / 2, h - 120, title)
    mycolor = Color(0.5, 0.5, 0.5, alpha=0.25)
    
    # Draw your logo
    try:
        pdf.drawInlineImage(logo, 60, h - 80)
    except Exception as e:
        print(f"Error drawing logo: {e}")
    
    # Table 1
    data = [
        ["File Number", f"KEPL/2024-25/HR/{answers['File']}                                                                        ", "Date ", answers['Offer_date']],
        ["To", f"{answers['Name']} {answers['Surname']}"],
        [" " , f"{answers['Address']}\n{answers['City']}\n\nEmail: {answers['Email']}\nPhone Number: {answers['Contact']}"],
        ["Reference", f"Your Application dated {answers['App_date']}"]
    ]

    table1 = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), mycolor),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
        ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica'),
    ])
    

    table1.setStyle(style)
    table1.wrapOn(pdf, w, h)
    table1.drawOn(pdf, x=60, y=h - 250)
    
    # Letter Body 1
    pdf.setFont('Helvetica', 11)
    pdf.drawString(60, h - 280, f"{salutation} {answers['Title']} {answers['Name']},")
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontSize = 11
    style.leftIndent = 60
    style.rightIndent = 60
    letterbody1 = Paragraph(letterBody1, style)
    letterbody1.wrapOn(pdf, w, h)
    letterbody1.drawOn(pdf, 0, h - 330)

    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawCentredString(w / 2, h - 360, "Schedule")
    
    # Table 2
    data2 = [
        ["Name", f"{answers['Name']} {answers['Surname']}", "Identity", f"{answers['Aadhar']}         "],
        ["Position", answers['Position'], "Place of Work", answers['Place']],
        ["Responsibilities", res[answers['Practice']]],
        ["Effort", f"{answers['Effort']} Hours a week (Monday to Friday)", "Stipend", answers['Stipend']],
        ["From", answers['Start_date'], "To", answers['End_date']]
    ]

    table2 = Table(data2)
    style2 = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), mycolor),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
        ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),
        ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
        ('FONTNAME', (0, 4), (0, 4), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
        ('FONTNAME', (2, 1), (2, 1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 2), (2, 2), 'Helvetica-Bold'),
        ('FONTNAME', (2, 3), (2, 3), 'Helvetica-Bold'),
        ('FONTNAME', (2, 4), (2, 4), 'Helvetica-Bold'),
    ])

    table2.setStyle(style2)
    table2.wrapOn(pdf, w, h)
    table2.drawOn(pdf, x=60, y=h - 460)
    
    # Letter Body 2
    letterbody2 = Paragraph(letterBody2, style)
    letterbody2.wrapOn(pdf, w, h)
    letterbody2.drawOn(pdf, 0, h - 510)

    pdf.setFont('Helvetica', 11)
    pdf.drawString(60, h - 560, closing)

    # Draw your signature
    try:
        pdf.drawInlineImage(sign, 60, h - 620)
    except Exception as e:
        print(f"Error drawing signature: {e}")
    
    pdf.drawString(60, h - 630, signature1)
    pdf.drawString(60, h - 645, signature2)

    pdf.save()
    print(f"Offer letter generated successfully: {filename}")

# Call the function 
if __name__ == "__main__":
    print("Application Started")
    
    answers = collect_input()
    file_number = insert_data_to_mongodb(answers)

    if file_number is not None:
        print(file_number)
        generate_offer_letter(answers)
    
    
    
    
