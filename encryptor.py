import json
import string
import argparse
import sys
from collections import defaultdict

lowercase = string.ascii_lowercase
uppercase = lowercase.upper()
cycle = len(lowercase)


def caesar_symbol(char, key, letter_type):
    return letter_type[(letter_type.index(char) + key) % cycle]


def encryption_caesar_symbol(char, key):
    if char.isalpha():
        return caesar_symbol(char, key, lowercase if char.islower() else uppercase)
    return char


def encryption_caesar(s, key):
    return "".join(encryption_caesar_symbol(char, key) for char in s)


def vigenere_symbol(char, num, key, letter_type):
    return letter_type[(letter_type.index(char) + lowercase.index(key[num % len(key)].lower())) % cycle]


def encryption_vigenere_symbol(char, num, key):
    if char.isalpha():
        return vigenere_symbol(char, num, key, lowercase if char.islower() else uppercase)
    return char


def encryption_vigenere(s, key):
    res = []
    count = 0
    for char in s:
        res.append(encryption_vigenere_symbol(char, count, key))
        if char.isalpha():
            count += 1
    return "".join(char for char in res)


def bar_chart(s):
    dict_s = defaultdict(int)
    count = 0
    for char in s:
        if char.isalpha():
            dict_s[char.lower()] += 1
            count += 1
    for char in dict_s:
        dict_s[char] /= count
    return dict_s


def hack(s, dict_train):
    key = 0
    dict_s = bar_chart(s)
    diff = compare_chart(dict_train, dict_s)
    for i in range(1, cycle):
        comp = compare_chart(dict_train, dict_s, i)
        if comp < diff:
            diff = comp
            key = i
    return cycle - key


def compare_chart(dict_train, dict_s, num=0):
    diff = 0
    for char in dict_train:
        diff += abs(dict_train[char] - dict_s[lowercase[(lowercase.index(char) + num) % cycle]])
    return diff


def get_text(file):
    if file is not None:
        with open(file, "r") as f:
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
            f.write(res)
    else:
        print(res)


def process_encode(args):
    key = get_key(args)

    s = get_text(args.input_file)

    if args.cipher == "caesar":
        if args.subparsers_name == "decode":
            key = cycle - key % cycle
        res = encryption_caesar(s, key)
    else:
        if args.subparsers_name == "decode":
            new_key = []
            for i in key:
                new_key.append(lowercase[(cycle - lowercase.index(i) % cycle) % cycle])
            key = new_key
        res = encryption_vigenere(s, key)

    write_text(args, res)


def process_train(args):
    s = get_text(args.text_file)

    dict_train = bar_chart(s)
    json.dump(dict_train, open(args.model_file, "w"))


def process_hack(args):
    s = get_text(args.input_file)

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
