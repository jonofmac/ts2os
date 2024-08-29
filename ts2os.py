# Name: ts2os.py
# Version: 1.1 - 2024/08/29
# Description: Run with python ./ts2os.py, when the prompt comes up, copy and paste the lines from the trade steward bot log for the fill.
# E.g. 	Leg 1: Sell to Open -1x SPXW 08/29/24 5545P @ $4.25 (4.20/4.30); 12.8 Delta
#       Leg 2: Buy to Open 1x SPXW 08/30/24 5545P @ $7.12 (7.00/7.10); 16.7 Delta
#       Leg 3: Sell to Open -1x SPXW 08/29/24 5685C @ $4.55 (4.50/4.60); 14.5 Delta
#       Leg 4: Buy to Open 1x SPXW 08/30/24 5685C @ $8.08 (8.00/8.20); 19.6 Delta
#
# Once input is done, press enter on an empty line. There's no error checking. Quick and dirty...
# 
# Changelog:
# V 1.1 - 2024/08/29
#   - Added number of legs per option
#
# V 1.0 - 2024/08/05
#   - Initial release
import re
import math

class Option:
    def __init__ (self, stringInput):
        self.expiration = None
        self.strike = None
        self.type = None
        self.quantity = 0
        self.ticker = None
        self.premium = None
        self.gcd = 1
        self.processString(stringInput)
        
    def processString(self, stringInput):
        # Parse a string from TradeSteward's bot log
        reResult = re.search(r'\w+: (Sell|Buy) to Open ([-]*\d+)x (\w+) (\d+[/]\d+[/]\d+) (\d+)(C|P) [@] [$](\d+[.]?\d+)', stringInput)
        
        # Quantity
        self.quantity = int(reResult[2])
        print ("Quantity is: ",reResult[2], " Processed:", self.quantity)

        # Ticker
        self.ticker = reResult[3]

        # Date
        dateArray = re.search(r'(\d+)[/](\d+)[/](\d+)', reResult[4])
        dateString = dateArray[3]+dateArray[1]+dateArray[2]
        self.expiration = dateString
        
        # Strike
        self.strike = reResult[5]

        # Type
        self.type = reResult[6]

        # Premium
        self.premium = reResult[7]

    def getQuantity(self):
        return self.quantity

    def setQuantityDivisor(self, gcd):
        self.gcd = gcd

    def getOSString(self):
        stringOut = ""
        if (self.quantity < 0):
            stringOut = "-"
        stringOut = stringOut+"."+self.ticker+self.expiration+self.type+self.strike+"x"+str(int(abs(self.quantity)/self.gcd))+"@"+self.premium
        return stringOut


if __name__ == "__main__":
    print ("Paste the order information string (Press enter on empty line to end input): ")
    options = []
    while True:
        inString = input()
        if inString == "":
            break
        options.append(Option(inString))


    print("There are",str(len(options)), "option legs: ")
    # Not the most elegant way to do this... but I need the main ticker... tickers ending in W or Q need to be cleaned
    baseTicker = re.search(r'(?:(\w{3,})[WQ]|(\w+))', options[0].ticker)

    baseURL = "https://optionstrat.com/build/custom/" + baseTicker[baseTicker.lastindex] + "/"
    fullURL = baseURL
    optCount = 0
    gcdList = []
    for opt in options:
        gcdList.append(abs(opt.getQuantity()))
        
    gcd = math.gcd(*gcdList)

    for opt in options:
        if optCount > 0:
            fullURL = fullURL + ","
        opt.setQuantityDivisor(gcd)
        fullURL = fullURL + opt.getOSString()
        optCount = optCount + 1

    print (fullURL)
