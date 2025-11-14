# Stock-Market-Simulator
Different simulations of the stock market with a basic order book and random limit orders and aggressive orders coming in. 

This simulator sets a starting market price and at each 'tick' or timestep, a random bidder or seller comes and places a bid or ask. Lets call the current market price $p_{market}$. The bidder or seller will come in and randomly place their bid/ask at $p_{market} \pm x$ where $x \in [0, .01*p_{market}]$. 

## Observed Patterns

Low points and high points in the market price were capped by the highest bid price and the lowest ask price. 

## Future Work

Currently looking into Brownian Motion.

## Use

download repo and run
`python market_sim.py`




