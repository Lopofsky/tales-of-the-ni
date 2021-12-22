from multiprocessing import *
from itertools import permutations
import os

letters = 'αθχυνρωτηκε'
num_of_letters = 0
min_letters_search = 3

def multi_p(letters, i, fin_words):
    all_words = []
    all_words = [''.join(p) for p in permutations(letters, i) if ''.join(p) not in all_words]
    fin_words.append(all_words)
    print("I'm done! i =", i)

def find_actual_words(contents, fin_words):
    results = list(set(fin_words).intersection(set(contents)))
    print("Dictionary File Contents & Random Words Combinations, Comparison Completed => Results =", len(results))
    return results

if __name__ == '__main__':
    manager = Manager()
    fin_words = manager.list()
    all_processes = []
    if num_of_letters == 0:
        for num_of_letters in range(min_letters_search, len(letters) + 1, 1):
            p = Process(target=multi_p, args=(letters, num_of_letters, fin_words))
            all_processes.append(p)
            p.start()
    else:
        p = Process(target=multi_p, args=(letters, num_of_letters, fin_words))
        all_processes.append(p)
        p.start()
    for process in all_processes:
        process.join()
    fin_words = [an_item for a_list in fin_words for an_item in a_list]
    #os.chdir("words")
    with open("res.txt", "r+", encoding="utf-8") as f:
        contents = f.read().splitlines()
    actual_words = find_actual_words(contents, fin_words)
    print("Dictionary's Size:", len(contents))
    print("All possible combinations:", len(fin_words))
    print("All possible words (count):", len(actual_words))
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(actual_words))
    print("Done! Find the results @", os.getcwd(), ', "results.txt" file.')