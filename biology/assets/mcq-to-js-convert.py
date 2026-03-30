#!/usr/bin/env python3
"""
mcq-to-js-convert.py
Usage: python3 mcq-to-js-convert.py <file1.txt> <file2.txt> ...

Reads each *_MCQs.txt JSON file, merges all chapters into
biology/assets/mcq-data.js (same directory as this script).

Chapter name is derived from the filename:
  The_Living_World_MCQs.txt  ->  The Living World
"""

import json
import os
import sys


def name_from_file(path):
    base = os.path.basename(path)
    name = base
    for suffix in ('_MCQs.txt', '_mcqs.txt', '_MCQ.txt', '_mcq.txt', '.txt'):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name.replace('_', ' ')


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 mcq-to-js-convert.py <file1.txt> [file2.txt ...]')
        sys.exit(1)

    chapters = []
    for path in sys.argv[1:]:
        path = os.path.abspath(path)
        if not os.path.isfile(path):
            print(f'Warning: file not found, skipping — {path}')
            continue
        with open(path, encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f'Warning: JSON parse error in {path}, skipping — {e}')
                continue
        questions = data if isinstance(data, list) else []
        chapter_name = name_from_file(path)
        chapters.append({'name': chapter_name, 'questions': questions})
        print(f'  Loaded: {chapter_name!r}  ({len(questions)} questions)')

    if not chapters:
        print('No valid files loaded. Aborting.')
        sys.exit(1)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcq-data.js')
    js = 'const MCQ_DATA = ' + json.dumps(chapters, ensure_ascii=False, indent=2) + ';\n'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(js)

    print(f'\nWrote {len(chapters)} chapter(s) -> {out_path}')


if __name__ == '__main__':
    main()
