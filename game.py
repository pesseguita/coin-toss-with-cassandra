import datetime
import random

def validation(session, player, country):
    """
    VALIDATION THAT USER AND COUNTRY EXIST IN THE DATABASE
    """
    #Checking if we have the username in the database
    #We have to choose username and country because table profile had partition key Country. Cluster is username and email
    row = session.execute(f"select username from profile where username='{player}' and country='{country}';")
    if len(row.current_rows) == 0:
        print('USER DOES NOT EXIST! DO YOU WANT TO CREATE THIS USER?')
        create = input('y or n')
        if create=='y':
            email=input('INSERT EMAIL:')
            last_name=input('INSERT LAST NAME:')
    #inserting the new user in case it doesn't exist and the user wants to create a new one
            row = session.execute(f"INSERT INTO profile(username, lastname, email, country) VALUES ('{player}', '{last_name}', '{email}', '{country}');")
        else:
            raise ValueError('EXIT')

def insert_winner(session, player_a, player_b, winner):
    #we will insert into table plays
    row = session.execute(f"insert into game.plays (\"id\", \"year\", \"month\", \"player_a\", \"player_b\", \"winner\") Values (now(),'2022','July','{player_a}','{player_b}', '{winner}');")

def profile_toss(session):
    """
    USER LOGIN
    """
    print('@@@ COIN TOSS GAME @@@')
    print('Please login')
    print('----PLAYER A----')

    player_a = input('Insert username:')
    country_a = input('Insert your country:')
    validation(session, player_a, country_a)

    print('----PLAYER B----')
    player_b = input('Insert username:')
    country_b = input('Insert your country:')
    validation(session, player_b, country_b)

    # HEADS OR TAILS SELECTION - PLAYER A CHOOSES FIRST ALWAYS

    print(f'\nPlayer {player_a} chooses coin side')
    pick = input('Heads or Tails? (h/t)')
    print(f'Player {player_a} chooses {pick}')
    print('\n...Tossing coin...')

    #RANDOM COIN TOSS
    toss = 'h' if random.random()<0.5 else 't'
    if pick==toss:
        print(f'@@@ {player_a} WINS @@@')
        insert_winner(session, player_a, player_b, player_a)
    else:
        print(f'@@@ {player_b} WINS @@@')
        insert_winner(session, player_a, player_b, player_b)
    return player_a,player_b

def rank(session, player_a):
    #QUERY USER RANK
        print(f'@@@ PLAYER A {player_a} RANK @@@')
        year = input('YEAR:')
        month = input('MONTH:')
        row = session.execute(f"SELECT count(winner) FROM game.plays WHERE year='{year}' and month='{month}'and winner='{player_a}' ALLOW FILTERING;")
        print('NUMBER OF TIMES A WINNER:', row[0][0])
