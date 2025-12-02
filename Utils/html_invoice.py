from pathlib import Path
import tempfile


def generate_invoice_html(template_path, replacements):

    # Racine du projet = le dossier où se trouve app.py
    project_root = Path.cwd()

    template_file = project_root / template_path

    if not template_file.exists():
        raise FileNotFoundError(f"Template introuvable: {template_file}")

    html = template_file.read_text(encoding="utf-8")

    for key, val in replacements.items():
        html = html.replace(f"{{{{{key}}}}}", str(val))

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")

    with open(tmp.name, "w", encoding="utf-8") as f:
        f.write(html)

    return tmp.name
