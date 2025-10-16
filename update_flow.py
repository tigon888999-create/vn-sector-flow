import yfinance as yf
import pandas as pd
import yaml

# Đọc danh mục ngành từ file YAML
with open("sectors.yaml", "r", encoding="utf-8") as f:
    sectors = yaml.safe_load(f)

records = []
for sector, codes in sectors.items():
    total_value = 0
    for code in codes:
        try:
            data = yf.Ticker(f"{code}.VN").history(period="1d")
            if not data.empty:
                close = data['Close'].iloc[-1]
                volume = data['Volume'].iloc[-1]
                total_value += close * volume
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu {code}: {e}")
            continue
    records.append({"Ngành": sector, "GTGD (proxy)": total_value})

# Sắp xếp và in kết quả
df = pd.DataFrame(records).sort_values("GTGD (proxy)", ascending=False)
pd.set_option("display.float_format", lambda x: f"{x:,.0f}")
print("🏆 Top ngành hút tiền hôm nay (proxy):")
print(df)
