from pathlib import Path
import tempfile


def generate_invoice_html(template_path, replacements):

    # On force la racine du projet, peu importe où Streamlit démarre
    project_root = Path(__file__).resolve().parents[1]

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
