import requests
import json

def fetchPokemon(name):
    pokemonToSearch = name.lower()
    apiUrl = "https://pokeapi.co/api/v2/pokemon/" + pokemonToSearch 

    response = requests.get(apiUrl, timeout=5)

    if response.status_code != 200:
        raise Exception(pokemonToSearch.capitalize() +" is not a registered pokemon")

    pokemonInfo = response.json()
    pokemonTypes = pokemonInfo["types"]

    pokemonName = pokemonInfo["forms"][0]["name"]
    pokemonDexNumber = pokemonInfo["id"]
    secondType = None
    dualType = False

    #Setting up types
    firstType = pokemonTypes[0]["type"]["name"] #first type
    if(len(pokemonTypes)) == 2: #if it has two types (to not go out of range/bounds)
        secondType = pokemonTypes[1]["type"]["name"] #second type
        dualType = True

    spriteUrl = str(pokemonInfo["sprites"]["front_default"])
    artworkUrl = str(pokemonInfo["sprites"]["other"]["official-artwork"]["front_default"])

    speciesInfo = requests.get(pokemonInfo["species"]["url"], timeout=5).json()

    allEntries = speciesInfo["flavor_text_entries"]
    pokedexEntry = None
    #Looks for the english version
    for e in allEntries:
        if e["language"]["name"] == "en":
            pokedexEntry = e["flavor_text"]
            break
    
    statHP = pokemonInfo["stats"][0]["base_stat"]
    statAtk = pokemonInfo["stats"][1]["base_stat"]
    StatDef = pokemonInfo["stats"][2]["base_stat"]
    StatSpAtk = pokemonInfo["stats"][3]["base_stat"]
    StatSpDef = pokemonInfo["stats"][4]["base_stat"]
    StatSpd = pokemonInfo["stats"][5]["base_stat"]


    pokedata = {"name": str(pokemonName).capitalize(),
                "dexNumber": pokemonDexNumber,
                "dualType": dualType,
                "firstType": firstType,
                "secondType": secondType,
                "spriteUrl": spriteUrl,
                "artworkUrl": artworkUrl,
                "dexEntry": pokedexEntry,
                "HP": statHP,
                "Attack": statAtk,
                "Defence": StatDef,
                "SpecialAttack": StatSpAtk,
                "SpecialDefense": StatSpDef,
                "Speed": StatSpd,}
    

    return pokedata