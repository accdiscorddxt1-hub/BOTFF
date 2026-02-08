import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
from APIS import insta
from flask import Flask, jsonify, request
import asyncio
import signal
import sys

import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from keep_alive import keep_alive

keep_alive()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# Biến toàn cục 
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
spam_request_running = False
spam_request_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
# Thêm với các biến toàn cục khác
reject_spam_running = False
reject_spam_task = None
lag_running = False
lag_task = None
# Thêm các biến này cùng với các biến toàn cục khác ở đầu
reject_spam_running = False
reject_spam_task = None
evo_cycle_running = False
evo_cycle_task = None
evo_emotes = {
    "1": "909000063",   # AK
    "2": "909000068",   # SCAR
    "3": "909000075",   # 1st MP40
    "4": "909040010",   # 2nd MP40
    "5": "909000081",   # 1st M1014
    "6": "909039011",   # 2nd M1014
    "7": "909000085",   # XM8
    "8": "909000090",   # Famas
    "9": "909000098",   # UMP
    "10": "909035007",  # M1887
    "11": "909042008",  # Woodpecker
    "12": "909041005",  # Groza
    "13": "909033001",  # M4A1
    "14": "909038010",  # Thompson
    "15": "909038012",  # G18
    "16": "909045001",  # Parafal
    "17": "909049010",  # P90
    "18": "909051003"   # m60
}
#------------------------------------------#

# Ánh xạ emote cho lệnh evo
EMOTE_MAP = {
    1: 909000063,
    2: 909000081,
    3: 909000075,
    4: 909000085,
    5: 909000134,
    6: 909000098,
    7: 909035007,
    8: 909051012,
    9: 909000141,
    10: 909034008,
    11: 909051015,
    12: 909041002,
    13: 909039004,
    14: 909042008,
    15: 909051014,
    16: 909039012,
    17: 909040010,
    18: 909035010,
    19: 909041005,
    20: 909051003,
    21: 909034001
}

# Giá trị huy hiệu cho lệnh s1 đến s5 - sử dụng giá trị chính xác của bạn
BADGE_VALUES = {
    "s1": 1048576,    # Huy hiệu đầu tiên của bạn
    "s2": 32768,      # Huy hiệu thứ hai của bạn  
    "s3": 2048,       # Huy hiệu thứ ba của bạn
    "s4": 64,         # Huy hiệu thứ tư của bạn
    "s5": 262144     # Huy hiệu thứ bảy của bạn
}

# ------------------- Luồng API Insta -------------------
def start_insta_api():
    port = insta.find_free_port()
    print(f"🚀 Đang khởi động API Insta trên cổng {port}")
    insta.app.run(host="0.0.0.0", port=port, debug=False)
# ------------------- Kết thúc Luồng API Insta -------------------

# Hàm hỗ trợ cho ghost join
def dec_to_hex(decimal):
    """Chuyển đổi thập phân sang chuỗi hex"""
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()

async def encrypt_packet(packet_hex, key, iv):
    """Mã hóa gói tin sử dụng AES CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    """Wrapper cho encrypt_packet"""
    return await encrypt_packet(packet_hex, key, iv)
    



def get_idroom_by_idplayer(packet_hex):
    """Trích xuất ID phòng từ gói tin - chuyển đổi từ TCP khác của bạn"""
    try:
        json_result = get_available_room(packet_hex)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        idroom = data['15']["data"]
        return idroom
    except Exception as e:
        print(f"Lỗi khi trích xuất ID phòng: {e}")
        return None

async def check_player_in_room(target_uid, key, iv):
    """Kiểm tra người chơi có trong phòng không bằng cách gửi yêu cầu trạng thái"""
    try:
        # Gửi gói tin yêu cầu trạng thái
        status_packet = await GeT_Status(int(target_uid), key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', status_packet)
        
        # Bạn sẽ cần bắt gói tin phản hồi và phân tích nó
        # Hiện tại, trả về True và chúng ta sẽ xử lý phát hiện phòng trong vòng lặp chính
        return True
    except Exception as e:
        print(f"Lỗi khi kiểm tra trạng thái phòng của người chơi: {e}")
        return False
        
        
        


class MultiAccountManager:
    def __init__(self):
        self.accounts_file = "accounts.json"
        self.accounts_data = self.load_accounts()
    
    def load_accounts(self):
        """Tải nhiều tài khoản từ tệp JSON"""
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                accounts = json.load(f)

                return accounts
        except FileNotFoundError:
            print(f"❌ Không tìm thấy tệp tài khoản {self.accounts_file}!")
            return {}
        except Exception as e:
            print(f"❌ Lỗi khi tải tài khoản: {e}")
            return {}
    
    
    
    async def get_account_token(self, uid, password):
        """Lấy token truy cập cho một tài khoản cụ thể"""
        try:
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {
                "Host": "100067.connect.garena.com",
                "User-Agent": await Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            }
            data = {
                "uid": uid,
                "password": password,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        open_id = data.get("open_id")
                        access_token = data.get("access_token")
                        return open_id, access_token
            return None, None
        except Exception as e:
            print(f"❌ Lỗi khi lấy token cho {uid}: {e}")
            return None, None
    
    async def send_join_from_account(self, target_uid, account_uid, password, key, iv, region):
        """Gửi yêu cầu tham gia từ một tài khoản cụ thể"""
        try:
            # Lấy token cho tài khoản này
            open_id, access_token = await self.get_account_token(account_uid, password)
            if not open_id or not access_token:
                return False
            
            # Tạo gói tin tham gia sử dụng thông tin đăng nhập của tài khoản
            join_packet = await self.create_account_join_packet(target_uid, account_uid, open_id, access_token, key, iv, region)
            if join_packet:
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                return True
            return False
            
        except Exception as e:
            print(f"❌ Lỗi khi gửi tham gia từ {account_uid}: {e}")
            return False
            
async def SEnd_InV_with_Cosmetics(Nu, Uid, K, V, region):
    """Phiên bản đơn giản - chỉ thêm trường 5 với trang phục cơ bản"""
    region = "ind"
    fields = {
        1: 2, 
        2: {
            1: int(Uid), 
            2: region, 
            4: int(Nu),
            # Đơn giản thêm trường 5 với trang phục cơ bản
            5: {
                1: "BOT",                    # Tên
                2: int(await get_random_avatar()),     # Avatar
                5: random.choice([1048576, 32768, 2048]),  # Huy hiệu ngẫu nhiên
            }
        }
    }

    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)   
            
async def join_custom_room(room_id, room_password, key, iv, region):
    """Tham gia phòng tùy chỉnh với cấu trúc gói tin Free Fire đúng"""
    fields = {
        1: 61,  # Loại gói tin tham gia phòng (đã xác minh cho Free Fire)
        2: {
            1: int(room_id),
            2: {
                1: int(room_id),  # ID Phòng
                2: int(time.time()),  # Thời gian
                3: "BOT",  # Tên người chơi
                5: 12,  # Không xác định
                6: 9999999,  # Không xác định
                7: 1,  # Không xác định
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,  # Loại phòng
            },
            3: str(room_password),  # Mật khẩu phòng
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
    
async def leave_squad(key, iv, region):
    """Rời đội - chuyển đổi từ hàm leave_s() TCP cũ của bạn"""
    fields = {
        1: 7,
        2: {
            1: 12480598706  # Giá trị chính xác từ TCP cũ
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    """Gửi yêu cầu tham gia với huy hiệu cụ thể - chuyển đổi từ TCP cũ của bạn"""
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] KRISHNA",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                       97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\c\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(await get_random_avatar()),
            26: "",
            28: "",
            31: {
                1: 1,
                2: badge_value  # Giá trị huy hiệu động
            },
            32: badge_value,    # Giá trị huy hiệu động
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def reset_bot_state(key, iv, region):
    """Đặt lại bot về chế độ solo trước khi spam - Bước quan trọng từ TCP cũ của bạn"""
    try:
        # Rời đội hiện tại (sử dụng hàm leave_s chính xác của bạn)
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        
        print("✅ Trạng thái bot đã được đặt lại - đã rời đội")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi đặt lại bot: {e}")
        return False    
    
async def create_custom_room(room_name, room_password, max_players, key, iv, region):
    """Tạo phòng tùy chỉnh"""
    fields = {
        1: 3,  # Loại gói tin tạo phòng
        2: {
            1: room_name,
            2: room_password,
            3: max_players,  # 2, 4, 8, 16, etc.
            4: 1,  # Chế độ phòng
            5: 1,  # Bản đồ
            6: "en",  # Ngôn ngữ
            7: {   # Thông tin người chơi
                1: "BotHost",
                2: int(await get_random_avatar()),
                3: 330,
                4: 1048576,
                5: "BOTCLAN"
            }
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)              
            
async def real_multi_account_join(target_uid, key, iv, region):
    """Gửi yêu cầu tham gia sử dụng phiên tài khoản thực"""
    try:
        # Tải tài khoản
        accounts_data = load_accounts()
        if not accounts_data:
            return 0, 0
        
        success_count = 0
        total_accounts = len(accounts_data)
        
        for account_uid, password in accounts_data.items():
            try:
                print(f"🔄 Đang xác thực tài khoản: {account_uid}")
                
                # Lấy token đúng cho tài khoản này
                open_id, access_token = await GeNeRaTeAccEss(account_uid, password)
                if not open_id or not access_token:
                    print(f"❌ Không thể xác thực {account_uid}")
                    continue
                
                # Tạo yêu cầu tham gia đúng sử dụng danh tính tài khoản
                # Chúng ta sẽ sử dụng hàm SEnd_InV hiện có nhưng với ngữ cảnh tài khoản
                join_packet = await create_authenticated_join(target_uid, account_uid, key, iv, region)
                
                if join_packet:
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                    success_count += 1
                    print(f"✅ Đã gửi tham gia từ tài khoản đã xác thực: {account_uid}")
                
                # Quan trọng: Chờ giữa các yêu cầu
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Lỗi với tài khoản {account_uid}: {e}")
                continue
        
        return success_count, total_accounts
        
    except Exception as e:
        print(f"❌ Lỗi tham gia đa tài khoản: {e}")
        return 0, 0



async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Xử lý lệnh huy hiệu riêng lẻ"""
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Cách dùng: /{cmd} (uid)\nVí dụ: /{cmd} 123456789\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Vui lòng nhập ID người chơi hợp lệ!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Gửi tin nhắn ban đầu
    initial_msg = f"[B][C][1E90FF]🌀 Đã nhận yêu cầu! Đang chuẩn bị spam {target_uid}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        # Đặt lại trạng thái bot
        await reset_bot_state(key, iv, region)
        
        # Tạo và gửi gói tin tham gia
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        spam_count = 3
        
        for i in range(spam_count):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            print(f"✅ Đã gửi yêu cầu /{cmd} #{i+1} với huy hiệu {badge_value}")
            await asyncio.sleep(0.1)
        
        success_msg = f"[B][C][00FF00]✅ Đã gửi thành công {spam_count} Yêu cầu Tham gia!\n🎯 Mục tiêu: {target_uid}\n🏷️ Huy hiệu: {badge_value}\n"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Dọn dẹp
        await asyncio.sleep(1)
        await reset_bot_state(key, iv, region)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Lỗi trong /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def create_authenticated_join(target_uid, account_uid, key, iv, region):
    """Tạo yêu cầu tham gia xuất hiện từ tài khoản cụ thể"""
    try:
        # Sử dụng hàm mời tiêu chuẩn nhưng đảm bảo sử dụng ngữ cảnh tài khoản
        join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
        return join_packet
    except Exception as e:
        print(f"❌ Lỗi khi tạo gói tin tham gia: {e}")
        return None        
    
    async def create_account_join_packet(self, target_uid, account_uid, open_id, access_token, key, iv, region):
        """Tạo gói tin yêu cầu tham gia cho tài khoản cụ thể"""
        try:
            # Đây là nơi bạn sử dụng UID thực của tài khoản thay vì UID bot chính
            fields = {
                1: 33,
                2: {
                    1: int(target_uid),  # UID mục tiêu
                    2: region.upper(),
                    3: 1,
                    4: 1,
                    5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                    6: f"BOT:[C][B][FF0000] ACCOUNT_{account_uid[-4:]}",  # Hiển thị UID tài khoản
                    7: 330,
                    8: 1000,
                    10: region.upper(),
                    11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                               97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
                    12: 1,
                    13: int(account_uid),  # Sử dụng UID của TÀI KHOẢN ở đây, không phải UID mục tiêu!
                    14: {
                        1: 2203434355,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0013\c\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    },
                    16: 1,
                    17: 1,
                    18: 312,
                    19: 46,
                    23: bytes([16, 1, 24, 1]),
                    24: int(await get_random_avatar()),
                    26: "",
                    28: "",
                    31: {
                        1: 1,
                        2: 32768  # Huy hiệu V
                    },
                    32: 32768,
                    34: {
                        1: int(account_uid),  # Sử dụng UID của TÀI KHOẢN ở đây nữa!
                        2: 8,
                        3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
                    }
                },
                10: "en",
                13: {
                    2: 1,
                    3: 1
                }
            }
            
            packet = (await CrEaTe_ProTo(fields)).hex()
            
            if region.lower() == "ind":
                packet_type = '0514'
            elif region.lower() == "bd":
                packet_type = "0519"
            else:
                packet_type = "0515"
                
            return await GeneRaTePk(packet, packet_type, key, iv)
            
        except Exception as e:
            print(f"❌ Lỗi khi tạo gói tin tham gia cho {account_uid}: {e}")
            return None

