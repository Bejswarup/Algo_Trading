# Algo Trading without API Key with Zerodha Kite

**Important: This guide is intended for Zerodha Kite users only. This is for trailing stop loss in naked directional trade.**

## Introduction

Algo Trading with Zerodha Kite is a Python-based algorithmic trading system that helps traders make informed decisions while trading options on the NSE (National Stock Exchange) platform. This system aims to eliminate emotional trading and provide a structured approach to option trading.

## Repository Contents

This GitHub repository, named "Algo_Trading," contains the following Python files:

1. **Intraday_Option_trading.py**: This file likely contains the core logic for intraday option trading.

2. **kite_trade.py**: This file is responsible for interacting with the Zerodha Kite API to execute trades.

3. **TESTing.py**: This file acts as the main interface for users to input their trading parameters and execute option trades.

## How to Use

To use this algorithmic trading system, follow these steps:

1. **Clone the Repository**: Clone the GitHub repository "Algo_Trading" to your local machine.

2. **Set Up API Credentials**: You do not need to provide the Zerodha Kite API Key; provide only the `enctoken`. Here's how to obtain it:

    - Log in to your Zerodha Kite account.
    
    - Right-click anywhere on the page and select "Inspect" to open the browser's developer tools.

    - Go to the "Network" tab.

    - Press `Ctrl+R` to reload the page.

    - Click on the "position" request in the network traffic list.

    - In the "Headers" section, locate the "Authorization" header. The `enctoken` will be found here.

3. **Run TESTING.py**: After placing all three Python files in the same directory and providing the `enctoken`, run the `TESTing.py` file.

4. **Follow the Prompts**: The script will prompt you to make several choices:

    - Choose the instrument (NSE:NIFTY FIN SERVICE, NSE:NIFTY BANK, NSE:NIFTY 50, NSE:NIFTY MID SELECT) by selecting 0, 1, 2, or 3.

    - Choose Call (CE) or Put (PE) options by entering 0 or 1.

    - Select At The Money (ATM), In The Money (ITM), or Out of The Money (OTM) options in the same way.

    - Decide whether you want to Buy or Sell the selected option.

    - Set a Stop Loss (sl) and a Target. If you select 0 as the target, the system will trail the stop loss.

    - If you put a target other than 0, the system will trail the stop loss as explained in the description.
    - If you want to do virtual trade coose 0 otherwise choose 1.

5. **Execute the Trade**: The system will execute the chosen option trade based on your inputs and continuously manage the trade according to your specified stop loss and target parameters.

6. **Let's walk through an example of how trailing stop loss works in your Algo Trading system using the parameters you provided**:

Suppose you decide to Sell a NIFTY23SEP19700CE option for 50 rupees. You set a Stop Loss (sl) of 5 rupees and a Target of 0 (indicating you want to trail the stop loss).

Here's how the trailing stop loss would work:

1. Initial Setup:
   - You sell the NIFTY23SEP19700CE option for 50 rupees.
   - Your initial stop loss is set at 5 rupees.
   - Your initial target is set to 0 (indicating trailing stop loss).

2. Price Movements:
   - If the Last Traded Price (LTP) increases to 55 rupees, your exit price remains at 55 rupees, and you book a loss (since your stop loss is 5 rupees below the entry price).

   - If the LTP decreases to 45 rupees, your exit price is adjusted to 50 rupees (the original entry price), and you still book a loss.

   - If the LTP decreases further to 40 rupees, your exit price is adjusted to 45 rupees. At this point, if the price increases to 45 rupees, you break even (exit at the entry price).

   - If the LTP decreases to 35 rupees, your exit price is adjusted to 40 rupees, and so on. The stop loss is constantly adjusted as the LTP moves in your favor.

3. Trailing Stop Loss Activation:
   - As long as the LTP keeps decreasing and your exit price is adjusted downwards, the trailing stop loss remains in effect.

4. Profit Booking:
   - If the LTP increases and hits your exit price, you exit the trade. For example, if the LTP reaches 55 rupees, you book a loss of 5 rupees.

The key idea is that the trailing stop loss adapts to market conditions. It moves in your favor as the price increases but remains static when the price decreases, allowing you to potentially capture more profit while protecting yourself from significant losses.

Remember that trailing stop loss can be a useful strategy, but it doesn't guarantee profits, and it's essential to carefully consider your risk tolerance and overall trading plan.

## Why Algo Trading?

The Algo Trading system is designed to help traders avoid impulsive decisions driven by emotions like greed and fear. By following a structured approach, it aims to improve trading discipline and potentially enhance trading results.

## Feedback and Contact

If you find this repository helpful, please consider giving it a star. If you have questions or want to discuss coding your own trading strategy, feel free to contact the author at the following:

- Phone: 7602056463
- Email: bejswarup90@gmail.com

Happy trading with Algo Trading and may your investments be successful!
