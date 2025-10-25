import os
from bs4 import BeautifulSoup
import requests

source_folder = "./source/www.slowgerman.com" # Папка с исходными HTML
target_folder = "./out/podcast"               # Папка для новых файлов
os.makedirs(target_folder, exist_ok=True)

# Рекурсивно обходим все файлы
for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    soup = BeautifulSoup(f, "html.parser")
                except Exception as e:
                    print(f"Error parsing {path}: {e}")
                    continue

                # Ищем заголовок h1
                h1_tag = soup.find("h1", class_="entry-title")
                if not h1_tag:
                    continue
                h1_text = h1_tag.get_text(strip=True)
                if h1_text.find("SG ") == -1 and h1_text.find("#") == -1 and h1_text.find("Kleiner Alien") == -1:
                    continue

                # Формируем безопасное имя файла
                safe_name = "".join(c for c in h1_text if c.isalnum() or c in " _-#").strip()
                new_file_path = os.path.join(target_folder, f"{safe_name}")
                print(new_file_path)


                # Ищем контент
                content_div = soup.find("div", class_="entry-content")
                if not content_div:
                    continue

                paragraphs = [
                    str(p)
                    for p in content_div.find_all("p")
                    if "Text der Episode als PDF:" not in p.get_text()
                ]
                p_content = " ".join(paragraphs)

                # Записываем в новый файл
                with open(new_file_path + ".html", "w", encoding="utf-8") as out_f:
                    out_f.write(str(h1_tag) + "\n\n" + p_content)


                # mp3
                if False:
                    source_tag = content_div.find("source", {"type": "audio/mpeg"})
                    mp3_filename = new_file_path + ".mp3"
                    if not os.path.exists(mp3_filename) and source_tag and source_tag.get("src"):
                        mp3_url = source_tag["src"]
                        mp3_url = mp3_url.replace("../../../../", "https://slowgerman.com/")


                        # скачиваем
                        try:
                            r = requests.get(mp3_url)
                            r.raise_for_status()
                            with open(mp3_filename, "wb") as f:
                                f.write(r.content)

                            print(f"MP3 сохранён: {mp3_filename}")
                        except Exception as e:
                            print(f"Ошибка при скачивании MP3: {e}")



print("Готово!")
