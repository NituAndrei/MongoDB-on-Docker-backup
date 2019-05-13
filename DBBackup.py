import sys
import ast
from pymongo import MongoClient

def Backup(players): #todo: compress

    output = open('output', 'w')  # open the output file

    for dictKeyIndex in range(1,len(list(players[0].keys()))):  # writes the key names first as a sort of header for the output file
        output.write(list(players[0].keys())[dictKeyIndex])
        if dictKeyIndex != len(list(players[0].keys()))-1:
            output.write('---')
    output.write('\n')

    for player in players:  # writes the actual data, without the keys to reduce output size
        outputString = ''
        for dictValue in player:
            if dictValue == '_id':
                continue
            outputString += (str(player[dictValue]))
            outputString += ('---')
        outputString = outputString[0:len(outputString)-3]
        output.write(outputString)
        output.write('\n')

def Restore(playersCol):#todo: modify for compressed data
    file = open('output') #todo: replace
    penguins = file.read()

    penguins = penguins.split('\n')  # split the string into individual players individual players (and the dictKeys)
    dictKeys = penguins[0].split('---')  # get the dictionary keys
    playersDict = dict.fromkeys(dictKeys)  # initialize the dictionary
    penguins = penguins[1:len(penguins)-1]

    for player in penguins:
        player = player.split('---')
        i=0
        for key in playersDict:
            playersDict[key] = player[i]
            i+=1
        playersCol.insert_one(playersDict)
    # penguins = penguins.split('},')
    # for i in range(len(penguins) - 1):
    #     penguins[i] = penguins[i] + '}'
    #
    # # adding the data to penguinsDict
    # penguinsDict = []
    # for i in range(len(penguins)):
    #     print(penguins[i])
    #     penguinsDict.append(ast.literal_eval(penguins[i]))
    # print(penguinsDict[0])

while True:
    client = MongoClient()
    db = client[sys.argv[1]]  # get the db whose name we parsed to the script
    playersCol = db['players']

    players = playersCol.find()  # extract all players from the database

    Restore(playersCol) #todo: remove this
    print('press 1 to backup\n' + 'press 2 to restore\n' + 'press anything else to exit\n')
    selector = input()
    if(selector == '1'):
        Backup(players)
    elif(selector == '2'):
        Restore(playersCol)
    else:
        break
