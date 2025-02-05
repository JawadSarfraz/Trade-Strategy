def detect_order_imbalance(exchange):
    """Checks if buy-side or sell-side is significantly stronger."""
    total_bid_volume = sum([bid[1] for bid in order_books[exchange]["bids"]])
    total_ask_volume = sum([ask[1] for ask in order_books[exchange]["asks"]])

    imbalance_ratio = total_bid_volume / (total_ask_volume + 1e-9)  # Avoid division by zero

    print(f"\n📊 [ANALYSIS] {exchange.upper()} Order Book Imbalance Ratio: {imbalance_ratio:.2f}")

    if imbalance_ratio > 2.0:
        print("🚀 Bullish Signal: Buy-side is MUCH stronger!")
    elif imbalance_ratio < 0.5:
        print("⚠️ Bearish Signal: Sell-side is much stronger.")
