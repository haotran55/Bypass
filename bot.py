#Không hiểu về code xem kĩ video
import telebot
import datetime
import time
import os
import re
import subprocess
import requests
import sys
#Điền bot token của bạn
bot_token = '8025225779:AAHjpXQ9OZ3aoiv1pQn_tFQHezKDtza0Rgo'
bot = telebot.TeleBot(bot_token)
#Điền id tele của mình
processes = []
ADMIN_ID = '7658079324'

name_bot = "Bypass"

def TimeStamp():
    return str(datetime.date.today())

def get_user_file_path(user_id):
    today_day = datetime.date.today().day
    user_dir = f'./user/{today_day}'
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return f'{user_dir}/{user_id}_key.txt'

def is_key_expired(user_id):
    file_path = get_user_file_path(user_id)
    if not os.path.exists(file_path):
        return True
    with open(file_path, 'r') as f:
        timestamp = f.read().strip()
    try:
        key_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
    except ValueError:
        return True
    return (datetime.datetime.now() - key_time).days >= 1

@bot.message_handler(commands=['getkey'])
def startkey(message):
    bot.reply_to(message, text='Vui Lòng Chờ🤔')
    user_id = message.from_user.id
    if is_key_expired(user_id):
        key = "thanhdev" + str(int(user_id) * int(datetime.date.today().day) - 12666)
        key = "https://dichvukey.site/key.html?key=" + key
        api_token = ''
        url = requests.get(f'https://link4m.co/api-shorten/v2?api=662270a8632b4b42511ca862&url={api_token}&url={key}').json()
        url_key = url['shortenedUrl']
        with open(get_user_file_path(user_id), 'w') as f:
            f.write(TimeStamp())
        text = f'''
- LINK LẤY KEY {TimeStamp()} LÀ: {url_key} -
- KHI LẤY KEY XONG, DÙNG LỆNH /key <key> ĐỂ TIẾP TỤC -
        '''
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, 'Bạn Đã GetKey Rồi💤')

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Vui Lòng Nhập Key🔑')
        return

    user_id = message.from_user.id
    key = message.text.split()[1]
    expected_key = "haoesport" + str(int(user_id) * int(datetime.date.today().day) - 12666)
    
    if key == expected_key:
        bot.reply_to(message, 'Key Hợp Lệ Bạn Được Phép Dùng Lệnh /spam.')
        with open(get_user_file_path(user_id), "w") as f:
            f.write(TimeStamp())
    else:
        bot.reply_to(message, 'Key Sai Vui Lòng Kiểm Tra Lại Hoặc Lh Admin')

@bot.message_handler(commands=['superspam'])
def superspam(message):
    user_id = message.from_user.id
    if not os.path.exists(f"./vip/{user_id}.txt"):
        bot.reply_to(message, 'Đăng Kí Vip Đi Rẻ Lắm😭')
        return
    with open(f"./vip/{user_id}.txt") as fo:
        data = fo.read().split("|")
    past_date = data[0].split('-')
    past_date = datetime.date(int(past_date[0]), int(past_date[1]), int(past_date[2]))
    today_date = datetime.date.today()
    days_passed = (today_date - past_date).days
    if days_passed < 0:
        bot.reply_to(message, 'Key Vip Cài Vào ngày khác')
        return
    if days_passed >= int(data[1]):
        bot.reply_to(message, 'Key Vip Hết Hạn Mua Típ Đi😪')
        os.remove(f"./vip/{user_id}.txt")
        return
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI')
        return
    if len(message.text.split()) == 2:
        bot.reply_to(message, 'Thiếu dữ kiện !!!')
        return
    lap = message.text.split()[2]
    if lap.isnumeric():
        if not (1 <= int(lap) <= 30):
            bot.reply_to(message, "Spam Không Hợp Lệ Chỉ Spam Từ 1-30 Lần🚨")
            return
    lap = message.text.split()[2]
    if not lap.isnumeric():
        bot.reply_to(message, "Sai dữ kiện !!!")
        return
    phone_number = message.text.split()[1]
    if not re.search(r"^(?:\+84|0)(3[2-9]|5[6-9]|7[0-9]|8[0-689]|9[0-4])[0-9]{7}$", phone_number):
        bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
        return
    if phone_number in ["0528300000"]:
        bot.reply_to(message, "Spam cái đầu buồi tao huhu")
        return
    file_path = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, lap])
    processes.append(process)
    bot.reply_to(message, f'🌠 Tấn Công Thành Công 🌠 \n+ Bot 👾: smsdevsp_bot \n+ Số Tấn Công 📱: [ {phone_number} ]\n+ Lặp lại : {lap}\n+ Admin 👑: Đoàn LongThành\n+ Tiktok : DoanLongThanh_15\n+ Key : vip')

