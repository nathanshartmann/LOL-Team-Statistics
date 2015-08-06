#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: nathanhartmann
# @Date:   2015-06-12 21:41:27
# @Last Modified by:   nathanhartmann
# @Last Modified time: 2015-06-29 16:34:05

playerList = [
    (3341755, 'Nathan Space'),
    (3163151, 'Darlan Space'),
    (3336310, 'Alan Space'),
    (416442, 'quad Space'),
    (515991, 'Cooisa'),
    (2578179, 'mtS Space'),
    (3225185, 'BRDemon'),
    (5370631, 'LinkAllan')
]

playersId = [player[0] for player in playerList]

versus3_filename = 'pkl/matches_3v3.pkl'
versus5_filename = 'pkl/matches_5v5.pkl'
champions_filename = 'pkl/champions.pkl'


api_key = 'api_key=7201f0cb-602c-4f70-9730-6940aee5ab30'
dynamic_api_prefix_url = 'https://br.api.pvp.net/api/lol/br/'
static_api_prefix_url = 'https://global.api.pvp.net/api/lol/static-data/'

api_champions_url = "{prefix}{data}{key}".format(
    prefix=static_api_prefix_url,
    data='br/v1.2/champion?',
    key=api_key
)

api_match_url = "{prefix}{data}{key}".format(
    prefix=dynamic_api_prefix_url,
    data='v2.2/match/{gameId}?',
    key=api_key
)

api_team_url = "{prefix}{data}{key}".format(
    prefix=dynamic_api_prefix_url,
    data='v2.4/team/by-summoner/3341755?',
    key=api_key
)
