import json
import string
import argparse
import sys


lowercase = string.ascii_lowercase
uppercase = lowercase.upper()


def encryption_caesar_symbol(i, key):
    if i in lowercase:
        return lowercase[(lowercase.index(i) + key) % 26]
    if i in uppercase:
        return uppercase[(uppercase.index(i) + key) % 26]
    return i


def encryption_caesar(s, key):
    res = ""
    for i in s:
        res += encryption_caesar_symbol(i, key)
    return res


def encryption_vigenere_symbol(i, num, key):
    if i in lowercase:
        return lowercase[(lowercase.index(i) + lowercase.index(key[num % len(key)].lower())) % 26]
    if i in uppercase:
        return uppercase[(uppercase.index(i) + lowercase.index(key[num % len(key)].lower())) % 26]
    return i


def encryption_vigenere(s, key):
    res = ""
    count = 0
    for i in range(len(s)):
        res += encryption_vigenere_symbol(s[i], count, key)
        if s[i] in lowercase or s[i] in uppercase:
            count += 1
    return res


def decryption_caesar_symbol(i, key):
    if i in lowercase:
        return lowercase[(lowercase.index(i) + 26 - key % 26) % 26]
    if i in uppercase:
        return uppercase[(uppercase.index(i) + 26 - key % 26) % 26]
    return i


def decryption_caesar(s, key):
    res = ""
    for i in s:
        res += decryption_caesar_symbol(i, key)
    return res


def decryption_vigenere_symbol(i, num, key):
    if i in lowercase:
        return lowercase[
            (lowercase.index(i) + 26 - lowercase.index(key[num % len(key)].lower())) % 26
        ]
    if i in uppercase:
        return uppercase[
            (uppercase.index(i) + 26 - lowercase.index(key[num % len(key)].lower())) % 26
        ]
    return i


def decryption_vigenere(s, key):
    res = ""
    count = 0
    for i in range(len(s)):
        res += decryption_vigenere_symbol(s[i], count, key)
        if s[i] in lowercase or s[i] in uppercase:
            count += 1
    return res


def bar_chart(s):
    arr = {}
    count = 0
    for i in lowercase:
        arr[i] = 0
    for i in s.lower():
        if i in lowercase:
            arr[i] += 1
            count += 1
    for i in arr:
        arr[i] /= count
    return arr


def hack(s, dict):
    diff = None
    key = 0
    for i in range(26):
        res = encryption_caesar(s, i)
        arr = bar_chart(res)
        comp = compare_chart(dict, arr)
        if diff is None or comp < diff:
            diff = comp
            key = i
    return key


def compare_chart(dict, arr):
    diff = 0
    for i in dict:
        diff += abs(dict[i] - arr[i])
    return diff


def get_text(args):
    if args.input_file is not None:
        with open(args.input_file, "r") as f:
            s = f.read()
    else:
        s = sys.stdin.read()
    return s


def write_text(args, res):
    if args.output_file is not None:
        with open(args.output_file, "w") as f:
            f.write(res)
    else:
        print(res)


def process_encode(args):
    key = args.key
    if args.cipher == "caesar":
        key = int(args.key)

    s = get_text(args)

    if args.cipher == "caesar":
        res = encryption_caesar(s, key)
    else:
        res = encryption_vigenere(s, key)

    write_text(args, res)


def process_decode(args):
    key = args.key
    if args.cipher == "caesar":
        key = int(args.key)

    s = get_text(args)

    if args.cipher == "caesar":
        res = decryption_caesar(s, key)
    else:
        res = decryption_vigenere(s, key)

    write_text(args, res)


def process_train(args):
    if args.text_file is not None:
        with open(args.text_file, "r") as f:
            s = f.read()
    else:
        s = sys.stdin.read()

    arr = bar_chart(s)
    json.dump(arr, open(args.model_file, "w"))


def process_hack(args):
    s = get_text(args)

    with open(args.model_file, "r") as f:
        dict = json.load(f)
    key = hack(s, dict)
    res = encryption_caesar(s, key)

    write_text(args, res)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="select mode")
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
    decode_parser.set_defaults(func=process_decode)

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