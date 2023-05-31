from random_words import RandomWords
import random


def generate_txt(line_num, words_per_line):
    rw = RandomWords()
    words = rw.random_words(count=40)

    with open("../resources/words.txt", "w") as f:
        for i in range(line_num):
            line = " ".join([random.choice(words) for _ in range(words_per_line)])
            f.write(line + "\n")


if __name__ == '__main__':
    line_num = 1000
    words_per_line = 10
    generate_txt(line_num, words_per_line)
