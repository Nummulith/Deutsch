import csv

input_file  = ".\\cards\\some\\Место wo, da (Dict).csv"
output_file = ".\\out\\QA.csv"

Q = 'De'
A = 'Ru'

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=['Question', 'Answer'])

    writer.writeheader()
    for row in reader:
        writer.writerow({
            'Question': row[Q],
            'Answer'  : row[A]
        })
