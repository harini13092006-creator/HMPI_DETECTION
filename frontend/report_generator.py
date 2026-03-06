from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(df):

    file = "pollution_report.pdf"

    c = canvas.Canvas(file, pagesize=letter)

    c.setFont("Helvetica",14)
    c.drawString(200,750,"Heavy Metal Pollution Report")

    y = 700

    for i,row in df.iterrows():

        text = f"{row['Location']}  HMPI:{round(row['HMPI'],2)}  Risk:{row['Risk']}"

        c.drawString(50,y,text)

        y -= 20

        if y < 100:
            c.showPage()
            y = 700

    c.save()

    return file

