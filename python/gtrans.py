import os
import html
import time
import random

from googletrans import Translator
# pip install googletrans==4.0.0-rc1

# pip install transformers torch

from transformers import MarianMTModel, MarianTokenizer

# Загружаем модель и токенизатор
model_de_en_name = "Helsinki-NLP/opus-mt-de-en" # Helsinki-NLP
tokenizer_de_en = MarianTokenizer.from_pretrained(model_de_en_name, local_files_only=True)
model_de_en = MarianMTModel.from_pretrained(model_de_en_name)

model_en_ru_name = "Helsinki-NLP/opus-mt-en-ru"
tokenizer_en_ru = MarianTokenizer.from_pretrained(model_en_ru_name, local_files_only=True)
model_en_ru = MarianMTModel.from_pretrained(model_en_ru_name)

def hl_translate(text: str) -> str:
    tr = text.lower()

    inputs = tokenizer_de_en(tr, return_tensors="pt", padding=True)
    translated = model_de_en.generate(**inputs)
    tr = tokenizer_de_en.decode(translated[0], skip_special_tokens=True)

    inputs = tokenizer_en_ru(tr, return_tensors="pt", padding=True)
    translated = model_en_ru.generate(**inputs)
    tr = tokenizer_en_ru.decode(translated[0], skip_special_tokens=True)

    return tr

dct = {}

translator = Translator()

remchr = str.maketrans("", "", ",?!.:;\"'()[]{}«»–-„“")

def trans(text, cache = False):

    if cache:
        if text in dct:
            return dct[text]

    # time.sleep(random.uniform(0.8, 1.5))

    try:
        # translation = translator.translate(text, src='de', dest='ru')
        # res = translation.text
        res = hl_translate(text)
    except Exception as e:
        if cache:
            dct[text] = "!"
        print(f"Ошибка перевода: {text} - {e}")
        return "<Ошибка перевода>"


    if cache:
        dct[text] = res

    print(f"\r{text} -> {res}", end="", flush=True)

    return res

# text = "Hallo, wie geht es dir?"
# print(f"Исходный текст: {text}")
# print(f"Перевод: {trans(text)}")


folder     = "./out/podcast"  # укажи путь к папке
out_folder = "./out/podcast"
# os.makedirs(out_folder, exist_ok=True)

def word_to_span(word: str) -> str:
    safe_word = html.escape(word)

    trword = word.translate(remchr)
    if trword != "":
        trword = trans(trword, True)
        safe_word = f'<span title="{trword}">{safe_word}</span>'

    return safe_word

for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(folder, filename)
        out_path = os.path.join(out_folder, filename.replace(".txt", ".html"))
        if os.path.exists(out_path):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if not lines:
            continue

        title = f"<h1>{html.escape(lines[0])}</h1>\n"
        body = ""
        for line in lines[1:]:
            words = line.split()
            spans = " ".join(word_to_span(w) for w in words)
            body += f"<p class='de'>{spans}</p>\n"
            body += f"<p class='ru'>{trans(line)}</p>\n"
        html_text = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>{html.escape(lines[0])}</title>
<style>
body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
h1 {{ color: darkred; }}
span[title] {{
  cursor: help;
  border-bottom: 1px dotted gray;
}}
.de {{
    font-size: 1.5em;   /* чуть меньше обычного */
    font-weight: bold;  /* жирный */
    line-height: 1.0;   /* относительное значение, множитель шрифта */
    margin-top: 7px;    /* расстояние сверху */
    margin-bottom: 0px; /* расстояние снизу */
}}
.ru {{
    font-size: 1.2em;   /* чуть меньше обычного */
    color: blue;        /* синий */
    line-height: 1.0;   /* относительное значение, множитель шрифта */
    margin-top: 4px;    /* расстояние сверху */
    margin-bottom: 0px; /* расстояние снизу */
}}
</style>
</head>
<body>
{title}
{body}
</body>
</html>"""

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_text)

        print(f"Создан: {out_path}")

        # continue