# Thể hiện toàn cục
multi_account_manager = MultiAccountManager()
    
    
    
async def auto_rings_emote_dual(sender_uid, key, iv, region):
    """Gửi emote The Rings cho cả người gửi và bot để hiệu ứng dual emote"""
    try:
        # ID emote The Rings
        rings_emote_id = 909050009
        
        # Lấy UID của bot
        bot_uid = 13699776666
        
        # Gửi emote cho NGƯỜI GỬI (người mời)
        emote_to_sender = await Emote_k(int(sender_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
        
        # Độ trễ nhỏ giữa các emote
        await asyncio.sleep(0.5)
        
        # Gửi emote cho BOT (bot thực hiện emote lên chính nó)
        emote_to_bot = await Emote_k(int(bot_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_bot)
        
        print(f"🤖 Bot đã thực hiện dual Rings emote với người gửi {sender_uid} và bot {bot_uid}!")
        
    except Exception as e:
        print(f"Lỗi khi gửi dual rings emote: {e}")    
        
        
async def Room_Spam(Uid, Rm, Nm, K, V):
   
    same_value = random.choice([32768])  #bạn có thể thêm bất kỳ giá trị huy hiệu nào 
    
    fields = {
        1: 78,
        2: {
            1: int(Rm),  
            2: "iG:[C][B][FF0000] ROSHAN ODEX",  
            3: {
                2: 1,
                3: 1
            },
            4: 330,      
            5: 6000,     
            6: 201,      
            10: int(await get_random_avatar()),  
            11: int(Uid), # UID mục tiêu
            12: 1,       
            15: {
                1: 1,
                2: same_value  
            },
            16: same_value,    
            18: {
                1: 11481904755,  
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\c\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            
            31: {
                1: 1,
                2: same_value  
            },
            32: same_value,    
            34: {
                1: int(Uid),   
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        }
    }
    
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)
    
async def evo_cycle_spam(uids, key, iv, region):
    """Lặp qua tất cả evolution emotes từng cái một với độ trễ 5 giây"""
    global evo_cycle_running
    
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        print(f"Bắt đầu chu kỳ evolution emote #{cycle_count}")
        
        for emote_number, emote_id in evo_emotes.items():
            if not evo_cycle_running:
                break
                
            print(f"Đang gửi evolution emote {emote_number} (ID: {emote_id})")
            
            for uid in uids:
                try:
                    uid_int = int(uid)
                    H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                    print(f"Đã gửi emote {emote_number} đến UID: {uid}")
                except Exception as e:
                    print(f"Lỗi khi gửi evo emote {emote_number} đến {uid}: {e}")
            
            # Chờ 5 giây trước khi chuyển sang emote tiếp theo (như yêu cầu)
            if evo_cycle_running:
                print(f"Đang chờ 5 giây trước emote tiếp theo...")
                for i in range(5):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
        
        # Độ trễ nhỏ trước khi bắt đầu lại chu kỳ
        if evo_cycle_running:
            print("Đã hoàn thành một chu kỳ đầy đủ của tất cả evolution emotes. Đang khởi động lại...")
            await asyncio.sleep(2)
    
    print("Chu kỳ evolution emote đã dừng")
    
async def reject_spam_loop(target_uid, key, iv):
    """Gửi gói tin reject spam đến mục tiêu trong nền"""
    global reject_spam_running
    
    count = 0
    max_spam = 150
    
    while reject_spam_running and count < max_spam:
        try:
            # Gửi cả hai gói tin
            packet1 = await banecipher1(target_uid, key, iv)
            packet2 = await banecipher(target_uid, key, iv)
            
            # Gửi đến kết nối Online
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet1)
            await asyncio.sleep(0.1)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet2)
            
            count += 1
            print(f"Đã gửi reject spam #{count} đến {target_uid}")
            
            # Độ trễ 0.2 giây giữa các chu kỳ spam
            await asyncio.sleep(0.2)
            
        except Exception as e:
            print(f"Lỗi trong reject spam: {e}")
            break
    
    return count    
    
async def handle_reject_completion(spam_task, target_uid, sender_uid, chat_id, chat_type, key, iv):
    """Xử lý hoàn thành reject spam và gửi tin nhắn cuối cùng"""
    try:
        spam_count = await spam_task
        
        # Gửi tin nhắn hoàn thành
        if spam_count >= 150:
            completion_msg = f"[B][C][00FF00]✅ Reject Spam Đã Hoàn Thành Thành Công Cho ID {target_uid}\n✅ Tổng số gói tin đã gửi: {spam_count * 2}\n"
        else:
            completion_msg = f"[B][C][FFFF00]⚠️ Reject Spam Hoàn Thành Một Phần Cho ID {target_uid}\n⚠️ Tổng số gói tin đã gửi: {spam_count * 2}\n"
        
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
        
    except asyncio.CancelledError:
        print("Reject spam đã bị hủy")
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ LỖI trong reject spam: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)    
    
async def banecipher(client_id, key, iv):
    """Tạo gói tin reject spam 1 - Chuyển đổi sang định dạng async mới"""
    banner_text = f"""
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███




"""        
    fields = {
        1: 5,
        2: {
            1: int(client_id),
            2: 1,
            3: int(client_id),
            4: banner_text
        }
    }
    
    # Sử dụng CrEaTe_ProTo từ xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Sử dụng EnC_PacKeT từ xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Tính độ dài header
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Xây dựng gói tin cuối cùng dựa trên độ dài header
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)

async def banecipher1(client_id, key, iv):
    """Tạo gói tin reject spam 2 - Chuyển đổi sang định dạng async mới"""
    gay_text = f"""
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][0000FF]======================================================================================================================================================================================================================================================
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███




"""        
    fields = {
        1: int(client_id),
        2: 5,
        4: 50,
        5: {
            1: int(client_id),
            2: gay_text,
        }
    }
    
    # Sử dụng CrEaTe_ProTo từ xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Sử dụng EnC_PacKeT từ xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Tính độ dài header
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Xây dựng gói tin cuối cùng dựa trên độ dài header
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)
    

async def lag_team_loop(team_code, key, iv, region):
    """Vòng lặp tham gia/rời nhanh để tạo lag"""
    global lag_running
    count = 0
    
    while lag_running:
        try:
            # Tham gia đội
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
            # Độ trễ rất ngắn trước khi rời
            await asyncio.sleep(0.01)  # 10 mili giây
            
            # Rời đội
            leave_packet = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            
            count += 1
            print(f"Chu kỳ lag #{count} hoàn thành cho đội: {team_code}")
            
            # Độ trễ ngắn trước chu kỳ tiếp theo
            await asyncio.sleep(0.01)  # 10 mili giây giữa các chu kỳ
            
        except Exception as e:
            print(f"Lỗi trong vòng lặp lag: {e}")
            # Tiếp tục vòng lặp ngay cả khi có lỗi
            await asyncio.sleep(0.1)
 
####################################

