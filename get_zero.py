import requests
import sys

from tqdm import tqdm


URL = "http://localhost:5007/get_path"


def main():
    for line in tqdm(sys.stdin):
        word = line.strip()
        data = {"text": word, "depth": 1}
        response = requests.post(URL, json=data)
        zeroes = response.json()['result']['zero_paths']
        print("{}\t{}".format(word, ",".join(w.split('_')[0] for w in zeroes)))


if __name__ == "__main__":
    main()
