import pdfkit
from jinja2 import Environment, FileSystemLoader
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

WKHTML_PATH = "/usr/bin/wkhtmltopdf"

config = pdfkit.configuration(wkhtmltopdf=WKHTML_PATH)


def generate_estimation_pdf(data: dict) -> bytes:
    template = env.get_template("estimations.html")
    html = template.render(**data)

    pdf_bytes = pdfkit.from_string(html, False, configuration=config)

    return pdf_bytes