#Thông-tin-clan-theo-id-clan
def Get_clan_info(clan_id):
    try:
        url = f"https://get-clan-info.vercel.app/get_clan_info?clan_id={clan_id}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            msg = f""" 
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
▶▶▶▶CHI TIẾT GUILD◀◀◀◀
Thành tựu: {data['achievements']}\n\n
Số dư : {fix_num(data['balance'])}\n\n
Tên Clan : {data['clan_name']}\n\n
Thời gian hết hạn : {fix_num(data['guild_details']['expire_time'])}\n\n
Thành viên trực tuyến : {fix_num(data['guild_details']['members_online'])}\n\n
Khu vực : {data['guild_details']['regional']}\n\n
Thời gian thưởng : {fix_num(data['guild_details']['reward_time'])}\n\n
Tổng thành viên : {fix_num(data['guild_details']['total_members'])}\n\n
ID : {fix_num(data['id'])}\n\n
Hoạt động lần cuối : {fix_num(data['last_active'])}\n\n
Cấp độ : {fix_num(data['level'])}\n\n
Hạng : {fix_num(data['rank'])}\n\n
Khu vực : {data['region']}\n\n
Điểm số : {fix_num(data['score'])}\n\n
Thời gian 1 : {fix_num(data['timestamp1'])}\n\n
Thời gian 2 : {fix_num(data['timestamp2'])}\n\n
Tin nhắn chào mừng: {data['welcome_message']}\n\n
XP: {fix_num(data['xp'])}\n\n
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
            """
            return msg
        else:
            msg = """
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
Không thể lấy thông tin, vui lòng thử lại sau!!

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
            """
            return msg
    except:
        pass
#LẤY THÔNG TIN THEO ID NGƯỜI CHƠI
def get_player_info(player_id):
    url = f"https://like2.vercel.app/player-info?uid={player_id}&server={server2}&key={key2}"
    response = requests.get(url)
    print(response)    
    if response.status_code == 200:
        try:
            r = response.json()
            return {
                "Booyah Pass Tài khoản": f"{r.get('booyah_pass_level', 'N/A')}",
                "Tài khoản được tạo": f"{r.get('createAt', 'N/A')}",
                "Cấp độ Tài khoản": f"{r.get('level', 'N/A')}",
                "Lượt thích Tài khoản": f" {r.get('likes', 'N/A')}",
                "Tên": f"{r.get('nickname', 'N/A')}",
                "UID": f" {r.get('accountId', 'N/A')}",
                "Khu vực Tài khoản": f"{r.get('region', 'N/A')}",
                }
        except ValueError as e:
            pass
            return {
                "error": "Phản hồi JSON không hợp lệ"
            }
    else:
        pass
        return {
            "error": f"Không thể lấy dữ liệu: {response.status_code}"
        }
#LẤY TIỂU SỬ NGƯỜI CHƠI 
def get_player_bio(uid):
    try:
        url = f"https://info-wotaxxdev-api.vercel.app/info?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # Tiểu sử nằm trong socialInfo -> signature
            bio = data.get('socialInfo', {}).get('signature', None)
            if bio:
                return bio
            else:
                return "Không có tiểu sử"
        else:
            return f"Không thể lấy tiểu sử. Mã trạng thái: {res.status_code}"
    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"
#TRÒ CHUYỆN VỚI AI
def talk_with_ai(question):
    url = f"https://aashish-ai-api.vercel.app/ask?key=AASHISH65&message={question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        msg = data["message"]["content"]
        return msg
    else:
        return "Đã xảy ra lỗi khi kết nối đến máy chủ."
#SPAM YÊU CẦU
def spam_requests(player_id):
    # URL này giờ trỏ đúng đến ứng dụng Flask bạn đã cung cấp
    url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
    try:
        res = requests.get(url, timeout=20) # Đã thêm timeout
        if res.status_code == 200:
            data = res.json()
            # Trả về thông báo mô tả hơn dựa trên phản hồi JSON của API
            return f"Trạng thái API: Thành công [{data.get('success_count', 0)}] Thất bại [{data.get('failed_count', 0)}]"
        else:
            # Trả về trạng thái lỗi từ API
            return f"Lỗi API: Trạng thái {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Xử lý trường hợp API không chạy hoặc không thể truy cập
        print(f"Không thể kết nối đến API spam: {e}")
        return "Không thể kết nối đến API spam."
####################################

# ** HÀM THÔNG TIN MỚI sử dụng API mới **
def newinfo(uid):
    # URL cơ sở không có tham số
    url = "https://like2.vercel.app/player-info"
    # Từ điển tham số - đây là cách robust để thực hiện
    params = {
        'uid': uid,
        'server': server2,  # Cố định thành bd như yêu cầu
        'key': key2
    }
    try:
        # Truyền tham số đến requests.get()
        response = requests.get(url, params=params, timeout=10)
        
        # Kiểm tra nếu yêu cầu thành công
        if response.status_code == 200:
            data = response.json()
            # Kiểm tra nếu cấu trúc dữ liệu mong đợi có trong phản hồi
            if "basicInfo" in data:
                return {"status": "ok", "data": data}
            else:
                # API trả về 200, nhưng dữ liệu không như mong đợi (ví dụ: thông báo lỗi trong JSON)
                return {"status": "error", "message": data.get("error", "ID không hợp lệ hoặc không tìm thấy dữ liệu.")}
        else:
            # API trả về mã trạng thái lỗi (ví dụ: 404, 500)
            try:
                # Thử lấy thông báo lỗi cụ thể từ phản hồi của API
                error_msg = response.json().get('error', f"API trả về trạng thái {response.status_code}")
                return {"status": "error", "message": error_msg}
            except ValueError:
                # Nếu phản hồi lỗi không phải JSON
                return {"status": "error", "message": f"API trả về trạng thái {response.status_code}"}

    except requests.exceptions.RequestException as e:
        # Xử lý lỗi mạng (ví dụ: timeout, không có kết nối)
        return {"status": "error", "message": f"Lỗi mạng: {str(e)}"}
    except ValueError: 
        # Xử lý trường hợp phản hồi không phải JSON hợp lệ
        return {"status": "error", "message": "Phản hồi JSON không hợp lệ từ API."}
        
    async def run_spam(chat_type, message, count, uid, chat_id, key, iv):
        try:
            for i in range(count):
                await safe_send_message(chat_type, message, uid, chat_id, key, iv)
                await asyncio.sleep(0.12)
        except Exception as e:
            print("Lỗi Spam:", e)
        
    async def send_title_msg(self, chat_id, key, iv):
        """Xây dựng gói tin tiêu đề sử dụng cấu trúc từ điển như GenResponsMsg"""
    
        fields = {
            1: 1,  # loại
            2: {   # dữ liệu
                1: "13777777720",  # uid
                2: str(chat_id),   # chat_id  
                3: f"{{\"TitleID\":{get_random_title()},\"type\":\"Title\"}}",  # tiêu đề
                4: int(datetime.now().timestamp()),  # thời gian
                5: 0,   # loại_chat
                6: "en", # ngôn ngữ
                9: {    # trường9 - chi tiết người chơi
                    1: "[C][B][FF0000] KRN ON TOP",  # Biệt danh
                    2: await get_random_avatar(),          # avatar_id
                    3: 330,                          # hạng
                    4: 102000015,                    # huy hiệu
                    5: "TEMP GUILD",                 # Tên_Clan
                    6: 1,                            # trường10
                    7: 1,                            # vị_trí_hạng_toàn_cầu
                    8: {                             # thông_tin_huy_hiệu
                        1: 2                         # giá trị
                    },
                    9: {                             # thông_tin_prime
                        1: 1158053040,               # prime_uid
                        2: 8,                        # prime_level
                        3: "\u0010\u0015\b\n\u000b\u0015\c\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"  # prime_hex
                    }
                },
                13: {   # trường13 - tùy chọn url
                    1: 2,   # loại_url
                    2: 1    # nền_tảng_curl
                },
                99: b""  # trường_trống
            }
        }

        # **GIỐNG HỆT GenResponsMsg:**
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_length = len(encrypt_packet(packet, key, iv)) // 2
        header_length_final = dec_to_hex(header_length)
    
        # **CHÌA KHÓA: Sử dụng 0515 cho gói tin tiêu đề thay vì 1215**
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
    
        return bytes.fromhex(final_packet)
        
        

	
#THÊM-100-LƯỢT-THÍCH-TRONG-24H
def send_likes(uid):
    try:
        likes_api_response = requests.get(
             f"https://yourlikeapi/like?uid={uid}&server_name={server2}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS_TOKEN}",
             timeout=15
             )
      
      
        if likes_api_response.status_code != 200:
            return f"""
[C][B][FF0000]━━━━━
[FFFFFF]Lỗi API Like!
Mã trạng thái: {likes_api_response.status_code}
Vui lòng kiểm tra xem uid có đúng không.
━━━━━
"""

        api_json_response = likes_api_response.json()

        player_name = api_json_response.get('PlayerNickname', 'Không xác định')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # ✅ Thành công
            return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Trạng thái Like:

[00FF00]Đã gửi Like Thành công!

[FFFFFF]Tên người chơi : [00FF00]{player_name}  
[FFFFFF]Like đã thêm : [00FF00]{likes_added}  
[FFFFFF]Like trước đó : [00FF00]{likes_before}  
[FFFFFF]Like sau đó : [00FF00]{likes_after}  
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Đăng ký: [FFFFFF]SPIDEERIO YT [00FF00]!!
"""
        elif status == 2 or likes_before == likes_after:
            # 🚫 Đã nhận / Đã đạt giới hạn
            return f"""
[C][B][FF0000]━━━━━━━━━━━━

[FFFFFF]Không gửi Like!

[FF0000]Bạn đã nhận like với UID này rồi.
Thử lại sau 24 giờ.

[FFFFFF]Tên người chơi : [FF0000]{player_name}  
[FFFFFF]Like trước đó : [FF0000]{likes_before}  
[FFFFFF]Like sau đó : [FF0000]{likes_after}  
[C][B][FF0000]━━━━━━━━━━━━
"""
        else:
            # ❓ Trường hợp không mong đợi
            return f"""
[C][B][FF0000]━━━━━━━━━━━━
[FFFFFF]Phản hồi không mong đợi!
Đã xảy ra lỗi.

Vui lòng thử lại hoặc liên hệ hỗ trợ.
━━━━━━━━━━━━
"""

    except requests.exceptions.RequestException:
        return """
[C][B][FF0000]━━━━━
[FFFFFF]Kết nối API Like Thất bại!
Máy chủ API (app.py) có đang chạy không?
━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]Đã xảy ra lỗi không mong đợi:
[FF0000]{str(e)}
━━━━━
"""
#TÊN NGƯỜI DÙNG ĐẾN THÔNG TIN INSTA 
def send_insta_info(username):
    try:
        response = requests.get(f"http://127.0.0.1:8080/api/insta/{username}", timeout=15)
        if response.status_code != 200:
            return f"[B][C][FF0000]❌ Lỗi API Instagram! Mã trạng thái: {response.status_code}"

        user = response.json()
        full_name = user.get("full_name", "Không xác định")
        followers = user.get("edge_followed_by", {}).get("count") or user.get("followers_count", 0)
        following = user.get("edge_follow", {}).get("count") or user.get("following_count", 0)
        posts = user.get("media_count") or user.get("edge_owner_to_timeline_media", {}).get("count", 0)
        profile_pic = user.get("profile_pic_url_hd") or user.get("profile_pic_url")
        private_status = user.get("is_private")
        verified_status = user.get("is_verified")

        return f"""
[B][C][FB0364]╭[D21A92]─[BC26AB]╮[FFFF00]╔═══════╗
[C][B][FF7244]│[FE4250]◯[C81F9C]֯│[FFFF00]║[FFFFFF]THÔNG_TIN_INSTAGRAM[FFFF00]║
[C][B][FDC92B]╰[FF7640]─[F5066B]╯[FFFF00]╚═══════╝
[C][B][FFFF00]━━━━━━━━━━━━
[C][B][FFFFFF]Tên: [66FF00]{full_name}
[C][B][FFFFFF]Tên người dùng: [66FF00]{username}
[C][B][FFFFFF]Người theo dõi: [66FF00]{followers}
[C][B][FFFFFF]Đang theo dõi: [66FF00]{following}
[C][B][FFFFFF]Bài viết: [66FF00]{posts}
[C][B][FFFFFF]Riêng tư: [66FF00]{private_status}
[C][B][FFFFFF]Đã xác minh: [66FF00]{verified_status}
[C][B][FFFF00]━━━━━━━━━━━━
"""
    except requests.exceptions.RequestException:
        return "[B][C][FF0000]❌ Kết nối API Instagram Thất bại!"
    except Exception as e:
        return f"[B][C][FF0000]❌ Lỗi không mong đợi: {str(e)}"

####################################
#KIỂM TRA TÀI KHOẢN BỊ CẤM

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB51"}

# ---- Màu Ngẫu Nhiên ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

print(get_random_color())
    
# ---- Avatar Ngẫu Nhiên ----
async def get_random_avatar():
    await asyncio.sleep(0)  # làm cho nó async nhưng tức thì
    avatar_list = [
        '902050001', '902050002', '902050003', '902039016', '902050004',
        '902047011', '902047010', '902049015', '902050006', '902049020'
    ]
    return random.choice(avatar_list)
    
print(get_random_avatar())

