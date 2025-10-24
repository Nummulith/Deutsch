import os
import re

folder = "./out/Linguistica 360/intermediate"  # укажи путь к папке

for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(folder, filename)

        # читаем содержимое
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().strip()

        # первая строка (заголовок) и остальное
        lines = text.split("\n", 1)
        header = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ""

        # разбиваем текст на предложения по . ! ? 
        # при этом сохраняем знак препинания
        sentences = re.split(r'([.!?])', body)

        # склеиваем обратно, чтобы было предложение + перенос строки
        formatted_body = ""
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i].strip()
            punct = sentences[i+1].strip()
            if sentence:
                formatted_body += sentence + punct + "\n"

        # если что-то осталось без знака (например, оборванный конец)
        if len(sentences) % 2 != 0 and sentences[-1].strip():
            formatted_body += sentences[-1].strip() + "\n"

        # собираем итог
        new_text = header + "\n\n" + formatted_body.strip() + "\n"

        # перезаписываем файл
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_text)
