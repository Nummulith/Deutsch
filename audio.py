from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import csv
from pathlib import Path

def pr(txt):
    print(f"\r{(txt):<70}", end='', flush=True)

print()

subfolder = "/current"
input  = './cards' + subfolder
output = './audio' + subfolder

outputPath = Path(output)
outputPath.mkdir(exist_ok=True)

tmp_path = f"./audio/tmp.mp3"

gTTS("вопрос", lang='ru').save(tmp_path)
q_pre = AudioSegment.from_mp3(tmp_path) - 10

gTTS("ответ" , lang='ru').save(tmp_path)
a_pre = AudioSegment.from_mp3(tmp_path) - 10

for csv_file in Path(input).glob('*.csv'):
    folder_name = csv_file.stem
    target_fwd = outputPath / (folder_name + ".fwd")
    target_rev = outputPath / (folder_name + ".rev")

    fwd = True
    rev = False
    q_lang = 'de'
    a_lang = 'ru'

    pauseLen = 3000
    pause = AudioSegment.silent(duration=pauseLen)  # 3 сек

    with open(f"{input}/{csv_file.name}", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        i = 0
        for row in reader:
            q_text = row['Question']
            a_text = row['Answer']

            if q_text[0] == "~":
                if   q_text == "~reverse":
                    rev = a_text != "False"
                elif q_text == "~forward":
                    fwd = a_text != "False"
                elif q_text == "~question_language":
                    q_lang = a_text
                elif q_text == "~answer_language":
                    a_lang = a_text
                elif q_text == "~pause":
                    pauseLen = int(a_text)
                    pause = AudioSegment.silent(duration=pauseLen)  # 3 сек
                continue

            make_fwd = False
            if fwd:
                target_fwd.mkdir(exist_ok=True)
                name_fwd = target_fwd / f"{i:03}.mp3"
                make_fwd = not name_fwd.exists()

            make_rev = False
            if rev:
                target_rev.mkdir(exist_ok=True)
                name_rev = target_rev / f"{i:03}.mp3"
                make_rev = not name_rev.exists()

            if make_fwd or make_rev:
                q_audio = gTTS(q_text, lang=q_lang).save(tmp_path)
                q = AudioSegment.from_mp3(tmp_path)

                a_audio = gTTS(a_text, lang=a_lang).save(tmp_path)
                a = AudioSegment.from_mp3(tmp_path)

                i = i + 1

            if make_fwd:
                pr(f"{target_fwd.name}/{name_fwd.name}")
                card = q_pre + q + pause + a_pre + a
                card.export(name_fwd, format="mp3")

            if make_rev:
                pr(f"{target_rev.name}/{name_rev.name}")
                card = q_pre + a + pause + a_pre + q
                card.export(name_rev, format="mp3")
