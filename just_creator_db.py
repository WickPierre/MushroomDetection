"""
If you need new db data
"""

import sqlite3

conn = sqlite3.connect("mushrooms.db")
cursor = conn.cursor()

mushroom_data = [
    ("Agaricus bisporus", "photos/1.jpg", "2025-02-09"),
    ("Amanita muscaria", "photos/1.jpg", "2025-02-09"),
    ("Boletus edulis", "photos/1.jpg", "2025-02-09"),
    ("Cantharellus cibarius", "photos/1.jpg", "2025-02-09"),
    ("Cortinarius rubellus", "photos/1.jpg", "2025-02-09"),
    ("Gyromitra esculenta", "photos/1.jpg", "2025-02-09"),
    ("Lactarius deliciosus", "photos/1.jpg", "2025-02-09"),
    ("Morchella esculenta", "photos/1.jpg", "2025-02-09"),
    ("Pleurotus ostreatus", "photos/1.jpg", "2025-02-09"),
    ("Russula emetica", "photos/1.jpg", "2025-02-09"),
]


mushroom_history_data = [
    (
        "Agaricus bisporus",
        "photos/1.jpg",
        "2025-02-09",
        "Съедобный, широко используемый в кулинарии."
        * 100,  # Текст прокручивается без проблем
    ),
    (
        "Amanita muscaria",
        "photos/1.jpg",
        "2025-02-09",
        "Ядовитый, содержит психоактивные вещества.",
    ),
    (
        "Boletus edulis",
        "photos/1.jpg",
        "2025-02-09",
        "Высоко ценится в кулинарии, обладает насыщенным вкусом.",
    ),
    (
        "Cantharellus cibarius",
        "photos/1.jpg",
        "2025-02-09",
        "Ароматный, съедобный гриб, любимый в европейской кухне.",
    ),
    (
        "Cortinarius rubellus",
        "photos/1.jpg",
        "2025-02-09",
        "Очень ядовитый, вызывает тяжелое отравление.",
    ),
    (
        "Gyromitra esculenta",
        "photos/1.jpg",
        "2025-02-09",
        "Токсичный, но в некоторых странах употребляется после специальной обработки.",
    ),
    (
        "Lactarius deliciosus",
        "photos/1.jpg",
        "2025-02-09",
        "Съедобный гриб с пикантным вкусом.",
    ),
    (
        "Morchella esculenta",
        "photos/1.jpg",
        "2025-02-09",
        "Высоко ценится в кулинарии, особенно во французской кухне.",
    ),
    (
        "Pleurotus ostreatus",
        "photos/1.jpg",
        "2025-02-09",
        "Популярный съедобный гриб, легко выращивается.",
    ),
    (
        "Russula emetica",
        "photos/1.jpg",
        "2025-02-09",
        "Ядовитый гриб, вызывает рвоту и отравление.",
    ),
]
cursor.executemany(
    "INSERT INTO mushroom_history (name, image_path, scan_date, description) VALUES (?, ?, ?, ?);",
    mushroom_history_data,
)

conn.commit()
conn.close()

"Данные успешно добавлены в базу."
