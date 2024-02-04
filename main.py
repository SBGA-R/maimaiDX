import math
from dataclasses import dataclass


@dataclass
class RatingTable:
    name: str
    achieve: int
    offset: int


# https://zh.moegirl.org.cn/Maimai%E7%B3%BB%E5%88%97
RECORDS: list[RatingTable] = [
    RatingTable("SSS+", 1005000, 224),
    RatingTable("SSS", 1004999, 222),  #
    RatingTable("SSS", 1000000, 216),
    RatingTable("SS+", 999999, 214),  #
    RatingTable("SS+", 995000, 211),
    RatingTable("SS", 990000, 208),
    RatingTable("S+", 989999, 206),  #
    RatingTable("S+", 980000, 203),
    RatingTable("S", 970000, 200),
    RatingTable("AAA", 969999, 176),  #
    RatingTable("AAA", 940000, 168),
    RatingTable("AA", 900000, 152),  #
    RatingTable("A", 800000, 136),
    RatingTable("BBB", 799999, 128),
    RatingTable("BBB", 750000, 120),
    RatingTable("BB", 700000, 112),
    RatingTable("B", 600000, 96),
    RatingTable("C", 500000, 80),
    RatingTable("D", 400000, 64),
    RatingTable("D", 300000, 48),
    RatingTable("D", 200000, 32),
    RatingTable("D", 100000, 16),
    RatingTable("D", 0, 0),
]


def rating(_achievement: int, _difficulty: float):
    assert 0 <= _achievement <= 101_0000
    assert 0 <= _difficulty <= 15

    _rt = filter(lambda _r: _achievement >= _r.achieve, RECORDS).__next__()
    return math.floor(_difficulty * _rt.achieve * _rt.offset / 1_0000 / 100 / 10)


if __name__ == '__main__':
    print(rating(101_0000, 15))
