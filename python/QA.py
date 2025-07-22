import csv

inputQ = ".\\out\\Q.csv"
inputA = ".\\out\\A.csv"
output = ".\\out\\QA.csv"

with open(inputQ, newline='', encoding='utf-8') as q_file:
    questions = [row[0] for row in csv.reader(q_file)]

with open(inputA, newline='', encoding='utf-8') as a_file:
    answers = [row[0] for row in csv.reader(a_file)]

if len(questions) != len(answers):
    raise ValueError(f"Количество вопросов ({len(questions)}) и ответов ({len(answers)}) не совпадает.")

with open(output, 'w', newline='', encoding='utf-8') as result_file:
    writer = csv.writer(result_file)
    writer.writerow(['Question', 'Answer'])  # Заголовки
    writer.writerows(zip(questions, answers))
