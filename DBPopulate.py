from pymongo import MongoClient
import ast

# extract db data from json file
file = open("penguins_players.json")
penguins = file.read()

# doing some cleanup, as the string data needs to be converted to a dictionary
penguins = penguins.split('},')
for i in range(len(penguins)-1):
    penguins[i] = penguins[i]+'}'

# adding the data to penguinsDict
penguinsDict = []
for i in range(len(penguins)):
    penguinsDict.append(ast.literal_eval(penguins[i]))

# populating the database
client = MongoClient()
db = client["Penguins"]
players = db["players"]
players.insert_many(penguinsDict)