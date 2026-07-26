#!/usr/bin/env python3
"""Отправляет Markdown-рецепт в Notes.app (только macOS).

Использование:
    python3 save_to_notes.py recipe.md ["Имя папки в Notes"]

Notes.app не понимает Markdown, поэтому файл сначала конвертируется
в минимальный HTML: заголовки, списки, ссылки, абзацы. Этого достаточно
для рецепта и не требует внешних зависимостей.
"""

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

APPLESCRIPT = """
on run argv
    set htmlPath to item 1 of argv
    set folderName to item 2 of argv
    set noteBody to (read (POSIX file htmlPath as alias) as \u00abclass utf8\u00bb)
    tell application "Notes"
        if folderName is "" then
            make new note with properties {body:noteBody}
        else
            if not (exists folder folderName) then
                error "NOFOLDER"
            end if
            tell folder folderName
                make new note with properties {body:noteBody}
            end tell
        end if
    end tell
end run
"""


def inline(text: str) -> str:
    """Экранирует HTML и разбирает **жирный**, *курсив* и [ссылки](url)."""
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"<i>\1</i>", text)
    return text


def markdown_to_html(md: str) -> str:
    out: list[str] = []
    list_tag: str | None = None

    def close_list() -> None:
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>")
            list_tag = None

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            close_list()
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            close_list()
            level = min(len(heading.group(1)) + 1, 6)
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            continue

        bullet = re.match(r"^\s*[-*+]\s+(.*)$", line)
        if bullet:
            if list_tag != "ul":
                close_list()
                out.append("<ul>")
                list_tag = "ul"
            out.append(f"<li>{inline(bullet.group(1))}</li>")
            continue

        numbered = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        if numbered:
            if list_tag != "ol":
                close_list()
                out.append("<ol>")
                list_tag = "ol"
            out.append(f"<li>{inline(numbered.group(1))}</li>")
            continue

        close_list()
        out.append(f"<div>{inline(line)}</div>")

    close_list()
    return "\n".join(out)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    if sys.platform != "darwin":
        print(
            "Notes.app доступен только на macOS. Здесь можно отдать пользователю .md файл.",
            file=sys.stderr,
        )
        return 3

    source = Path(sys.argv[1])
    if not source.is_file():
        print(f"Файл не найден: {source}", file=sys.stderr)
        return 4

    folder = sys.argv[2] if len(sys.argv) > 2 else ""
    body = markdown_to_html(source.read_text(encoding="utf-8"))

    with tempfile.NamedTemporaryFile(
        "w", suffix=".html", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(body)
        tmp_path = tmp.name

    result = subprocess.run(
        ["osascript", "-", tmp_path, folder],
        input=APPLESCRIPT,
        capture_output=True,
        text=True,
    )
    Path(tmp_path).unlink(missing_ok=True)

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "NOFOLDER" in stderr:
            print(
                f"Папки «{folder}» нет в Notes. Создай её вручную или запусти без имени папки.",
                file=sys.stderr,
            )
        else:
            print(f"AppleScript вернул ошибку: {stderr}", file=sys.stderr)
        return 1

    where = f"в папку «{folder}»" if folder else "в папку по умолчанию"
    print(f"Заметка создана {where}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
