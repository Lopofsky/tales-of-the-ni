from itertools import permutations
letters = 'ααστλιχ'
num_of_letters = 5
fin_words = []


def gen(string, num_of_letters):
    tempword = ''
    if num_of_letters == 0:
        for i in range(0, len(letters) + 1, 1):
            for p in permutations(string, i):
                tempword = ''.join(p)
                if tempword not in fin_words:
                    print(tempword)
                    fin_words.append(tempword)
    else:
        for p in permutations(string, num_of_letters):
            tempword = ''.join(p)
            if tempword not in fin_words:
                print(tempword)
                fin_words.append(tempword)


gen(letters, num_of_letters)
with open("res.txt", "r+", encoding="utf-8") as f:
    contents = f.read().splitlines()
# Reduce diplicates - deprecated:
# fin_words = list(dict.fromkeys(fin_words))
possible_words_count = 0
for a_word in fin_words:
    if a_word in contents:
        possible_words_count += 1
        print(">>> ", a_word)
print("All possible combinations:", len(fin_words))
print("All possible words:", possible_words_count)
