"""Testing Cracking stuff"""
import random
import uuid
import pytest
from random_word import RandomWords
from cracking import oop, dynamic, collections, concurrent, hard

def generate_array(size):
    if not size:
        return []
    arr = [0] * size
    for index in range(size):
        arr[index] = random.randint(0, size+1)
    return arr

def generate_sequential_array(low, high, miss=False):
    if low == high:
        return []
    arr = []
    remove = None
    for idx in range(low, high):
        arr.append(idx)
    if miss:
        remove = random.randint(8, len(arr)-2)
        arr.pop(remove)
    return arr, remove

def generate_words(amount, with_synonyms=False):
    rwords = RandomWords()
    words = rwords.get_random_words(limit=amount)
    synonyms = None
    if with_synonyms:
        synonyms = []
        for idx, _ in enumerate(words):
            if random.randint(20, 1000)%11 > 7 and idx < len(words)-1:
                pair = (words[idx], words[idx+1])
                synonyms.append(pair)
    return words, synonyms

@pytest.mark.parametrize("test_input,expected", [
    (10, False),
])
def test_minesweeper(test_input, expected):
    minesmap = oop.Map(test_input, random.randint(0, 2))
    minesmap.click(2, 2)
    minesmap.click(random.randint(0, test_input),
                   random.randint(0, test_input))
    print("\n")
    print(minesmap)
    assert not expected

@pytest.mark.parametrize("test_input,expected", [
    (10, 274),
    (3, 4),
    (0, 0),
    (20, 121415),
    (50, 10562230626642)
])
def test_triple_step(test_input, expected):
    assert dynamic.triple_step(test_input) == expected

@pytest.mark.parametrize("test_input,expected", [
    ([1, 2, 3, 4, 4], 4),
    ([1, 2, 3, 4, 5], -1),
    ([0, 2, 4], 0),
    ([1, 2, 3], -1)
])
def test_magic_index(test_input, expected):
    assert dynamic.magic_index(test_input) == expected

@pytest.mark.parametrize("test_input,expected", [
    (3, [2, 1, 0]),
    (2, [1, 0]),
    (4, [3, 2, 1, 0]),
    (5, [4, 3, 2, 1, 0])
])
def test_hanoi_towers(test_input, expected):
    first_tower = dynamic.Tower()
    for i in reversed(range(test_input)):
        first_tower.push(i)
    towers = {
        1: first_tower,
        2: dynamic.Tower(0),
        3: dynamic.Tower(0)
    }

    assert dynamic.hanoi_towers(towers, 1, 3).get(3).stack == expected

@pytest.mark.parametrize("len1,len2", [
    (10, 20),
    (20, 2),
    (100, 5),
    (2, 100)
])
def test_sorted_merge(len1, len2):
    arr1 = sorted(generate_array(len1))
    arr2 = sorted(generate_array(len2))
    expected = sorted(arr1 + arr2)
    res = collections.sorted_merge(arr1, arr2)
    assert res == expected


@pytest.mark.parametrize("size,num", [
    (20, 10),
    (20, 2),
    (100, 5),
    (2000, 1500)
])
def test_listy_search(size, num):
    arr = generate_array(size)
    expected = num in arr
    listy = collections.Listy(arr)
    found = collections.listy_search(listy, num) != -1
    assert found == expected

@pytest.mark.parametrize("stream,numbers", [
    ([5, 1, 4, 4, 5, 9, 7, 7, 7, 7, 13, 3], {1: 0, 3: 1, 4: 3, 7: 9}),
    ([0, 0, 1, 4, 6, 7, 10, 10], {0: 1, 1: 2, 7: 5})
])
def test_ranker(stream, numbers):
    ranker = collections.StreamRanker()
    for num in stream:
        ranker.track(num)
    for val, rank in numbers.items():
        assert ranker.get_rank(val) == rank

