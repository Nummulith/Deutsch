import csv

# https://github.com/repodiac/german_compound_splitter
from german_compound_splitter import comp_split

print("-")

dictionary = '.\\german.dic'
ahocs = comp_split.read_dictionary_from_file(dictionary)

input = 'statistix.csv'
output = "splitter.txt"

with open(input, encoding='utf-8') as f:
    reader = csv.DictReader(f)

    with open(output, "w", encoding="utf-8") as outfile:
        
        for i, row in enumerate(reader):
            # pr(f"{i}, {row["Question"]}, {row["Answer"]}")
            compound = row["Wort"].strip()
            if not compound:
                continue
            
            # compound = 'Donaudampfschifffahrtskapitänsmützenabzeichen'
            # print(f'SPLIT WORDS: plain: {compound}')

            try:
                dissection = comp_split.dissect(compound, ahocs, make_singular=True)
                postMerge  = comp_split.merge_fractions(dissection)
            except Exception as e:
                dissection = [compound]
                postMerge  = [compound]
                # print(f"error {compound}: {e}")

            # dissection = comp_split.dissect(compound, ahocs, make_singular=True)
            if len(postMerge) > 1:
                print(f'SPLIT WORDS: {compound}, plain: {dissection}, post-merge:{postMerge}')
            # print(f'post-merge:{comp_split.merge_fractions(dissection)}')

            # lang, _ = langid.classify(line)
            # if lang == "de":
            #     words = line.split()
            #     split_line = []
            #     for word in words:
            #         parts = dc.split(word)
            #         split_line.extend(parts if parts else [word])
            outfile.write(" ".join(postMerge) + "\n")
