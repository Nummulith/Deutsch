import os
# pip install -U openai-whisper
import whisper

# Путь к папке с MP3
mp3_folder = "out/Linguistica 360/advanced"
# Папка для текстов
text_folder = "out/Linguistica 360/advanced"
os.makedirs(text_folder, exist_ok=True)

model = whisper.load_model("small")  # "medium", можно "small" для скорости

for file in os.listdir(mp3_folder):
    if file.lower().endswith(".mp3"):
        mp3_path = os.path.join(mp3_folder, file)
        text_path = os.path.join(text_folder, file.replace(".mp3", ".txt"))

        if os.path.exists(text_path):
                continue

        print(f"Распознаю {file}...")
        result = model.transcribe(mp3_path, language="de")
        
        # Сохраняем текст
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

print("Готово! Все тексты сохранены.")
