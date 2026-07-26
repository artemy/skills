#!/usr/bin/env python3
"""Сверяет числа готового рецепта с текстом источника.

Использование:
    python3 check_numbers.py recipe.md source.txt

Идея простая: в правильно оформленном рецепте любое число либо взято
из источника напрямую, либо является пересчётом числа, которое стоит
рядом в скобках (`240 мл (1 cup)`). Значит, всё, что не находится
в источнике и не имеет оригинала в скобках, — кандидат в отсебятину.

Скрипт ничего не доказывает, он лишь сокращает область ручной проверки.
Ложные срабатывания нормальны: номера шагов, части диапазонов,
числа, записанные в источнике словами.
"""

import re
import sys
import unicodedata
from pathlib import Path

NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
# `240 мл (1 cup)` — число в скобках считается заявленным оригиналом
WITH_ORIGINAL = re.compile(r"(\d+(?:[.,]\d+)?)\s*[^()\n]{0,20}?\(([^)]*?\d[^)]*?)\)")
SKIP_SECTIONS = ("дополнительные заметки", "источник")


def normalize(value: str) -> str:
    """`1,50` и `1.5` — одно и то же число; целые не трогаем."""
    value = value.replace(",", ".")
    if "." in value:
        value = value.rstrip("0").rstrip(".")
    return value or "0"


def numbers_in(text: str) -> set[str]:
    return {normalize(m.group()) for m in NUMBER.finditer(text)}


def strip_numbering(line: str) -> str:
    """Убирает номер шага в начале строки — он не из источника."""
    return re.sub(r"^\s*\d+[.)]\s+", "", line)


def relevant_lines(md: str) -> list[tuple[int, str]]:
    """Строки разделов «Ингредиенты» и «Рецепт»; заметки и источник пропускаем."""
    lines: list[tuple[int, str]] = []
    active = False
    for i, raw in enumerate(md.splitlines(), start=1):
        heading = re.match(r"^#{1,6}\s+(.*)$", raw)
        if heading:
            title = heading.group(1).strip().lower()
            active = any(k in title for k in ("ингредиент", "рецепт", "порц"))
            if any(title.startswith(s) for s in SKIP_SECTIONS):
                active = False
            continue
        if raw.strip().lower().startswith(SKIP_SECTIONS):
            active = False
            continue
        if active and raw.strip():
            lines.append((i, raw))
    return lines


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2

    recipe_path, source_path = Path(sys.argv[1]), Path(sys.argv[2])
    for path in (recipe_path, source_path):
        if not path.is_file():
            print(f"Файл не найден: {path}", file=sys.stderr)
            return 4

    recipe = unicodedata.normalize("NFKC", recipe_path.read_text(encoding="utf-8"))
    source_numbers = numbers_in(
        unicodedata.normalize("NFKC", source_path.read_text(encoding="utf-8"))
    )

    findings: list[tuple[int, str, str]] = []
    for lineno, raw in relevant_lines(recipe):
        line = strip_numbering(raw)

        # Числа, для которых рядом указан оригинал в скобках,
        # проверяются по оригиналу, а не по пересчитанному значению.
        handled: set[str] = set()
        for match in WITH_ORIGINAL.finditer(line):
            metric = normalize(match.group(1))
            original = numbers_in(match.group(2))
            handled.add(metric)
            handled |= original
            if not original & source_numbers:
                findings.append(
                    (lineno, ", ".join(sorted(original)), "оригинала нет в источнике")
                )

        for value in numbers_in(line) - handled:
            if value not in source_numbers:
                findings.append((lineno, value, "нет в источнике"))

    if not findings:
        print("Все числа прослеживаются до источника.")
        return 0

    print(f"Требуют проверки ({len(findings)}):")
    for lineno, value, reason in findings:
        print(f"  строка {lineno}: {value} — {reason}")
    print("\nЧасть срабатываний может быть законной (диапазоны, числа словами).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
