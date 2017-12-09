# Pyrrr
For now, it works just like a scanner that works just like the marketplace filter, wraped in python.

The idea for the future is to extend and modularize, allowing you to write purchase scripts. For example: keep looking for a gold beard topaz with a price below 0.05. If found, send it to the automatic purchase module.

Contributions in that regard are totally welcome, please fork me.
For now, t

# Usage

      usage: pyrrrscanner.py [-h] [-gen GEN] [-p MAX_PRICE] [-mp MIN_PRICE] [-v]                               
                             [-go] [-s] [-c CATTRIBUTES] [-color MAIN_COLOR]                                   
                             [-k KITTY]                   

      prrrruuscanner - cryptokitties.co (CK) scanner, build with pruu love by nelown                           

      optional arguments:                                 
        -h, --help            show this help message and exit                                                  
        -gen GEN, --gen GEN   Cryptokittie generation(s) to search for. Ex: -gen 1,                            
                              -gen 1,3,5                  
        -p MAX_PRICE, --max_price MAX_PRICE               
                              Top price filter, set the maximum price here                                     
        -mp MIN_PRICE, --min_price MIN_PRICE              
                              The minium price filter.    
        -v, --virgin          True if you are looking for virgins kitties, falsle                              
                              otherwise                   
        -go, --goodies_only   Check for the best cattributes only                                              
        -s, --sire            Search for siring auctions instead of selling.                                   
        -c CATTRIBUTES, --cattributes CATTRIBUTES         
                              Search for informed cattributes only. Same format as                             
                              -gen                        
        -color MAIN_COLOR, --main_color MAIN_COLOR        
                              Search for informed main color only. Same format as                              
                              -gen                        
        -k KITTY, --kitty KITTY                           
                              Retrieve all kitty info

# Example

Searching for a gen3 cymric beard:

        python pyrrrscanner.py -gen 3 -c cymric,beard
        prrrruuscanner - cryptokitties.co (CK) scanner, build with pru by nelown                                 
        Feel free to donate some kitties :) 0xccAb13D1e0430b11213a385223423eb4Fe18A129

        [*] Scanner init                                    
        [*] QuerySearch Config: "
                |_ gen: 3
                |_ maxPrice: 1.0
                |_ minPrice: 0.0
                |_ virgin: False
                |_ goodies: False
                |_ sire: False
                |_ cattributes: ['cymric', 'beard']
                |_ mainColor: [],
                |_ cooldownMaxIndex: 10
        [*] Scanner starting
        (...)
        [Kitty 145590]
        |_ name: None
        |_ gen: 3
        |_ virgin: True
        |_ color: mintgreen
        |_ born: 2017-12-08T06:33:36.000Z
        |_ catributes: ['orangesoda', 'chocolate', 'thicccbrowz', 'beard', 'mintgreen', 'totesbasic', 'emeraldgreen', 'cymric']
        |_ is ready: True
        |_ cooldown index: 1
        |_ cooldown: 1442287584405
        |_ price: 0.113717
        (...)
        [SCANNER] Shutting down.                            
        [SCANNER] Found 7 kitties that match parameters.    
        [SCANNER] median price for this search: 0.406399    
        [112096] ETH 1.000000 - https://www.cryptokitties.co/kitty/112096                                        
        [121290] ETH 0.140000 - https://www.cryptokitties.co/kitty/121290                                        
        [101661] ETH 0.550000 - https://www.cryptokitties.co/kitty/101661                                        
        [145590] ETH 0.113717 - https://www.cryptokitties.co/kitty/145590                                        
        [159387] ETH 0.473263 - https://www.cryptokitties.co/kitty/159387                                        
        [98716] ETH 0.126127 - https://www.cryptokitties.co/kitty/98716                                          
        [148349] ETH 0.441688 - https://www.cryptokitties.co/kitty/148349     

Search for any kitty that has color gold, beard and chocolate as cattributes and costs less than 0.05 eth:

        python g.py -s -p 0.05 -color gold -c beard,chocolate
        [*] Scanner init
        [*] QuerySearch Config: "
                |_ gen:
                |_ maxPrice: 10.0
                |_ minPrice: 0.0
                |_ virgin: False
                |_ goodies: False
                |_ sire: True
        [*] Scanner starting
        [*] Scan offset configs
                |_ offset: 0
                |_ limit: 50
        [CryptokittieAPI] - Getting auctions: https://api.cryptokitties.co/auctions?offset=0&limit=50&type=sire&status=open&sorting=young&orderBy=current_price&orderDirection=asc&search=+beard+chocolate+gold
        [SCANNER] Got a total of 1 auctions.
        [CryptokittieAPI] Getting kitty 128521: https://api.cryptokitties.co/kitties/128521
        [SELECTOR 128521] Scanning for desired cattributes.
        [SELECTOR 128521] Found chocolate.
        [SELECTOR 128521] Found beard.
        [SELECTOR 128521] Found gold as main color
        [*] Total found so far: 1

        [Kitty 128521]
        |_ name: Gold Mauveover
        |_ gen: 4
        |_ virgin: False
        |_ color: gold
        |_ born: 2017-12-07T13:07:05.000Z
        |_ catributes: ['luckystripe', 'granitegrey', 'chocolate', 'munchkin', 'thicccbrowz', 'beard', 'mauveover', 'gold']
        |_ price: 0.085000

Search for any gen 2 or 3 virgin kitty, costing less than 0.05 eth:

        python pyrrrscanner.py -gen 2 -v -p 0.005

You can also search for siring gold gen2 costing les .005:

        python pyrrrscanner.py -gen 2 -p 0.005 -s -c gold
