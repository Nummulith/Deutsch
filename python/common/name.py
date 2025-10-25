import os

directory="./out/Linguistica 360/intermediate"
for filename in os.listdir(directory):
    if filename.endswith(".name"):
        base = filename[:-5]  # убираем ".name"
        name_file = os.path.join(directory, filename)
        txt_file = os.path.join(directory, base + ".txt")

        if os.path.exists(txt_file):
            # читаем содержимое .name
            with open(name_file, "r", encoding="utf-8") as f:
                name_content = f.read().strip()

            # читаем содержимое .txt
            with open(txt_file, "r", encoding="utf-8") as f:
                txt_content = f.read()

            # добавляем имя в начало .txt
            new_content = name_content + "\n" + txt_content

            # записываем обратно
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"Обновлён: {txt_file}")
        else:
            print(f"Нет txt-файла для {name_file}")