async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    """Tham gia đội, xác thực chat, thực hiện emote, và tự động rời đi"""
    try:
        # Bước 1: Tham gia đội
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        print(f"🤖 Đã tham gia đội: {team_code}")
        
        # Chờ dữ liệu đội và xác thực chat
        await asyncio.sleep(1.5)  # Tăng lên để đảm bảo kết nối đúng
        
        # Bước 2: Bot cần được phát hiện trong đội và xác thực chat
        # Điều này xảy ra tự động trong TcPOnLine, nhưng chúng ta cần chờ nó
        
        # Bước 3: Thực hiện emote đến UID mục tiêu
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        print(f"🎭 Đã thực hiện emote {emote_id} đến UID {target_uid}")
        
        # Chờ emote đăng ký
        await asyncio.sleep(0.5)
        
        # Bước 4: Rời đội
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print(f"🚪 Đã rời đội: {team_code}")
        
        return True, f"Tấn công emote nhanh hoàn thành! Đã gửi emote đến UID {target_uid}"
        
    except Exception as e:
        return False, f"Tấn công emote nhanh thất bại: {str(e)}"
        
        
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Không thể lấy token truy cập"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Độ dài không mong đợi') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'Loại Không Hỗ Trợ ! >> Lỗi (:():)' 

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    """Gửi tin nhắn an toàn với cơ chế thử lại"""
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            print(f"Tin nhắn đã gửi thành công ở lần thử {attempt + 1}")
            return True
        except Exception as e:
            print(f"Không thể gửi tin nhắn (lần thử {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)  # Chờ trước khi thử lại
    return False

async def fast_emote_spam(uids, emote_id, key, iv, region):
    """Hàm spam emote nhanh gửi emotes nhanh chóng"""
    global fast_spam_running
    count = 0
    max_count = 25  # Spam 25 lần
    
    while fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Lỗi trong fast_emote_spam cho uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # Khoảng cách 0.1 giây giữa các chu kỳ spam

# HÀM MỚI: Spam emote tùy chỉnh với số lần xác định
async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    """Hàm spam emote tùy chỉnh gửi emotes số lần xác định"""
    global custom_spam_running
    count = 0
    
    while custom_spam_running and count < times:
        try:
            uid_int = int(uid)
            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.1)  # Khoảng cách 0.1 giây giữa các emote
        except Exception as e:
            print(f"Lỗi trong custom_emote_spam cho uid {uid}: {e}")
            break

