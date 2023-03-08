from poem_gen.form_ngrams import FormNgrams


ngrams = FormNgrams('data', randomness=0.1)
ngrams.load_txt('Mayakovsky.txt')

print('prompt = ""')
for n in range(1, 4):
    print(f'{n})', ngrams.generate(''))
print('\nprompt = "любовь"')
for n in range(1, 4):
    print(f'{n})', ngrams.generate('любовь'))
print('\nprompt = "ведь если"')
for n in range(1, 4):
    print(f'{n})', ngrams.generate('ведь если'))
