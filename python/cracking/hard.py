"""Hard Stuff"""
import math
import re
from . import bits
def no_plus_add(num1, num2):
    nstr1 = str(num1)
    nstr2 = str(num2)
    mlen = max(len(nstr1), len(nstr2))
    nstr1 = nstr1[::-1].ljust(mlen, "0")
    nstr2 = nstr2[::-1].ljust(mlen, "0")

    carry_over = "0"
    out = ""
    addition_matrix = [
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
        ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        ["4", "5", "6", "7", "8", "9", "10", "11", "12", "13"],
        ["5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
        ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
        ["7", "8", "9", "10", "11", "12", "13", "14", "15", "16"],
        ["8", "9", "10", "11", "12", "13", "14", "15", "16", "17"],
        ["9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
    ]
    for idx in range(0, mlen):
        char1 = nstr1[idx]
        char2 = nstr2[idx]
        temp_carry = "0"
        nsum = addition_matrix[int(char2)][int(char1)]
        if len(nsum) > 1:
            temp_carry = nsum[0]
            nsum = nsum[1]
        # Semi-redundant carry over check
        if carry_over != "0":
            nsum = addition_matrix[int(nsum)][int(carry_over)]
            if len(nsum) > 1:
                temp_carry = nsum[0]
                nsum = nsum[1]
        out += nsum
        carry_over = temp_carry
    out += carry_over
    out = out[::-1].lstrip("0")
    if not out:
        out = "0"
    return out

def missing_int_by_bit(arr):
    size = len(arr)
    missing = None
    for idx in range(size):
        if not idx%2:
            zero = bits.get_bit(arr[idx], 0)
            if zero != 0:
                missing = idx-1
                zero = bits.get_bit(arr[idx-1], 0)
                if zero != 0:
                    missing = idx
                print("Missing odd {}".format(bin(missing-1)))
        if idx%2 and not missing:
            one = bits.get_bit(arr[idx], int(math.log(max(idx-1, 1), 2)))
            if one != 1:
                missing = idx - 1
        if missing:
            return missing
    return missing

def letters_and_numbers(arr):
    print("".join(arr))
    letters = 0
    numbers = 0
    previous = ''
    index_map = {}
    for idx, char in enumerate(arr):
        if char.isalpha():
            if not previous.isalpha():
                letters = 0
            letters += 1
            if letters == numbers:
                start_idx = idx + 1 - letters - numbers
                index_map.update({start_idx: letters})
                numbers = 0
        else:
            if previous.isalpha():
                numbers = 0
            numbers += 1
            if letters == numbers:
                start_idx = idx + 1 - letters - numbers
                index_map.update({start_idx: letters})
                letters = 0
        previous = char
    max_idx = 0
    max_val = 0
    for key, val in index_map.items():
        if val > max_val:
            max_idx = key
            max_val = val
    print("Max length {}".format(index_map.get(max_idx)))
    return arr[max_idx:(max_idx + index_map.get(max_idx) + index_map.get(max_idx))]

def baby_names(name_stats, synonyms):
    all_names = {}
    all_stats = {}
    for pair in synonyms:
        entry = all_names.get(pair[0], set())
        entry.add(pair[1])
        entry.add(pair[0])
        all_names.update({pair[0]: entry})
        entry = all_names.get(pair[1], set())
        entry.add(pair[1])
        entry.add(pair[0])
        all_names.update({pair[1]: entry})
    for name_stat in name_stats:
        nicks = all_names.get(name_stat[0], [])
        for nick in nicks:
            total = all_stats.get(nick, 0)
            total += name_stat[1]
            all_stats.update({nick: total})
    return all_stats

def prime_multiples(offset):
    primes = [3, 5, 7]
    multiple = [1]
    for idx in range(0, offset, 3):
        for prime in primes:
            base = multiple[idx]
            multiple.append(base*prime)
    return multiple[offset-1]

def upcase_group(matchobj):
    return " " + matchobj.group(0).upper() + " "

def re_space(text, vocab):
    for word in vocab:
        text = re.sub(word, upcase_group, text)
    return text

def schedule(arr):
    one = 0
    two = 0
    size = len(arr) - 1
    while size > 0:
        best = arr[size] + two
        alt_best = one
        current = max(best, alt_best)
        two = one
        one = current
        size -= 1
    return one

def size_subarray(arr, subarray):
    collected = []
    size = 0
    for num in arr:
        size += 1
        if num in subarray:
            collected.append(num)
        if sorted(collected) == sorted(subarray):
            break
    return size

def shortest_superseq(arr, subarray):
    starts = {}
    size = len(arr)
    idx = 0
    while idx < size:
        if arr[idx] in subarray:
            subsize = size_subarray(arr[idx:], subarray)
            starts.update({idx: subsize})
        idx += 1
    start = 0
    max_size = 0
    for idx, size in starts.items():
        if size > max_size:
            start = idx
            max_size = size
    return (start, start+max_size)

def volume_histogram(arr):
    size = len(arr)
    vol = 0

    idx = 0
    left_maxes = [0] * size
    l_max = arr[idx]
    while idx < size:
        l_max = max(l_max, arr[idx])
        left_maxes[idx] = l_max
        idx += 1

    idx = size-1
    r_max = arr[idx]
    while idx >= 0:
        r_max = max(r_max, arr[idx])
        sub_max = min(r_max, left_maxes[idx])
        if sub_max > arr[idx]:
            vol += sub_max - arr[idx]
        idx -= 1
    return vol
