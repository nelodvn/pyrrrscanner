#!/usr/bin/python2.6
import time
import kittyapi
import sys
import argparse

class KittyManager():
    def __init__(self):
        self.kitties = []

    def addGoldKitty(self, auction, kitty):
        self.kitties.append(auction)
        print "[*] Total found so far: %d" %len(self.kitties)

        self.printKittyInfo(auction, kitty)
    def printKittyInfo(self, auction, kitty):
        ckutils = kittyapi.CKUtils()
        cattributes = ckutils.getKittyCattributes(kitty)

        format =\
"""
[Kitty %s]
|_ name: %s
|_ gen: %s
|_ virgin: %s
|_ color: %s
|_ born: %s
|_ catributes: %s
|_ is ready: %s
|_ cooldown index: %s
|_ cooldown: %s
|_ price: %f
"""
        isVirgin = False
        breedSize = 0
        try:
            if len(kitty['children']) > 0:
                isVirgin = False
            else:
                isVirgin = True
        except KeyError:
            isVirgin = True

        print format % (kitty['id'],\
        kitty['name'],\
        kitty['generation'], \
        isVirgin, \
        kitty['color'],\
        kitty['created_at'], \
        str(cattributes),\
        kitty['status']['is_ready'],\
        kitty['status']['cooldown_index'],\
        kitty['status']['cooldown'],\
        (float(auction['current_price'])/1000000000000000000))



banner = description_string = "prrrruuscanner - cryptokitties.co (CK) scanner, build with pru by nelown\nFeel free to donate some kitties :) 0xccAb13D1e0430b11213a385223423eb4Fe18A129\n"
parser = argparse.ArgumentParser(description=description_string)

parser.add_argument('-gen', '--gen', type=str, help='Cryptokittie generation(s) to search for. Ex: -gen 1, -gen 1,3,5', required=False)
parser.add_argument('-p', '--max_price', type=float, help='Top price filter, set the maximum price here', required=False)
parser.add_argument('-mp', '--min_price', type=float, help='The minium price filter.', required=False)
parser.add_argument('-v', '--virgin', action='store_true', help='True if you are looking for virgins kitties, falsle otherwise', required=False)
parser.add_argument('-go', '--goodies_only', action='store_true', help='Check for the best cattributes only', required=False)
parser.add_argument('-s', '--sire', action='store_true', help='Search for siring auctions instead of selling.', required=False)
parser.add_argument('-c', '--cattributes', type=str, help='Search for informed cattributes only. Same format as -gen', required=False)
parser.add_argument('-color', '--main_color', type=str, help='Search for informed main color only. Same format as -gen', required=False)
parser.add_argument('-k', '--kitty', type=str, help='Retrieve all kitty info', required=False)
parser.add_argument('-f', '--forever', action='store_true', help='Keep scanning forever', required=False)
#parser.add_argument('-cf', '--cattributes_file', action='store_true', help='Search for siring auctions instead of selling. Same format as -gen', required=False)
parser.add_argument('-cooldown', '--cooldown', type=int, help='Filter the cooldown max limit index (fast, snappy, etc)', required=False)

parser.add_argument
args = parser.parse_args()

if __name__ == "__main__":
    print banner

    manager = KittyManager()

    if args.kitty:
        api = kittyapi.CryptokittieAPI()
        manager.printKittyInfo(api.getKitty(args.kitty))
        sys.exit()

    gen = []
    maxPrice = 0
    virginOnly = False
    checkForGoodies = False

    # i'm sure that gotta be a better way of doing this, but...
    if args.gen:
        if "," in args.gen:
            for s in args.gen.split(","):
                gen.append(s)
        else:
            gen.append(args.gen)

    cattributesQueryParam = []
    if args.cattributes:
        if "," in args.cattributes:
            for s in args.cattributes.split(","):
                cattributesQueryParam.append(s)
        else:
            cattributesQueryParam.append(args.cattributes)

    mainColorQueryParam = []
    if args.main_color:
        if "," in args.main_color:
            for s in args.main_color.split(","):
                mainColorQueryParam.append(s)
        else:
            mainColorQueryParam.append(args.main_color)

    if args.cooldown == None:
        args.cooldown = 10

    if not args.max_price:
        args.max_price = float(1)
    if not args.min_price:
        args.min_price = float(0)

    searchParameters = kittyapi.SearchQuery(gen, maxPrice=args.max_price, minPrice=args.min_price, virginOnly=args.virgin, goodiesOnly=args.goodies_only, sire=args.sire, cattributes=cattributesQueryParam, mainColor=mainColorQueryParam, cooldownMaxIndex=args.cooldown)
    scan = kittyapi.Scanner(searchParameters, manager=manager)
    try:
        if args.forever:
            try:
                scan.scanForever()
            except:
                pass
        else:
            scan.scan()
    except KeyboardInterrupt:
        sys.exit()
