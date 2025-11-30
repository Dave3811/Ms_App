from jinja2 import Environment, FileSystemLoader
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def generate_estimation_html(data: dict) -> str:
    template = env.get_template("estimations.html")
    html = template.render(**data)
    return html
