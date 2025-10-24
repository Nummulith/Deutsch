import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Папка с HTML
source_folder = "./out/www.newsinslowgerman.com"
# Папка для сохранённых mp3
output_folder = "./out/Linguistica 360"
os.makedirs(output_folder, exist_ok=True)

for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith(".html"):
            html_path = os.path.join(root, file)

            with open(html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            # Формируем имя: путь к html + его имя (с заменой / на пробел)
            rel_path    = os.path.relpath(html_path, source_folder)
            safe_name   = rel_path.replace(os.sep, " ")
            safe_name   = os.path.splitext(safe_name)[0]

            if safe_name.endswith("beginners"   ): safe_name = "beginners/"    + safe_name
            if safe_name.endswith("intermediate"): safe_name = "intermediate/" + safe_name
            if safe_name.endswith("advanced"    ): safe_name = "advanced/"     + safe_name
            
            output_path = os.path.join(output_folder, safe_name)

            name = ""
            for h1 in soup.find_all("h1"):
                name = name.strip() + (" " + h1.get_text()).strip()

            name += ". "

            # for h2 in soup.find_all("h2"):
            #     name += h2.get_text().strip() + " "

            for h3 in soup.find_all("h3"):
                name = name.strip() + " " + (h3.get_text()).strip()

            print(f"{root.replace(source_folder, "")} \\ {file} → {output_path} → {name}")
            # Записываем в новый файл
            with open(output_path + ".name", "w", encoding="utf-8") as out_f:
                out_f.write(name)


            # mp3

            # players = soup.find_all("div", class_="player", attrs={"data-src": True})
            # for player in players:
            #     mp3_url = player.get("data-src")
            #     if not mp3_url.endswith(".mp3"):
            #         continue


                # # Скачиваем
                # print(f"Скачиваю: {mp3_url} → {output_path}.mp3")
                # try:
                #     r = requests.get(mp3_url, stream=True)
                #     r.raise_for_status()
                #     with open(output_path + ".mp3", "wb") as out_f:
                #         for chunk in r.iter_content(chunk_size=8192):
                #             out_f.write(chunk)
                # except Exception as e:
                #     print(f"Ошибка при скачивании {mp3_url}: {e}")



print("Готово!")
