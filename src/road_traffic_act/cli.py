import re

import typer

app = typer.Typer()
from road_traffic_act._main import LAW_ID, get_xml

from ._main import format


@app.command()
def search(regex: str) -> None:
    """Find articles matching the regular expression."""

    for name, id in LAW_ID.items():
        xml = get_xml(id)
        for article in xml.findall(".//Article"):
            if re.search(regex, format(article)):
                print(f"{name}\n{format(article)}")
