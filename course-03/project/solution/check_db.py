import sqlite3

# Check external database
ext_conn = sqlite3.connect('data/external/cultpass.db')
ext_cursor = ext_conn.cursor()

# Get tables
ext_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
ext_tables = ext_cursor.fetchall()
print("External DB Tables:", [t[0] for t in ext_tables])

# Check row counts
for table in ext_tables:
    table_name = table[0]
    ext_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = ext_cursor.fetchone()[0]
    print(f"  {table_name}: {count} rows")

ext_conn.close()

# Check core database
core_conn = sqlite3.connect('data/core/udahub.db')
core_cursor = core_conn.cursor()

core_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
core_tables = core_cursor.fetchall()
print("\nCore DB Tables:", [t[0] for t in core_tables])

# Check row counts
for table in core_tables:
    table_name = table[0]
    core_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = core_cursor.fetchone()[0]
    print(f"  {table_name}: {count} rows")

core_conn.close()

