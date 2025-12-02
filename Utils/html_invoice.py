from pathlib import Path
import tempfile


def generate_invoice_html(template_path, replacements):

    html = Path(template_path).read_text(encoding="utf-8")

    for tag, value in replacements.items():
        html = html.replace(f"{{{{{tag}}}}}", str(value))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")

    with open(temp_file.name, "w", encoding="utf-8") as f:
        f.write(html)

    return temp_file.name
