# Paper Trading Bot - เวอร์ชันง่ายที่เข้าใจง่าย
import pandas as pd
import numpy as np
from datetime import datetime
import time

class SimplePaperBot:
    def __init__(self, start_money=10000):
        """เริ่มต้นด้วยเงิน 10,000 USD"""
        self.cash = start_money  # เงินสด
        self.start_money = start_money  # เงินเริ่มต้น
        self.coins = {}  # เหรียญที่ถือ {"BTC": 0.5, "ETH": 2.0}
        self.trades = []  # ประวัติการเทรด
        self.current_prices = {}  # ราคาปัจจุบัน
        
        print(f"🎯 เริ่มต้น Paper Trading ด้วยเงิน ${start_money:,}")
        
    def create_fake_price(self, coin_name):
        """สร้างราคาปลอมให้ดูเหมือนจริง"""
        # ราคาเริ่มต้น
        base_prices = {
            "BTC": 45000,
            "ETH": 3000, 
            "BNB": 300,
            "ADA": 0.5,
            "SOL": 100
        }
        
        base = base_prices.get(coin_name, 100)
        
        # เปลี่ยนแปลงแบบสุ่ม ±5%
        change = np.random.uniform(-0.05, 0.05)
        new_price = base * (1 + change)
        
        self.current_prices[coin_name] = new_price
        return new_price
    
    def get_price(self, coin_name):
        """ดึงราคาปัจจุบัน"""
        price = self.create_fake_price(coin_name)
        print(f"📊 {coin_name} ราคาปัจจุบัน: ${price:,.2f}")
        return price
    
    def buy_coin(self, coin_name, amount_usd):
        """ซื้อเหรียญ"""
        price = self.get_price(coin_name)
        
        if amount_usd > self.cash:
            print(f"❌ เงินไม่พอ! มีเงิน ${self.cash:,.2f} ต้องการ ${amount_usd:,.2f}")
            return False
        
        coin_amount = amount_usd / price  # จำนวนเหรียญที่ได้
        
        # อัพเดทยอด
        self.cash -= amount_usd
        self.coins[coin_name] = self.coins.get(coin_name, 0) + coin_amount
        
        # บันทึกการเทรด
        trade = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "action": "BUY",
            "coin": coin_name,
            "price": price,
            "usd": amount_usd,
            "coin_amount": coin_amount
        }
        self.trades.append(trade)
        
        print(f"✅ ซื้อ {coin_amount:.6f} {coin_name} ด้วย ${amount_usd:,.2f}")
        print(f"💰 เงินคงเหลือ: ${self.cash:,.2f}")
        return True
    
    def sell_coin(self, coin_name, percentage=100):
        """ขายเหรียญ (percentage = เปอร์เซ็นต์ที่จะขาย)"""
        if coin_name not in self.coins or self.coins[coin_name] <= 0:
            print(f"❌ ไม่มี {coin_name} ให้ขาย!")
            return False
        
        price = self.get_price(coin_name)
        coin_to_sell = self.coins[coin_name] * (percentage / 100)
        usd_received = coin_to_sell * price
        
        # อัพเดทยอด
        self.cash += usd_received
        self.coins[coin_name] -= coin_to_sell
        
        # บันทึกการเทรด
        trade = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "action": "SELL",
            "coin": coin_name,
            "price": price,
            "usd": usd_received,
            "coin_amount": coin_to_sell
        }
        self.trades.append(trade)
        
        print(f"✅ ขาย {coin_to_sell:.6f} {coin_name} ได้ ${usd_received:,.2f}")
        print(f"💰 เงินคงเหลือ: ${self.cash:,.2f}")
        return True
    
    def show_portfolio(self):
        """แสดงพอร์ตการลงทุนปัจจุบัน"""
        print("\n" + "="*60)
        print("📊 PORTFOLIO ปัจจุบัน")
        print("="*60)
        print(f"💵 เงินสด: ${self.cash:,.2f}")
        
        total_coin_value = 0
        
        if self.coins:
            print("\n🪙 เหรียญที่ถือ:")
            for coin, amount in self.coins.items():
                if amount > 0:
                    price = self.current_prices.get(coin, self.create_fake_price(coin))
                    value = amount * price
                    total_coin_value += value
                    print(f"   {coin:<5}: {amount:>12.6f} × ${price:>8,.2f} = ${value:>10,.2f}")
        
        total_value = self.cash + total_coin_value
        profit = total_value - self.start_money
        profit_pct = (profit / self.start_money) * 100
        
        print(f"\n📈 มูลค่ารวม: ${total_value:,.2f}")
        print(f"📊 กำไร/ขาดทุน: ${profit:+,.2f} ({profit_pct:+.2f}%)")
        
        if profit > 0:
            print("🎉 กำไร! เก่งมาก!")
        elif profit < 0:
            print("😔 ขาดทุน แต่ไม่เป็นไร เรียนรู้ต่อไป!")
        else:
            print("😐 เท่าทุน")
    
    def show_trade_history(self):
        """แสดงประวัติการเทรด"""
        if not self.trades:
            print("📝 ยังไม่มีการเทรด")
            return
        
        print("\n📝 ประวัติการเทรด:")
        print("-" * 70)
        print(f"{'เวลา':<8} {'Action':<4} {'Coin':<5} {'ราคา':<10} {'จำนวน USD':<12}")
        print("-" * 70)
        
        for trade in self.trades[-10:]:  # แสดง 10 รายการล่าสุด
            print(f"{trade['time']:<8} {trade['action']:<4} {trade['coin']:<5} "
                  f"${trade['price']:<9,.2f} ${trade['usd']:<11,.2f}")

