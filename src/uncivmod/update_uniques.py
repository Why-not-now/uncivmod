from __future__ import annotations

import re

import requests


def main():
    unique_files = requests.get(
        "https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/UniqueType.kt",
        timeout=10,
    )
    uniques = re.search(r"", unique_files.text)


if __name__ == "__main__":
    main()
