import sys
import ast
from pymongo import MongoClient

def Backup(players):

    output = open('output', 'w')  # open the output file

    for dictKeyIndex in range(1,len(list(players[0].keys()))):  # writes the key names first as a sort of header for the output file
        output.write(list(players[0].keys())[dictKeyIndex])
        if dictKeyIndex != len(list(players[0].keys()))-1:
            output.write('---')
    output.write('\n')

    for player in players:  # writes the actual data, without the keys to reduce output size
        outputString = ''  # initialize the string which will be written to disk
        for dictValue in player:
            if dictValue == '_id':
                continue
            outputString += (str(player[dictValue]))
            outputString += ('---')  # separates values
        outputString = outputString[0:len(outputString)-3]
        output.write(outputString)
        output.write('\n')  # separates players

def Restore(playersCol):
    file = open('output')
    penguins = file.read()

    penguins = penguins.split('\n')  # split the string into dictKeys + individual players
    dictKeys = penguins[0].split('---')  # get the dictionary keys
    playersDict = dict.fromkeys(dictKeys)  # initialize the dictionary
    penguins = penguins[1:len(penguins)-1]  # ignore the first line, which was used in the previous line

    for player in penguins:
        player = player.split('---')
        playersDictCopy = playersDict.copy()
        i=0
        for key in playersDictCopy:
            playersDictCopy[key] = player[i]  # insert values in the dictionary
            i+=1
        playersCol.insert_one(playersDictCopy)  # insert the dictionary in the database
        print('inserted', playersDictCopy)

while True:
    client = MongoClient()
    db = client[sys.argv[1]]  # get the db whose name we parsed to the script
    playersCol = db['players']

    players = playersCol.find()  # extract all players from the database

    print('press 1 to backup\n' + 'press 2 to restore\n' + 'press anything else to exit\n')
    selector = input()
    if(selector == '1'):
        Backup(players)
    elif(selector == '2'):
        Restore(playersCol)
    else:
        break
