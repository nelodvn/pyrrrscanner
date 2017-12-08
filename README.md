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

        python pyrrrscanner.py -s -p 10 -color gold -c beard,chocolate
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