@pytest.mark.parametrize("size", [
    (100),
    (200),
    (300)
])
def test_peaks_and_valleys(size):
    arr = generate_array(size)
    res = collections.peaks_and_valleys(arr.copy())
    assert res != arr

@pytest.mark.parametrize("num", [
    (100),
    (200),
    (300)
])
def test_mt_fizzbuzz(num):
    assert concurrent.mt_fizzbuzz(num) == num

@pytest.mark.parametrize("num1,num2", [
    (1, 2),
    (11, 21),
    (39, 399),
    (10000, 123),
    (99999, 1),
    (0, 0)
])
def test_no_plus_add(num1, num2):
    res = hard.no_plus_add(num1, num2)
    print("Sum of {} and {} is {}".format(num1, num2, res))
    assert int(res) == (num1 + num2)


@pytest.mark.parametrize("low,high", [
    (0, 100),
    (0, 220),
    (0, 300)
])
def test_missing_int_by_bit(low, high):
    arr, removed = generate_sequential_array(low, high, True)
    print("Removed {}".format(removed))
    diff = abs(hard.missing_int_by_bit(arr) - removed)
    assert diff < 2

@pytest.mark.parametrize("times", [
    (1),
    (5),
    (7)
])
def test_letters_and_numbers(times):
    arr = []
    for _ in range(times):
        add = list(str(uuid.uuid4()).replace("-", ""))
        arr += add
    subarray = hard.letters_and_numbers(arr)
    print("Subarray {}".format(subarray))
    assert subarray

@pytest.mark.parametrize("amount", [
    (10),
    (20),
    (100),
    (1000)
])
def test_baby_names(amount):
    names, nicks = generate_words(amount, True)
    names = list(map(lambda word: (word, random.randint(2, 30)), names))
    stat_totals = hard.baby_names(names, nicks)
    assert stat_totals

@pytest.mark.parametrize("offset", [
    (10),
    (20),
    (100),
    (1000)
])
def test_prime_multiples(offset):
    multiple = hard.prime_multiples(offset)
    print("{}th is {}".format(offset, multiple))
    assert multiple > offset

@pytest.mark.parametrize("size", [
    (10),
    (20),
    (100),
    (300)
])
def test_re_space(size):
    words, _ = generate_words(size, False)
    text = ''.join(words)
    vocab = []
    for _ in range(int(size*0.75)):
        vocab.append(random.choice(words))
    assert hard.re_space(text, vocab)

@pytest.mark.parametrize("size", [
    (10),
    (20),
    (100),
    (300)
])
def test_schedule(size):
    arr = generate_array(size)
    arr = [x*15 for x in arr]
    work = hard.schedule(arr)
    print("Appts: {}\n\tWork: {}".format(arr, work))
    assert work


@pytest.mark.parametrize("size", [
    (10),
    (20),
    (100),
    (300)
])
def test_shortest_superseq(size):
    arr = generate_array(size)
    subarr = [arr[random.randint(2, size)],
              arr[random.randint(2, size)],
              arr[random.randint(2, size)]
             ]
    subseq = hard.shortest_superseq(arr, subarr)
    print("In array {}\nSubarray {}\n\tsubsequence is {}"
          .format(arr, subarr, arr[subseq[0]:subseq[1]]))
    assert subarr

@pytest.mark.parametrize("arr", [
    [0, 0, 4, 0, 0, 6, 0, 0, 3, 0, 8, 0, 2, 0, 5, 2, 0, 3, 0, 0],
    [0, 2, 0, 0, 3, 0, 8, 0, 3, 0, 2, 5],
    [9, 0, 4, 0, 0, 6, 0, 0, 3, 0, 8, 0, 2, 0, 5, 2, 0, 3, 0, 2],
    [0, 0, 0, 0, 1, 0, 1]
])
def test_volume_histogram(arr):
    volume = hard.volume_histogram(arr)
    print("Histogram: {}\nhas volume: {}".format(arr, volume))
    assert volume
