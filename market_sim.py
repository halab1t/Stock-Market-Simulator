import random
import time
import matplotlib.pyplot as plt

# Enable interactive mode for live plotting
plt.ion()

# Create figure and axis
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('Time Step')
ax.set_ylabel('Price (Arbitrary Units)')

# Initial data
prices = []
line, = ax.plot([], [], 'b-', label='Market Price')  # Blue line for price
low_ask_line, = ax.plot([], [], 'g--', label='Lowest Ask')  # Green dashed line for lowest ask
high_bid_line, = ax.plot([], [], 'r--', label='Highest Bid')  # Red dashed line for highest bid


# Fixed spread for market maker (simulates liquidity)
spread = 0.5  # 0.5% spread

# Order book dictionaries to store bids and asks
# Structure: {price: [quantity, timestamp, filled_status]}
order_book_bids = {}  # Higher price = better bid
order_book_asks = {}  # Lower price = better ask

def update_plot(new_price):
    prices.append(new_price)
    line.set_xdata(range(len(prices)))
    line.set_ydata(prices)
    
    # Update bid/ask line
    if order_book_bids and order_book_asks:
        highest_bid = max(order_book_bids.keys())
        lowest_ask = min(order_book_asks.keys())
        low_ask_line.set_xdata([0, len(prices)-1])
        high_bid_line.set_xdata([0, len(prices)-1])
        low_ask_line.set_ydata([lowest_ask, lowest_ask])
        high_bid_line.set_ydata([highest_bid, highest_bid])
    elif order_book_bids:
        highest_bid = max(order_book_bids.keys())
        high_bid_line.set_xdata([0, len(prices)-1])
        high_bid_line.set_ydata([highest_bid, highest_bid])
    elif order_book_asks:
        lowest_ask = min(order_book_asks.keys())
        low_ask_line.set_xdata([0, len(prices)-1])
        low_ask_line.set_ydata([lowest_ask, lowest_ask])
    else:
        low_ask_line.set_xdata([])
        high_bid_line.set_xdata([])
        low_ask_line.set_ydata([])
        high_bid_line.set_ydata([])

    ax.relim()
    ax.autoscale_view()
    ax.legend()
    fig.canvas.draw()
    fig.canvas.flush_events()


# Initial market price
current_price = 100.0
update_plot(current_price)

# Function to add order to book
def add_to_order_book(is_buy, price, quantity=1):
    if is_buy:
        order_book_bids[price] = [quantity, time.time(), False]
    else:
        order_book_asks[price] = [quantity, time.time(), False]

# Function to match and execute trades
def match_orders():
    global current_price, current_bid, current_ask
    while order_book_bids and order_book_asks and max(order_book_bids.keys()) >= min(order_book_asks.keys()):
        best_bid = max(order_book_bids.keys())
        best_ask = min(order_book_asks.keys())
        if best_bid >= best_ask:
            trade_price = best_ask  # Trade at the ask price (seller's perspective)
            current_price = trade_price

            # Update quantities and remove filled orders
            if order_book_bids[best_bid][0] > 1:
                order_book_bids[best_bid][0] -= 1
            else:
                del order_book_bids[best_bid]

            if order_book_asks[best_ask][0] > 1:
                order_book_asks[best_ask][0] -= 1
            else:
                del order_book_asks[best_ask]

            update_plot(current_price)

            # Reset market maker bid/ask
            current_bid = current_price * (1 - spread / 200)
            current_ask = current_price * (1 + spread / 200)
            add_to_order_book(True, current_bid)
            add_to_order_book(False, current_ask)

# Initial bid and ask from market maker
current_bid = current_price * (1 - spread / 200)
current_ask = current_price * (1 + spread / 200)
add_to_order_book(True, current_bid)
add_to_order_book(False, current_ask)

while True:
    # Randomly decide if incoming order is a buy (bid) or sell (ask)
    is_buy = random.choice([True, False])

    # Randomly decide if it's flexible (market order) or fixed (limit order)
    is_flexible = random.choice([True, False])

    if is_flexible:
        # Flexible: Market order, hits the current best opposite side
        if is_buy and order_book_asks:
            best_ask = min(order_book_asks.keys())
            if order_book_asks[best_ask][0] > 1:
                order_book_asks[best_ask][0] -= 1
            else:
                del order_book_asks[best_ask]
            trade_price = best_ask
        elif not is_buy and order_book_bids:
            best_bid = max(order_book_bids.keys())
            if order_book_bids[best_bid][0] > 1:
                order_book_bids[best_bid][0] -= 1
            else:
                del order_book_bids[best_bid]
            trade_price = best_bid
        else:
            continue  # No opposite orders to match
    else:
        # Fixed: Limit order within 1% of current market price
        deviation = random.uniform(-0.01, 0.01)
        order_price = current_price * (1 + deviation)
        add_to_order_book(is_buy, order_price)
        match_orders()
        continue  # Match_orders handles trade and price update

    if 'trade_price' in locals():
        current_price = trade_price
        update_plot(current_price)

    # Delay to simulate time between orders
    time.sleep(0.1)
