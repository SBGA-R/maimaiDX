import asyncio
from operator import attrgetter

from . import *
from .data import Mai2ProfileDetail, Mai2ScoreBest, get_sm_by_music_id_level, is_current_version_by_music_id, \
    is_sd_by_musicId_level
from .libraries.maimai_best_50 import ChartInfo, computeRa, UserInfo, Data, DrawBest

if __name__ == '__main__':
    user = 10001
    pd = Mai2ProfileDetail.select().where(Mai2ProfileDetail.user == user)
    pd = list(pd)[-1]

    nickname = pd.userName
    rating = pd.playerRating

    sd: list[ChartInfo] = []
    dx: list[ChartInfo] = []

    for m2sb in Mai2ScoreBest.select().where(  # Utage
            Mai2ScoreBest.user == user, Mai2ScoreBest.level != 10):

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
            type='SD' if is_sd_by_musicId_level(m2sb.musicId, m2sb.level) else 'DX'
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
