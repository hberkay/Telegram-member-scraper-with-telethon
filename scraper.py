from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient
import csv
channel='' #channel link etc. https://t.me/***
api_id = 1 
api_hash = ''
phone = '' #phone numer 
client = TelegramClient(phone, api_id, api_hash)
client.connect()
client(JoinChannelRequest(channel))
chats = []
last_date = None
chunk_size = 200
groups = []
client.start()
result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Choose a group to scrape members from:')
i = 0
for g in groups:
    print(str(i) + '- ' + g.title)
    i += 1

g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

print('Fetching Members...')
all_participants = []
all_participants = client.get_participants(target_group, limit=5000)

print('Saving In file...')
with open("filename.csv", "w", encoding='UTF-8') as f: 
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['user id','onlinestatus'])
    for user in all_participants:
        if user.username:
            username = user.username
        if not user.username==" ":
            writer.writerow([user.username,user.status])
print('Members scraped successfully.')
