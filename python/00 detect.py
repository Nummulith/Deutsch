import langid

input  = '.\\out\\00 base.txt'
output = '.\\out\\00 detect.txt'

with open(input , "r", encoding="utf-8") as infile , \
     open(output, "w", encoding="utf-8") as outfile:
    
    for line in infile:
        line = line.strip()
        if not line:
            continue  # пропускаем пустые строки
        
        lang, prob = langid.classify(line)

        print(line, lang)

        if lang != "ru" and lang != "uk" and lang != "be" and lang != "bg" and lang != "kk":
            outfile.write(line + "\n")
