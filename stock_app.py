import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Analyzer", layout="wide")

st.title("📈 Stock & Gold Analyzer")
st.markdown("---")

# SET50 Stock List
SET50_STOCKS = {
    "BDMS": "BDMS.BK",      # Bangkok Dusit Medical Services
    "AOT": "AOT.BK",        # Airports of Thailand
    "PTT": "PTT.BK",        # PTT
    "PTTEP": "PTTEP.BK",    # PTT Exploration and Production
    "SCB": "SCB.BK",        # Siam Commercial Bank
    "KBANK": "KBANK.BK",    # Kasikorn Bank
    "BBL": "BBL.BK",        # Bank of Ayudhya
    "KTB": "KTB.BK",        # Krung Thai Bank
    "SCC": "SCC.BK",        # Siam Cement
    "TOP": "TOP.BK",        # Thai Oil
    "IRPC": "IRPC.BK",      # IRPC
    "CPF": "CPF.BK",       # Charoen Pokphand Foods
    "CPALL": "CPALL.BK",   # CP All
    "TRUE": "TRUE.BK",      # True Corporation
    "ADVANC": "ADVANC.BK",  # Advanced Info Service
    "DTAC": "DTAC.BK",      # DTAC
    "SPRC": "SPRC.BK",      # Thai Oil
    "ESSO": "ESSO.BK",      # ESSO Thailand
    "BCP": "BCP.BK",        # Bangchak Corporation
    "BGRIM": "BGRIM.BK",    # Banpu
    "GULF": "GULF.BK",      # Gulf Energy Development
    "MINT": "MINT.BK",      # Minor International
    "BH": "BH.BK",          # Bangkok Hospital
    "AEONTS": "AEONTS.BK",  # AEON Thana Sinsap
    "BJC": "BJC.BK",        # Berli Jucker
    "CRC": "CRC.BK",        # Central Retail
    "COM7": "COM7.BK",      # COM7
    "CPN": "CPN.BK",        # Central Pattana
    "DELTA": "DELTA.BK",     # Delta Electronics
    "EGCO": "EGCO.BK",       # Electricity Generating
    "GPSC": "GPSC.BK",       # Global Power Synergy
    "HANA": "HANA.BK",       # Hana Microelectronics
    "HMPRO": "HMPRO.BK",    # Home Product Center
    "INTUCH": "INTUCH.BK",  # Intouch Holdings
    "ITC": "ITC.BK",         # Indorama Ventures
    "KCE": "KCE.BK",        # KCE Electronics
    "MEGA": "MEGA.BK",       # Mega Lifesciences
    "MTC": "MTC.BK",        # Muang Thai Insurance
    "PLANB": "PLANB.BK",    # Plan B Media
    "PTG": "PTG.BK",        # PTG Energy
    "PTL": "PTL.BK",        # Polyplex
    "RATCH": "RATCH.BK",     # Ratchaburi Power
    "SAWAD": "SAWAD.BK",    # Srithai Superware
    "SINGER": "SINGER.BK",   # Singer Thailand
    "SPALI": "SPALI.BK",    # Supalai
    "STEC": "STEC.BK",       # Sino-Thai Engineering
    "TISCO": "TISCO.BK",    # TISCO Financial
    "TMB": "TMB.BK",        # TMB Bank
    "TTB": "TTB.BK",        # TTB Bank
    "WHA": "WHA.BK",        # WHA Corporation
}

# Sidebar - Select Asset
st.sidebar.header("ตั้งค่า")
asset_type = st.sidebar.selectbox("เลือกประเภท", ["หุ้นไทย (SET)", "ทองคำ (Gold)", "SET50 แนวโน้ม 6 เดือน"])

if asset_type == "SET50 แนวโน้ม 6 เดือน":
    st.header("📊 SET50 แนวโน้ม 6 เดือน")
    
    @st.cache_data
    def get_set50_performance():
        results = []
        progress_bar = st.progress(0)
        
        for i, (name, symbol) in enumerate(SET50_STOCKS.items()):
            try:
                data = yf.download(symbol, period="6mo", progress=False)
                if not data.empty:
                    start_price = float(data['Close'].iloc[0])
                    end_price = float(data['Close'].iloc[-1])
                    change_pct = ((end_price - start_price) / start_price) * 100
                    results.append({
                        "ชื่อหุ้น": name,
                        "สัญลักษณ์": symbol.replace(".BK", ""),
                        "ราคาเริ่ม": round(start_price, 2),
                        "ราคาปัจจุบัน": round(end_price, 2),
                        "% เปลี่ยนแปลง": round(change_pct, 2)
                    })
            except:
                pass
            progress_bar.progress((i + 1) / len(SET50_STOCKS))
        
        return pd.DataFrame(results)
    
    if st.button("📥 โหลดข้อมูล SET50"):
        with st.spinner("กำลังโหลดข้อมูล..."):
            df = get_set50_performance()
            if not df.empty:
                # Sort by % change
                df = df.sort_values("% เปลี่ยนแปลง", ascending=False)
                
                # Add emoji based on performance
                def get_emoji(x):
                    if x > 5:
                        return "🟢🟢"
                    elif x > 0:
                        return "🟢"
                    elif x > -5:
                        return "🔴"
                    else:
                        return "🔴🔴"
                
                df["แนวโน้ม"] = df["% เปลี่ยนแปลง"].apply(get_emoji)
                
                st.dataframe(df, use_container_width=True)
                
                st.markdown("---")
                st.write("**🟢🟢 = ขึ้นมาก | 🟢 = ขึ้น | 🔴 = ลงเล็กน้อย | 🔴🔴 = ลงมาก**")
        st.stop()

