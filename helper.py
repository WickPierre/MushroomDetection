from PIL import Image

# Открываем изображение
image_path = "back_of_design.jpg"
image = Image.open(image_path)

# Определяем новый размер с соотношением 3:4
new_width = 900  # Можно выбрать другое значение
new_height = int(new_width * 4 / 3)

# Изменяем размер изображения
resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

# Сохраняем обработанное изображение
output_path = "/mnt/data/resized_back_of_design.webp"
resized_image.save(output_path)
output_path
