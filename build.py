#!/usr/bin/env python3
"""
YARC - Yet Another Runeword Calculator
build.py - Compile yarc_seed.sql → yarc.db → yarc_standalone.html
Usage: python build.py
"""

import sqlite3
import base64
import sys
import os

# ── Paths ──
ROOT        = os.path.dirname(os.path.abspath(__file__))
SQL_FILE    = os.path.join(ROOT, 'yarc_seed.sql')
DB_FILE     = os.path.join(ROOT, 'yarc.db')
HTML_TPL    = os.path.join(ROOT, 'yarc.html')
HTML_OUT    = os.path.join(ROOT, 'yarc_standalone.html')

DB_PLACEHOLDER = '/* __YARC_DB_B64__ */'

def log(msg): print(f'  {msg}')

def step(msg): print(f'\n▶ {msg}')


def build_db():
    step('Compiling yarc_seed.sql → yarc.db')

    if not os.path.exists(SQL_FILE):
        print(f'ERROR: {SQL_FILE} not found.')
        sys.exit(1)

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        log('Removed existing yarc.db')

    con = sqlite3.connect(DB_FILE)
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        sql = f.read()
    con.executescript(sql)
    con.commit()

    # Stats
    cur = con.cursor()
    tables = ['runes', 'rune_effects', 'item_types', 'runewords', 'runeword_item_types', 'runeword_effects']
    for table in tables:
        n = cur.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        log(f'{table:<25} : {n} rows')
    con.close()

    size = os.path.getsize(DB_FILE)
    log(f'yarc.db size : {size // 1024} kb')
    return DB_FILE


def encode_db(db_file):
    step('Encoding yarc.db → base64')
    with open(db_file, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    log(f'Base64 size  : {len(b64) // 1024} kb')
    return b64


def build_html(b64):
    step(f'Embedding DB into {os.path.basename(HTML_TPL)} → yarc_standalone.html')

    if not os.path.exists(HTML_TPL):
        print(f'ERROR: {HTML_TPL} not found.')
        sys.exit(1)

    with open(HTML_TPL, 'r', encoding='utf-8') as f:
        html = f.read()

    if DB_PLACEHOLDER not in html:
        print(f'ERROR: placeholder "{DB_PLACEHOLDER}" not found in yarc.html.')
        print('Make sure yarc.html contains this exact comment where the DB should be injected.')
        sys.exit(1)

    # Injection du base64
    html = html.replace(DB_PLACEHOLDER, b64)

    with open(HTML_OUT, 'w', encoding='utf-8') as f:
        f.write(html)

    size = os.path.getsize(HTML_OUT)
    log(f'yarc_standalone.html : {size // 1024} kb')


def main():
    print('━' * 40)
    print('  YARC build.py')
    print('━' * 40)

    db_file = build_db()
    b64     = encode_db(db_file)
    build_html(b64)

    print('
' + '━' * 40)
    print('  ✓ Build complete')
    print('━' * 40)


if __name__ == '__main__':
    main()
