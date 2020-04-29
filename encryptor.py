import json
import string
import argparse
import sys
from collections import defaultdict

lowercase = string.ascii_lowercase
uppercase = lowercase.upper()
cycle = 26


def caesar_symbol(i, key, letter_type):
    return letter_type[(letter_type.index(i) + key) % cycle]


def encryption_caesar_symbol(i, key):
    if i.isalpha():
        return caesar_symbol(i, key, lowercase if i in lowercase else uppercase)
    return i


def encryption_caesar(s, key):
    return "".join(encryption_caesar_symbol(i, key) for i in s)


def vigenere_symbol(i, num, key, letter_type):
    return letter_type[(letter_type.index(i) + lowercase.index(key[num % len(key)].lower())) % cycle]


def encryption_vigenere_symbol(i, num, key):
    if i.isalpha():
        return vigenere_symbol(i, num, key, lowercase if i in lowercase else uppercase)
    return i


def encryption_vigenere(s, key):
    res = []
    count = 0
    for i in range(len(s)):
        res.append(encryption_vigenere_symbol(s[i], count, key))
        if s[i].isalpha():
            count += 1
    return res


def bar_chart(s):
    dict_s = defaultdict(int)
    count = 0
    for i in s.lower():
        if i in lowercase:
            dict_s[i] += 1
            count += 1
    for i in dict_s:
        dict_s[i] /= count
    return dict_s


def hack(s, dict_train):
    diff = None
    key = 0
    for i in range(cycle):
        res = encryption_caesar(s, i)
        dict_s = bar_chart(res)
        comp = compare_chart(dict_train, dict_s)
        if diff is None or comp < diff:
            diff = comp
            key = i
    return key


def compare_chart(dict_train, dict_s):
    diff = 0
    for i in dict_train:
        diff += abs(dict_train[i] - dict_s[i])
    return diff


def get_text(args):
    if args.input_file is not None:
        with open(args.input_file, "r") as f:
            s = f.read()
    else:
        s = sys.stdin.read()
    return s


def get_key(args):
    key = args.key
    if args.cipher == "caesar":
        key = int(args.key)
    return key


def write_text(args, res):
    if args.output_file is not None:
        with open(args.output_file, "w") as f:
            for i in range(len(res)):
                f.write(res[i])
    else:
        for i in range(len(res)):
            print(res[i], end="")


def process_encode(args):
    key = get_key(args)

    s = get_text(args)

    if args.cipher == "caesar":
        if args.subparsers_name == "decode":
            key = 26 - key % 26
        res = encryption_caesar(s, key)
    else:
        if args.subparsers_name == "decode":
            new_key = []
            for i in key:
                new_key.append(lowercase[(26 - lowercase.index(i) % 26) % 26])
            key = new_key
        res = encryption_vigenere(s, key)

    write_text(args, res)


def process_train(args):
    if args.text_file is not None:
        with open(args.text_file, "r") as f:
            s = f.read()
    else:
        s = sys.stdin.read()

    dict_train = bar_chart(s)
    json.dump(dict_train, open(args.model_file, "w"))


def process_hack(args):
    s = get_text(args)

    with open(args.model_file, "r") as f:
        dict_train = json.load(f)
    key = hack(s, dict_train)
    res = encryption_caesar(s, key)

    write_text(args, res)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="subparsers_name")
    encode_parser = subparsers.add_parser("encode")
    encode_parser.add_argument("--cipher", required=True)
    encode_parser.add_argument("--key", required=True)
    encode_parser.add_argument("--input-file", dest="input_file")
    encode_parser.add_argument("--output-file", dest="output_file")
    encode_parser.set_defaults(func=process_encode)

    decode_parser = subparsers.add_parser("decode")
    decode_parser.add_argument("--cipher", required=True)
    decode_parser.add_argument("--key", required=True)
    decode_parser.add_argument("--input-file", dest="input_file")
    decode_parser.add_argument("--output-file", dest="output_file")
    decode_parser.set_defaults(func=process_encode)

    train_parser = subparsers.add_parser("train")
    train_parser.add_argument("--text-file")
    train_parser.add_argument("--model-file", required=True)
    train_parser.set_defaults(func=process_train)

    hack_parser = subparsers.add_parser("hack")
    hack_parser.add_argument("--input-file", dest="input_file")
    hack_parser.add_argument("--output-file", dest="output_file")
    hack_parser.add_argument("--model-file", required=True)
    hack_parser.set_defaults(func=process_hack)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
