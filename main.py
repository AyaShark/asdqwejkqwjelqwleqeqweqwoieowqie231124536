import os
import asyncio
import json
import websockets
import random
from colorama import Fore

# --- ตั้งค่าตรงนี้ได้เลย ---

SERVER_ID = "1043535469771767808"
CHANNEL_ID = "1485874458584416370"

# -----------------------



# ตัวแปรระบบ (พรางค่าเพื่อความปลอดภัย)
_S='desktop'
_R='Discord'
_Q='windows'
_N='properties'
_M='heartbeat_interval'
_J='ioqwpeiopqwiopeqoipi.txt' # ชื่อไฟล์ใหม่ที่คุณต้องการ
_H='self_deaf'
_G='self_mute'
_F='channel_id'
_E='guild_id'
_C=True
_B='op'
_A='d'

# การตั้งค่าประสิทธิภาพ
MAX_WORKERS = 30 
RECONNECT_DELAY = 15
HEARTBEAT_MULTIPLIER = 1.2

async def connect(token):
    while _C:
        try:
            async with websockets.connect(
                'wss://gateway.discord.gg/?v=9&encoding=json',
                ping_interval=30,
                ping_timeout=60
            ) as websocket:
                # รับสัญญาณ Hello
                hello = await websocket.recv()
                hello_json = json.loads(hello)
                heartbeat_interval = hello_json[_A][_M] * HEARTBEAT_MULTIPLIER
                
                # ส่ง Identify (Login)
                await websocket.send(json.dumps({
                    _B: 2,
                    _A: {
                        'token': token, 
                        _N: {'$os': _Q, '$browser': _R, '$device': _S}
                    }
                }))
                
                # ส่งคำสั่งเข้าห้องเสียง (Mute: True / Deaf: False)
                await websocket.send(json.dumps({
                    _B: 4,
                    _A: {
                        _E: SERVER_ID, 
                        _F: CHANNEL_ID, 
                        _G: True,  # ปิดไมค์ (Mute)
                        _H: False  # เปิดหูฟัง (ไม่ Deaf)
                    }
                }))

                print(f"{Fore.GREEN}[+] Token {token[:15]}... ทำงานแล้ว (Muted)")

                # Loop เลี้ยงสัญญาณ (Heartbeat)
                while _C:
                    await asyncio.sleep(heartbeat_interval / 1000)
                    await websocket.send(json.dumps({
                        _B: 1,
                        _A: random.randint(1, 1000000)
                    }))
        except Exception as e:
            print(f"{Fore.RED}[!] Token {token[:15]}... เกิดข้อผิดพลาด: {e}. รอ {RECONNECT_DELAY} วินาที...")
            await asyncio.sleep(RECONNECT_DELAY)

async def main():
    # ตรวจสอบไฟล์ Token
    if not os.path.exists(_J):
        print(f"{Fore.RED}[!] ไม่พบไฟล์ {_J}! กรุณาสร้างไฟล์และใส่ Token ของคุณลงไป")
        return

    with open(_J, 'r') as f:
        tokens = [t.strip().strip('"').strip("'") for t in f.readlines() if t.strip()]

    if not tokens:
        print(f"{Fore.RED}[!] ไฟล์ {_J} ว่างเปล่า!")
        return

    print(f"{Fore.CYAN}[*] เริ่มทำงานกับ {len(tokens)} บัญชี...")
    
    tasks = []
    for token in tokens[:MAX_WORKERS]:
        tasks.append(asyncio.create_task(connect(token)))
        await asyncio.sleep(0.8) # กันโดน Spam Rate Limit
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print(f"{Fore.YELLOW}--- Discord Auto Voice (Silent Mode) ---")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping...")