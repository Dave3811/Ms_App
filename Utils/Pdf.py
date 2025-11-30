from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def generate_estimation_pdf(data: dict) -> bytes:
    template = env.get_template("estimations.html")
    html = template.render(**data)

    pdf = HTML(string=html).write_pdf()

    return pdf
