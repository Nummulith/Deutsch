import os
import glob

def rename_files(base_dir="."):
    # ищем все файлы *.name
    for name_file in glob.glob(os.path.join(base_dir, "*.name")):
        # пример имени: "series 2 season 1 chapter 1 beginners.name"
        filename = os.path.basename(name_file)
        
        parts = filename.split()
        try:
            series = parts[1]
            season = parts[3]
            chapter = parts[5]
        except IndexError:
            print(f"Не удалось распарсить: {filename}")
            continue

        # читаем Имя из .name файла
        with open(name_file, "r", encoding="utf-8") as f:
            human_name = f.readline().strip()

        # формируем новое имя без расширения
        new_base = f"{series}-{season}-{chapter}-L0 {human_name}"

        # обрабатываем все расширения
        for ext in [".name", ".txt", ".mp3"]:
            old_file = name_file.replace(".name", ext)
            if os.path.exists(old_file):
                new_file = os.path.join(base_dir, new_base + ext)
                print(f"{old_file} -> {new_file}")
                os.rename(old_file, new_file)

if __name__ == "__main__":
    rename_files("./out/Linguistica 360/intermediate")
