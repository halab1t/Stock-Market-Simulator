import random
import time
import matplotlib.pyplot as plt

# Enable interactive mode for live plotting
plt.ion()

# Create figure and axis
fig = plt.figure()
ax = fig.add_subplot(111)

# Initial data
prices = []
line, = ax.plot([], [], 'b-')  # Blue line for price

def update_plot(new_price):
    prices.append(new_price)
    line.set_xdata(range(len(prices)))
    line.set_ydata(prices)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()

# Initial market price
current_price = 100.0
update_plot(current_price)

# Fixed spread for market maker (simulates liquidity)
spread = 0.5  # 0.5% spread

# Initial bid and ask
current_bid = current_price * (1 - spread / 200)  # Divide by 200 for percentage/2
current_ask = current_price * (1 + spread / 200)

while True:
    # Randomly decide if incoming order is a buy (bid) or sell (ask)
    is_buy = random.choice([True, False])

    # Randomly decide if it's flexible (market order) or fixed (limit order)
    is_flexible = random.choice([True, False])

    trade_occurred = False
    trade_price = None

    if is_flexible:
        # Flexible: Market order, hits the current best opposite side
        if is_buy:
            trade_price = current_ask
        else:
            trade_price = current_bid
        trade_occurred = True
    else:
        # Fixed: Limit order within 1% of current market price
        deviation = random.uniform(-0.01, 0.01)
        order_price = current_price * (1 + deviation)

        # Check if it crosses the book (hits the opposite side)
        if is_buy and order_price >= current_ask:
            trade_price = current_ask
            trade_occurred = True
        elif not is_buy and order_price <= current_bid:
            trade_price = current_bid
            trade_occurred = True
        else:
            # Doesn't cross, add to the book and improve bid/ask if better
            if is_buy:
                if order_price > current_bid:
                    current_bid = order_price
            else:
                if order_price < current_ask:
                    current_ask = order_price

    if trade_occurred:
        # Update market price to the trade price
        current_price = trade_price

        # Reset bid/ask around new price (simulates market maker replenishing liquidity)
        current_bid = current_price * (1 - spread / 200)
        current_ask = current_price * (1 + spread / 200)

        # Update the plot
        update_plot(current_price)

    # Delay to simulate time between orders (adjust as needed)
    time.sleep(0.1)
