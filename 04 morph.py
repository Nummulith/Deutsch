import csv

print("spacy.load")
import spacy
nlp = spacy.load("de_core_news_sm")
print("spacy.loaded")

input  = ".\\out\\translate.csv"
output = ".\\out\\morph.csv"

with open(output, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Wort", "Num", "Ru", "Lemma", "Pos", "Number", "Case", "Gender", "VerbForm", "Person", "Mood", "Tense", "Degree", "PronType", "Foreign", "Poss", "Definite", "Reflex"]) # , "Morph"

    with open(input, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):

            word = row['Wort']
            num  = row['Num']
            ru   = row['Ru']
            print(f"\r{(f'Wort: {word}'):<70}", end='', flush=True)

            doc = nlp(word)
            for token in doc:
                morph = dict(item.split('=') for item in str(token.morph).split('|') if item != "")
                row = [
                    token.text,
                    num,
                    ru,
                    token.lemma_,
                    token.pos_,
                    morph.get("Number", ""),
                    morph.get("Case", ""),
                    morph.get("Gender", ""),
                    morph.get("VerbForm", ""),
                    morph.get("Person", ""),
                    morph.get("Mood", ""),
                    morph.get("Tense", ""),
                    morph.get("Degree", ""),
                    morph.get("PronType", ""),
                    morph.get("Foreign", ""),
                    morph.get("Poss", ""),
                    morph.get("Definite", ""),
                    morph.get("Reflex", "")
                    # token.morph
                ]
                # row = [word for word in morph]

                writer.writerow(row)
