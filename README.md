Simple script to quickly build a link on OptionStrat from TradeSteward's bot log.

### Instructions ###
You need to find the detailed summary for fill order for a bot:
```
Leg 1: Sell To Open SPXW 07/18/24 5650P @ $21.13 (21.20/21.50); 49.4 Delta
Leg 2: Buy To Open SPXW 07/18/24 5620P @ $10.35 (10.40/10.70); 29.3 Delta
Leg 3: Buy To Open SPXW 07/16/24 5620P @ $2.67 (2.70/2.80); 16.9 Delta
```

1. Simply run the python script: `python ./ts2OS.py`
2. Go to a bot activity log on trade steward and find the line that says `The bot recorded information on the strikes filled on the opening of the trade.` and copy summary (like above)
3. Paste the details into the console. Each leg will be an individual line
4. Once done with input, press enter on an empty line
5. Script prints an option strat link with the provided details

### Known short-comings ###
* No input sanitation. Garbage in, garbage out applies
* As of August 5th, 2024, TradeSteward's bot log does not give the quantities of each leg in the summary, so you will have to manually select the number of legs if it's not 1x
