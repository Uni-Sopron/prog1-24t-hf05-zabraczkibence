import json

def foo():
    with open("data/guests.json", "w") as g:
        g.write("ASD")
    with open("data/guests.json") as g:
        print(g.read())