# HÀM MỚI: Vòng lặp spam yêu cầu nhanh hơn - Gửi chính xác 30 yêu cầu nhanh chóng
async def spam_request_loop_with_cosmetics(target_uid, key, iv, region):
    """Hàm spam yêu cầu với trang phục - sử dụng cấu trúc giống của bạn"""
    global spam_request_running
    
    count = 0
    max_requests = 30
    
    # Các giá trị huy hiệu khác nhau để xoay vòng
    badge_rotation = [1048576, 32768, 2048, 64, 4094, 11233, 262144]
    
    while spam_request_running and count < max_requests:
        try:
            # Xoay vòng qua các huy hiệu khác nhau
            current_badge = badge_rotation[count % len(badge_rotation)]
            
            # Tạo đội (giống trước)
            PAc = await OpEnSq(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
            await asyncio.sleep(0.2)
            
            # Thay đổi kích thước đội (giống trước)
            C = await cHSq(5, int(target_uid), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
            await asyncio.sleep(0.2)
            
            # Gửi lời mời VỚI TRANG PHỤC (phiên bản nâng cao)
            V = await SEnd_InV_With_Cosmetics(5, int(target_uid), key, iv, region, current_badge)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
            
            # Rời đội (giống trước)
            E = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
            
            count += 1
            print(f"✅ Đã gửi lời mời có trang phục #{count} đến {target_uid} với huy hiệu {current_badge}")
            
            # Độ trễ ngắn
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"Lỗi trong spam có trang phục: {e}")
            await asyncio.sleep(0.5)
    
    return count
            


# HÀM MỚI: Spam emote evolution với ánh xạ
async def evo_emote_spam(uids, number, key, iv, region):
    """Gửi evolution emotes dựa trên ánh xạ số"""
    try:
        emote_id = EMOTE_MAP.get(int(number))
        if not emote_id:
            return False, f"Số không hợp lệ! Chỉ sử dụng 1-21."
        
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Lỗi khi gửi evo emote đến {uid}: {e}")
        
        return True, f"Đã gửi evolution emote {number} (ID: {emote_id}) đến {success_count} người chơi"
    
    except Exception as e:
        return False, f"Lỗi trong evo_emote_spam: {str(e)}"

# HÀM MỚI: Spam evolution emote nhanh
async def evo_fast_emote_spam(uids, number, key, iv, region):
    """Hàm spam evolution emote nhanh"""
    global evo_fast_spam_running
    count = 0
    max_count = 25  # Spam 25 lần
    
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Số không hợp lệ! Chỉ sử dụng 1-21."
    
    while evo_fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Lỗi trong evo_fast_emote_spam cho uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # ĐÃ THAY ĐỔI: 0.5 giây thành 0.1 giây
    
    return True, f"Đã hoàn thành spam evolution emote nhanh {count} lần"

# HÀM MỚI: Spam evolution emote tùy chỉnh với số lần xác định
async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    """Spam evolution emote tùy chỉnh với số lần lặp xác định"""
    global evo_custom_spam_running
    count = 0
    
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Số không hợp lệ! Chỉ sử dụng 1-21."
    
    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Lỗi trong evo_custom_emote_spam cho uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.1)  # ĐÃ THAY ĐỔI: 0.5 giây thành 0.1 giây
    
    return True, f"Đã hoàn thành spam evolution emote tùy chỉnh {count} lần"

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break
                
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        print(data2.hex()[10:])
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        print(packet)
                        packet = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)


                        # Trong hàm TcPOnLine, sau khi tự động tham gia thành công:
                        message = f'[B][C]{get_random_color()}\n- Chào Mừng Đến Với Emote Bot ! '
                        P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
 
                       # THÊM DUAL EMOTE CHO AUTO-JOINS NỮA
                        try:
                            await auto_rings_emote_dual(OwNer_UiD, key, iv, region)
                        except Exception as emote_error:
                            print(f"Tự động dual emote thất bại: {emote_error}")
                    except:
                        if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                            try:
                                print(data2.hex()[10:])
                                packet = await DeCode_PackEt(data2.hex()[10:])
                                print(packet)
                                packet = json.loads(packet)
                                OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                                JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)


                                message = f'[B][C]{get_random_color()}\n- Chào Mừng Đến Với Emote Bot ! \n\n{get_random_color()}- Lệnh : @a {xMsGFixinG('player_uid')} {xMsGFixinG('909000001')}\n\n[00FF00]Dev : @{xMsGFixinG('ROSHAM ')}'
                                P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                            except:
                                pass

            online_writer.close() ; await online_writer.wait_closed() ; online_writer = None

        except Exception as e: print(f"- Lỗi Với {ip}:{port} - {e}") ; online_writer = None
        await asyncio.sleep(reconnect_delay)
        
                    

                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, evo_cycle_running, evo_cycle_task, reject_spam_running, reject_spam_task
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - BoT Mục Tiêu trong CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT Đã Kết Nối Với CLan ChaT Thành Công ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                
                if data.hex().startswith("120000"):

                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                        
                        # In gỡ lỗi để xem chúng ta đang nhận được gì
                        print(f"Đã nhận tin nhắn: {inPuTMsG} từ UID: {uid} trong loại chat: {XX}")
                        
                    except:
                        response = None


                    if response:
                        # TẤT CẢ LỆNH GIỜ HOẠT ĐỘNG TRONG TẤT CẢ LOẠI CHAT (SQUAD, GUILD, PRIVATE)
                        
                        # Lệnh AI - /ai
                        if inPuTMsG.strip().startswith('/ai '):
                            print('Đang xử lý lệnh AI trong bất kỳ loại chat nào')
                            
                            question = inPuTMsG[4:].strip()
                            if question:
                                initial_message = f"[B][C]{get_random_color()}\n🤖 AI đang suy nghĩ...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                # Sử dụng ThreadPoolExecutor để tránh chặn vòng lặp async
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    ai_response = await loop.run_in_executor(executor, talk_with_ai, question)
                                
                                # Định dạng phản hồi AI
                                ai_message = f"""
[B][C][00FF00]🤖 Phản Hồi AI:

[FFFFFF]{ai_response}

[C][B][FFB300]Câu hỏi: [FFFFFF]{question}
"""
                                await safe_send_message(response.Data.chat_type, ai_message, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Vui lòng cung cấp câu hỏi sau /ai\nVí dụ: /ai Free Fire là gì?\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Lệnh Likes - /likes
                        if inPuTMsG.strip().startswith('/likes '):
                            print('Đang xử lý lệnh likes trong bất kỳ loại chat nào')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /likes (uid)\nVí dụ: /likes 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nĐang gửi 100 likes đến {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                # Sử dụng ThreadPoolExecutor để tránh chặn vòng lặp async
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    likes_result = await loop.run_in_executor(executor, send_likes, target_uid)
                                
                                await safe_send_message(response.Data.chat_type, likes_result, uid, chat_id, key, iv)
                                
                                #LỆNH SPAM TIN NHẮN ĐỘI
                        if inPuTMsG.strip().startswith('/ms '):
                            print('Đang xử lý lệnh /ms')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ LỖI! Cách dùng:\n"
                                        "/ms <tin_nhắn>\n"
                                        "Ví dụ: /ms ROSHAN"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    user_message = parts[1].strip()

                                    for _ in range(30):
                                        color = get_random_color()  # màu ngẫu nhiên từ danh sách của bạn
                                        colored_message = f"[B][C]{color} {user_message}"  # định dạng đúng
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Đã xảy ra lỗi:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                #SPAM TIN NHẮN GALI 
                        if inPuTMsG.strip().startswith('/gali '):
                            print('Đang xử lý lệnh /gali')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ LỖI! Cách dùng:\n"
                                        "/gali <tên>\n"
                                        "Ví dụ: /gali người_ghét"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    name = parts[1].strip()

                                    messages = [
                                        "{Name} TƐRI SƐXY BHEN KI CHXT ME ME L0DA DAAL KAR RAAT BHAR JOR JOR SE CH0DUNGA",
                                        "{Name} MADHERXHOD TƐRI MÁÁ KI KALI G4ND MƐ LÀND MARU",
                                        "{Name} TƐRI BHƐN KI TIGHT CHXT KO 5G KI SPEED SE CHÒD DU",
                                        "{Name} TƐRI BEHEN KI CHXT ME L4ND MARU",
                                        "{Name} TƐRI MÁÁ KI CHXT 360 BAR",
                                        "{Name} TƐRI BƐHƐN KI CHXT 720 BAR",
                                        "{Name} BEHEN KE L0DE",
                                        "{Name} MADARCHXD",
                                        "{Name} BETE TƐRA BAAP HUN ME",
                                        "{Name} G4NDU APNE BAAP KO H8 DEGA",
                                        "{Name} KI MÀÀ KI CHXT PER NIGHT 4000",
                                        "{Name} KI BƐHƐN KI CHXT PER NIGHT 8000",
                                        "{Name} R4NDI KE BACHHƐ APNE BAP KO H8 DEGA",
                                        "INDIA KA NO-1 G4NDU {Name}",
                                        "{Name} CHAPAL CH0R",
                                        "{Name} TƐRI MÀÀ KO GB ROAD PE BETHA KE CHXDUNGA",
                                        "{Name} BETA JHULA JHUL APNE BAAP KO MAT BHUL"
            ]

                                    # Gửi từng tin nhắn một với màu ngẫu nhiên
                                    for msg in messages:
                                        colored_message = f"[B][C]{get_random_color()} {msg.replace('{Name}', name.upper())}"
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Đã xảy ra lỗi:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                #TÊN NGƯỜI DÙNG INSTA ĐẾN THÔNG TIN-/ig
                        if inPuTMsG.strip().startswith('/ig '):
                            print('Đang xử lý lệnh insta trong bất kỳ loại chat nào')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /ig <tên_người_dùng>\nVí dụ: /ig virat.kohli\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_username = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nĐang lấy thông tin Instagram cho {target_username}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
        # Sử dụng ThreadPoolExecutor để tránh chặn vòng lặp async
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    insta_result = await loop.run_in_executor(executor, send_insta_info, target_username)
        
                                await safe_send_message(response.Data.chat_type, insta_result, uid, chat_id, key, iv)
                                #LẤY TIỂU SỬ NGƯỜI CHƠI-/bio
                        if inPuTMsG.strip().startswith('/bio '):
                            print('Đang xử lý lệnh bio trong bất kỳ loại chat nào')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /bio <uid>\nVí dụ: /bio 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nĐang lấy tiểu sử người chơi...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                                # Sử dụng ThreadPoolExecutor để tránh chặn vòng lặp async
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    bio_result = await loop.run_in_executor(executor, get_player_bio, target_uid)

                                await safe_send_message(response.Data.chat_type, f"[B][C]{get_random_color()}\n{bio_result}", uid, chat_id, key, iv)

                        # LỆNH TẤN CÔNG EMOTE NHANH - /quick [team_code] [emote_id] [target_uid?]
                        if inPuTMsG.strip().startswith('/quick'):
                            print('Đang xử lý lệnh tấn công emote nhanh')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /quick (mã_đội) [id_emote] [uid_mục_tiêu]\n\n[FFFFFF]Ví dụ:\n[00FF00]/quick ABC123[FFFFFF] - Tham gia, gửi Rings emote, rời\n[00FF00]/ghostquick ABC123[FFFFFF] - Ghost tham gia, gửi emote, rời\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
        
                                # Đặt giá trị mặc định
                                emote_id = parts[0]
                                target_uid = str(response.Data.uid)  # Mặc định: UID người gửi
        
                                # Phân tích tham số tùy chọn
                                if len(parts) >= 3:
                                    emote_id = parts[2]
                                if len(parts) >= 4:
                                    target_uid = parts[3]
        
                                # Xác định tên mục tiêu cho tin nhắn
                                if target_uid == str(response.Data.uid):
                                    target_name = "Chính bạn"
                                else:
                                    target_name = f"UID {target_uid}"
        
                                initial_message = f"[B][C][FFFF00]⚡ TẤN CÔNG EMOTE NHANH!\n\n[FFFFFF]🎯 Đội: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Mục tiêu: [00FF00]{target_name}\n[FFFFFF]⏱️ Ước tính: [00FF00]2 giây\n\n[FFFF00]Đang thực thi chuỗi...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Thử phương pháp thông thường trước
                                    success, result = await ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region)
            
                                    if success:
                                        success_message = f"[B][C][00FF00]✅ TẤN CÔNG NHANH THÀNH CÔNG!\n\n[FFFFFF]🏷️ Đội: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Mục tiêu: [00FF00]{target_name}\n\n[00FF00]Bot đã tham gia → emoted → rời! ✅\n"
                                    else:
                                        success_message = f"[B][C][FF0000]❌ Tấn công thông thường thất bại: {result}\n"
                                    
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print("thất bại")
            
            
                        # Lệnh Mời - /inv (tạo nhóm 5 người chơi và gửi yêu cầu)
                        if inPuTMsG.strip().startswith('/inv '):
                            print('Đang xử lý lệnh mời trong bất kỳ loại chat nào')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /inv (uid)\nVí dụ: /inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nĐang tạo Nhóm 5 Người chơi và gửi yêu cầu đến {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Tạo đội nhanh và mời cho 5 người chơi
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                    
                                    C = await cHSq(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                                    await asyncio.sleep(0.3)
                                    
                                    V = await SEnd_InV(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                                    await asyncio.sleep(0.3)
                                    
                                    E = await ExiT(None, key, iv)
                                    await asyncio.sleep(2)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                                    
                                    # THÔNG BÁO THÀNH CÔNG
                                    success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Lời mời Nhóm 5 Người chơi đã được gửi thành công đến {target_uid}!\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ LỖI gửi lời mời: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/6")):
                            # Xử lý lệnh /6 - Tạo nhóm 4 người chơi
                            initial_message = f"[B][C]{get_random_color()}\n\nĐang tạo Nhóm 6 Người chơi...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Tạo đội nhanh và mời cho 4 người chơi
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # THÔNG BÁO THÀNH CÔNG
                            success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Lời mời Nhóm 6 Người chơi đã được gửi thành công đến {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/3")):
                            # Xử lý lệnh /3 - Tạo nhóm 3 người chơi
                            initial_message = f"[B][C]{get_random_color()}\n\nĐang tạo Nhóm 3 Người chơi...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Tạo đội nhanh và mời cho 6 người chơi
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # THÔNG BÁO THÀNH CÔNG
                            success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Lời mời Nhóm 6 Người chơi đã được gửi thành công đến {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/roommsg'):
                            print('Đang xử lý lệnh tin nhắn phòng')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Cách dùng: /roommsg (id_phòng) (tin_nhắn)\nVí dụ: /roommsg 489775386 Xin chào phòng!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                message = " ".join(parts[2:])
        
                                initial_msg = f"[B][C][00FF00]📢 Đang gửi đến phòng {room_id}: {message}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Lấy UID bot
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else 13699776666
            
                                    # Gửi chat phòng sử dụng cấu trúc gói tin bị rò rỉ
                                    room_chat_packet = await send_room_chat_enhanced(message, room_id, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', room_chat_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Đã gửi tin nhắn đến phòng {room_id}!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"✅ Đã gửi tin nhắn phòng đến {room_id}: {message}")
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Thất bại: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith(("/5")):
                            # Xử lý lệnh /5 trong bất kỳ loại chat nào
                            initial_message = f"[B][C]{get_random_color()}\n\nĐang gửi Lời Mời Nhóm...\n\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            # Tạo đội nhanh và mời
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Giảm độ trễ
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Giảm độ trễ
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)  # Giảm từ 3 giây
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                            # THÔNG BÁO THÀNH CÔNG
                            success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Lời mời nhóm đã được gửi thành công đến {uid}!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip() == "/admin":
                            # Xử lý lệnh /admin trong bất kỳ loại chat nào
                            admin_message = """
[C][B][FF0000]╔══════════╗
[FFFFFF]✨ theo dõi trên Instagram   
[FFFFFF]          ⚡ ROSHAN CODEX ❤️  
[FFFFFF]                   cảm ơn vì đã hỗ trợ 
[FF0000]╠══════════╣
[FFD700]⚡ CHỦ SỞ HỮU : [FFFFFF]ROSHAN CODEX    
[FFD700]✨ Tên trên instagram : [FFFFFF] THEROSHANCODEX07
[FF0000]╚══════════╝
[FFD700]✨ Nhà phát triển —͟͞͞ </> THE ROSHAN CODEX ❄️  ⚡
"""
                            await safe_send_message(response.Data.chat_type, admin_message, uid, chat_id, key, iv)

                        # Thêm phần này với các trình xử lý lệnh khác trong hàm TcPChaT
                        if inPuTMsG.strip().startswith('/multijoin'):
                            print('Đang xử lý yêu cầu tham gia đa tài khoản')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Cách dùng: /multijoin (uid_mục_tiêu)\nVí dụ: /multijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ Vui lòng nhập ID người chơi hợp lệ!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                initial_msg = f"[B][C][00FF00]🚀 Đang bắt đầu tấn công tham gia đa tài khoản trên {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Thử phương pháp đa tài khoản giả (đáng tin cậy hơn)
                                    success_count, total_attempts = await real_multi_account_join(target_uid, key, iv, region)
            
                                    if success_count > 0:
                                        result_msg = f"""
[B][C][00FF00]✅ TẤN CÔNG THAM GIA ĐA TÀI KHOẢN ĐÃ HOÀN THÀNH!

🎯 Mục tiêu: {target_uid}
✅ Yêu cầu Thành công: {success_count}
📊 Tổng Lần Thử: {total_attempts}
⚡ Đã gửi các biến thể đội khác nhau!

💡 Kiểm tra trò chơi của bạn để xem yêu cầu tham gia!
"""
                                    else:
                                        result_msg = f"[B][C][FF0000]❌ Tất cả yêu cầu tham gia thất bại! Kiểm tra kết nối bot.\n"
            
                                    await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Lỗi tham gia đa tài khoản: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

           
                        if inPuTMsG.strip().startswith('/fastmultijoin'):
                            print('Đang xử lý spam tham gia đa tài khoản nhanh')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /fastmultijoin (uid)\nVí dụ: /fastmultijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Tải tài khoản
                                accounts_data = load_accounts()
                                if not accounts_data:
                                    error_msg = f"[B][C][FF0000]❌ LỖI! Không tìm thấy tài khoản!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
                                
                                initial_msg = f"[B][C][00FF00]⚡ SPAM THAM GIA ĐA TÀI KHOẢN NHANH!\n🎯 Mục tiêu: {target_uid}\n👥 Tài khoản: {len(accounts_data)}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    join_count = 0
                                    # Gửi yêu cầu tham gia nhanh chóng từ tất cả tài khoản
                                    for uid, password in accounts_data.items():
                                        try:
                                            # Sử dụng hàm yêu cầu tham gia hiện có của bạn
                                            join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                            join_count += 1
                                            print(f"✅ Tham gia nhanh từ tài khoản {uid}")
                    
                                            # Độ trễ rất ngắn
                                            await asyncio.sleep(0.1)
                    
                                        except Exception as e:
                                            print(f"❌ Tham gia nhanh thất bại cho {uid}: {e}")
                                            continue
            
                                    success_msg = f"[B][C][00FF00]✅ THAM GIA ĐA TÀI KHOẢN NHANH ĐÃ HOÀN THÀNH!\n🎯 Mục tiêu: {target_uid}\n✅ Thành công: {join_count}/{len(accounts_data)}\n⚡ Tốc độ: Siêu nhanh\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ LỖI trong tham gia đa tài khoản nhanh: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
           

                        # Cập nhật trình xử lý lệnh
                        if inPuTMsG.strip().startswith('/reject'):
                            print('Đang xử lý lệnh spam reject trong bất kỳ loại chat nào')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /reject (uid_mục_tiêu)\nVí dụ: /reject 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Dừng bất kỳ spam reject hiện có nào
                                if reject_spam_task and not reject_spam_task.done():
                                    reject_spam_running = False
                                    reject_spam_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Gửi tin nhắn bắt đầu
                                start_msg = f"[B][C][1E90FF]🌀 Đã bắt đầu Spam Reject trên: {target_uid}\n🌀 Gói tin: 150 mỗi loại\n🌀 Khoảng cách: 0.2 giây\n"
                                await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
        
                                # Bắt đầu spam reject trong nền
                                reject_spam_running = True
                                reject_spam_task = asyncio.create_task(reject_spam_loop(target_uid, key, iv))
        
                                # Chờ hoàn thành trong nền và gửi tin nhắn hoàn thành
                                asyncio.create_task(handle_reject_completion(reject_spam_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv))


                        if inPuTMsG.strip() == '/reject_stop':
                            if reject_spam_task and not reject_spam_task.done():
                                reject_spam_running = False
                                reject_spam_task.cancel()
                                stop_msg = f"[B][C][00FF00]✅ Spam reject đã dừng thành công!\n"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ Không có spam reject nào đang hoạt động để dừng!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                                    
                                                                        
                        # Trong trình xử lý lệnh nơi bạn gọi Room_Spam:
                        if inPuTMsG.strip().startswith('/room'):
                            print('Đang xử lý lệnh spam phòng nâng cao')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /room (uid)\nVí dụ: /room 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                room_id = parts[2]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ LỖI! Vui lòng nhập ID người chơi hợp lệ!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                # Gửi tin nhắn ban đầu
                                initial_msg = f"[B][C][00FF00]🔍 Đang thực hiện spam phòng cho {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                
                                try:
                                    # Phương pháp 1: Thử lấy ID phòng từ các gói tin gần đây
                                
                                    

                                    room_msg = f"[B][C][00FF00]🎯 Đã phát hiện người chơi trong phòng {room_id}\n"
                                    await safe_send_message(response.Data.chat_type, room_msg, uid, chat_id, key, iv)
            
                                    # Tạo gói tin spam
                                    spam_packet = await Room_Spam(target_uid, room_id, "ROSHAN", key, iv)
            
                                    # Gửi 99 gói tin spam nhanh chóng (giống TCP khác của bạn)
                                    spam_count = 99
                                    
                                    start_msg = f"[B][C][00FF00]🚀 Đang bắt đầu spam: {spam_count} gói tin đến phòng {room_id}\n"
                                    await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
            
                                    for i in range(spam_count):
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
                
                                        # Cập nhật tiến độ
                                        if (i + 1) % 25 == 0:
                                            progress_msg = f"[B][C][00FF00]📦 Tiến độ: {i+1}/{spam_count} gói tin đã gửi\n"
                                            await safe_send_message(response.Data.chat_type, progress_msg, uid, chat_id, key, iv)
                                            print(f"Tiến độ spam phòng: {i+1}/{spam_count} đến UID: {target_uid}")
                
                                        # Độ trễ rất ngắn (0.05 giây = 50ms)
                                        await asyncio.sleep(0.05)
            
                                    # Tin nhắn thành công cuối cùng
                                    success_msg = f"[B][C][00FF00]✅ SPAM PHÒNG ĐÃ HOÀN THÀNH!\n🎯 Mục tiêu: {target_uid}\n📦 Gói tin: {spam_count}\n🏠 Phòng: {room_id}\n⚡ Tốc độ: Siêu nhanh\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"Spam phòng hoàn thành cho UID: {target_uid}")
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ LỖI trong spam phòng: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    print(f"Lỗi spam phòng: {e}")          
                                    
                                    
                        # Trình xử lý lệnh riêng cho /s1 đến /s5
                        if inPuTMsG.strip().startswith('/s1'):
                            await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
    
                        if inPuTMsG.strip().startswith('/s2'):
                            await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s3'):
                            await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s4'):
                            await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s5'):
                            await handle_badge_command('s5', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                            
                            #SPAM YÊU CẦU TẤT CẢ HUY HIỆU 
                        if inPuTMsG.strip().startswith('/spam'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]❌ Cách dùng: /spam <uid>\nVí dụ: /spam 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                total_requests = 10  # tổng yêu cầu tham gia
                                sequence = ['s1', 's2', 's3', 's4', 's5']  # tất cả lệnh huy hiệu

                                # Gửi tin nhắn ban đầu hợp nhất
                                initial_msg = f"[B][C][1E90FF]🌀 Đã nhận yêu cầu! Đang chuẩn bị spam {target_uid} với tất cả huy hiệu...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)

                                count = 0
                                while count < total_requests:
                                    for cmd in sequence:
                                        if count >= total_requests:
                                            break
                                        # Xây dựng chuỗi lệnh giả như "/s1 123456789"
                                        fake_command = f"/{cmd} {target_uid}"
                                        await handle_badge_command(cmd, fake_command, uid, chat_id, key, iv, region, response.Data.chat_type)
                                        count += 1

                                # Tin nhắn thành công sau tất cả 30 yêu cầu
                                success_msg = f"[B][C][00FF00]✅ Đã gửi thành công {total_requests} Yêu cầu Tham gia!\n🎯 Mục tiêu: {target_uid}\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                                    
                                                                                             #THAM GIA PHÒNG       
                        if inPuTMsG.strip().startswith('/joinroom'):
                            print('Đang xử lý lệnh tham gia phòng tùy chỉnh')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Cách dùng: /joinroom (id_phòng) (mật_khẩu)\nVí dụ: /joinroom 123456 0000\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                room_password = parts[2]
        
                                initial_msg = f"[B][C][00FF00]🚀 Đang tham gia phòng tùy chỉnh...\n🏠 Phòng: {room_id}\n🔑 Mật khẩu: {room_password}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Tham gia phòng tùy chỉnh
                                    join_packet = await join_custom_room(room_id, room_password, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Đã tham gia phòng tùy chỉnh {room_id}!\n🤖 Bot giờ đang trong chat phòng!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Không thể tham gia phòng: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/createroom'):
                            print('Đang xử lý tạo phòng tùy chỉnh')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Cách dùng: /createroom (tên_phòng) (mật_khẩu) [người_chơi=4]\nVí dụ: /createroom BOTROOM 0000 4\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_name = parts[1]
                                room_password = parts[2]
                                max_players = parts[3] if len(parts) > 3 else "4"
        
                                initial_msg = f"[B][C][00FF00]🏠 Đang tạo phòng tùy chỉnh...\n📛 Tên: {room_name}\n🔑 Mật khẩu: {room_password}\n👥 Số Người chơi Tối đa: {max_players}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Tạo phòng tùy chỉnh
                                    create_packet = await create_custom_room(room_name, room_password, int(max_players), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', create_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Phòng tùy chỉnh đã được tạo!\n🏠 Phòng: {room_name}\n🔑 Mật khẩu: {room_password}\n👥 Tối đa: {max_players}\n🤖 Bot đang làm chủ phòng!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Không thể tạo phòng: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)                                                                                                                                                                                                               
                                                
                                              
                                                                                          # LỆNH THAM GIA ĐÃ SỬA
                        if inPuTMsG.startswith('/join'):
                            # Xử lý lệnh /join trong bất kỳ loại chat nào
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /join (mã_đội)\nVí dụ: /join ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                sender_uid = response.Data.uid  # Lấy UID của người gửi lệnh
        
                                initial_message = f"[B][C]{get_random_color()}\nĐang tham gia đội với mã: {CodE}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Thử sử dụng phương pháp tham gia thông thường trước
                                    EM = await GenJoinSquadsPacket(CodE, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
            
                                    # Chờ một chút để việc tham gia hoàn thành
                                    await asyncio.sleep(2)
            
                                    # DUAL RINGS EMOTE - CẢ NGƯỜI GỬI VÀ BOT
                                    try:
                                        await auto_rings_emote_dual(sender_uid, key, iv, region)
                                    except Exception as emote_error:
                                        print(f"Dual emote thất bại nhưng tham gia thành công: {emote_error}")
            
                                    # THÔNG BÁO THÀNH CÔNG
                                    success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Đã tham gia đội: {CodE}!\n💍 Dual Rings emote đã kích hoạt!\n🤖 Bot + Bạn = 💕\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print(f"Tham gia thông thường thất bại, đang thử ghost join: {e}")
                                    # Nếu tham gia thông thường thất bại, thử ghost join
                                    try:
                                        # Lấy UID bot từ ngữ cảnh toàn cục hoặc dữ liệu đăng nhập
                                        bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else TarGeT
                
                                        ghost_packet = await ghost_join_packet(bot_uid, CodE, key, iv)
                                        if ghost_packet:
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                    
                                            # Chờ một chút để ghost join hoàn thành
                                            await asyncio.sleep(2)
                    
                                            # DUAL RINGS EMOTE - CẢ NGƯỜI GỬI VÀ BOT
                                            try:
                                                await auto_rings_emote_dual(sender_uid, key, iv, region)
                                            except Exception as emote_error:
                                                print(f"Dual emote thất bại nhưng ghost join thành công: {emote_error}")
                    
                                            success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Đã ghost tham gia đội: {CodE}!\n💍 Dual Rings emote đã kích hoạt!\n🤖 Bot + Bạn = 💕\n"
                                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                        else:
                                            error_msg = f"[B][C][FF0000]❌ LỖI! Không thể tạo gói tin ghost join.\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                    
                                    except Exception as ghost_error:
                                        print(f"Ghost join cũng thất bại: {ghost_error}")
                                        error_msg = f"[B][C][FF0000]❌ LỖI! Không thể tham gia đội: {str(ghost_error)}\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                
                        if inPuTMsG.strip().startswith('/ghost'):
                            # Xử lý lệnh /ghost trong bất kỳ loại chat nào
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /ghost (mã_đội)\nVí dụ: /ghost ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nĐang ghost tham gia đội với mã: {CodE}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Lấy UID bot từ ngữ cảnh toàn cục hoặc dữ liệu đăng nhập
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else TarGeT
                                    
                                    ghost_packet = await ghost_join_packet(bot_uid, CodE, key, iv)
                                    if ghost_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                        success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Đã ghost tham gia đội với mã: {CodE}!\n"
                                        await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ LỖI! Không thể tạo gói tin ghost join.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ LỖI! Ghost join thất bại: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # LỆNH LAG MỚI
                        if inPuTMsG.strip().startswith('/lag '):
                            print('Đang xử lý lệnh lag trong bất kỳ loại chat nào')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /lag (mã_đội)\nVí dụ: /lag ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                
                                # Dừng bất kỳ tác vụ lag hiện có nào
                                if lag_task and not lag_task.done():
                                    lag_running = False
                                    lag_task.cancel()
                                    await asyncio.sleep(0.1)
                                
                                # Bắt đầu tác vụ lag mới
                                lag_running = True
                                lag_task = asyncio.create_task(lag_team_loop(team_code, key, iv, region))
                                
                                # THÔNG BÁO THÀNH CÔNG
                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Tấn công lag đã bắt đầu!\nĐội: {team_code}\nHành động: Tham gia/rời nhanh\nTốc độ: Siêu nhanh (mili giây)\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # LỆNH DỪNG LAG
                        if inPuTMsG.strip() == '/stop lag':
                            if lag_task and not lag_task.done():
                                lag_running = False
                                lag_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Tấn công lag đã dừng thành công!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Không có tấn công lag nào đang hoạt động để dừng!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.startswith('/exit'):
                            # Xử lý lệnh /exit trong bất kỳ loại chat nào
                            initial_message = f"[B][C]{get_random_color()}\nĐang rời đội hiện tại...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)
                            
                            # THÔNG BÁO THÀNH CÔNG
                            success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Đã rời đội thành công!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/start'):
                            # Xử lý lệnh /start trong bất kỳ loại chat nào
                            initial_message = f"[B][C]{get_random_color()}\nĐang bắt đầu trận đấu...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
                            
                            # THÔNG BÁO THÀNH CÔNG
                            success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Lệnh bắt đầu trận đấu đã được gửi!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/title'):
                            # Xử lý lệnh /title trong bất kỳ loại chat nào
                            parts = inPuTMsG.strip().split()
    
                            # Kiểm tra xem bot có trong đội không
              
                            initial_message = f"[B][C]{get_random_color()}\nĐang gửi tiêu đề đến đội hiện tại...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
    
                            try:
                                # Gửi gói tin tiêu đề
                                title_packet = await send_title_msg(chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', title_packet)
        
                                # THÔNG BÁO THÀNH CÔNG
                                success_message = f"[B][C][00FF00]✅ THÀNH CÔNG! Đã gửi tiêu đề đến đội hiện tại!\n"
                                await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
        
                            except Exception as e:
                                print(f"Gửi tiêu đề thất bại: {e}")
                                error_msg = f"[B][C][FF0000]❌ LỖI! Không thể gửi tiêu đề: {str(e)}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Lệnh Emote - hoạt động trong tất cả loại chat
                        if inPuTMsG.strip().startswith('/e'):
                            print(f'Đang xử lý lệnh emote trong loại chat: {response.Data.chat_type}')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /e (uid) (id_emote)\nVí dụ: /e 123456789 909000001\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
                                
                            initial_message = f'[B][C]{get_random_color()}\nĐang gửi emote đến mục tiêu...\n'
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                            uid2 = uid3 = uid4 = uid5 = None
                            s = False
                            target_uids = []

                            try:
                                target_uid = int(parts[1])
                                target_uids.append(target_uid)
                                uid2 = int(parts[2]) if len(parts) > 2 else None
                                if uid2: target_uids.append(uid2)
                                uid3 = int(parts[3]) if len(parts) > 3 else None
                                if uid3: target_uids.append(uid3)
                                uid4 = int(parts[4]) if len(parts) > 4 else None
                                if uid4: target_uids.append(uid4)
                                uid5 = int(parts[5]) if len(parts) > 5 else None
                                if uid5: target_uids.append(uid5)
                                idT = int(parts[-1])  # Phần cuối cùng là ID emote

                            except ValueError as ve:
                                print("ValueError:", ve)
                                s = True
                            except Exception as e:
                                print(f"Lỗi phân tích lệnh emote: {e}")
                                s = True

                            if not s:
                                try:
                                    for target in target_uids:
                                        H = await Emote_k(target, idT, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        await asyncio.sleep(0.1)
                                    
                                    # THÔNG BÁO THÀNH CÔNG
                                    success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Đã gửi emote {idT} đến {len(target_uids)} người chơi!\nMục tiêu: {', '.join(map(str, target_uids))}\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ LỖI gửi emote: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng UID không hợp lệ. Cách dùng: /e (uid) (id_emote)\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                

                        # LỆNH BẮT ĐẦU CHU KỲ EVO - /evos
                        if inPuTMsG.strip().startswith('/evo'):
                            print('Đang xử lý lệnh bắt đầu chu kỳ evo trong bất kỳ loại chat nào')
    
                            parts = inPuTMsG.strip().split()
                            uids = []
    
                            # Luôn sử dụng UID của người gửi (người đã gõ /evos)
                            sender_uid = str(response.Data.uid)
                            uids.append(sender_uid)
                            print(f"Đang sử dụng UID người gửi: {sender_uid}")
    
                            # Tùy chọn: Cũng cho phép chỉ định thêm UID
                            if len(parts) > 1:
                                for part in parts[1:]:  # Bỏ phần đầu tiên là "/evos"
                                    if part.isdigit() and len(part) >= 7 and part != sender_uid:  # UID thường có 7+ chữ số
                                        uids.append(part)
                                        print(f"Đã thêm UID bổ sung: {part}")

                            # Dừng bất kỳ chu kỳ evo hiện có nào
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                await asyncio.sleep(0.5)
    
                            # Bắt đầu chu kỳ evo mới
                            evo_cycle_running = True
                            evo_cycle_task = asyncio.create_task(evo_cycle_spam(uids, key, iv, region))
    
                            # THÔNG BÁO THÀNH CÔNG
                            if len(uids) == 1:
                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Chu kỳ evolution emote đã bắt đầu!\n🎯 Mục tiêu: Chính bạn\n🎭 Emotes: Tất cả 18 evolution emotes\n⏰ Độ trễ: 5 giây giữa các emote\n🔄 Chu kỳ: Vòng lặp liên tục cho đến /sevos\n"
                            else:
                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Chu kỳ evolution emote đã bắt đầu!\n🎯 Mục tiêu: Chính bạn + {len(uids)-1} người chơi khác\n🎭 Emotes: Tất cả 18 evolution emotes\n⏰ Độ trễ: 5 giây giữa các emote\n🔄 Chu kỳ: Vòng lặp liên tục cho đến /sevos\n"
    
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            print(f"Đã bắt đầu chu kỳ evolution emote cho UID: {uids}")
                        
                        # LỆNH DỪNG CHU KỲ EVO - /sevos
                        if inPuTMsG.strip() == '/sevos':
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Chu kỳ evolution emote đã dừng thành công!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                print("Chu kỳ evolution emote đã dừng theo lệnh")
                            else:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Không có chu kỳ evolution emote nào đang hoạt động để dừng!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Lệnh spam emote nhanh - hoạt động trong tất cả loại chat
                        if inPuTMsG.strip().startswith('/fast'):
                            print('Đang xử lý spam emote nhanh trong bất kỳ loại chat nào')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /fast uid1 [uid2] [uid3] [uid4] id_emote\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Phân tích uid và id_emote
                                uids = []
                                emote_id = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) > 3:  # Giả sử UID dài hơn 3 chữ số
                                            uids.append(part)
                                        else:
                                            emote_id = part
                                    else:
                                        break
                                
                                if not emote_id and parts[-1].isdigit():
                                    emote_id = parts[-1]
                                
                                if not uids or not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng không hợp lệ! Cách dùng: /fast uid1 [uid2] [uid3] [uid4] id_emote\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    # Dừng bất kỳ spam nhanh hiện có nào
                                    if fast_spam_task and not fast_spam_task.done():
                                        fast_spam_running = False
                                        fast_spam_task.cancel()
                                    
                                    # Bắt đầu spam nhanh mới
                                    fast_spam_running = True
                                    fast_spam_task = asyncio.create_task(fast_emote_spam(uids, emote_id, key, iv, region))
                                    
                                    # THÔNG BÁO THÀNH CÔNG
                                    success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Spam emote nhanh đã bắt đầu!\nMục tiêu: {len(uids)} người chơi\nEmote: {emote_id}\nSố lần spam: 25 lần\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Lệnh spam emote tùy chỉnh - hoạt động trong tất cả loại chat
                        if inPuTMsG.strip().startswith('/p'):
                            print('Đang xử lý spam emote tùy chỉnh trong bất kỳ loại chat nào')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /p (uid) (id_emote) (số_lần)\nVí dụ: /p 123456789 909000001 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    emote_id = parts[2]
                                    times = int(parts[3])
                                    
                                    if times <= 0:
                                        error_msg = f"[B][C][FF0000]❌ LỖI! Số lần phải lớn hơn 0!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    elif times > 100:
                                        error_msg = f"[B][C][FF0000]❌ LỖI! Tối đa 100 lần được cho phép để an toàn!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        # Dừng bất kỳ spam tùy chỉnh hiện có nào
                                        if custom_spam_task and not custom_spam_task.done():
                                            custom_spam_running = False
                                            custom_spam_task.cancel()
                                            await asyncio.sleep(0.5)
                                        
                                        # Bắt đầu spam tùy chỉnh mới
                                        custom_spam_running = True
                                        custom_spam_task = asyncio.create_task(custom_emote_spam(target_uid, emote_id, times, key, iv, region))
                                        
                                        # THÔNG BÁO THÀNH CÔNG
                                        success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Spam emote tùy chỉnh đã bắt đầu!\nMục tiêu: {target_uid}\nEmote: {emote_id}\nSố lần: {times}\n"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng số không hợp lệ! Cách dùng: /p (uid) (id_emote) (số_lần)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ LỖI! {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Lệnh spam yêu cầu - hoạt động trong tất cả loại chat
                        if inPuTMsG.strip().startswith('/spm_inv'):
                            print('Đang xử lý spam mời với trang phục')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Cách dùng: /spm_inv (uid)\nVí dụ: /spm_inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Dừng bất kỳ spam yêu cầu hiện có nào
                                if spam_request_task and not spam_request_task.done():
                                    spam_request_running = False
                                    spam_request_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Bắt đầu spam yêu cầu mới VỚI TRANG PHỤC
                                spam_request_running = True
                                spam_request_task = asyncio.create_task(spam_request_loop_with_cosmetics(target_uid, key, iv, region))
        
                                # THÔNG BÁO THÀNH CÔNG
                                success_msg = f"[B][C][00FF00]✅ SPAM CÓ TRANG PHỤC ĐÃ BẮT ĐẦU!\n🎯 Mục tiêu: {target_uid}\n📦 Yêu cầu: 30\n🎭 Tính năng: Huy hiệu V + Trang phục\n⚡ Mỗi lời mời có trang phục khác nhau!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Lệnh dừng spam yêu cầu - hoạt động trong tất cả loại chat
                        if inPuTMsG.strip() == '/stop spm_inv':
                            if spam_request_task and not spam_request_task.done():
                                spam_request_running = False
                                spam_request_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Spam yêu cầu đã dừng thành công!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Không có spam yêu cầu nào đang hoạt động để dừng!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # LỆNH EVO MỚI
                        if inPuTMsG.strip().startswith('/evo '):
                            print('Đang xử lý lệnh evo trong bất kỳ loại chat nào')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /evo uid1 [uid2] [uid3] [uid4] số(1-21)\nVí dụ: /evo 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Phân tích uid và số
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Số nên là 1-21 (1 hoặc 2 chữ số)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng không hợp lệ! Cách dùng: /evo uid1 [uid2] [uid3] [uid4] số(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ LỖI! Số phải nằm trong khoảng 1-21!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nĐang gửi evolution emote {number_int}...\n"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            
                                            success, result_msg = await evo_emote_spam(uids, number_int, key, iv, region)
                                            
                                            if success:
                                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ LỖI! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng số không hợp lệ! Chỉ sử dụng 1-21.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/evo_fast '):
                            print('Đang xử lý lệnh evo_fast trong bất kỳ loại chat nào')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /evo_fast uid1 [uid2] [uid3] [uid4] số(1-21)\nVí dụ: /evo_fast 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Phân tích uid và số
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Số nên là 1-21 (1 hoặc 2 chữ số)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng không hợp lệ! Cách dùng: /evo_fast uid1 [uid2] [uid3] [uid4] số(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ LỖI! Số phải nằm trong khoảng 1-21!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Dừng bất kỳ spam evo_fast hiện có nào
                                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                                evo_fast_spam_running = False
                                                evo_fast_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Bắt đầu spam evo_fast mới
                                            evo_fast_spam_running = True
                                            evo_fast_spam_task = asyncio.create_task(evo_fast_emote_spam(uids, number_int, key, iv, region))
                                            
                                            # THÔNG BÁO THÀNH CÔNG
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Spam evolution emote nhanh đã bắt đầu!\nMục tiêu: {len(uids)} người chơi\nEmote: {number_int} (ID: {emote_id})\nSố lần spam: 25 lần\nKhoảng cách: 0.1 giây\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng số không hợp lệ! Chỉ sử dụng 1-21.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # LỆNH EVO_CUSTOM MỚI
                        if inPuTMsG.strip().startswith('/evo_c '):
                            print('Đang xử lý lệnh evo_c trong bất kỳ loại chat nào')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Cách dùng: /evo_c uid1 [uid2] [uid3] [uid4] số(1-21) số_lần(1-100)\nVí dụ: /evo_c 123456789 1 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Phân tích uid, số, và số lần
                                uids = []
                                number = None
                                time_val = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Số hoặc thời gian nên là 1-100 (1, 2, hoặc 3 chữ số)
                                            if number is None:
                                                number = part
                                            elif time_val is None:
                                                time_val = part
                                            else:
                                                uids.append(part)
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                # Nếu vẫn không có time_val, thử lấy nó từ phần cuối
                                if not time_val and len(parts) >= 3:
                                    last_part = parts[-1]
                                    if last_part.isdigit() and len(last_part) <= 3:
                                        time_val = last_part
                                        # Xóa time_val khỏi uids nếu nó được thêm nhầm
                                        if time_val in uids:
                                            uids.remove(time_val)
                                
                                if not uids or not number or not time_val:
                                    error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng không hợp lệ! Cách dùng: /evo_c uid1 [uid2] [uid3] [uid4] số(1-21) số_lần(1-100)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        time_int = int(time_val)
                                        
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ LỖI! Số phải nằm trong khoảng 1-21!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        elif time_int < 1 or time_int > 100:
                                            error_msg = f"[B][C][FF0000]❌ LỖI! Số lần phải nằm trong khoảng 1-100!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Dừng bất kỳ spam evo_custom hiện có nào
                                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                                evo_custom_spam_running = False
                                                evo_custom_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Bắt đầu spam evo_custom mới
                                            evo_custom_spam_running = True
                                            evo_custom_spam_task = asyncio.create_task(evo_custom_emote_spam(uids, number_int, time_int, key, iv, region))
                                            
                                            # THÔNG BÁO THÀNH CÔNG
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Spam evolution emote tùy chỉnh đã bắt đầu!\nMục tiêu: {len(uids)} người chơi\nEmote: {number_int} (ID: {emote_id})\nLặp lại: {time_int} lần\nKhoảng cách: 0.1 giây\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ LỖI! Định dạng số/số_lần không hợp lệ! Chỉ sử dụng số.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Lệnh dừng spam evo_fast
                        if inPuTMsG.strip() == '/stop evo_fast':
                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                evo_fast_spam_running = False
                                evo_fast_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Spam evolution nhanh đã dừng thành công!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Không có spam evolution nhanh nào đang hoạt động để dừng!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Lệnh dừng spam evo_custom
                        if inPuTMsG.strip() == '/stop evo_c':
                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                evo_custom_spam_running = False
                                evo_custom_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ THÀNH CÔNG! Spam evolution tùy chỉnh đã dừng thành công!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ LỖI! Không có spam evolution tùy chỉnh nào đang hoạt động để dừng!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

# HỆ THỐNG MENU TRỢ GIÚP KIỂU CÂY ĐƯỢC CẢI THIỆN (Các lệnh trong menu gốc của chúng) 🌳
                        if inPuTMsG.strip().lower() in ("help", "/help", "menu", "/menu", "commands"):
                            print(f"Phát hiện lệnh trợ giúp từ UID: {uid} trong loại chat: {response.Data.chat_type}")

                            # Đầu trang
                            header = f"[b][c]{get_random_color()}Chào Người Dùng Chào Mừng Đến Với ROSHAN ˣ ʙᴏᴛ"
                            await safe_send_message(response.Data.chat_type, header, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Lệnh Nhóm ─────
                            group_commands = """[C][B][FFD700]═══⚡ LỆNH NHÓM ⚡═══[00FFFF][B]
├─ [00FFFF]Tạo Nhóm 3 Người chơi
│  └─ [FF69B4]/3
├─ [00FFFF]Tạo Nhóm 5 Người chơi
│  └─ [FF69B4]/5
├─ [00FFFF]Tạo Nhóm 6 Người chơi
│  └─ [FF69B4]/6
├─ [00FFFF]Mời Người chơi
│  └─ [FF69B4]/inv [uid]
├─ [00FFFF]Tham gia Đội
│  └─ [FF69B4]/join [mã_đội]
├─ [00FFFF]Rời Nhóm
│  └─ [FF69B4]/exit
└─ [00FFFF]Bắt đầu Trận đấu
   └─ [FF69B4]/start
[00FFFF]━━━━━━━━━━━━[FF69B4]"""
                            await safe_send_message(response.Data.chat_type, group_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Lệnh Nâng Cao ─────
                            advanced_commands = """[C][B][800080]═══⚡ LỆNH NÂNG CAO ⚡═══[FF1493][B]
├─ [FF1493]Spam Mời (30x)
│  └─ [BA55D3]/spm_inv [uid]
├─ [FF1493]Dừng Spam Mời
│  └─ [BA55D3]/stop spm_inv
├─ [FF1493]Ghost Tham gia Đội
│  └─ [BA55D3]/ghost [mã]
├─ [FF1493]Tấn công Lag Đội
│  └─ [BA55D3]/lag [mã]
├─ [FF1493]Dừng Tấn công Lag
│  └─ [BA55D3]/stop lag
└─ [FF1493]Spam Reject
   └─ [BA55D3]/reject [uid]
[FF1493]━━━━━━━━━━━━[BA55D3]"""
                            await safe_send_message(response.Data.chat_type, advanced_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Lệnh Emote ─────
                            emote_commands = """[C][B][32CD32]═══⚡ LỆNH EMOTE ⚡═══[7CFC00][B]
├─ [7CFC00]Gửi Emote Đơn
│  └─ [32CD32]/e [uid] [id]
├─ [7CFC00]Emote Nhanh (25x)
│  └─ [32CD32]/fast [uid] [id]
└─ [7CFC00]Emote Tùy Chỉnh (X lần)
   └─ [32CD32]/p [uid] [id] [x]
[7CFC00]━━━━━━━━━━━━[32CD32]"""
                            await safe_send_message(response.Data.chat_type, emote_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Lệnh Evolution Emote ─────
                            evo_commands = """[C][B][FFA500]═══⚡ EVOLUTION EMOTES ⚡═══[FF6347][B]
├─ [FF6347]Gửi Evolution Emote
│  └─ [FFA500]/evo [uid] [1-21]
├─ [FF6347]Evo Nhanh (25x)
│  └─ [FFA500]/evo_fast [uid] [1-21]
├─ [FF6347]Evo Tùy Chỉnh (X lần)
│  └─ [FFA500]/evo_c [uid] [1-21] [x]
├─ [FF6347]Tự Động Chu Kỳ Tất Cả Evo Emote
│  └─ [FFA500]/evos [uid]
└─ [FF6347]Dừng Chu Kỳ Evo Emote
   └─ [FFA500]/sevos
[FF6347]━━━━━━━━━━━━[FFA500]"""
                            await safe_send_message(response.Data.chat_type, evo_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Lệnh AI & Tiện Ích ─────
                            ai_commands = """[C][B][1E90FF]═══⚡ CÔNG CỤ & LỆNH VUI ⚡═══[00CED1][B]
├─ [00CED1]Lấy tiểu sử người chơi theo uid
│  └─ [1E90FF]/bio [uid]
├─ [00CED1]Lấy thông tin người dùng Instagram
│  └─ [1E90FF]/ig [tên_người_dùng]
├─ [00CED1]Gửi tin nhắn spam tùy chỉnh
│  └─ [1E90FF]/ms <văn_bản>
├─ [00CED1]Hỏi AI Bất cứ điều gì
│  └─ [1E90FF]/ai [câu_hỏi]
├─ [00CED1]Thông tin Quản trị viên
│  └─ [1E90FF]/admin
└─ [00CED1]Kiểm tra Trạng thái Bot
   └─ [1E90FF]/status
[00CED1]━━━━━━━━━━━━[1E90FF]"""
                            await safe_send_message(response.Data.chat_type, ai_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Lệnh Huy Hiệu ─────
                            badge_commands = """[C][B][FF4500]═══⚡ YÊU CẦU THAM GIA HUY HIỆU ⚡═══[FF69B4][B]
├─ [FF69B4]Yêu cầu Tham gia Huy hiệu Craftland
│  └─ [FF4500]/s1 [uid]
├─ [FF69B4]Yêu cầu Tham gia Huy hiệu V Mới
│  └─ [FF4500]/s2 [uid]
├─ [FF69B4]Yêu cầu Tham gia Huy hiệu Moderator
│  └─ [FF4500]/s3 [uid]
├─ [FF69B4]Yêu cầu Tham gia Huy hiệu V Nhỏ
│  └─ [FF4500]/s4 [uid]
├─ [FF69B4]Yêu cầu Tham gia Huy hiệu Pro
│  └─ [FF4500]/s5 [uid]
└─ [FF69B4]Yêu cầu Tham gia Tất cả Huy hiệu
   └─ [FF4500]/spam [uid]
[FF69B4]━━━━━━━━━━━━[FF4500]"""
                            await safe_send_message(response.Data.chat_type, badge_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            
                            footer ="""[00FFFA]╔═•══•════════════════•══•═╗
[FF1493]║ ⚡ [B][FFFF00]THÔNG TIN BOT[FFFF00][/B] ⚡
[00FFFA]║
[FFFF00]║ 👤 Nhà phát triển    :: [FF1493]ROSHAN CODEX
[32CD32]║ 💻 Trạng thái        :: [32CD32]ĐANG HOẠT ĐỘNG
[1E90FF]║ 🛠 Phiên bản      :: [1E90FF]NÂNG CẤP V2
[00FFFA]╚═•══•════════════════•══•═╝"""

    


                            await safe_send_message(response.Data.chat_type, footer, uid, chat_id, key, iv)
                        response = None
                            
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
                    
                    	
                    	
        except Exception as e: print(f"Lỗi {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)





async def MaiiiinE():
    Uid , Pw = '4231734356','69BBE0EF5291CC5F53BD8E141BB6967BBB0D85B472607DE9D60BC4B95BF53925'
    

    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: print("Lỗi - Tài Khoản Không Hợp Lệ") ; return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("Tài Khoản Mục Tiêu => Bị Cấm / Chưa Đăng Ký ! ") ; return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    # Trong hàm MaiiiinE, tìm và comment các câu lệnh print này:
    os.system('clear')
    print("🔄 Đang khởi động Kết nối TCP...")
    print("📡 Đang kết nối đến máy chủ Free Fire...")
    print("🌐 Đã thiết lập kết nối máy chủ")

    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    print("🔐 Xác thực thành công")
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: print("Lỗi - Đang Lấy Cổng Từ Dữ Liệu Đăng Nhập !") ; return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    #print(acc_name)
    
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))  

    os.system('clear')
    print("Đang khởi tạo ROSHAN Bot...")
    print("┌────────────────────────────────────┐")
    print("│ █████████████░░░░░░░░░░░░░░░░░░ │")
    print("└────────────────────────────────────┘")
    time.sleep(0.5)
    os.system('clear')
    print("Đang kết nối đến máy chủ Free Fire...")
    print("┌────────────────────────────────────┐")
    print("│ ██████████████████████░░░░░░░░░░░░ │")
    print("└────────────────────────────────────┘")
    time.sleep(0.5)
    os.system('clear')

    print("🤖 ROSHAN BOT - ĐANG HOẠT ĐỘNG")
    print("┌────────────────────────────────────┐")
    print("│ ██████████████████████████████████ │")
    print("└────────────────────────────────────┘")
    print(f"🔹 UID: {TarGeT}")
    print(f"🔹 Tên: {acc_name}")
    print(f"🔹 Trạng thái: 🟢 SẴN SÀNG")
    print("")
    print("💡 Gõ /help để xem lệnh")
    await asyncio.gather(task1, task2)
    time.sleep(0.5)
    os.system('clear')
    await ready_event.wait()
    await asyncio.sleep(1)

    os.system('clear')
    print(render('ROSHAN', colors=['white', 'green'], align='center'))
    print('')
    print("🤖 ROSHAN BOT - ĐANG HOẠT ĐỘNG")
    print(f"🔹 UID: {TarGeT}")
    print(f"🔹 Tên: {acc_name}")
    print(f"🔹 Trạng thái: 🟢 SẴN SÀNG")
    


def handle_keyboard_interrupt(signum, frame):
    """Xử lý sạch cho Ctrl+C"""
    print("\n\n🛑 Yêu cầu tắt bot...")
    print("👋 Cảm ơn bạn đã sử dụng ROSHAN ")
    sys.exit(0)

# Đăng ký trình xử lý tín hiệu
signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    
async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except KeyboardInterrupt:
            print("\n\n🛑 Bot đã tắt bởi người dùng")
            print("👋 Cảm ơn bạn đã sử dụng ROSHAN !")
            break
        except asyncio.TimeoutError: print("Token Đã Hết Hạn ! , Đang Khởi Động Lại")
        except Exception as e: print(f"Lỗi TcP - {e} => Đang Khởi Động Lại ...")

if __name__ == '__main__':
    threading.Thread(target=start_insta_api, daemon=True).start()
    asyncio.run(StarTinG())
