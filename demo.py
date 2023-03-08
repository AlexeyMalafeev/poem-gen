from poem_gen.naive_ngrams import NaiveNgrams


ngrams = NaiveNgrams('data')
ngrams.load_txt('Mayakovsky.txt')
# print(f'{len(ngrams.ngrams1) = }')
# print(f'{len(ngrams.ngrams2) = }')
# print(f'{len(ngrams.ngrams3) = }')
# top_k = 10
# print(f'{ngrams.ngrams1.most_common(top_k) = }')
# print(f'{ngrams.ngrams2.most_common(top_k) = }')
# print(f'{ngrams.ngrams3.most_common(top_k) = }')

print(ngrams.generate(''))
print(ngrams.generate('любовь'))
print(ngrams.generate('ведь если'))

while True:
    print(ngrams.generate(input('> ')))
