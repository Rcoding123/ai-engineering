---
tags: [python, introducing-python, persistence, sql, sqlite, json, redis]
chapter: 23
---

# Data in a Box: Persistent Storage

Variables vanish when a program ends. This chapter shows how to keep data: plain files,
structured text (CSV, JSON, XML, TOML), binary files, SQL databases and key-value stores.
The SQL part matters most for a working engineer: you will store eval runs, costs and
cached prompts in tables like the ones here.

## Text Files

RAM is fast but forgets everything without power. A disk is slower but keeps data.
*Persistence* means writing data to disk (or a server) and reading it back later.
The simplest form is a flat text file (file reading and writing are in [[20 - Files|Chapter 20]]).

A *record* is one chunk of related data made of *fields*. In a *padded*
text file, every field has a fixed width, so every line is the same length. Then
`seek()` can jump to record n at byte n x line length without reading
the rest.

```python
import os
import tempfile

os.chdir(tempfile.mkdtemp())           # scratch folder for the examples
with open("fixed.txt", "w", encoding="utf-8", newline="\n") as f:
    for name, score in [("alpha", 91), ("beta", 78), ("gamma", 85)]:
        f.write(f"{name:<8}{score:>4}\n")      # 8 + 4 + newline = 13 chars
with open("fixed.txt", "r", encoding="utf-8", newline="") as f:
    f.seek(13)                                 # skip record 0
    print(repr(f.read(13)))
```

```text
'beta      78\n'
```

Fixed-width files are rare today. They are shown because they explain what databases do
for you: find a row without scanning everything.

The picture to keep in mind is a ladder. Move up only when the lower rung hurts.

```mermaid
flowchart LR
    A["text file<br/>lines"] --> B["CSV, JSON, TOML<br/>structured files"] --> C["SQLite<br/>one file, SQL"] --> D["PostgreSQL, MySQL<br/>server, many users"] --> E["Redis, NoSQL<br/>special shapes"]
```
Direction of travel: more data, more users, more structure, more setup.

## Tabular and Delimited Text Files

Lines are the only structure in plain text. These formats add more:

| **Format** | **Structure by** | **Good for** |
|---|---|---|
| CSV, TSV | delimiter (comma, tab, `\|`) | tables, spreadsheet exchange |
| XML, HTML | `<tags>` | documents, feeds, old enterprise data |
| JSON | braces, brackets, quotes | APIs, nested data, configs |
| YAML | indentation | human-edited configs |
| TOML | `[sections]`, `key = value` | configs (stdlib reader) |
| INI (`configparser`) | `[sections]` | simple settings |

### CSV

Do not split lines on commas yourself. Fields may contain commas, quotes or newlines, and
only the `csv` module handles all of that. It also works with other delimiters
(`delimiter="\t"`).

```mermaid
flowchart LR
    F["file on disk<br/>model,note<br/>m-small,fast cheap (quoted)<br/>m-big,says hi (quoted)"] --> R["csv.reader: list of str<br/>['model', 'note']<br/>['m-small', 'fast, cheap']"]
    F --> D["csv.DictReader: first line = keys<br/>{'model': 'm-small', 'note': 'fast, cheap'}"]
```

```python
import csv
from pathlib import Path

rows = [["model", "note"], ["m-small", "fast, cheap"], ["m-big", 'says "hi"']]
with open("runs.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
print(Path("runs.csv").read_text(encoding="utf-8"))

with open("runs.csv", newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        print(row)

with open("runs.csv", newline="", encoding="utf-8") as f:
    data = list(csv.DictReader(f))
print(data[0], type(data[0]))

with open("scores.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["model", "score"])
    w.writeheader()
    w.writerow({"model": "m-small", "score": 0.82})
with open("scores.csv", newline="", encoding="utf-8") as f:
    r = next(csv.DictReader(f))
print(r, type(r["score"]))
```

```text
model,note
m-small,"fast, cheap"
m-big,"says ""hi"""

['model', 'note']
['m-small', 'fast, cheap']
['m-big', 'says "hi"']
{'model': 'm-small', 'note': 'fast, cheap'} <class 'dict'>
{'model': 'm-small', 'score': '0.82'} <class 'str'>
```

> [!example] Type check
> CSV has no types. Every field comes back as `str`, even `0.82`. Convert yourself:
> `float(r["score"])`. A row is a `list[str]` from `reader`, a `dict[str, str]`
> from `DictReader` (plain `dict` in modern Python).

> [!warning] Trap: open CSV files with `newline=""`
> Without it, Windows can write blank lines between rows and can break quoted fields that
> contain newlines. Also pass `encoding="utf-8"` so the file means the same on every
> machine.

### XML

XML nests data in tags. A tag can have attributes, text and child tags. Python's
`xml.etree.ElementTree` module parses it into a tree.

```mermaid
flowchart TD
    M["models"] --> F1["family name=small"]
    M --> F2["family name=big"]
    F1 --> A["model price=0.10<br/>text: m-s1"]
    F1 --> B["model price=0.25<br/>text: m-s2"]
    F2 --> C["model price=3.00<br/>text: m-b1"]
```

```python
import xml.etree.ElementTree as ET

xml_text = """<models>
  <family name="small">
    <model price="0.10">m-s1</model>
    <model price="0.25">m-s2</model>
  </family>
  <family name="big">
    <model price="3.00">m-b1</model>
  </family>
</models>"""
root = ET.fromstring(xml_text)          # parse from a str
print(root.tag, len(root))
for fam in root:
    print(fam.tag, fam.attrib, len(fam))
for m in root.iter("model"):             # every <model> at any depth
    print(m.text, m.attrib["price"], type(m.attrib["price"]))
print(root.find("family[@name='big']/model").text)
```

```text
models 2
family {'name': 'small'} 2
family {'name': 'big'} 1
m-s1 0.10 <class 'str'>
m-s2 0.25 <class 'str'>
m-b1 3.00 <class 'str'>
m-b1
```

