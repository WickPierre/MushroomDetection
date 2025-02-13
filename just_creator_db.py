import sqlite3
import random
from datetime import datetime, timedelta

# Подключение к базе данных
db_path = "mushrooms.db"  # Укажите путь к вашему файлу базы
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получение списка всех доступных грибов
cursor.execute("SELECT id FROM mushroom;")
mushroom_ids = [row[0] for row in cursor.fetchall()]

# Генерация случайных 10 записей в mushroom_history
random_mushrooms = random.sample(mushroom_ids, min(10, len(mushroom_ids)))
mushroom_history_data = []

for mushroom_id in random_mushrooms:
    random_time = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    formatted_time = random_time.strftime("%Y-%m-%d %H:%M:%S")
    mushroom_history_data.append((mushroom_id, formatted_time))

# Вставка данных в mushroom_history
cursor.executemany(
    "INSERT INTO mushroom_history (mushroom_id, scan_date) VALUES (?, ?);",
    mushroom_history_data,
)
conn.commit()
conn.close()
