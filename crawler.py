# -*- coding: utf-8 -*-

from urllib import urlopen
import json as jlib
import contextlib
import pickle
from config import (api_champions_url, api_match_url, api_team_url,
                    champions_filename, playersId, playerList,
                    versus3_filename, versus5_filename)


def get_champions():

    url = api_champions_url
    with contextlib.closing(urlopen(url)) as sock:
        html = sock.read()
    json = jlib.loads(html)
    dic = {value['id']: key for key, value in json['data'].items()}
    return dic


def get_team_matchlist():

    url = api_team_url
    with contextlib.closing(urlopen(url)) as sock:
        html = sock.read()
    json = jlib.loads(html)
    for game in json['3341755'][0]['matchHistory']:
        yield{'gameId': game['gameId'],
              'opposingTeamName': game['opposingTeamName'],
              'result': game['win']}


def get_match(match_id):

    url = api_match_url.format(gameId=match_id)
    with contextlib.closing(urlopen(url)) as sock:
        try:
            html = sock.read()
            return jlib.loads(html)
        except:
            return None


def get_players_reference(dic):

    players_reference = []
    for summoner in dic['participantIdentities']:
            if summoner['player']['summonerId'] in playersId:
                id = playersId.index(summoner['player']['summonerId'])
                players_reference.append(
                    (summoner['participantId'], playerList[id][1]))
    return players_reference


def get_new_content(mode):

    matches = get_team_matchlist()
    datas = list()

    for match in matches:
        dic = get_match(match['gameId'])
        if not dic:
            continue

        players_reference = get_players_reference(dic)
        if mode == '5v5' and len(players_reference) != 5:
            continue
        if mode == '3v3' and len(players_reference) != 3:
            continue
        participant_id = [i[0] for i in players_reference]
        player_data = [data for data in dic['participants'] if data['participantId'] in participant_id]
        datas.append([match, player_data, players_reference])
    return datas


def store_new_content(new_content, mode):

    if mode == '5v5':
        matches_filename = versus5_filename
    elif mode == '3v3':
        matches_filename = versus3_filename
    else:
        raise Exception("Tipo de partida não reconhecido para recolha.")
    print(mode)
    with open(matches_filename) as fp:
        matches = pickle.load(fp)
    print("Tamanho anterior da base {}".format(len(matches)))
    for content in new_content:
        if content[0]['gameId'] not in [j[0]['gameId'] for j in matches]:
            matches += [content]
    print("Tamanho atual da base {}".format(len(matches)))
    with open(matches_filename, 'w') as fp:
        pickle.dump(matches, fp)


def print_content(content):

    match = content[0]
    player_data = content[1]
    players_reference = content[2]

    with open(champions_filename) as fp:
        champions = pickle.load(fp)

    print('\n')
    print("---------------------")
    print("Space Team VS {opponent} -- {result}".format(
        opponent=match['opposingTeamName'].encode('utf-8'), result='Vitória'
        if match['result'] is True else 'Derrota'))
    print("---------------------")
    for i in range(len(player_data)):
        stats = player_data[i]['stats']
        print("Jogador: {}".format(players_reference[i][1]))
        print("---")
        print("Campeão: {}".format(champions[player_data[i]['championId']]))
        print("Finalizações: {}".format(stats['kills']))
        print("Mortes: {}".format(stats['deaths']))
        print("Assistências: {}".format(stats['assists']))
        print("Dano causado: {}".format(stats['totalDamageDealtToChampions']))
        print("Dano recebido: {}".format(stats['totalDamageTaken']))
        print("---")
        print("Ouro conquistado: {}".format(stats['goldEarned']))
        print("Tropas eliminadas: {}".format(stats['minionsKilled']))
        print('\n')


def print_matches_database(mode):

    if mode == '5v5':
        matches_filename = versus5_filename
    elif mode == '3v3':
        matches_filename = versus3_filename
    else:
        raise Exception("Tipo de partida não reconhecido para recolha.")
    with open(matches_filename) as fp:
        content_stored = pickle.load(fp)
    for content in content_stored:
        print_content(content)


if __name__ == "__main__":

    games = '5v5'
    new_content = get_new_content(games)
    store_new_content(new_content, games)

#    for content in new_content:
#        print_content(content)

#    print_matches_database(games)

    games = '3v3'
    new_content = get_new_content(games)
    store_new_content(new_content, games)
#    for content in new_content:
#        print_content(content)

#    print_matches_database(games)
