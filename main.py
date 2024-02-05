import asyncio
from operator import attrgetter

from peewee import MySQLDatabase, Model, IntegerField, FloatField, CharField

from . import *
from .libraries.maimai_best_50 import ChartInfo, computeRa, UserInfo, Data, DrawBest

MYSQL_DB = MySQLDatabase('aime', user='root',
                         unix_socket="/var/lib/mysql/mysql.sock")

MYSQL_DB.connect()


class Mai2ScoreBest(Model):
    achievement = IntegerField()

    musicId = IntegerField()
    level = IntegerField()

    user = IntegerField()

    deluxscoreMax = IntegerField()
    comboStatus = IntegerField()
    syncStatus = IntegerField()

    class Meta:
        database = MYSQL_DB
        table_name = 'mai2_score_best'


class Mai2StaticMusic(Model):
    difficulty = FloatField()

    songId = IntegerField()
    chartId = IntegerField()

    addedVersion = CharField()
    title = CharField()

    class Meta:
        database = MYSQL_DB
        table_name = 'mai2_static_music'


def get_sm_by_music_id_level(_music_id: int, _level: int) -> Mai2StaticMusic:
    return Mai2StaticMusic.select().where(
        Mai2StaticMusic.songId == _music_id,
        Mai2StaticMusic.chartId == _level
    )


def is_current_version_by_music_id(_music_id: int) -> bool:
    return Mai2StaticMusic.select().where(
        Mai2StaticMusic.songId == _music_id
    ).get().addedVersion == 'FESTiVALPLUS'


class Mai2ProfileDetail(Model):
    user = IntegerField()

    courseRank = IntegerField()

    userName = CharField()
    playerRating = IntegerField()

    class Meta:
        database = MYSQL_DB
        table_name = 'mai2_profile_detail'


if __name__ == '__main__':
    user = 10000
    pd = Mai2ProfileDetail.select().where(Mai2ProfileDetail.user == user).get()

    nickname = pd.userName
    rating = pd.playerRating

    sd: list[ChartInfo] = []
    dx: list[ChartInfo] = []

    for m2sb in Mai2ScoreBest.select().where(Mai2ScoreBest.user == user):
        sm = get_sm_by_music_id_level(m2sb.musicId, m2sb.level).get()
        ra, rate = computeRa(sm.difficulty, m2sb.achievement / 1_0000, True)

        ci = ChartInfo(
            achievements=m2sb.achievement / 1_0000,
            ds=sm.difficulty,
            dxScore=m2sb.deluxscoreMax,
            fc='' if m2sb.comboStatus == 0 else combo_rank[m2sb.comboStatus - 1],
            fs='' if m2sb.syncStatus == 0 else combo_rank[m2sb.syncStatus - 1],

            level='',  # TODO
            level_index=m2sb.level,
            level_label='',  # TODO

            ra=ra,
            rate=rate.lower(),

            song_id=m2sb.musicId,
            title=sm.title,
            type='DX' if is_current_version_by_music_id(m2sb.musicId) else 'SD'
        )

        if is_current_version_by_music_id(m2sb.musicId):
            dx += [ci]
        else:
            sd += [ci]

    dx = sorted(dx, key=attrgetter('ra'), reverse=True)[:15]
    sd = sorted(sd, key=attrgetter('ra'), reverse=True)[:35]

    userinfo = UserInfo(
        additional_rating=pd.courseRank,
        charts=Data(sd=sd, dx=dx),
        nickname=nickname,
        rating=rating,
        username=nickname
    )

    draw = DrawBest(userinfo).draw
    asyncio.run(draw()).save("img1.png")
