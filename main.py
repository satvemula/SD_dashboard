import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration (MUST BE FIRST)
st.set_page_config(page_title="Corn S&D Sensitivity Dashboard", layout="wide")

# 2. Professional CSS Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌽 US Corn Supply & Demand Sensitivity Model")
st.markdown("### *Physical Merchant Perspective: WASDE-668 Baseline*")

# --- BASE DATA (WASDE-668) ---
Base_Planted_Acres = 94.6
Base_Harvested_Acres = 86.5
Base_Yield = 177.3
Beginning_Stocks = 1360.0 
Imports = 25.0
Base_Feed = 5650.0
Base_Ethanol = 5450.0
Base_Exports = 2100.0
Base_Seed_Ind = 1385.0

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Scenario Controls")
yield_shock = st.sidebar.slider("Yield Shock (%)", -20.0, 5.0, 0.0, step=0.5)
export_adj = st.sidebar.slider("Export Demand Shift (mbu)", -500, 500, 0, step=50)
ethanol_adj = st.sidebar.slider("Ethanol Demand Shift (mbu)", -200, 200, 0, step=10)

st.sidebar.markdown("---")
st.sidebar.info("Pro Tip: A 10% yield shock simulates a moderate multi-state drought.")

# --- CALCULATIONS ---
current_yield = Base_Yield * (1 + yield_shock / 100)
production = current_yield * Base_Harvested_Acres
total_supply = Beginning_Stocks + production + Imports
total_demand = Base_Feed + Base_Ethanol + Base_Exports + Base_Seed_Ind + export_adj + ethanol_adj
ending_stocks = total_supply - total_demand

# Stock to Use Ratio
stu_ratio = (ending_stocks / total_demand) * 100 if total_demand > 0 else 0

# Price Prediction Model (Logarithmic Estimate)
est_price = 1.25 + (45.0 / stu_ratio) if stu_ratio > 2 else 7.50

# Market Status Logic
if stu_ratio < 10:
    color, status = "inverse", "Critical/Scarce"
elif stu_ratio < 13:
    color, status = "off", "Balanced"
else:
    color, status = "normal", "Burdened/Heavy"

# --- DASHBOARD METRICS ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1: st.metric("Final Yield", f"{current_yield:.1f} BPA", f"{yield_shock:+.1f}%")
with col2: st.metric("Ending Stocks", f"{int(ending_stocks)} mbu")
with col3: st.metric("S/U Ratio (%)", f"{stu_ratio:.2f}%", delta_color=color)
with col4: st.metric("Est. Farm Price", f"${est_price:.2f}/bu")
with col5:
    st.write(f"**Market Status**")
    st.subheader(status)

st.divider()

# --- WATERFALL CHART ---
fig = go.Figure(go.Waterfall(
    name = "Flow", orientation = "v",
    measure = ["relative", "relative", "relative", "total", "relative", "total"],
    x = ["Beg. Stocks", "Production", "Imports", "Total Supply", "Total Demand", "Ending Stocks"],
    textposition = "outside",
    y = [Beginning_Stocks, production, Imports, 0, -total_demand, 0],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
    decreasing = {"marker":{"color":"#EF553B"}},
    increasing = {"marker":{"color":"#00CC96"}},
    totals = {"marker":{"color":"#1f497d"}}
))
fig.update_layout(title="Supply/Demand Flow (Million Bushels)", height=500)
st.plotly_chart(fig, use_container_width=True)

# --- BALANCE SHEET TABLE ---
st.subheader("📋 Balance Sheet Details")
df_data = {
    "Category": ["Beginning Stocks", "Production", "Imports", "Total Supply", "Total Demand", "Ending Stocks"],
    "Volume (mbu)": [Beginning_Stocks, int(production), Imports, int(total_supply), int(total_demand), int(ending_stocks)]
}
st.table(pd.DataFrame(df_data))

# --- HISTORICAL BENCHMARKS ---
st.divider()
st.subheader("📜 Historical Benchmarks for Context")
st.markdown("Compare your current scenario to these historical 'Regimes'.")

historical_data = {
    "Market Year": ["2012/13 (Drought)", "2020/21 (Pandemic)", "2024/25 (Estimate)", "Current Scenario"],
    "S/U Ratio (%)": ["7.4%", "12.3%", "13.2%", f"{stu_ratio:.1f}%"],
    "Avg. Farm Price": ["$6.89/bu", "$4.53/bu", "$4.10/bu", f"${est_price:.2f}/bu"],
    "Market Regime": ["Extreme Scarcity", "Supply Chain Shock", "Abundant / Heavy", status]
}
st.dataframe(pd.DataFrame(historical_data), use_container_width=True)
st.info("**Analyst Note:** The 2012 drought is the 'Gold Standard' for scarcity. If your slider pushes the S/U ratio below 8%, expect extreme price volatility.")
