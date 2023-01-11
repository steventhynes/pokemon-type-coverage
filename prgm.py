from pprint import pprint
import string
from unicodedata import name
import pokemon
import urllib3
from itertools import product

types = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying", "Ghost", "Grass", "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock", "Steel", "Water"]
pokemon_data = {pokemon.Pokes[poke]["species"]:pokemon.Pokes[poke] for poke in pokemon.Pokes}
# print(pokemon_data)

def isSuperEffective(atktype, poke):
    deftypes = pokemon_data[poke]["types"]
    g = 1
    for z in deftypes:
        g *= getEffectivenessModifier(atktype, z)
        if atktype == "Ground" and "Levitate" in pokemon_data[poke]["abilities"].values():
            return False
        elif (atktype == "Fire" or atktype == "Ice") and "Thick Fat" in pokemon_data[poke]["abilities"].values():
            g *= 0.5
        elif atktype == "Fire":
            if "Dry Skin" in pokemon_data[poke]["abilities"].values() or "Fluffy" in pokemon_data[poke]["abilities"].values():
                g *= 2
            elif "Flash Fire" in pokemon_data[poke]["abilities"].values():
                return False
            elif "Heatproof" in pokemon_data[poke]["abilities"].values():
                g *= 0.5
        elif atktype == "Water":
            if "Dry Skin" in pokemon_data[poke]["abilities"].values() or "Water Absorb" in pokemon_data[poke]["abilities"].values() or "Storm Drain" in pokemon_data[poke]["abilities"].values():
                return False
        elif atktype == "Electric":
            if "Motor Drive" in pokemon_data[poke]["abilities"].values() or "Volt Absorb" in pokemon_data[poke]["abilities"].values() or "Lightning Rod" in pokemon_data[poke]["abilities"].values():
                return False
        elif atktype == "Grass" and "Sap Sipper" in pokemon_data[poke]["abilities"].values():
            return False
    if g > 1:
        return True
    return False

def getEffectivenessModifier(a, d):
    if a == "Bug":
        if d in ["Psychic", "Grass", "Dark"]:
            return 2
        if d in ["Fighting", "Fire", "Flying", "Ghost", "Poison", "Steel", "Fairy"]:
            return 0.5
    if a == "Dark":
        if d in ["Ghost", "Psychic"]:
            return 2
        if d in ["Dark", "Fighting", "Fairy"]:
            return 0.5
    if a == "Dragon":
        if d in ["Dragon"]:
            return 2
        if d in ["Steel"]:
            return 0.5
        if d in ["Fairy"]:
            return 0
    if a == "Electric":
        if d in ["Flying", "Water"]:
            return 2
        if d in ["Dragon", "Electric", "Grass"]:
            return 0.5
        if d in ["Ground"]:
            return 0
    if a == "Fairy":
        if d in ["Dark", "Dragon", "Fighting"]:
            return 2
        if d in ["Fire", "Poison", "Steel"]:
            return 0.5
    if a == "Fighting":
        if d in ["Dark", "Ice", "Normal", "Rock", "Steel"]:
            return 2
        if d in ["Bug", "Fairy", "Flying", "Poison", "Psychic"]:
            return 0.5
        if d in ["Ghost"]:
            return 0
    if a == "Fire":
        if d in ["Bug", "Grass", "Ice", "Steel"]:
            return 2
        if d in ["Dragon", "Fire", "Rock", "Water"]:
            return 0.5
    if a == "Flying":
        if d in ["Bug", "Fighting", "Grass"]:
            return 2
        if d in ["Electric", "Rock", "Steel"]:
            return 0.5
    if a == "Ghost":
        if d in ["Ghost", "Psychic"]:
            return 2
        if d in ["Dark"]:
            return 0.5
        if d in ["Normal"]:
            return 0
    if a == "Grass":
        if d in ["Ground", "Rock", "Water"]:
            return 2
        if d in ["Bug", "Dragon", "Fire", "Flying", "Grass", "Poison", "Steel"]:
            return 0.5
    if a == "Ground":
        if d in ["Electric", "Fire", "Poison", "Rock", "Steel"]:
            return 2
        if d in ["Bug", "Grass"]:
            return 0.5
        if d in ["Flying"]:
            return 0
    if a == "Ice":
        if d in ["Dragon", "Flying", "Grass", "Ground"]:
            return 2
        if d in ["Fire", "Ice", "Steel", "Water"]:
            return 0.5
    if a == "Normal":
        if d in ["Rock", "Steel"]:
            return 0.5
        if d in ["Ghost"]:
            return 0
    if a == "Poison":
        if d in ["Grass", "Fairy"]:
            return 2
        if d in ["Ghost", "Ground", "Poison", "Rock"]:
            return 0.5
        if d in ["Steel"]:
            return 0
    if a == "Psychic":
        if d in ["Fighting", "Poison"]:
            return 2
        if d in ["Psychic", "Steel"]:
            return 0.5
        if d in ["Dark"]:
            return 0
    if a == "Rock":
        if d in ["Bug", "Fire", "Flying", "Ice"]:
            return 2
        if d in ["Fighting", "Ground", "Steel"]:
            return 0.5
    if a == "Steel":
        if d in ["Fairy", "Ice", "Rock"]:
            return 2
        if d in ["Electric", "Fire", "Steel", "Water"]:
            return 0.5
    if a == "Water":
        if d in ["Fire", "Ground", "Rock"]:
            return 2
        if d in ["Dragon", "Grass", "Water"]:
            return 0.5
    return 1

usagedata = {}
currentDate = "2022-12"
tier = "gen6ou-0"
num_moves = 5

pm = urllib3.PoolManager()
usagetext = str(pm.request("GET", "http://www.smogon.com/stats/" + currentDate + "/" + tier + ".txt").data)
lines = usagetext.split("\\n")
for line in lines[5:-2]:
    poke = str.strip(line[10:28]) #gets name of pokemon
    if poke == "NidoranM":
        poke = "Nidoran-M"
    elif poke == "NidoranF":
        poke = "Nidoran-F"
    usage = str.strip(line[30:39]) #gets usage percentage
    # print((poke, usage))
    usagedata[poke] = usage


file = open("output.txt", "w")
print("Analysis is in progress. This will take a while.")
results = []
visited_combos = set()
# for a1 in types:
#     for a2 in types:
#         for a3 in types:
#             for a4 in types:
product_input = [types] * num_moves
all_combos = list(product(*product_input))
for move_tuple in all_combos:
    combo = frozenset(move_tuple)
    if combo in visited_combos:
        continue
    visited_combos.add(combo)
    score = 0
    beatenPokemon = []
    #file.write("\n" + a1 + ", " + a2 + ", " + a3 + ", " + a4)
    for p in usagedata:
        for move in move_tuple:
            if isSuperEffective(move, p):
                beatenPokemon.append(p)
                score += float(usagedata[p])
                break
    #file.write("\nResults: " + str(len(beatenPokemon)) + " out of " + str(len(usagedata)) + ", " + str(score) + " points")
    results.append(tuple([combo, score, tuple(beatenPokemon)]))
results_list = list(results)
print("Sorting...")
results_list.sort(key=lambda x: x[1], reverse=True)
for i in results_list:
    file.write("\n" + str(i))
print("\nFinished.")
