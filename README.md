

# 📈 Two-Asset Investment Tracker

A terminal-based Python tool that analyzes two stock tickers over a user-defined time range. It calculates and visualizes volatility, returns, profit simulations, and correlation — ideal for learning quantitative finance, Python, and basic data science.

---

## 🧠 Purpose

This script helps users:
- Compare the **volatility** and **returns** of two assets (stocks).
- Simulate profits from a chosen **entry point** to a future date.
- Analyze **daily return correlations** between the two assets.
- Visualize key metrics with **matplotlib** charts.
  
It’s meant as a learning tool for beginners or students studying **quantitative finance**, **data science**, or **Python programming**.

---

## ✅ Features

- User-defined **ticker selection** and **timeframe**.
- Automatically fetches data using **Yahoo Finance**.
- Computes:
  - Daily % returns
  - Standard deviation (volatility)
  - Upward and downward deviation
  - Total return from entry
  - Investment profit simulation
  - Correlation between assets
- Displays **clear interpretations** of correlation results.
- Plots:
  - Stock price evolution
  - Daily returns
  - Total return comparison
  - Simulated profit comparison

---

## 🛠 Requirements

Install the following Python packages if not already available:

```
pip install yfinance numpy pandas matplotlib
````

Ensure you're using **Python 3.8+** (tested with Python 3.13).

---

## 💻 How to Use

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/2-asset-investment-tracker.git
   cd 2-asset-investment-tracker
   ```

2. Run the script:

   ```
   python investment_tracker.py
   ```

3. Follow the on-screen prompts:

   * Enter two stock tickers (e.g., `AAPL, NVDA`)
   * Provide a start and end date in `YYYY-MM-DD` format
   * Choose an entry date within the range
   * Input a hypothetical investment amount

---

## 📌 Use Cases

* 📊 **Students**: Learn statistical concepts like standard deviation, correlation, and return.
* 💼 **Investors**: Backtest how two stocks performed over time.
* 🧪 **Python learners**: See real-world application of NumPy, Pandas, and Matplotlib.
* 📚 **Teachers**: Use this as a visual, interactive demo of financial principles.

---

## ⚠️ Common Issues & Fixes

| Problem                       | Fix                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| `nan` or `NaN` in correlation | Check that your date range includes enough trading days with data for both stocks. |
| Script crashes on download    | Check for ticker typos or internet connection issues.                              |
| Plot not displaying           | Make sure `matplotlib` is installed and your Python environment supports plotting. |

---

## 💡 Why I Made This

I wanted to **learn Python**, **understand finance better**, and build something hands-on. This project ties together:

* Math concepts from A-Level/Further Math
* Coding with real data
* Financial reasoning

---

## 🤝 License & Use

This tool is **free to use, modify, and learn from**. You can:

* Adapt it for other asset classes (e.g., crypto)
* Add a GUI interface
* Export data to Excel or CSV

> **Attribution appreciated but not required.** Just learn and have fun.

**Happy coding & investing! 🚀**

```
Let me know if you’d like help turning this into a Jupyter Notebook version or adding more features like Sharpe ratio, CSV export, or a GUI.
```
