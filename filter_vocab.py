import sys


def keep(word):
    return word.isalpha()


def main():
    for line in sys.stdin:
        word = line.strip().split('\t')[0]
        if keep(word):
            sys.stdout.write(line)


if __name__ == "__main__":
    main()
