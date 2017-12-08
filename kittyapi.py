#!bin/python
import requests

class CryptokittieAPI:
    def __init__(self):
        self.API_URL = "https://api.cryptokitties.co"
        self.API_KITTY = self.API_URL+"/kitties/"
        self.API_AUCTIONS = self.API_URL + "/auctions?offset=OFF_SET&limit=LIMIT&type=sale&status=open&sorting=young&orderBy=current_price&orderDirection=asc&search=SEARCH"
        self.API_OFFSET = 50

    def getKitty(self, kittyId):
        requestUrl = self.API_KITTY+str(kittyId)
        print "[CryptokittieAPI] Getting kitty %s: %s" % (kittyId, requestUrl)

        return requests.get(requestUrl).json()

    def getAudictionList(self, offset, limit, searchString, sire=False):
        requestUrl = self.API_AUCTIONS.replace("OFF_SET", str(offset)).replace("LIMIT", str(limit)).replace("SEARCH", str(searchString))
        if sire:
            requestUrl = requestUrl.replace("type=sale", "type=sire")

        print "[CryptokittieAPI] - Getting auctions: %s" % requestUrl

        return requests.get(requestUrl).json();

class CKUtils:
    def __init__(self):
        self.api = CryptokittieAPI()

    def getKittyCattributes(self,kitty):
        originalCattributes = kitty['cattributes']
        easyCattributes = []
        for attr in originalCattributes:
            easyCattributes.append(str(attr['description']))
        return easyCattributes



class Scanner:
    def __init__(self, searchQuery, manager=None):
        self.api = CryptokittieAPI()
        self.offset = 0
        self.limit = 50
        self.searchQuery = searchQuery
        self.manager = manager
        self.foundIds = []

        # change to debug
        print "[*] Scanner init"
        print str(self.searchQuery)


    def nextPage(self):
        payload = self.api.getAudictionList(self.offset, self.limit, self.searchQuery.searchQueryString(), self.searchQuery.sire)
        return payload

    def scanForever(self):
        while True:
            self.scan()

    def scan(self):
        print "[*] Scanner starting"
        print self
        data = self.nextPage()

        print len(data['auctions'])
        while len(data['auctions']) > 0:
            print "[SCANNER] Got a total of %d auctions." % len(data['auctions'])
            foundAuctions = 0
            for auction in data['auctions']:
                kitty = self.api.getKitty(auction['kitty']['id'])
                if self.isGold(auction, kitty):
                    if kitty['id'] not in self.foundIds:
                        self.manager.addGoldKitty(auction, kitty)
                        self.foundIds.append(auction['kitty']['id'])
                        foundAuctions += 1
            print "[SCANNER] offset result: %d/%d" % (foundAuctions,len(data['auctions']))
            self.offset += self.limit
            print "[SCANNER] offset: %d" % self.offset
            print "[SCANNER] limit: %d" % self.limit
            data = self.nextPage()
        print "[SCANNER] Shutting down."

    def __str__(self):
        msg = """[*] Scan offset configs
        |_ offset: %s
        |_ limit: %s"""

        return msg % (self.offset, self.limit)

    def isGold(self, auction, kitty):
        auctionPrice = float(auction['current_price'])/1000000000000000000

        if not (auctionPrice <= self.searchQuery.maxPrice and auctionPrice >= self.searchQuery.minPrice):
            # print '[SELECTOR %s] Price: %f, bad price range (%f,%f)' %(kitty['id'],auctionPrice, self.searchQuery.maxPrice, self.searchQuery.minPrice)
            return False

        if self.searchQuery.cattributes:
            hasCattributes = False
            print "[SELECTOR %s] Scanning for desired cattributes." % kitty['id']
            for attr in kitty['cattributes']:
                if str(attr['description']) in self.searchQuery.cattributes:
                    print "[SELECTOR %s] Found %s." % (kitty['id'], attr['description'])
                    hasCattributes = True

            if not hasCattributes:
                print "DISCARTING CATTRIBUTES"
                return False

        if self.searchQuery.mainColor:
            hasMainColor = False

            maincolor = str(kitty['color']) in self.searchQuery.mainColor
            mainColorInCattributes = str(kitty['color']) in self.searchQuery.cattributes

            if maincolor:
                print "[SELECTOR %s] Found %s as main color" % (kitty['id'],kitty['color'])
                hasMainColor = True
            if mainColorInCattributes:
                print "[SELECTOR %s] Found as main color %s in cattributes" % (kitty['id'],attr['color'])
                hasMainColor = True

            if not hasMainColor:
                print "DISCARTING COLOR"
                return False

        if self.searchQuery.virginOnly:
            try:
                child = kitty['children']
                if len(child) > 0:
                    return False
                else:
                    return True
            except KeyError:
                return  True

        if kitty['status']['cooldown_index'] > self.searchQuery.cooldownMaxIndex:
            return False
        return True

class SearchQuery:
    def __init__(self,gen, maxPrice=float(1), minPrice=float(0), virginOnly=True, goodiesOnly=False, sire=False, cattributes=[], mainColor=[], cooldownMaxIndex=10):
        self.gen = gen
        self.maxPrice = maxPrice
        self.minPrice = minPrice
        self.virginOnly = virginOnly
        self.searchForGoodies = goodiesOnly
        self.sire = sire
        self.cattributes = cattributes
        self.mainColor = mainColor
        self.cooldownMaxIndex = cooldownMaxIndex

    def searchQueryString(self):
        queryString = ""
        if self.gen:
            queryString += "gen:"
            for g in self.gen:
                queryString += str(g) + ","
            queryString = queryString[0:-1]

        if self.cattributes:
            for c in self.cattributes:
                queryString = queryString + ("+%s" % c )

        if self.mainColor:
            if len(self.mainColor)>1:
                # set the main color check for the scanner, not the querystring param
                # bcz the API accept only 1 main color
                for s in self.mainColor:
                    self.cattributes.append(s)
            else:
                queryString += ("+%s" % self.mainColor[0])
        return queryString;

    def __str__(self):
        gens = " ".join(str(i) for i in self.gen)

        config = """[*] QuerySearch Config: "
        |_ gen: %s
        |_ maxPrice: %s
        |_ minPrice: %s
        |_ virgin: %s
        |_ goodies: %s
        |_ sire: %s"""

        return config % (gens, self.maxPrice, self.minPrice, self.virginOnly, self.searchForGoodies, self.sire)
