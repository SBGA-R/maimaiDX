import math
from dataclasses import dataclass

from peewee import MySQLDatabase, Model, IntegerField, FloatField, CharField

from .libraries.maimai_best_50 import generate


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


def calculate_rating_by_achievement_difficulty(_achievement: int, _difficulty: float) -> int:
    assert 0 <= _achievement <= 101_0000
    assert 0 <= _difficulty <= 15

    _rt = filter(lambda _r: _achievement >= _r.achieve, RECORDS).__next__()
    return math.floor(_difficulty * _rt.achieve * _rt.offset / 1_0000 / 100 / 10)


MYSQL_DB = MySQLDatabase('aime', user='root',
                         unix_socket="/var/lib/mysql/mysql.sock")

MYSQL_DB.connect()


class Mai2ScoreBest(Model):
    achievement = IntegerField()

    musicId = IntegerField()
    level = IntegerField()

    user = IntegerField()

    class Meta:
        database = MYSQL_DB
        table_name = 'mai2_score_best'


class Mai2StaticMusic(Model):
    difficulty = FloatField()

    songId = IntegerField()
    chartId = IntegerField()

    addedVersion = CharField()

    class Meta:
        database = MYSQL_DB
        table_name = 'mai2_static_music'


def get_difficulty_by_music_id_level(_music_id: int, _level: int) -> float:
    return Mai2StaticMusic.select().where(
        Mai2StaticMusic.songId == _music_id,
        Mai2StaticMusic.chartId == _level
    ).get().difficulty


def is_current_version_by_music_id(_music_id: int) -> bool:
    return Mai2StaticMusic.select().where(
        Mai2StaticMusic.songId == _music_id
    ).get().addedVersion == 'FESTiVALPLUS'


if __name__ == '__main__':
    generate()
    exit()

    for m2sb in Mai2ScoreBest.select().where(Mai2ScoreBest.user == 10000):
        difficulty = get_difficulty_by_music_id_level(m2sb.musicId, m2sb.level)
        rating = calculate_rating_by_achievement_difficulty(m2sb.achievement, difficulty)

        print(is_current_version_by_music_id(m2sb.musicId))