> [!example] Type check
> `.tag` is a `str`, `.attrib` is a `dict[str, str]`, `.text` is a
> `str` or `None`, and `len(element)` counts child elements. Numbers inside XML
> are text until you convert them. `ET.parse(path)` reads a file; `ET.fromstring(s)`
> reads a string.

Other standard parsers: `xml.dom` loads the whole tree and lets you move around
freely (like a browser's DOM); `xml.sax` streams through the file without holding it
all in memory, so it suits very large files.

> [!warning] Trap: untrusted XML can attack you
> The “billion laughs” attack nests entity definitions so a few lines expand to gigabytes
> in memory. For XML you did not write, use the `defusedxml` package (a drop-in
> safe version of these parsers) instead of the plain standard-library ones.

HTML looks like XML but is usually messy and is meant for display, not data exchange. It
is handled with scraping tools in [[24 - The Web|Chapter 24]].

### JSON

JSON is the standard exchange format for APIs and the closest match to Python data. The
module is `json`: `dumps`/`loads` work with strings, `dump`/`load`
with files.

```python
import json

cfg = {"model": "m-small", "temp": 0.2, "stop": ["\n"],
       "seed": None, "ok": True}
text = json.dumps(cfg)
print(text)
print(json.dumps(cfg, indent=2, sort_keys=True))
back = json.loads(text)
print(back == cfg, back["seed"], back["ok"])
with open("cfg.json", "w", encoding="utf-8") as f:
    json.dump(cfg, f)
with open("cfg.json", encoding="utf-8") as f:
    print(json.load(f)["temp"])
try:
    json.loads("{'a': 1}")
except json.JSONDecodeError as e:
    print("JSONDecodeError:", e)
```

```text
{"model": "m-small", "temp": 0.2, "stop": ["\n"], "seed": null, "ok": true}
{
  "model": "m-small",
  "ok": true,
  "seed": null,
  "stop": [
    "\n"
  ],
  "temp": 0.2
}
True None True
0.2
JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

> [!example] Type check
>
> | **Python** | **JSON** |
> |---|---|
> | `dict` (str keys) | object `{...}` |
> | `list`, `tuple` | array `[...]` (a tuple comes back as a list) |
> | `str` | string (double quotes only) |
> | `int`, `float` | number |
> | `True`, `False`, `None` | `true`, `false`, `null` |
>
> `dumps` returns `str`. `set`, `datetime`, `Decimal` and your own
> classes are not JSON serializable and raise `TypeError`. JSON strings need double
> quotes: `{'a': 1}` is invalid JSON even though it is valid Python.

Teach `json` about extra types with a `default` function. It is called only for
objects the module cannot handle, and must return something serializable:

```python
import datetime
import json

def to_json(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"cannot serialize {type(obj).__name__}")

stamp = datetime.datetime(2026, 1, 5, 9, 30)
print(json.dumps({"at": stamp}, default=to_json))
print(json.dumps({"at": stamp}, default=str))      # quick and lazy
```

```text
{"at": "2026-01-05T09:30:00"}
{"at": "2026-01-05 09:30:00"}
```

Prefer ISO 8601 (`isoformat()`) for dates: it sorts correctly and every language
reads it. By default `dumps` writes non-ASCII characters as `\uXXXX`
escapes; pass `ensure_ascii=False` to keep readable text.

> [!tip] Rule: JSON for data, never pickle, across trust boundaries
> JSON can only carry data, not code. Use it for configs, API payloads and caches.

### YAML

YAML is like JSON but uses indentation and allows comments and more types (dates). It is
very common in config files (Docker Compose, CI, Kubernetes). The reader is third party:
`pip install pyyaml`. This was syntax-checked only.

```python
# needs: pip install pyyaml
import yaml

text = """
model: m-small
params:
  temperature: 0.2
  stops: [END, STOP]
debug: false
"""
conf = yaml.safe_load(text)            # dict; false -> False
print(conf["params"]["stops"])         # ['END', 'STOP']
```

> [!warning] Trap: `yaml.load` on untrusted text can run code
> Always call `yaml.safe_load`. Plain `load` can build arbitrary Python objects.

### TOML

TOML is a clear config format with comments, in the standard library since Python 3.11
(`tomllib`, read-only). `pyproject.toml` uses it.

```python
import tomllib

toml_text = """
title = "eval config"
[model]
name = "m-small"
temperature = 0.2
stops = ["END", "STOP"]
[limits]
max_tokens = 512
"""
conf = tomllib.loads(toml_text)         # loads takes a str
print(conf)
print(conf["limits"]["max_tokens"] + 1)

# not run: from a file, open in BINARY mode
# with open("pyproject.toml", "rb") as f:
#     conf = tomllib.load(f)
```

```text
{'title': 'eval config', 'model': {'name': 'm-small', 'temperature': 0.2, 'stops': ['END', 'STOP']}, 'limits': {'max_tokens': 512}}
513
```

> [!example] Type check
> TOML keeps types: strings, `int`, `float`, `bool`, lists, dates, tables
> (nested `dict`). `tomllib.load` needs a file opened with `"rb"`;
> `tomllib.loads` takes a `str`. It cannot write TOML.

### Tablib

Tablib (`pip install tablib`) imports, edits and exports tabular data between CSV,
JSON, YAML, Excel and DataFrames. In [[25 - Data Science|Chapter 25]] pandas does the same job and more.

### Configuration files

Do not invent your own config format. You would have to maintain both writer and parser.
Use one of the formats above. The standard `configparser` reads Windows-style
`.ini` files with sections:

```python
import configparser

ini = """[api]
base = https://example.test
timeout = 30
[paths]
home = /srv/app
logs = %(home)s/logs
"""
cp = configparser.ConfigParser()
cp.read_string(ini)                     # cp.read("file.ini") for a file
print(cp["api"]["timeout"], type(cp["api"]["timeout"]))
print(cp["api"].getint("timeout") + 1)
print(cp["paths"]["logs"])              # %(home)s was filled in
```

```text
30 <class 'str'>
31
/srv/app/logs
```

> [!example] Type check
> Every `configparser` value is a `str`. Use `getint`, `getfloat`,
> `getboolean`. Only two levels (section, key); for deeper nesting use JSON, YAML or
> TOML.

> [!tip] Rule: secrets do not go in config files you commit
> Keep API keys in environment variables or a secrets manager, not in `.json`,
> `.toml` or `.ini` files in git.

## Binary Files

Some formats are neither relational nor NoSQL; they store a particular shape of data in
bytes.

### Padded binary files and memory mapping

Like the padded text file, but with fixed-size binary records. The `struct` module
packs values into bytes with a format string; `mmap` makes a file look like one big
`bytes`-like object so you can slice it without reading everything.

```python
import mmap
import struct

rec = struct.Struct("<8sIf")            # 8-byte name, uint32, float32
print(rec.size)
with open("fixed.bin", "wb") as f:
    records = [(b"alpha", 1, 0.5), (b"beta", 2, 1.5), (b"gamma", 3, 2.5)]
    for name, n, x in records:
        f.write(rec.pack(name, n, x))
with open("fixed.bin", "rb") as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        chunk = mm[rec.size:2 * rec.size]      # record 1, no full read
        print(rec.unpack(chunk))
```

```text
16
(b'beta\x00\x00\x00\x00', 2, 1.5)
```

> [!example] Type check
> Everything here is `bytes`. A fixed-width string field comes back padded with
> `b"\x00"`; strip it and decode: `raw.rstrip(b"\x00").decode("utf-8")`.
> `"<"` in the format means little-endian with no alignment padding.

This is low-level work, used close to hardware or in file formats you must match. Chapter
18 covers `struct` in depth.

### Spreadsheets, HDF5 and TileDB

| **Format** | **How to use it from Python** |
|---|---|
| Excel (`.xlsx`) | export to CSV and use `csv`; or use a library (`openpyxl`, Tablib, pandas `read_excel`) |
| HDF5 | binary format for huge numeric arrays and hierarchies, fast random access; write once, read many. Packages `h5py` (low level), PyTables (database-like) |
| TileDB | successor to HDF5 for dense or sparse arrays (`pip install tiledb`); science oriented |

## Relational Databases

A relational database stores data in *tables* and lets you combine tables. It gives
you things files do not:

- many users at once, without corrupting the data;
- a *schema*: columns with types and rules (*constraints*);
- fast lookups with *indexes*;
- *joins*: combine tables by shared values;
- a declarative query language, SQL: you say *what* you want, not how to get it.

### Tables, keys and indexes

```text
 table runs
 primary key: unique
        |
        v
 +----+------+-------+
 | id | task | score |   <- column: name and type
 +----+------+-------+
 |  1 | qa   | 0.71  |
 |  2 | code | 0.55  |   <- row: one record
 |  3 | qa   | NULL  |   <- NULL: value missing
 +----+------+-------+
```

- **Primary key**: a column (or group) whose values are unique in the table.
  It identifies a row and is indexed automatically.
- **Index**: a side structure, like a book index, that finds rows by a column
  without scanning the whole table. Without one the database does a *table scan*.
- **Foreign key**: a column holding another table's primary key. It links rows
  across tables.
- **NULL**: “no value”. It is not zero and not an empty string.

“Database” is used for three things: the server program, a named container of tables,
and the stored data. Say “database server”, “database” and “data” when it matters.

## SQL

SQL is a text language sent to the database, which decides how to run it. It is not
case-sensitive, but keywords are written in capitals by tradition. Dialects differ slightly
between vendors; the core below works on SQLite, PostgreSQL and MySQL.

| **Group** | **Statements** |
|---|---|
| DDL (data definition) | `CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`, `CREATE INDEX`: shape of the data |
| DML (data manipulation) | `INSERT`, `SELECT`, `UPDATE`, `DELETE`: the data itself. Known as CRUD: Create, Read, Update, Delete |

```text
CREATE TABLE t (id INTEGER PRIMARY KEY, label TEXT NOT NULL);   -- DDL
INSERT INTO t (label) VALUES ('first');                          -- create
SELECT id, label FROM t WHERE id > 0;                            -- read
UPDATE t SET label = 'one' WHERE id = 1;                         -- update
DELETE FROM t WHERE id = 1;                                      -- delete
DROP TABLE t;                                                    -- DDL
```

> [!warning] Trap: `UPDATE` or `DELETE` without `WHERE` hits every row
> Write the `WHERE` first. Run it as a `SELECT` to see which rows it matches, then
> change `SELECT` to `DELETE`.

### A small dataset

We use SQLite from the standard library (details in the next section). Two tables: models
and their eval runs. `runs.model_id` is a foreign key to `models.id`. The helper
`q` runs a query and returns the rows.

```python
import sqlite3

conn = sqlite3.connect(":memory:")       # lives in RAM; gone at exit
conn.execute("""
CREATE TABLE models (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL UNIQUE,
    vendor    TEXT NOT NULL,
    usd_per_m REAL NOT NULL
)""")
conn.execute("""
CREATE TABLE runs (
    id       INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL REFERENCES models(id),
    task     TEXT NOT NULL,
    score    REAL,
    tokens   INTEGER NOT NULL
)""")
conn.executemany(
    "INSERT INTO models (name, vendor, usd_per_m) VALUES (?, ?, ?)",
    [("m-small", "acme", 0.10), ("m-big", "acme", 3.00),
     ("m-open", "libre", 0.0)],
)
conn.executemany(
    "INSERT INTO runs (model_id, task, score, tokens) VALUES (?, ?, ?, ?)",
    [(1, "qa", 0.71, 1200), (1, "code", 0.55, 3000), (2, "qa", 0.90, 1100),
     (2, "code", 0.84, 2900), (2, "qa", 0.88, 1000), (3, "qa", None, 800)],
)
conn.commit()

def q(sql, params=()):
    return conn.execute(sql, params).fetchall()

print(q("SELECT * FROM models"))
```

```text
[(1, 'm-small', 'acme', 0.1), (2, 'm-big', 'acme', 3.0), (3, 'm-open', 'libre', 0.0)]
```

Notice that the last run has `score = None`: it becomes SQL `NULL`.

### SELECT, WHERE, ORDER BY, LIMIT

`SELECT` picks columns, `FROM` the table, `WHERE` filters rows,
`ORDER BY` sorts (`DESC` for descending), `LIMIT` caps the count.

```python
print(q("SELECT task, score FROM runs WHERE score > 0.7 AND task = 'qa'"))
print(q("""SELECT id, score FROM runs WHERE score IS NOT NULL
           ORDER BY score DESC LIMIT 3"""))
print(q("SELECT id FROM runs WHERE score = NULL"))    # wrong
print(q("SELECT id FROM runs WHERE score IS NULL"))   # right
```

```text
[('qa', 0.71), ('qa', 0.9), ('qa', 0.88)]
[(3, 0.9), (5, 0.88), (4, 0.84)]
[]
[(6,)]
```

> [!warning] Trap: `= NULL` never matches
> `NULL` means “unknown”, and nothing equals unknown. Use `IS NULL` and
> `IS NOT NULL`. Also note that `AVG` and `MAX` skip NULLs.

Other filters: `IN ('a','b')`, `BETWEEN 1 AND 5`, `LIKE 'm-%'` (`%`
means any text), `OR`, `NOT`.

### Aggregates and GROUP BY

Aggregate functions collapse many rows into one value: `COUNT`, `SUM`,
`AVG`, `MIN`, `MAX`. `GROUP BY` makes one bucket per distinct value and
runs the aggregate once per bucket. `HAVING` filters buckets (`WHERE` filters rows
*before* grouping).

```mermaid
flowchart LR
    subgraph rows["rows of runs (model_id | score)"]
        r1["1 | 0.71"]
        r2["1 | 0.55"]
        r3["2 | 0.90"]
        r4["2 | 0.84"]
        r5["2 | 0.88"]
        r6["3 | NULL"]
    end
    subgraph buckets["buckets: GROUP BY model_id"]
        b1["0.71, 0.55"]
        b2["0.90, 0.84, 0.88"]
        b3["NULL"]
    end
    r1 --> b1
    r2 --> b1
    r3 --> b2
    r4 --> b2
    r5 --> b2
    r6 --> b3
    b1 --> o1["1 | n=2 | avg 0.63"]
    b2 --> o2["2 | n=3 | avg 0.873"]
    b3 --> o3["3 | n=1 | avg NULL"]
```

```python
print(q("SELECT COUNT(*), AVG(score), MAX(tokens), SUM(tokens) FROM runs"))
print(q("""SELECT model_id, COUNT(*) AS n, ROUND(AVG(score), 3) AS avg_score
           FROM runs GROUP BY model_id ORDER BY model_id"""))
print(q("""SELECT model_id, COUNT(*) AS n FROM runs
           GROUP BY model_id HAVING COUNT(*) >= 2"""))
```

```text
[(6, 0.776, 3000, 10000)]
[(1, 2, 0.63), (2, 3, 0.873), (3, 1, None)]
[(1, 2), (2, 3)]
```

`AS` gives a column an alias. `COUNT(*)` counts rows; `COUNT(score)` skips
NULLs. Model 3 has an average of `None` because its only score is NULL.

### JOIN

A join combines rows of two tables where the `ON` condition is true. Here: each run
row is matched with the model row whose `id` equals the run's `model_id`.

```mermaid
erDiagram
    models ||--o{ runs : "ON m.id = r.model_id"
    models {
        int id PK
        text name
    }
    runs {
        int model_id FK
        real score
    }
```

```text
result of the JOIN: name + score
+---------+-------+
| m-small | 0.71  |   <- run with model_id 1
| m-big   | 0.90  |   <- run with model_id 2
| m-big   | 0.88  |   <- run with model_id 2
| m-open  | NULL  |   <- run with model_id 3
+---------+-------+
```

```python
print(q("""SELECT m.name, r.task, r.score
           FROM runs AS r JOIN models AS m ON m.id = r.model_id
           WHERE r.task = 'qa' ORDER BY r.score DESC"""))
for row in q("""SELECT m.name, SUM(r.tokens) AS toks,
                       SUM(r.tokens) * m.usd_per_m / 1000000.0 AS usd
                FROM models m JOIN runs r ON r.model_id = m.id
                GROUP BY m.id ORDER BY usd DESC"""):
    print(row)
```

```text
[('m-big', 'qa', 0.9), ('m-big', 'qa', 0.88), ('m-small', 'qa', 0.71),
 ('m-open', 'qa', None)]
('m-big', 5000, 0.015)
('m-small', 4200, 0.00042)
('m-open', 800, 0.0)
```

The second query is the shape you will use daily: join, group by, aggregate. It computes
cost per model from token counts and a price per million tokens.

`JOIN` (inner join) drops rows with no partner. `LEFT JOIN` keeps every row of
the left table and fills missing right-side columns with NULL:

```python
conn.execute("INSERT INTO models (name, vendor, usd_per_m) "
             "VALUES ('m-new', 'acme', 1.0)")
print(q("""SELECT m.name, COUNT(r.id) FROM models m
           LEFT JOIN runs r ON r.model_id = m.id GROUP BY m.id"""))
print(q("""SELECT m.name, COUNT(r.id) FROM models m
           JOIN runs r ON r.model_id = m.id GROUP BY m.id"""))
```

```text
[('m-small', 2), ('m-big', 3), ('m-open', 1), ('m-new', 0)]
[('m-small', 2), ('m-big', 3), ('m-open', 1)]
```

`m-new` has no runs. The `LEFT JOIN` still lists it, with count 0; the inner
`JOIN` loses it.

### The order SQL really runs

You write `SELECT` first, but the database starts at `FROM`. This explains most
“why can't I use that here?” errors, for instance why an alias from `SELECT` cannot
be used in `WHERE`.

```mermaid
flowchart LR
    A["FROM / JOIN"] --> B["WHERE"] --> C["GROUP BY"] --> D["HAVING"] --> E["SELECT"] --> F["ORDER BY"] --> G["LIMIT"]
```
Pick tables, filter rows, make buckets, filter buckets, choose columns, sort, cut.

### UPDATE, DELETE and indexes

```python
cur = conn.execute("UPDATE runs SET score = 0.5 WHERE score IS NULL")
print(cur.rowcount)                      # rows changed
cur = conn.execute("DELETE FROM runs WHERE score < 0.6")
print(cur.rowcount)                      # rows removed
conn.commit()
```

```text
1
2
```

An index speeds up lookups and joins on a column but slows writes slightly and uses
space. Index columns you filter or join on often (foreign keys are good candidates):

```text
CREATE INDEX idx_runs_model ON runs (model_id);
```

## DB-API and SQLite

*DB-API* is Python's standard interface to relational databases. Drivers for SQLite,
PostgreSQL and MySQL all follow it, so the shape of your code stays the same.

```mermaid
flowchart LR
    A["connect()"] --> B["cursor()"] --> C["execute()"] --> D["fetch*()"] --> E["commit()"] --> F["close()"]
```
The connection is the line to the database; the cursor holds one query and its results.

| **Call** | **What it does** |
|---|---|
| `connect(...)` | open a connection (file name for SQLite; host, user, password for servers) |
| `conn.cursor()` | create a cursor, the object that runs statements and holds results |
| `execute(sql, params)` / `executemany(sql, seq)` | run one statement / run it once per parameter set |
| `fetchone()`, `fetchmany(n)`, `fetchall()` | read result rows |
| `conn.commit()` / `conn.rollback()` | make changes permanent / undo them |

SQLite is a SQL database in a library: no server, one ordinary file, built into Python
(`import sqlite3`). Browsers and phones use it. `":memory:"` gives a temporary
database in RAM, ideal for tests.

### Placeholders and what comes back

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, plan TEXT)")
conn.executemany("INSERT INTO users VALUES (?, ?)",
                 [("ana", "free"), ("bo", "pro"), ("cy", "pro")])

name = "nobody' OR '1'='1"                 # hostile input

bad = f"SELECT name FROM users WHERE name = '{name}'"
print(bad)
print(conn.execute(bad).fetchall())        # leaks every row

good = "SELECT name FROM users WHERE name = ?"
print(conn.execute(good, (name,)).fetchall())

print(conn.execute("SELECT name FROM users WHERE plan = :p AND name > :n",
                   {"p": "pro", "n": "bo"}).fetchall())
```

```text
SELECT name FROM users WHERE name = 'nobody' OR '1'='1'
[('ana',), ('bo',), ('cy',)]
[]
[('cy',)]
```

> [!warning] Trap: SQL injection
> Building SQL with f-strings, `%` or `+` lets user input become SQL. The
> hostile text above turned a one-row lookup into “return everyone”. With `?`
> placeholders the driver sends the values separately and they are always treated as data.
> **Always pass values as parameters**, including for LLM-generated text.

> [!example] Type check
> Parameters must be a *sequence*: `("pro",)` with the trailing comma, not
> `"pro"`. A bare string is treated as a sequence of characters.
> Placeholders can stand for *values only*, not table or column names: `"SELECT `
> FROM ?"} is a syntax error. If a table name must vary, check it against a fixed allow-list.
> SQLite uses `?` and `:name`; psycopg2 (PostgreSQL) uses `%s`.

```python
try:
    conn.execute("SELECT name FROM users WHERE plan = ?",
                 "pro")                       # not a tuple
except sqlite3.ProgrammingError as err:
    print("ProgrammingError:", err)
sql = "SELECT name FROM users WHERE plan = ?"
print(conn.execute(sql, ("pro",)).fetchall())
try:
    conn.execute("SELECT * FROM ?", ("users",))
except sqlite3.OperationalError as err:
    print("OperationalError:", err)
```

```text
ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 3 supplied.
[('bo',), ('cy',)]
OperationalError: near "?": syntax error
```

Now the row type. `fetch*` returns *tuples*; `fetchall` returns a list of
tuples. Column names are in `cursor.description`. Set
`conn.row_factory = sqlite3.Row` to also read columns by name.

```python
cur = conn.execute("SELECT name, plan FROM users ORDER BY name")
row = cur.fetchone()
print(type(row), row, row[0])
print([d[0] for d in cur.description])
print(cur.fetchmany(1), cur.fetchall(), cur.fetchone())

conn.row_factory = sqlite3.Row
sql = "SELECT name, plan FROM users WHERE name = 'bo'"
row = conn.execute(sql).fetchone()
print(type(row).__name__, row["plan"], row[0], row.keys(), tuple(row))
```

```text
<class 'tuple'> ('ana', 'free') ana
['name', 'plan']
[('bo', 'pro')] [('cy', 'pro')] None
Row pro bo ['name', 'plan'] ('bo', 'pro')
```

> [!example] Type check
> A cursor is used up as you read it: `fetchone` returns the next row or `None` when
> there are no more rows; `fetchall` then returns `[]`. SQL `NULL` becomes
> `None`. SQLite types are loose: it *coerces* values to the column type when it
> can and stores the rest as is.

```python
conn.row_factory = None
conn.execute("CREATE TABLE t (a INTEGER, b TEXT)")
conn.execute("INSERT INTO t VALUES (1, 'x')")
conn.execute("INSERT INTO t VALUES ('7', 5)")        # coerced, not rejected
print(conn.execute("SELECT a, b, typeof(a), typeof(b) FROM t").fetchall())

conn.execute("CREATE TABLE k (name TEXT UNIQUE)")
conn.execute("INSERT INTO k VALUES ('a')")
try:
    conn.execute("INSERT INTO k VALUES ('a')")
except sqlite3.IntegrityError as err:
    print("IntegrityError:", err)
```

```text
[(1, 'x', 'integer', 'text'), (7, '5', 'integer', 'text')]
IntegrityError: UNIQUE constraint failed: k.name
```

Constraints (`UNIQUE`, `NOT NULL`, `PRIMARY KEY`, foreign keys) make the
database reject bad data. That is what the schema is for.

### Transactions: commit or lose it

Changes happen inside a *transaction*. Other connections do not see them until you
`commit()`. `rollback()` throws them away.

```mermaid
sequenceDiagram
    participant A as connection A
    participant B as connection B
    A->>A: INSERT (pending)
    B->>B: COUNT(*) = 0
    A->>A: commit()
    A-->>B: change becomes visible
    B->>B: COUNT(*) = 1
```

```python
import os
import sqlite3
import tempfile

d = tempfile.mkdtemp()
path = os.path.join(d, "app.db")

a = sqlite3.connect(path)
a.execute("CREATE TABLE ev (id INTEGER PRIMARY KEY, msg TEXT)")
a.commit()
a.execute("INSERT INTO ev (msg) VALUES ('one')")
b = sqlite3.connect(path)
print("before commit:", b.execute("SELECT COUNT(*) FROM ev").fetchone())
a.commit()
print("after commit :", b.execute("SELECT COUNT(*) FROM ev").fetchone())

a.execute("INSERT INTO ev (msg) VALUES ('two')")
print("in_transaction:", a.in_transaction)
a.rollback()
print("after rollback:", a.execute("SELECT COUNT(*) FROM ev").fetchone())
```

```text
before commit: (0,)
after commit : (1,)
in_transaction: True
after rollback: (1,)
```

The connection is also a context manager: leaving the `with` block commits, or rolls
back if an exception escaped. It does *not* close the connection.

```python
try:
    with a:
        a.execute("INSERT INTO ev (msg) VALUES ('three')")
        raise RuntimeError("boom")
except RuntimeError:
    pass
print("after failed with:", a.execute("SELECT COUNT(*) FROM ev").fetchone())
with a:
    a.execute("INSERT INTO ev (msg) VALUES ('four')")
print("after good with  :", a.execute("SELECT COUNT(*) FROM ev").fetchone())
a.close()
b.close()

c = sqlite3.connect(path)                # a file keeps its data
print([r[0] for r in c.execute("SELECT msg FROM ev ORDER BY id")])
c.close()
```

```text
after failed with: (1,)
after good with  : (2,)
['one', 'four']
```

> [!warning] Trap: forgetting `commit()`
> Close a connection without committing and your inserts silently vanish. Use
> `with conn:` around each unit of work. Also close connections (or use
> `contextlib.closing`); they hold files and locks.

> [!tip] Rule: one function, parameters, with-block
> Wrap writes in `with conn:`, pass values as parameters, and use
> `executemany` for bulk inserts: it is much faster than a Python loop of single
> `execute` calls.

## DuckDB, MySQL and PostgreSQL

| **Database** | **Runs as** | **Python package** | **Notes** |
|---|---|---|---|
| SQLite | library, one file | `sqlite3` (stdlib) | simple apps, tests, local caches |
| DuckDB | library, in-process | `duckdb` | analytics (OLAP): fast scans and aggregates; queries CSV, JSON, Parquet files directly ([[25 - Data Science\|Chapter 25]]) |
| MySQL | server | `mysqlclient`, `PyMySQL`, `mysql-connector-python` | popular open source server |
| PostgreSQL | server | `psycopg2` (or `psycopg`) | full-featured, strict, extensible; also does JSON and vectors |

Servers are used when many programs on different machines need the same data. The API is
the same DB-API; only the connection arguments and the placeholder style change. None of
this was run here (no servers, no packages); syntax-checked only.

```python
# needs: pip install duckdb psycopg2-binary  (and a running PostgreSQL)
import duckdb
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="evals", user="me",
                        password="x")
with conn, conn.cursor() as cur:               # commit on success
    cur.execute("SELECT name FROM models WHERE vendor = %s", ("acme",))
    print(cur.fetchall())                      # %s, not ?, in psycopg2
conn.close()

print(duckdb.sql("SELECT avg(score) FROM 'runs.csv'").fetchall())
```

`psycopg2` needs the PostgreSQL client libraries unless you install the
`-binary` variant. Get the password from an environment variable, never from code.

## SQLAlchemy

SQL dialects differ, and DB-API only goes so far. *SQLAlchemy* is the most popular
cross-database toolkit. It has three levels; use the lowest that does the job.

```mermaid
flowchart TB
    ORM["ORM: classes and sessions; rows become objects"]
    EXPR["SQL Expression Language: build queries in Python"]
    ENG["Engine: connection pool, dialect, raw SQL"]
    DRV["DB-API driver (sqlite3, psycopg2, ...)"]
    DB[("the database")]
    ORM --> EXPR --> ENG --> DRV --> DB
```
Going up the stack: more abstract, less SQL visible.

The connection string (URL) selects the dialect and driver:

```text
dialect+driver://user:password@host:port/dbname
sqlite:///:memory:                    in-memory SQLite
sqlite:///zoo.db                      file in the current folder
postgresql+psycopg2://me:pw@localhost:5432/evals
```

Below is the current (2.x) style for all three levels. It needs
`pip install sqlalchemy`; not run here, syntax-checked only. Older tutorials that call
`conn.execute("raw string")` do not work on 2.x: wrap raw SQL in `sa.text()`.

```python
# needs: pip install sqlalchemy  (2.x)
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = sa.create_engine("sqlite:///:memory:")

# level 1: engine + raw SQL, named parameters
with engine.begin() as conn:                    # begin() commits at the end
    conn.execute(sa.text(
        "CREATE TABLE ev (id INTEGER PRIMARY KEY, msg TEXT)"))
    conn.execute(sa.text("INSERT INTO ev (msg) VALUES (:m)"), {"m": "hi"})
    rows = conn.execute(sa.text("SELECT id, msg FROM ev")).fetchall()
    print(rows)                                 # [(1, 'hi')]

```

Level 2, the expression language, builds the same SQL from Python objects:

```python
# level 2: expression language
meta = sa.MetaData()
runs = sa.Table(
    "runs", meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("task", sa.String),
    sa.Column("score", sa.Float),
)
meta.create_all(engine)
with engine.begin() as conn:
    conn.execute(sa.insert(runs), [{"task": "qa", "score": 0.9}])
    stmt = sa.select(runs.c.task, runs.c.score).where(runs.c.score > 0.5)
    print(conn.execute(stmt).all())

```

Level 3, the ORM, maps a class to a table and a row to an instance:

```python
# level 3: ORM
class Base(DeclarativeBase):
    pass

class Model(Base):
    __tablename__ = "models"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    usd_per_m: Mapped[float]

Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add(Model(name="m-small", usd_per_m=0.10))
    session.commit()
    found = session.scalars(sa.select(Model).where(Model.usd_per_m < 1)).all()
    print(found[0].name)
```

> [!example] Type check
> Levels 1 and 2 return `Row` objects that behave like tuples.
> Level 3 returns *instances of your class* (`Model`); attributes are typed through
> `Mapped[int]`, `Mapped[str]`, ...

An ORM (object-relational mapper) lets you stay in Python objects. But it is an
abstraction, and abstractions leak: when it misbehaves you must understand the SQL it
generates. Learn SQL first, then use an ORM for simple, table-shaped apps. FastAPI projects
often use SQLAlchemy or SQLModel.

Lighter tools: `dataset` (“databases for lazy people”, built on SQLAlchemy) and
`records` (“SQL for humans”: plain SQL strings, exports via Tablib).

## NoSQL Data Stores

Not all data is a rectangle. NoSQL (“not only SQL”) stores trade the strict table model
for flexibility or scale. The simplest kind is a *key-value store*: a dictionary on
disk or on a server.

| **Store** | **Lives** | **Notes** |
|---|---|---|
| `dbm` | file, stdlib | dict-like; keys and values are bytes |
| Memcached | server, RAM | pure cache; may forget data any time |
| Redis / Valkey | server, RAM + optional disk | keys with rich values (list, hash, set, sorted set); expiry |

### The dbm family

`dbm` behaves like a dict saved on disk. Modes: `"r"` read, `"w"` write,
`"c"` read/write and create. You cannot iterate over the object, but `keys()`,
`len()` and `get()` work.

```python
import dbm
import os
import tempfile

path = os.path.join(tempfile.mkdtemp(), "defs")
with dbm.open(path, "c") as db:
    db["mustard"] = "yellow"           # str is encoded for you
    db[b"ketchup"] = b"red"
    print(len(db), db["mustard"], type(db["mustard"]))
    print(db.get("none"), db.get("none", b"dflt"))
with dbm.open(path, "r") as db:
    print(db["mustard"].decode("utf-8"))
    print(sorted(db.keys()))
```

```text
2 b'yellow' <class 'bytes'>
None b'dflt'
yellow
[b'ketchup', b'mustard']
```

> [!example] Type check
> dbm returns `bytes`, even if you stored a `str`. Decode on the way out.

### Memcached

A fast in-memory cache server, often placed in front of a database. Data can disappear at
any time (it is a cache). Python drivers: `python-memcached`, `pymemcache`.
Operations: set/get, increment/decrement, delete. Use it only for data you can recompute.

### Redis

Redis is a *data structure server*: keys map to strings, lists, hashes, sets or sorted
sets. Data lives in memory, with optional saving to disk. Redis types map closely to
Python types, so it makes a handy shared scratchpad between programs. Install
`pip install redis` and run a Redis server on localhost. All code in this section is
syntax-checked only; the comments show what you should see.

```text
  string        list              hash               set              sorted set
+---------+  +--------------+  +--------------+  +--------------+  +----------------+
| "calls" |  | "queue"      |  | "run:7"      |  | "tags:a"     |  | "leaders"      |
|   ->    |  |   ->         |  |   ->         |  |   ->         |  |   ->           |
|  "11"   |  | [job-a,job-b]|  | model:m-small|  | {qa, code}   |  | m-small 0.71   |
|         |  | order kept   |  | score:0.91   |  | unique,      |  | m-big   0.90   |
|         |  | push/pop     |  |              |  | no order     |  | sorted by score|
+---------+  +--------------+  +--------------+  +--------------+  +----------------+
```

```python
# needs: pip install redis, and a Redis (or Valkey) server on localhost
import json
import time

import redis

r = redis.Redis(decode_responses=True)          # str in, str out

# strings and counters
r.set("model:default", "m-small")
print(r.get("model:default"))                   # 'm-small'
r.set("calls", 0)
r.incr("calls")
r.incr("calls", 10)
print(r.get("calls"))                           # '11'  (a str!)
print(r.setnx("model:default", "other"))        # False: key exists

# list (a queue)
r.rpush("queue", "job-a", "job-b")
print(r.lpop("queue"), r.llen("queue"))         # job-a 1

# hash (one level of fields, all strings)
r.hset("run:7", mapping={"model": "m-small", "score": "0.91"})
print(r.hget("run:7", "score"), r.hgetall("run:7"))

# set
r.sadd("tags:a", "qa", "code")
r.sadd("tags:b", "qa", "math")
print(r.sinter("tags:a", "tags:b"))             # {'qa'}

# sorted set (leaderboard)
r.zadd("leaders", {"m-small": 0.71, "m-big": 0.90})
print(r.zrange("leaders", 0, -1, withscores=True))
print(r.zrevrange("leaders", 0, 0))             # ['m-big']

# cache with expiry
r.set("cache:abc123", json.dumps({"text": "hi"}), ex=60)
print(r.ttl("cache:abc123"))                    # about 60
time.sleep(61)
print(r.get("cache:abc123"))                    # None
```

| **Type** | **Commands (redis-py method names)** |
|---|---|
| String | `set`, `get`, `setnx` (only if absent), `getset`, `mset`/`mget`, `incr`/`decr`, `incrbyfloat`, `delete` |
| List | `lpush`/`rpush`, `lpop`/`rpop`, `lrange(k, 0, -1)`, `llen`, `ltrim`, blocking `brpop` |
| Hash | `hset`, `hget`, `hmget`, `hgetall`, `hkeys`, `hvals`, `hlen` |
| Set | `sadd`, `smembers`, `srem`, `sinter`, `sunion`, `sdiff`, `scard` |
| Sorted set | `zadd(k, {member: score})`, `zrange`, `zrank`, `zscore`; use for leaderboards, time series (score = timestamp) |
| Expiry | `expire(k, seconds)`, `ex=` option of `set`, `ttl`; after that the key is gone |

> [!example] Type check
> Without `decode_responses=True`, redis-py returns `bytes`: `b'11'`. Numbers
> come back as text (strings) from `get` even if you stored `11`; `incr`
> returns an `int`. Hash fields and list items are strings only. For nested data, store
> `json.dumps(...)` as one string. `smembers` gives a `set`.

Expiry makes Redis a good cache. A common AI use is caching model replies so the same
request is not paid for twice. The flow (*cache-aside*):

```mermaid
flowchart LR
    A["request<br/>model + prompt"] --> B["key = hash of the request"] --> C["cache lookup<br/>GET key"]
    C -->|found| D["hit: return stored reply"]
    C -->|absent| E["miss: call the API"] --> F["SET key reply<br/>with expiry"]
```

The same logic works with a plain dictionary, so it can be tried without a server:

```python
import hashlib
import json
import time

cache = {}                                   # key -> (expires_at, value)
calls = 0

def cache_key(model, prompt):
    raw = json.dumps([model, prompt]).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12]

def fake_llm(prompt):                        # stands in for a paid API call
    global calls
    calls += 1
    return prompt.upper()

def ask(model, prompt, ttl=60):
    key = cache_key(model, prompt)
    hit = cache.get(key)
    if hit and hit[0] > time.time():         # found and not expired
        return hit[1]
    value = fake_llm(prompt)
    cache[key] = (time.time() + ttl, value)
    return value

print(ask("m1", "hello"), ask("m1", "hello"), ask("m1", "other"))
print("api calls:", calls, "cache size:", len(cache))
print(cache_key("m1", "hello"))
```

```text
HELLO HELLO OTHER
api calls: 2 cache size: 2
f3a65b99fca4
```

> [!tip] Rule: cache keys must contain everything that changes the answer
> Hash the model name, the prompt *and* the sampling settings. Set an expiry so stale
> answers disappear. Never cache anything that must be fresh or private to one user.

### Redis alternative: Valkey

In 2024 Redis moved to a non-open-source license. Valkey is an API-compatible open source
fork maintained by Redis core developers. Install `pip install valkey`; the client API
mirrors redis-py.

### Other NoSQL families

| **Family** | **Shape of data / use** | **Examples (Python package)** |
|---|---|---|
| Document | JSON-like records with varying fields, nested; the ODM is the ORM of this world | MongoDB (PyMongo), DynamoDB (boto3), CouchDB |
| Time series | measurements stamped with time (metrics) | InfluxDB, Prometheus client, TimescaleDB (TigerData) |
| Graph | nodes joined by edges (users who follow users) | Neo4j (`neo4j`), ArangoDB |
| Wide-column / other | huge data over many machines | Cassandra, HBase |
| Full-text search | index every word; find the poem about windmills | Elasticsearch, Solr, Whoosh, Lucene |
| Vector | arrays of numbers (embeddings) for *similarity* search, not exact match | Chroma, pgvector, others |
| Geospatial | maps and locations | PostGIS, SpatiaLite, GeoPandas |

PostgreSQL can imitate several of these: `jsonb` columns store and index JSON
documents, arrays store lists in a cell, and the `pgvector` extension adds vector
search, all while keeping transactions and foreign keys. For an AI engineer, vector
databases are the important one here: they store embeddings and answer “which stored
texts are closest in meaning to this one”. That is the core of retrieval-augmented
generation (RAG).

> [!danger] Boss fight: choosing storage
> There is no best store; there is the one that matches the shape and the access pattern.
> Ask: *How big? Who writes and reads, and how many at once? What must survive a crash*
> Do I query by many fields, or by one key?}
>
> | **If you need** | **Start with** |
> |---|---|
> | a small config, read at startup | TOML or JSON file |
> | a table to exchange or inspect | CSV |
> | queries, joins, one app, local | SQLite |
> | many writers or services | PostgreSQL |
> | a fast cache with expiry | Redis |
> | nearest-neighbour search on embeddings | a vector database or `pgvector` |
>

## Practice

> [!question-] Practice
>
> 1. Write a CSV file with a column whose values contain commas and quotes. Read it back
>   with `DictReader`. What type is a number column, and how do you convert it?
> 1. Create a SQLite database file with a table `evals(model, task, score, usd)`.
>   Load rows from a CSV with `executemany`. Commit, reopen the file, and print the
>   three best scores.
> 1. This query is unsafe: `conn.execute(f"DELETE FROM evals WHERE model = '{m}'")`.
>   Show an input that deletes everything. Rewrite it safely. Why can you not use a
>   placeholder for the table name?
> 1. Using `models` and `runs` from this chapter, write one query that returns
>   total cost per *vendor*, only for vendors with more than 3000 tokens in total.
>   Which clause filters the buckets?
> 1. Give an example where `LEFT JOIN` and `JOIN` return different row counts.
>   Which rows are missing in the inner join?
> 1. (Needs Redis or Valkey.) Cache replies with a 30-second expiry, store run details as a
>   hash, and show `ttl` counting down.
>

> [!success] Achievement unlocked: Persistent Data
> You can now:
>
> - read and write CSV, JSON, TOML and XML and say what types each preserves;
> - create SQLite tables and run SELECT, WHERE, ORDER BY, GROUP BY and JOIN queries;
> - use parameterized queries, commit and rollback, and explain SQL injection;
> - tell the three SQLAlchemy levels apart and know why to learn SQL first;
> - pick between a file, SQLite, PostgreSQL, Redis and a vector store for a job.
>

---
Related: [[20 - Files]] · [[17 - Text Data]] · [[22 - Data in Space - Networks]] · [[24 - The Web]] · [[25 - Data Science]] · [[26 - AI]] · [[18 - Binary Data]]
