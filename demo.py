from poem_gen.data_processing import Ngrams


ngrams = Ngrams('data')
ngrams.load_txt('Mayakovsky.txt')
print(f'{len(ngrams.ngrams1) = }')
print(f'{len(ngrams.ngrams2) = }')
print(f'{len(ngrams.ngrams3) = }')
print(f'{ngrams.ngrams1.most_common(10) = }')
print(f'{ngrams.ngrams2.most_common(10) = }')
print(f'{ngrams.ngrams3.most_common(10) = }')
