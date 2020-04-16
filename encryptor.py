import json
import string
import argparse

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
        return lowercase[(lowercase.index(i) +
                          lowercase.index(key[num % len(key)].lower())) % 26]
    if i in uppercase:
        return uppercase[(uppercase.index(i) +
                          lowercase.index(key[num % len(key)].lower())) % 26]
    return i


def encryption_vigenere(s, key):
    res = ""
    for i in range(len(s)):
        res += encryption_vigenere_symbol(s[i], i, key)
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
        return lowercase[(lowercase.index(i) + 26 -
                          lowercase.index(key[num % len(key)].lower())) % 26]
    if i in uppercase:
        return uppercase[(uppercase.index(i) + 26 -
                          lowercase.index(key[num % len(key)].lower())) % 26]
    return i


def decryption_vigenere(s, key):
    res = ""
    for i in range(len(s)):
        res += decryption_vigenere_symbol(s[i], i, key)
    return res


def bar_chart(s):
    arr = {}
    for i in lowercase:
        arr[i] = 0
    for i in s:
        arr[i] += 1
    for i in arr:
        arr[i] /= len(s)
    return arr


def hack(s, dict):
    diff = 26 * 26
    key = 0
    for i in range(26):
        res = encryption_caesar(s, i)
        arr = bar_chart(res)
        comp = compare_chart(dict, arr)
        if comp < diff:
            diff = comp
            key = i
    return key


def compare_chart(dict, arr):
    diff = 0
    for i in dict:
        diff += abs(dict[i] - arr[i])
    return diff


parser = argparse.ArgumentParser()
parser.add_argument('act')
parser.add_argument('--cipher')
parser.add_argument('--key', dest='key')
parser.add_argument('--input-file', dest='input_file')
parser.add_argument('--output-file', dest='output_file')
parser.add_argument('--text-file', dest='text_file')
parser.add_argument('--model-file', dest='model_file')
args = parser.parse_args()

key = args.key
if args.cipher == "caesar":
    key = int(args.key)

if args.input_file is not None:
    with open(args.input_file, 'r') as f:
        s = f.read()
else:
    s = str(input())

if args.act == "encode":
    if args.cipher == "caesar":
        res = encryption_caesar(s, key)
    else:
        res = encryption_vigenere(s, key)

if args.act == "decode":
    if args.cipher == "caesar":
        res = decryption_caesar(s, key)
    else:
        res = decryption_vigenere(s, key)

if args.act == "train":
    arr = bar_chart(s)
    json.dump(arr, open(args.model_file, "w"))

if args.act == "hack":
    with open(args.model_file, 'r') as f:
        dict = json.load(f)
    key = hack(s, dict)
    res = encryption_caesar(s, key)

if args.act != 'train':
    if args.output_file is not None:
        with open(args.output_file, 'w') as f:
            f.write(res)
    else:
        print(res)

