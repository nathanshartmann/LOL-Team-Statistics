#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: nathanhartmann
# @Date:   2015-06-12 21:39:25
# @Last Modified by:   nathanhartmann
# @Last Modified time: 2015-06-29 17:25:09

from config import versus3_filename, versus5_filename, champions_filename
import pickle


def print_content(champion_by_player):

    with open(champions_filename) as fp:
        champions_reference = pickle.load(fp)
    print('\n')
    print("---------------------")
    for player, data in champion_by_player.items():
        print("Jogador: {}".format(player))
        print("---")
        for champion, result in data.items():
            champion_name = champions_reference[champion]

            if result['lose'] > 0:
                total = result['victory'] + result['lose']
                percentual_vitoria = float(result['victory']) / total * 100
            else:
                percentual_vitoria = 100

            if result['deaths'] > 0:
                worth = result['kills'] + result['assists']
                kda = float(worth) / result['deaths']
            else:
                kda = result['kills'] + result['assists']
            matches = result['victory'] + result['lose']
            print("Campeão: {}".format(champion_name))
            print("\tVitórias/Derrotas: {victory}/{lose} ({percent}%)".format(
                  victory=result['victory'],
                  lose=result['lose'],
                  percent=round(percentual_vitoria, 2)))
            print("\tKDA: {k}/{d}/{a} ({kda})").format(
                k=round(result['kills'] / float(matches), 2),
                d=round(result['deaths'] / float(matches), 2),
                a=round(result['assists'] / float(matches), 2),
                kda=round(kda, 2))
            print("\tWards compradas: {wards}".format(
                  wards=round(result['wards'] / float(matches), 2)))
            print("\tGold por kill: {gold}".format(
                  gold=round(result['gold'] / worth, 2)))
            print('\n')
        print("---------------------")


def update_champion_performance(pool):

    champion_by_player = dict()
    for play in pool:
        player = play[0]
        champion = play[1]
        details = play[2]
        result = play[3]
        if player not in champion_by_player:
            champion_by_player[player] = dict()
        if champion not in champion_by_player[player]:
            champion_by_player[player][champion] = {'victory': 0,
                                                    'lose': 0,
                                                    'kills': 0,
                                                    'deaths': 0,
                                                    'assists': 0,
                                                    'wards': 0,
                                                    'gold': 0}
        if result:
            champion_by_player[player][champion]['victory'] += 1
        else:
            champion_by_player[player][champion]['lose'] += 1
        champion_by_player[player][champion]['kills'] += details['kills']
        champion_by_player[player][champion]['deaths'] += details['deaths']
        champion_by_player[player][champion]['assists'] += details['assists']
        champion_by_player[player][champion]['wards'] += details['wards']
        champion_by_player[player][champion]['gold'] += details['gold']
    return champion_by_player


def get_champions_performance(mode):

    if mode == '5v5':
        matches_filename = versus5_filename
    elif mode == '3v3':
        matches_filename = versus3_filename
    else:
        raise Exception("Tipo de partida não reconhecido para recolha.")

    with open(matches_filename) as fp:
        matches = pickle.load(fp)

    pool = list()
    for match in matches:
        result = match[0]['result']
        details = match[1]
        players_ref = match[2]
        players_id = [id for id, _ in players_ref]

        for player in details:
            player_id = player['participantId']
            player_name = players_ref[players_id.index(player_id)][1]
            champion_id = player['championId']
            wards = player['stats']['sightWardsBoughtInGame'] + \
                player['stats']['visionWardsBoughtInGame']
            gold = \
                sum(i for i in player['timeline']['goldPerMinDeltas'].values())

            player_details = {'kills': player['stats']['kills'],
                              'deaths': player['stats']['deaths'],
                              'assists': player['stats']['assists'],
                              'wards': wards,
                              'gold': gold}
            pool.append((player_name, champion_id, player_details, result))
    return update_champion_performance(pool)

if __name__ == "__main__":

    games = '5v5'
#    games = '3v3'

    champion_by_player = get_champions_performance(games)

    print_content(champion_by_player)
