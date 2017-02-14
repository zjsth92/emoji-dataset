import json
with open('emoji.json', 'r') as emojis_json:
    emojis = json.load(emojis_json)
    print "emoji.json loaded"
# inverse emoji.json
emojis_dic = {}
for name in emojis.keys():
    emoji_name = emojis[name].encode('utf-8')
    emojis_dic[emoji_name] = name.encode('utf-8')

# write into emoji_inverse.json
with open('emoji_inverse.json', 'w') as outfile:
        json.dump(emojis_dic, outfile, indent=4, sort_keys=True, ensure_ascii=False, encoding='utf-8')
        print "emoji_inverse.json wrote"