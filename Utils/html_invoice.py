from pathlib import Path
import tempfile


def generate_invoice_html(template_path, replacements):

    # Résout chemin ABSOLU en partant de la racine du projet
    root = Path(__file__).resolve().parent.parent
    template_file = root / template_path

    html = template_file.read_text(encoding="utf-8")

    for key, value in replacements.items():
        html = html.replace(f"{{{{{key}}}}}", str(value))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")

    with open(temp_file.name, "w", encoding="utf-8") as f:
        f.write(html)

    return temp_file.name
