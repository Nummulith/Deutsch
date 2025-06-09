import langid

input  = '.\\cards\\some\\test+.txt'
output = '.\\out\\detect.txt'

with open(input , "r", encoding="utf-8") as infile , \
     open(output, "w", encoding="utf-8") as outfile:
    
    for line in infile:
        line = line.strip()
        if not line:
            continue  # пропускаем пустые строки
        
        lang, prob = langid.classify(line)
        if lang == "de":
            outfile.write(line + "\n")
