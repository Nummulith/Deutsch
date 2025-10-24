import os
import re
from bs4 import BeautifulSoup

# папка с html-файлами
input_dir = "./out/podcast"
output_dir = "./out/podcast"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(".html"):
        filepath = os.path.join(input_dir, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        result_lines = []

        # h1 -> просто текст + \n
        for h1 in soup.find_all("h1"):
            text = h1.get_text(strip=True)
            if text:
                result_lines.append(text)
                result_lines.append("")  # пустая строка после заголовка

        # p -> разбиваем на предложения + \n
        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                # Разделение на предложения (по . ! ?), сохраняя разделители
                sentences = re.split(r'([.!?])', text)
                # Склеиваем пары: предложение + знак
                sentences = ["".join(sentences[i:i+2]).strip()
                             for i in range(0, len(sentences), 2)]
                result_lines.extend(sentences)
                # result_lines.append("")  # пустая строка после <p>

        # сохраняем в txt
        out_filename = os.path.splitext(filename)[0] + ".txt"
        out_path = os.path.join(output_dir, out_filename)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(result_lines))

print("Готово! Все txt-файлы лежат в папке:", output_dir)