def simple_trading_demo():
    """ตัวอย่างการเทรดง่ายๆ"""
    print("🚀 Paper Trading Bot Demo")
    print("=" * 50)
    
    # สร้าง Bot
    bot = SimplePaperBot(10000)
    
    # จำลองการเทรด 5 รอบ
    coins = ["BTC", "ETH", "BNB"]
    
    for round_num in range(5):
        print(f"\n🔄 รอบที่ {round_num + 1}")
        print("-" * 30)
        
        # ดูราคาปัจจุบัน
        for coin in coins:
            bot.get_price(coin)
        
        # การเทรดแบบสุ่ม
        action = np.random.choice(["buy", "sell", "hold"], p=[0.4, 0.3, 0.3])
        coin = np.random.choice(coins)
        
        if action == "buy" and bot.cash > 500:
            # ซื้อด้วยเงิน 500-2000 USD
            amount = np.random.randint(500, min(2000, int(bot.cash)))
            bot.buy_coin(coin, amount)
            
        elif action == "sell" and coin in bot.coins and bot.coins[coin] > 0:
            # ขายบางส่วน 30-70%
            percentage = np.random.randint(30, 71)
            bot.sell_coin(coin, percentage)
        
        else:
            print(f"💤 HOLD - ไม่ทำอะไร")
        
        # แสดงสถานะ
        bot.show_portfolio()
        
        # รอ 2 วินาที
        print("\n⏳ รอ 2 วินาที...")
        time.sleep(2)
    
    # สรุปผลการเทรด
    print("\n🎯 สรุปผลการเทรด")
    bot.show_trade_history()
    bot.show_portfolio()
    
    print("\n🎉 Paper Trading Demo จบแล้ว!")
    print("💡 นี่เป็นการจำลอง ไม่ใช่เงินจริงนะ!")

def manual_trading():
    """โหมดเทรดด้วยตัวเอง"""
    print("🎮 Manual Trading Mode")
    print("=" * 40)
    
    bot = SimplePaperBot(10000)
    
    while True:
        print("\n📋 เลือกคำสั่ง:")
        print("1. ดูราคา")
        print("2. ซื้อเหรียญ") 
        print("3. ขายเหรียญ")
        print("4. ดูพอร์ต")
        print("5. ดูประวัติ")
        print("6. ออก")
        
        choice = input("\n👉 เลือก (1-6): ").strip()
        
        if choice == "1":
            coin = input("🪙 ชื่อเหรียญ (BTC/ETH/BNB): ").upper()
            bot.get_price(coin)
            
        elif choice == "2":
            coin = input("🪙 ชื่อเหรียญ: ").upper()
            try:
                amount = float(input("💵 จำนวนเงิน USD: "))
                bot.buy_coin(coin, amount)
            except ValueError:
                print("❌ กรอกตัวเลขไม่ถูกต้อง")
                
        elif choice == "3":
            coin = input("🪙 ชื่อเหรียญ: ").upper()
            try:
                pct = float(input("📊 ขาย % (เช่น 50): "))
                bot.sell_coin(coin, pct)
            except ValueError:
                print("❌ กรอกตัวเลขไม่ถูกต้อง")
                
        elif choice == "4":
            bot.show_portfolio()
            
        elif choice == "5":
            bot.show_trade_history()
            
        elif choice == "6":
            print("👋 ขอบคุณที่ใช้งาน!")
            break
            
        else:
            print("❌ เลือกไม่ถูกต้อง")

# เรียกใช้งาน
if __name__ == "__main__":
    print("🎯 เลือกโหมด:")
    print("1. Demo อัตโนมัติ")
    print("2. เทรดด้วยตัวเอง")
    
    mode = input("👉 เลือก (1/2): ").strip()
    
    if mode == "1":
        simple_trading_demo()
    elif mode == "2":
        manual_trading()
    else:
        print("เลือกไม่ถูกต้อง รัน Demo อัตโนมัติ")
        simple_trading_demo()
