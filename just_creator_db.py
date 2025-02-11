"""
If you need new db data
"""

import sqlite3

conn = sqlite3.connect("mushrooms.db")
cursor = conn.cursor()

mushroom_data = [
    ("Agaricus bisporus", "mushroom_picture/2.jpg", "2025-02-09"),
    ("Amanita muscaria", "mushroom_picture/3.jpg", "2025-02-09"),
    ("Boletus edulis", "mushroom_picture/4.jpg", "2025-02-09"),
    ("Cantharellus cibarius", "mushroom_picture/5.jpg", "2025-02-09"),
    ("Cortinarius rubellus", "mushroom_picture/6.jpg", "2025-02-09"),
    ("Gyromitra esculenta", "mushroom_picture/7.jpg", "2025-02-09"),
    ("Lactarius deliciosus", "mushroom_picture/8.jpg", "2025-02-09"),
    ("Morchella esculenta", "mushroom_picture/9.jpg", "2025-02-09"),
    ("Pleurotus ostreatus", "mushroom_picture/10.jpg", "2025-02-09"),
    ("Russula emetica", "mushroom_picture/11.jpg", "2025-02-09"),
]


mushroom_history_data = [
    (
        "Agaricus bisporus",
        "mushroom_picture/3.jpg",
        "2025-02-09",
        "Съедобный, широко используемый в кулинарии."
        * 100,  # Текст прокручивается без проблем
    ),
    (
        "Amanita muscaria",
        "mushroom_picture/4.jpg",
        "2025-02-09",
        "Ядовитый, содержит психоактивные вещества.",
    ),
    (
        "Boletus edulis",
        "mushroom_picture/5.jpg",
        "2025-02-09",
        "Высоко ценится в кулинарии, обладает насыщенным вкусом.",
    ),
    (
        "Cantharellus cibarius",
        "mushroom_picture/6.jpg",
        "2025-02-09",
        "Ароматный, съедобный гриб, любимый в европейской кухне.",
    ),
    (
        "Cortinarius rubellus",
        "mushroom_picture/7.jpg",
        "2025-02-09",
        "Очень ядовитый, вызывает тяжелое отравление.",
    ),
    (
        "Gyromitra esculenta",
        "mushroom_picture/8.jpg",
        "2025-02-09",
        "Токсичный, но в некоторых странах употребляется после специальной обработки.",
    ),
    (
        "Lactarius deliciosus",
        "mushroom_picture/9.jpg",
        "2025-02-09",
        "Съедобный гриб с пикантным вкусом.",
    ),
    (
        "Morchella esculenta",
        "mushroom_picture/10.jpg",
        "2025-02-09",
        "Высоко ценится в кулинарии, особенно во французской кухне.",
    ),
    (
        "Pleurotus ostreatus",
        "mushroom_picture/11.jpg",
        "2025-02-09",
        "Популярный съедобный гриб, легко выращивается.",
    ),
    (
        "Russula emetica",
        "mushroom_picture/12.jpg",
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
