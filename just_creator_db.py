"""
If you need new db data
"""

import sqlite3

conn = sqlite3.connect("mushrooms.db")
cursor = conn.cursor()

mushroom_data = [
    (name := "Agaricus_bisporus".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Amanita_muscaria".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Boletus_edulis".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Cantharellus_cibarius".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Cortinarius_rubellus".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Gyromitra_esculenta".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Lactarius_deliciosus".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Morchella_esculenta".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Pleurotus_ostreatus".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
    (name := "Russula_emetica".lower(), f"mushroom_picture/{name}.jpg", "2025-02-09"),
]


mushroom_history_data = [
    (
        name := "Agaricus_bisporus".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Съедобный, широко используемый в кулинарии."
        * 100,  # Текст прокручивается без проблем
    ),
    (
        name := "Amanita_muscaria".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Ядовитый, содержит психоактивные вещества.",
    ),
    (
        name := "Boletus_edulis".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Высоко ценится в кулинарии, обладает насыщенным вкусом.",
    ),
    (
        name := "Cantharellus_cibarius".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Ароматный, съедобный гриб, любимый в европейской кухне.",
    ),
    (
        name := "Cortinarius_rubellus".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Очень ядовитый, вызывает тяжелое отравление.",
    ),
    (
        name := "Gyromitra_esculenta".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Токсичный, но в некоторых странах употребляется после специальной обработки.",
    ),
    (
        name := "Lactarius_deliciosus".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Съедобный гриб с пикантным вкусом.",
    ),
    (
        name := "Morchella_esculenta".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Высоко ценится в кулинарии, особенно во французской кухне.",
    ),
    (
        name := "Pleurotus_ostreatus".lower(),
        f"mushroom_picture/{name}.jpg",
        "2025-02-09",
        "Популярный съедобный гриб, легко выращивается.",
    ),
    (
        name := "Russula_emetica".lower(),
        f"mushroom_picture/{name}.jpg",
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
