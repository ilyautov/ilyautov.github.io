#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Карта сайта витрины: lastmod берётся из git, а не пишется руками.

Дата, которую правит человек, отстаёт молча. У этой карты она отстала на двое
суток: страницы изменились 14.09, а в карте стояло 12.09, и поисковик читал
её как «ничего не менялось».

    python3 scripts/build_sitemap.py            # записать
    python3 scripts/build_sitemap.py --check    # сверить, ничего не трогая
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://ilyautov.github.io"
# Приоритет и частота обхода это подсказка, а не факт из файла, поэтому живут
# здесь: главная важнее разделов, разделы важнее карточек проектов.
PAGES = [
    ("index.html", "/", "1.0"),
    ("mcp-i-skilly/index.html", "/mcp-i-skilly/", "0.8"),
    ("doc2md/index.html", "/doc2md/", "0.7"),
    ("rusvoice/index.html", "/rusvoice/", "0.7"),
    ("schema-mcp-core/index.html", "/schema-mcp-core/", "0.7"),
]


def last_commit(path: str) -> str:
    """Дата последнего коммита файла. Рабочая копия грязная — берём сегодня:
    иначе карта пообещает дату, которой у выложенной страницы ещё нет."""
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                         cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.strip() or "1970-01-01"


def build() -> str:
    body = "\n".join(
        f"  <url>\n    <loc>{SITE}{url}</loc>\n"
        f"    <lastmod>{last_commit(path)}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n    <priority>{pri}</priority>\n  </url>"
        for path, url, pri in PAGES
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    target = ROOT / "sitemap.xml"
    fresh = build()
    if a.check:
        if not target.exists() or target.read_text(encoding="utf-8") != fresh:
            print("карта сайта разошлась с датами коммитов", file=sys.stderr)
            sys.exit(1)
        print("карта сайта совпадает с датами коммитов")
        return
    target.write_text(fresh, encoding="utf-8")
    print(f"записано: sitemap.xml ({len(PAGES)} адресов)")


if __name__ == "__main__":
    main()
