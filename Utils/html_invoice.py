from pathlib import Path
import tempfile
import base64


def embed_image_base64(img_path):
    img_file = Path(img_path)

    if not img_file.exists():
        return ""

    encoded = base64.b64encode(img_file.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def generate_invoice_html(template_path, replacements):

    project_root = Path.cwd()
    template_file = project_root / template_path

    if not template_file.exists():
        raise FileNotFoundError(f"Template introuvable: {template_file}")

    html = template_file.read_text(encoding="utf-8")

    # --- EMBED LOGO ---
    logo_base64 = embed_image_base64("assets/logo.png")
    html = html.replace(
        '<img src="assets/logo.png" alt="Logo entreprise">',
        f'<img src="{logo_base64}" alt="Logo entreprise">'
    )

    # --- REMPLACES VARIABLES ---
    for key, val in replacements.items():
        html = html.replace(f"{{{{{key}}}}}", str(val))

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")

    with open(tmp.name, "w", encoding="utf-8") as f:
        f.write(html)

    return tmp.name