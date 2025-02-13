import sqlite3
from datetime import datetime
import os


def init_db():
    conn = sqlite3.connect("mushrooms.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS mushroom (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            image_path TEXT NOT NULL,
            description TEXT NOT NULL
        )
        """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS mushroom_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mushroom_id INTEGER NOT NULL,
            scan_date TEXT NOT NULL,
            FOREIGN KEY (mushroom_id) REFERENCES mushroom (id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()

    if not os.path.exists("mushroom_names.txt") or not os.path.exists("desc.txt"):
        return

    with open("mushroom_names.txt", "r", encoding="utf-8") as f:
        mushrooms = [line.strip() for line in f.readlines() if line.strip()]

    with open("desc.txt", "r", encoding="utf-8") as f:
        descriptions = f.read().split("?????")

    descriptions = [desc.strip() for desc in descriptions if desc.strip()]

    for i, mushroom in enumerate(mushrooms):
        description = (
            descriptions[i] if i < len(descriptions) else "Описание отсутствует."
        )
        cursor.execute(
            "INSERT OR IGNORE INTO mushroom (name, image_path, description) VALUES (?, ?, ?)",
            (mushroom, f"mushroom_picture/{mushroom}.jpg", description),
        )
    conn.commit()
    conn.close()


def get_mushroom_id(mushroom_name):
    conn = sqlite3.connect("mushrooms.db")
    cursor = conn.cursor()
    mushroom_id = cursor.execute(
        f"SELECT id FROM mushroom WHERE name='{mushroom_name}'"
    ).fetchone()[0]
    conn.close()
    return mushroom_id


def save_mushroom_scan(mushroom_name):
    conn = sqlite3.connect("mushrooms.db")
    cursor = conn.cursor()
    mushroom_id = get_mushroom_id(mushroom_name)
    cursor.execute(
        "INSERT INTO mushroom_history (mushroom_id, scan_date) VALUES (?, ?) ",
        (mushroom_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def get_saved_mushrooms():
    conn = sqlite3.connect("mushrooms.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT mh.id, m.name, m.image_path, mh.scan_date, m.description
        FROM mushroom_history mh
        JOIN mushroom m ON mh.mushroom_id = m.id
        ORDER BY mh.scan_date DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "history_id": row[0],
            "name": row[1],
            "image_path": row[2],
            "scan_date": row[3],
            "description": row[4],
        }
        for row in rows
    ]


def delete_mushroom_scan(history_id):
    conn = sqlite3.connect("mushrooms.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mushroom_history WHERE id = ?", (history_id,))
    conn.commit()
    conn.close()


def clear_history():
    conn = sqlite3.connect("mushrooms.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mushroom_history")
    conn.commit()
    conn.close()


# def init_db():
#     conn = sqlite3.connect("mushrooms.db")
#     cursor = conn.cursor()
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS mushroom_history (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             image_path TEXT NOT NULL,
#             scan_date TEXT NOT NULL,
#             description TEXT NOT NULL DEFAULT ''
#         )
#         """
#     )
#     conn.commit()
#     conn.close()


# def save_mushroom(name, image_path, description=""):
#     # just save
#     conn = sqlite3.connect("mushrooms.db")
#     cursor = conn.cursor()
#     cursor.execute(
#         """
#         INSERT INTO mushroom_history (name, image_path, scan_date, description)
#         VALUES (?, ?, ?, ?)
#         """,
#         (name, image_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description),
#     )
#     conn.commit()
#     conn.close()


# def get_saved_mushrooms():
#     # returner of info
#     conn = sqlite3.connect("mushrooms.db")
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT name, image_path, scan_date, description FROM mushroom_history"
#     )
#     rows = cursor.fetchall()
#     conn.close()
#     return [
#         {
#             "name": row[0],
#             "image_path": row[1],
#             "scan_date": row[2],
#             "description": row[3],
#         }
#         for row in rows
#     ]
#
#
# def delete_mushroom(mushroom_id):
#     # delete where id
#     conn = sqlite3.connect("mushrooms.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM mushroom_history WHERE id = ?", (mushroom_id,))
#     conn.commit()
#     conn.close()


# def clear_history():
#     # delete все записи из истории сканирований
#     conn = sqlite3.connect("mushrooms.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM mushroom_history")
#     conn.commit()
#     conn.close()
