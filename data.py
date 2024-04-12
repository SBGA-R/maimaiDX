from peewee import MySQLDatabase, Model, IntegerField, FloatField, CharField

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
    ).get().addedVersion == 'BUDDiES'


class Mai2ProfileDetail(Model):
    user = IntegerField()

    courseRank = IntegerField()

    userName = CharField()
    playerRating = IntegerField()

    class Meta:
        database = MYSQL_DB
        table_name = 'mai2_profile_detail'


class Mai2Playlog(Model):
    tapCriticalPerfect = IntegerField()
    tapPerfect = IntegerField()
    tapGreat = IntegerField()
    tapGood = IntegerField()
    tapMiss = IntegerField()

    holdCriticalPerfect = IntegerField()
    holdPerfect = IntegerField()
    holdGreat = IntegerField()
    holdGood = IntegerField()
    holdMiss = IntegerField()

    slideCriticalPerfect = IntegerField()
    slidePerfect = IntegerField()
    slideGreat = IntegerField()
    slideGood = IntegerField()
    slideMiss = IntegerField()

    touchCriticalPerfect = IntegerField()
    touchPerfect = IntegerField()
    touchGreat = IntegerField()
    touchGood = IntegerField()
    touchMiss = IntegerField()

    breakCriticalPerfect = IntegerField()
    breakPerfect = IntegerField()
    breakGreat = IntegerField()
    breakGood = IntegerField()
    breakMiss = IntegerField()

    musicId = IntegerField()
    level = IntegerField()

    class Meta:
        database = MYSQL_DB
        table_name = 'mai2_playlog'


def notes_by_musicId_level(_musicId: int, _level: int) -> list[int]:
    p = Mai2Playlog.select().where(
        Mai2Playlog.musicId == _musicId,
        Mai2Playlog.level == _level
    ).limit(1).get()

    return [
        p.tapCriticalPerfect + p.tapPerfect + p.tapGreat + p.tapGood + p.tapMiss,
        p.holdCriticalPerfect + p.holdPerfect + p.holdGreat + p.holdGood + p.holdMiss,
        p.slideCriticalPerfect + p.slidePerfect + p.slideGreat + p.slideGood + p.slideMiss,
        p.touchCriticalPerfect + p.touchPerfect + p.touchGreat + p.touchGood + p.touchMiss,
        p.breakCriticalPerfect + p.breakPerfect + p.breakGreat + p.breakGood + p.breakMiss
    ]


def is_sd_by_musicId_level(_musicId: int, _level: int) -> bool:
    return notes_by_musicId_level(_musicId, _level)[3] == 0
