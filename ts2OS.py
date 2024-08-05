# Name: ts2OS.py
# Version: 1.0 - 2024/08/05
# Description: Run with python ./buildOS.py, when the prompt comes up, copy and paste the lines from the trade steward bot log for the fill.
# E.g. Leg 1: Sell To Open SPXW 07/18/24 5650P @ $21.13 (21.20/21.50); 49.4 Delta
#      Leg 2: Buy To Open SPXW 07/18/24 5620P @ $10.35 (10.40/10.70); 29.3 Delta
#      Leg 3: Buy To Open SPXW 07/16/24 5620P @ $2.67 (2.70/2.80); 16.9 Delta
#
# Once input is done, press enter on an empty line. There's no error checking. Quick and dirty...
import re

class Option:
    def __init__ (self, stringInput):
        self.expiration = None
        self.strike = None
        self.type = None
        self.quantity = 0
        self.ticker = None
        self.premium = None
        self.processString(stringInput)
        
    def processString(self, stringInput):
        # Parse a string from TradeSteward's bot log
        reResult = re.search(r'\w+: (Sell|Buy) To Open (\w+) (\d+[/]\d+[/]\d+) (\d+)(C|P) [@] [$](\d+[.]?\d+)', stringInput)
        if "Sell" in (reResult[1]):
            self.quantity = -1
        elif "Buy" in reResult[1]:
            self.quantity = 1

        # Ticker
        self.ticker = reResult[2]

        # Date
        dateArray = re.search(r'(\d+)[/](\d+)[/](\d+)', reResult[3])
        dateString = dateArray[3]+dateArray[1]+dateArray[2]
        self.expiration = dateString
        
        # Strike
        self.strike = reResult[4]

        # Type
        self.type = reResult[5]

        # Premium
        self.premium = reResult[6]

    def getOSString(self):
        stringOut = ""
        if (self.quantity < 0):
            stringOut = "-"
        stringOut = stringOut+"."+self.ticker+self.expiration+self.type+self.strike+"x"+str(abs(self.quantity))+"@"+self.premium
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
    for opt in options:
        if optCount > 0:
            fullURL = fullURL + ","
        fullURL = fullURL + opt.getOSString()
        optCount = optCount + 1

    print (fullURL)