import csv
import re

dictionary = '.\\dict.cc\\dict.cc.csv'
input  = "statistix.csv"
output = "translate.csv"

with open(input , "r", encoding="utf-8") as infile,\
     open(output, 'w', encoding='utf-8', newline='') as csvout,\
     open(dictionary, "r", encoding='utf-8') as dictfile\
    :
    dictreader = csv.DictReader(dictfile, delimiter='\t')

    reader = csv.DictReader(infile)
    words = [row['Wort'] for row in reader]
    
    writer = csv.writer(csvout)
    writer.writerow(["Wort", "Ru"])

    trans = {}
    for row in dictreader:
        de = row['De'].lower()

        # subs = "{f},{m},{n},[+Akk.],[+Gen.],[+Dat.],(herum),[herum],[geh.],{pl},[fig.],[auch fig.],[ugs.],[pej.]"
        # subs = subs.split(',')
        # for sub in subs:
        #     de = de.replace(" " + sub, "")
        de = re.sub(r'\s*[\(\[\{\<][^)\]\}\>]*[\)\]\}\>]', '', de)

        if not de in words:
            continue

        ru = row['Ru'].lower()
        
        if not de in trans:
            trans[de] = ru
        else:
            trans[de] += " / " + ru

    for word in words:
        if word in trans:
            writer.writerow([word, trans[word]])
        else:
            writer.writerow([word, ""])
