from functools import cache
from pathlib import Path

from lxml import etree

CACHE_FOLDER = Path("~/.cache/road_traffic_act").expanduser()
LAW_ID = {
    "道路交通法": "335AC0000000105",
    "道路交通法施行令": "335CO0000000270",
    "道路交通法施行規則": "335M50000002060",
    "自動車の保管場所の確保等に関する法律": "337AC0000000145",
    "道路運送車両法": "326AC0000000185",
    "道路運送車両の保安基準": "326M50000800067",
    "車両制限令": "336CO0000000265",
    "自動車損害賠償保障法": "330AC0000000097",
    "高速自動車国道法": "332AC0000000079",
    "自動車点検基準": "326M50000800070",
    "自動車の運転により人を死傷させる行為等の処罰に関する法律": "425AC0000000086",
}


def _prepare() -> None:
    from subprocess import run

    if not (CACHE_FOLDER / "elaws-history").exists():
        CACHE_FOLDER.mkdir(parents=True, exist_ok=True)
        run(
            ["git", "clone", "https://github.com/kissge/elaws-history.git"],
            cwd=CACHE_FOLDER.as_posix(),
            check=True,
        )
    run(["git", "pull"], cwd=(CACHE_FOLDER / "elaws-history").as_posix(), check=True)


@cache
def _get_content(id: str) -> str:
    _prepare()
    directory = CACHE_FOLDER / "elaws-history" / "all_xml" / id[:3]
    candidates = list(directory.rglob(f"{id}_*.xml"))
    if not candidates:
        raise FileNotFoundError(f"No XML file found for ID {id} in cache.")
    return candidates[-1].read_text(encoding="utf-8")


def get_xml(id: str) -> etree._Element:
    conotrent = _get_content(id)
    return etree.fromstring(conotrent.encode("utf-8"))