@bot.message_handler(commands=['spam'])
def spam(message):
    user_id = message.from_user.id
    current_time = time.time()
    if not bot_active:
        msg = bot.reply_to(message, 'Bot hiện đang tắt.')
        time.sleep(10)
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error deleting message: {e}")
        return
    if admin_mode and user_id not in admins:
        msg = bot.reply_to(message, 'có lẽ admin đang fix gì đó hãy đợi xíu')
    if user_id in last_usage and current_time - last_usage[user_id] < 100:
        bot.reply_to(message, f"Vui lòng đợi {100 - (current_time - last_usage[user_id]):.1f} giây trước khi sử dụng lệnh lại.")
        return

    last_usage[user_id] = current_time

    # Phân tích cú pháp lệnh
    params = message.text.split()[1:]
    if len(params) != 2:
        bot.reply_to(message, "/spam sdt số_lần như này cơ mà - vì lý do server treo bot hơi cùi nên đợi 100giây nữa dùng lại nhé")
        return

    sdt, count = params

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        return

    count = int(count)

    if count > 5:
        bot.reply_to(message, "/spam sdt số_lần tối đa là 5 - đợi 100giây sử dụng lại.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    diggory_chat3 = f'''
┌──────⭓ {name_bot}
│ Spam: Thành Công 
│ Số Lần Spam Free: {count}
│ Đang Tấn Công : {sdt}
│ Spam 5 Lần Tầm 1-2p mới xong 
│ Hạn Chế Spam Nhé !  
└─────────────
    '''

    script_filename = "sms.py"  # Tên file Python trong cùng thư mục
    try:
        # Kiểm tra xem file có tồn tại không
        if not os.path.isfile(script_filename):
            bot.reply_to(message, "Không tìm thấy file script. Vui lòng kiểm tra lại.")
            return

        # Đọc nội dung file với mã hóa utf-8
        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        # Tạo file tạm thời
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Chạy file tạm thời
        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
         bot.send_message(
            message.chat.id,
            f'<blockquote>{diggory_chat3}</blockquote>\n<blockquote>GÓI NGƯỜI DÙNG: FREE</blockquote>',
            parse_mode='HTML'
        )
    except FileNotFoundError:
        bot.reply_to(message, "Không tìm thấy file.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi xảy ra: {str(e)}")



blacklist = ["112", "113", "114", "115", "116", "117", "118", "119", "0", "1", "2", "3", "4"]


@bot.message_handler(commands=['bot'])
def send_help(message):
    bot.reply_to(message, """<blockquote>
Danh sách lệnh:
┌───────────────⭓ 
│• /getkey: Lấy Key Dùng Lệnh
│• /key {key}: Nhập key Thưởng
│• /spam : Spam free
│• /superspam : SpamVip
│• /help: Danh sách lệnh
│• /status : Admin
│• /restart : Admin
│• /stop : Admin
│• /them : Admin
└────────────────
</blockquote>""", parse_mode='HTML')

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn Không Phải Admin')
        return
    process_count = len(processes)
    bot.reply_to(message, f'Số quy trình đang chạy: {process_count}.')

@bot.message_handler(commands=['restart'])
def restart(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn Không Phải Admin')
        return
    bot.reply_to(message, 'Bot sẽ được khởi động lại trong giây lát...')
    time.sleep(2)
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn Không Phải Admin')
        return
    bot.reply_to(message, 'Bot sẽ dừng lại trong giây lát...')
    time.sleep(2)
    bot.stop_polling()

@bot.message_handler(commands=['them'])
def them(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn Không Phải Admin')
        return
    try:
        idvip = message.text.split()[1]
        ngay = message.text.split()[2]
        hethan = message.text.split()[3]
        with open(f"./vip/{idvip}.txt", "w") as fii:
            fii.write(f"{ngay}|{hethan}")
        bot.reply_to(message, f'Thêm Thành Công {idvip} Làm Vip')
    except IndexError:
        bot.reply_to(message, 'Vui lòng cung cấp đủ thông tin: /them <idvip> <ngay> <hethan>')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Lệnh Không Hợp lệ Vui Lòng Ghi /bot để xem các lệnh📄')

bot.polling()
