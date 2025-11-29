from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_estimation_pdf(data: dict) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    y = height - 40
    line_height = 18

    def draw(label, value):
        nonlocal y
        c.drawString(40, y, f"{label}: {value}")
        y -= line_height

    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, y, "ESTIMATION")
    y -= 40

    c.setFont("Helvetica", 11)

    draw("Numéro", data["numero"])
    draw("Date", data["date_estimation"])
    draw("Ajouté par", data["utilisateur"])

    y -= 20

    draw("Client", data["client"])
    draw("Adresse", data["adresse"])
    draw("Téléphone", data["telephone"])
    draw("Courriel", data["couriel"])

    y -= 20

    draw("Service", data["service"])
    draw("Superficie", data["superficie"])
    draw("Description", data["description"])

    y -= 20

    draw("Travail", f'{data["montant"]}$')
    draw("Extras", f'{data["extraprix"]}$')
    draw("Taxes", f'{data["taxes"]}$')
    draw("Total", f'{data["total"]}$')

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()