if asset_type == "หุ้นไทย (SET)":
    # Dropdown to select SET50 stock
    selected_name = st.sidebar.selectbox("เลือกหุ้น SET50", list(SET50_STOCKS.keys()), index=0)
    symbol = st.sidebar.text_input("หรือพิมพ์สัญลักษณ์เอง", SET50_STOCKS[selected_name])
    data = yf.download(symbol, period="2y")
else:
    symbol = "GC=F"  # Gold futures
    data = yf.download(symbol, period="2y")

# Flatten columns if multi-index
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Calculate statistics
if not data.empty:
    # Current price (extract scalar value)
    current_price = float(data['Close'].iloc[-1])
    prev_price = float(data['Close'].iloc[-2])
    change_pct = ((current_price - prev_price) / prev_price) * 100
    
    # Moving Averages
    ma7 = data['Close'].rolling(window=7).mean()
    ma30 = data['Close'].rolling(window=30).mean()
    ma90 = data['Close'].rolling(window=90).mean()
    
    # Statistics
    avg_7 = float(data['Close'].tail(7).mean())
    avg_30 = float(data['Close'].tail(30).mean())
    avg_90 = float(data['Close'].tail(90).mean())
    
    highest_90 = float(data['Close'].tail(90).max())
    lowest_90 = float(data['Close'].tail(90).min())
    
    # Volatility (standard deviation)
    volatility_30 = float(data['Close'].tail(30).std())
    volatility_90 = float(data['Close'].tail(90).std())
    
    # Daily returns
    daily_returns = data['Close'].pct_change() * 100
    
    # Display Current Price
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ราคาปัจจุบัน", f"{current_price:.2f}", f"{change_pct:+.2f}%")
    with col2:
        st.metric("สูงสุด 90 วัน", f"{highest_90:.2f}")
    with col3:
        st.metric("ต่ำสุด 90 วัน", f"{lowest_90:.2f}")
    
    st.markdown("---")
    
    # Moving Averages & Chart
    st.subheader("📊 กราฟราคา + เส้นแนวโน้ม (Moving Average)")
    
    # Create chart with price and MA lines
    fig = go.Figure()
    
    # Main price line
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['Close'], 
        name="ราคาปิด", 
        line=dict(color='blue', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 0, 255, 0.1)'
    ))
    
    # Moving Average lines
    fig.add_trace(go.Scatter(x=data.index, y=ma7, name="MA 7 วัน", line=dict(color='green', width=1.5)))
    fig.add_trace(go.Scatter(x=data.index, y=ma30, name="MA 30 วัน", line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=data.index, y=ma90, name="MA 90 วัน", line=dict(color='red', width=2)))
    
    fig.update_layout(
        title=f"กราฟ {symbol} - 2 ปี (MA 7/30/90 วัน)",
        xaxis_title="วันที่",
        yaxis_title="ราคา (บาท)",
        height=500,
        hovermode="x unified",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Statistics Table
    st.subheader("📋 สถิติ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**ราคาเฉลี่ย (Average)**")
        st.write(f"- 7 วัน: {avg_7:.2f}")
        st.write(f"- 30 วัน: {avg_30:.2f}")
        st.write(f"- 90 วัน: {avg_90:.2f}")
        
        st.write("**")
        st.write("**ความผันผวน (Volatility)**")
        st.write(f"- 30 วัน: {volatility_30:.4f}")
        st.write(f"- 90 วัน: {volatility_90:.4f}")
    
    with col2:
        st.write("**% ขึ้น/ลง รายวัน (ย้อนหลัง 10 วัน)**")
        last_10 = daily_returns.tail(10).dropna()
        for i in range(len(last_10)):
            idx = len(last_10) - 1 - i
            date = last_10.index[idx]
            ret = float(last_10.iloc[idx])
            emoji = "🟢" if ret > 0 else "🔴"
            st.write(f"{emoji} {date.strftime('%Y-%m-%d')}: {ret:+.2f}%")
    
    st.markdown("---")
    
    # Correlation info
    st.subheader("🔗 Correlation")
    st.info("📌 Correlation กับทองคำ: ต้องเลือกหุ้นและทองพร้อมกันเพื่อคำนวณ")
    
else:
    st.error("ไม่พบข้อมูล ลองเปลี่ยนสัญลักษณ์หุ้น")

st.markdown("---")
st.caption("📌 หมายเหตุ: ข้อมูลจาก Yahoo Finance อาจมีความล่าช้า")
