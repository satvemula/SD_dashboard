Interactive Decision Support Tool for Commodity Merchants

Executive Summary
This project is an interactive Supply & Demand (S&D) Sensitivity Model designed for physical grain merchants and analysts. It allows users to simulate "what-if" scenarios regarding US Corn production shocks and demand shifts, providing real-time impacts on the Ending Stocks-to-Use (S/U) Ratio and estimated farm gate prices.

The model uses the WASDE-668 (February 2026) report as its "Ground Truth" baseline, enabling users to visualize how a multi-state drought or an export surge would shift the US balance sheet from a "Heavy" market into a "Scarcity" regime.

Key Features
Dynamic Yield Shocks: Adjust crop yields (BPA) via a slider to simulate weather events and drought severity.

Demand Sensitivity: Toggle shifts in Ethanol and Export demand to see how global consumption impacts domestic carryout.

Price Prediction Model: Utilizes a logarithmic regression formula (

Price=1.25+ 
S/U Ratio
45.0
​	
 
) to estimate the Average Farm Price based on calculated scarcity.

Visual S&D Waterfall: A Plotly-powered waterfall chart that visualizes the flow of grain from Beginning Stocks and Production through to Ending Stocks.

Historical Benchmarking: Compares the current simulated scenario against the 2012 Drought and the 2020 Pandemic regimes for market context.

Technical Stack
Language: Python 3.12

Framework: Streamlit (Web Interface)

Data Handling: Pandas

Visualization: Plotly Graph Objects (Interactive Waterfall Charts)

Deployment: Designed for local hosting or Google Colab tunneling via LocalTunnel.

How to Run
Clone the repository:

Bash
git clone https://github.com/your-username/corn-sd-dashboard.git
Install dependencies:

Bash
pip install streamlit pandas plotly
Launch the Dashboard:

Bash
streamlit run SDdashboard.py

Project Impact

This tool bypasses the static nature of traditional PDF reports, allowing a merchant to quantify risk instantly. For example, it demonstrates that a 7.5% yield drag is the "tipping point" that pushes the US S/U ratio below 10%, historically a catalyst for aggressive basis appreciation at the elevator level.
