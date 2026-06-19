import sqlite3

conn = sqlite3.connect("kbm_nav.db")

cur = conn.cursor()

# ======================
# kbm_nav_data
# ======================

cur.execute("""
CREATE TABLE IF NOT EXISTS kbm_nav_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,

    type INTEGER NOT NULL,

    subtype INTEGER,

    style TEXT,

    details TEXT,

    sub_items TEXT,

    deleted INTEGER NOT NULL DEFAULT 0,

    UNIQUE(title, type)
)
""")

# ======================
# kbm_nav_layout
# ======================

cur.execute("""
CREATE TABLE IF NOT EXISTS kbm_nav_layout (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    type INTEGER NOT NULL,

    row_index INTEGER NOT NULL,

    col_index INTEGER NOT NULL,

    data_id INTEGER NOT NULL
)
""")

conn.commit()

print("SQLite DB initialized.")

conn.close()