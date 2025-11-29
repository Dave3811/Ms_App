from jinja2 import Template
from weasyprint import HTML
from io import BytesIO


def render_html_template(template_path, data):
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    return template.render(**data)


# ---------- ESTIMATION ----------
def generate_estimation_pdf(data: dict) -> bytes:
    html_rendered = render_html_template(
        "utils/templates/estimation.html",
        data
    )

    buffer = BytesIO()
    HTML(string=html_rendered).write_pdf(buffer)
    buffer.seek(0)

    return buffer.read()


# ---------- FACTURE ----------
def generate_facture_pdf(data: dict) -> bytes:
    html_rendered = render_html_template(
        "utils/templates/facture.html",
        data
    )

    buffer = BytesIO()
    HTML(string=html_rendered).write_pdf(buffer)
    buffer.seek(0)

    return buffer.read()
