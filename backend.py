import pandas as pd
import json

#def import_price_file():
#    file = open("prices.csv", "r")
#    global df = pd.read_csv(file)
#    file.close()
    
def increment_counter():
    with open("global.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data["counter"] = data["counter"] + 1
    result = data["counter"]
    with open("global.json", "w") as jsonFile:
        json.dump(data, jsonFile)
    return result