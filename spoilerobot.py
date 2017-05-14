import json, urllib.error, urllib.parse, urllib.request, socket, sys
# minimal Telegram bot library
SENT = False
class TelegramBot():
    class attribute_dict():
        def __init__(self, data):
            self.__data__ = data
        def __getattr__(self, index):
            if index == "__data__": return object.__getattr__(self, "__data__")
            try:
                return self.__getitem__(index)
            except KeyError:
                raise AttributeError
        def __getitem__(self, index):
            return self.__data__[index]
        def __setattr__(self, index, value):
            if index == "__data__": return object.__setattr__(self, "__data__", value)
            self.__setitem__(index)
        def __setitem__(self, index, value):
            self.__data__[index] = value
        def __delattr__(self, index, value):
            if index == "__data__": return object.__delattr__(self, "__data__", value)
            self.__delitem__(index)
        def __delitem__(self, index, value):
            del self.__data__[index]
        def __repr__(self):
            return repr(self.__data__)
        def __iter__(self):
            return iter(self.__data__)
        def __len__(self):
            return len(self.__data__)
        def keys(self):
            return self.__data__.keys()
        def has(self, key):
            return key in self.__data__.keys() and self.__data__[key] != None
    def __init__(self, token):
        self.token = token
        self.retry = 0
    def __getattr__(self, attr):
        return self.func_wrapper(attr)
    def func_wrapper(self, fname):
        def func(self, unsafe, **kw):
            url_par={}
            for key in kw.keys():
                if kw[key] != None:
                    url_par[key] = urllib.parse.quote_plus(TelegramBot.escape(kw[key]))
            url = ("https://api.telegram.org/bot" + self.token + "/" + (fname.replace("__UNSAFE","") if fname.endswith("__UNSAFE") else fname) + "?" +
                    "&".join(map(lambda x:x+"="+url_par[x],url_par.keys())))
            RETRY = True
            while RETRY:
                try:
                    with urllib.request.urlopen(url, timeout=10) as f:
                        raw = f.read().decode('utf-8')
                    RETRY = False
                except urllib.error.HTTPError as e:
                    if "bad request" in str(e).lower() and not unsafe:
                        print(fname, url)
                        print(json.dumps(url_par))
                        print(e.read().decode('utf-8'))
                        traceback.print_exc()
                        return
                    elif "forbidden" in str(e).lower() and not unsafe:
                        print(fname, url)
                        print(json.dumps(url_par))
                        print(e.read().decode('utf-8'))
                        traceback.print_exc()
                        return
                    else:
                        raise e                    
                except socket.timeout:
                    if unsafe:
                        raise ValueError("timeout")
                    else:
                        print("timeout!")
                        time.sleep(1)
                except BaseException as e:
                    print(str(e))
                    time.sleep(0.5)
                    if "too many requests" in str(e).lower():
                        self.retry += 1
                        time.sleep(self.retry * 5)
                    elif "unreachable" in str(e).lower() or "bad gateway" in str(e).lower() or "name or service not known" in str(e).lower() or  "network" in str(e).lower() or "handshake operation timed out" in str(e).lower():
                        time.sleep(3)
                    elif "bad request" in str(e).lower() and not unsafe:
                        print(fname, url)
                        print(json.dumps(url_par))
                        traceback.print_exc()
                        return
                    elif "forbidden" in str(e).lower() and not unsafe:
                        print(fname, url)
                        print(json.dumps(url_par))
                        traceback.print_exc()
                        return
                    else:
                        raise e
            self.retry = 0
            return TelegramBot.attributify(json.loads(raw))
        return lambda **kw:func(self,fname.endswith("__UNSAFE"),**kw)
    @staticmethod
    def escape(obj):
        if type(obj) == str:
            return obj
        else:
            return json.dumps(obj).encode('utf-8')
    @staticmethod
    def attributify(obj):
        if type(obj)==list:
            return list(map(TelegramBot.attributify,obj))
        elif type(obj)==dict:
            d = obj
            for k in d.keys():
                d[k] = TelegramBot.attributify(d[k])
            return TelegramBot.attribute_dict(d)
        else:
            return obj

bot = TelegramBot("BOT_TOKEN_GOES_HERE")
BOT_OWNER_TAG = "@BOT_OWNER_USERNAME_GOES_HERE"

import time, pickle, os.path, traceback, random, threading
try:
    ME = bot.getMe().result
except:
    time.sleep(2)
    os.execl(sys.executable, sys.executable, *sys.argv)      
    quit()
ID = ME.id
UN = ME.username

SPOILERS = {}
SPOILERD = {}
SPOILERM = {}
TSPOILERS = {}
TSPOILERU = {}
PSPOILERU = {}
PPHASE = {}
PSPOILERS = {}
LSPOILERV = {}
DSPOILER = {}
XSPOILERS = {}
XSPOILERI = {}
OFF = 0

TSPOILERM = {}
TCSPOILERM = {}
TSPOILERC = {}

def dictify(d):
    if type(d) == TelegramBot.attribute_dict:
        return d.__data__
    return d

def superdictify(obj):
        if type(obj)==list:
            return list(map(superdictify,obj))
        elif type(obj)==TelegramBot.attribute_dict:
            d = obj
            for k in d.keys():
                d[k] = superdictify(d[k])
            return dictify(d)            
        elif type(obj)==dict:
            d = obj
            for k in d.keys():
                d[k] = superdictify(d[k])
            return d 
        else:
            return obj

def load():
    global SPOILERS, SPOILERD, SPOILERM, TSPOILERS, TSPOILERU, PSPOILERU, PPHASE, PSPOILERS, LSPOILERV, XSPOILERS, XSPOILERI
    if os.path.isfile("spoilerobot.dat"):
        try:
            with open("spoilerobot.dat", "rb") as f:
                SPOILERS, SPOILERD, SPOILERM, TSPOILERS, TSPOILERU, PSPOILERU, PPHASE, PSPOILERS, LSPOILERV, XSPOILERS, XSPOILERI = pickle.load(f)            
        except:
            traceback.print_exc()
            return

import copy
def save(reason):
    print("saving <" + reason + ">")
    try:
        SPOILERS_, SPOILERD_, SPOILERM_, TSPOILERS_, TSPOILERU_, PSPOILERU_, PPHASE_, PSPOILERS_, LSPOILERV_, XSPOILERS_, XSPOILERI_ = copy.deepcopy(SPOILERS), copy.deepcopy(SPOILERD), copy.deepcopy(SPOILERM), copy.deepcopy(TSPOILERS), copy.deepcopy(TSPOILERU), copy.deepcopy(PSPOILERU), copy.deepcopy(PPHASE), copy.deepcopy(PSPOILERS), copy.deepcopy(LSPOILERV), copy.deepcopy(XSPOILERS), copy.deepcopy(XSPOILERI)
        SPOILERS_, SPOILERD_, SPOILERM_, TSPOILERS_, TSPOILERU_, PSPOILERU_, PPHASE_, PSPOILERS_, LSPOILERV_, XSPOILERS_, XSPOILERI_ = superdictify(SPOILERS_), superdictify(SPOILERD_), superdictify(SPOILERM_), superdictify(TSPOILERS_), superdictify(TSPOILERU_), superdictify(PSPOILERU_), superdictify(PPHASE_), superdictify(PSPOILERS_), superdictify(LSPOILERV_), superdictify(XSPOILERS_), superdictify(XSPOILERI_)
        with open("spoilerobot.dat", "wb") as f:
            pickle.dump((SPOILERS_, SPOILERD_, SPOILERM_, TSPOILERS_, TSPOILERU_, PSPOILERU_, PPHASE_, PSPOILERS_, LSPOILERV_, XSPOILERS_, XSPOILERI_), f)
    except:
        print("error while saving...")
        traceback.print_exc()
    print("saved")
        

load()

def random_id():
    I = ""
    for _ in range(60):
        I += random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    return I

UPD_COUNTER = 0
SAVE_EVERY_N_UPDATES = 50
Restart = True

def html_escape(x):
    return x.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
import os, sys
tried_to = 0
saferes = True
try:
    def autoreset():
        time.sleep(600)
        while not saferes:
            time.sleep(0.5)
            tried_to = 10000
        time.sleep(30)
        save("quitting - backup thread")
        os.execl(sys.executable, sys.executable, *sys.argv)      
    if Restart:
        threading.Thread(target=autoreset, daemon=True).start()
    while True:
        tried_to += 1
        if tried_to >= 1000 and Restart:
            save("quitting")
            os.execl(sys.executable, sys.executable, *sys.argv)
        print("poll " + str(time.time()),end=":")
        saferes = False
        try:
            updates = bot.getUpdates__UNSAFE(offset=OFF, timeout=5).result
        except KeyboardInterrupt as e:
            print("E")
            raise e
        except BaseException as e:
            print("0")
            if str(e).strip().lower() != "timeout":
                print("poll failed: ", e)
            continue            
        print(len(updates))
        for update in updates:
            now = time.time()
            UPD_COUNTER += 1
            if UPD_COUNTER == SAVE_EVERY_N_UPDATES:
                save(str(UPD_COUNTER))
                UPD_COUNTER = 0
            OFF = update.update_id + 1
            if update.has("inline_query"):
                iq = update.inline_query
                iqi, iqu, iqq = iq.id, iq["from"].id, iq.query
                key = str(iqu) + "_" + str(int(time.time()*1000))
                results = []
                if iqq.startswith("Spoiler!?:"):
                    V = iqq[10:]
                    if len(V.split("_")) == 2:
                        if str(V.split("_")[0]) == str(iqu):
                            if len(V) < 50:
                                if V in SPOILERS.keys():
                                    if True:
                                        if True or TSPOILERU[iqu] == V:
                                            if type(SPOILERS[V]) == list or type(SPOILERS[V]) == dict:
                                                appearance = None
                                                if type(SPOILERS[V]) == list:
                                                    appearance = SPOILERS[V][1]
                                                else:
                                                    appearance = SPOILERS[V]["_"]
                                                results = []
                                                single = V in SPOILERM.keys() and bool(SPOILERM[V])
                                                try:
                                                    if not SPOILERS[V][0].startswith("http"):
                                                        raise ValueError
                                                    if type(SPOILERS[V]) == dict:
                                                        raise ValueError
                                                    results.append({"type":"article",
                                                            "id":random_id(),
                                                            "title":"Spoiler",
                                                            "input_message_content":{"message_text":appearance,"parse_mode":"HTML"},
                                                            "reply_markup":{"inline_keyboard":[[{"text":"Show spoiler","url":SPOILERS[V][0]}]]}})
                                                    bot.answerInlineQuery__UNSAFE(inline_query_id=iqi,
                                                          results=results,
                                                          cache_time=1,
                                                          is_personal=True)
                                                except:
                                                    results = []
                                                    results.append({"type":"article",
                                                                "id":random_id(),
                                                                "title":"Spoiler",
                                                                "input_message_content":{"message_text":appearance,"parse_mode":"HTML"},
                                                                "reply_markup":{"inline_keyboard":[[{"text":"Show spoiler" if single else "Double tap to show spoiler","callback_data":V}]]}})
                                                    bot.answerInlineQuery(inline_query_id=iqi,
                                                          results=results,
                                                          cache_time=1,
                                                          is_personal=True)
                                                continue
                if len(iqq.strip()) > 200:
                    results.append({"type":"article",
                                "id":random_id(),
                                "title":"Too long, please do not tap!",
                                "description":"Please use Advanced spoiler. (This is a Telegram limitation)",
                                "thumb_url":"http://i.imgur.com/zZMQBmK.png",
                                "thumb_width":512,
                                "thumb_height":512,
                                "input_message_content":{"message_text":"<i>Error: Too long for inline</i>","parse_mode":"HTML"}})
                elif len(iqq.strip()) > 0:
                    minorid = random_id()
                    if ":::" in iqq:
                        tok = iqq.split(":::",1)
                        minorid2 = random_id()
                        try:
                            title = tok[0].strip()
                            TSPOILERS[key] = tok[1].strip()
                            randid = random_id()
                            TSPOILERC[key] = [randid,minorid2]
                            TCSPOILERM[iqu] = minorid2
                            iqq2 = tok[1].strip()
                            linkd = False
                            if iqq2.startswith("http:") or iqq2.startswith("https:"):
                                try:
                                    results.append({"type":"article",
                                                "id":randid,
                                                "title":"Custom Major Spoiler",
                                                "description":"URL, custom title",
                                                "input_message_content":{"message_text":"<b>Major Spoiler:</b> <pre>" + title + "</pre>","parse_mode":"HTML"},
                                                "thumb_url":"http://i.imgur.com/kuIyXod.png",
                                                "thumb_width":512,
                                                "thumb_height":512,
                                                "reply_markup":{"inline_keyboard":[[{"text":("Show spoiler"),"url":iqq2}]]}})
                                    results.append({"type":"article",
                                                "id":minorid2,
                                                "title":"Custom Minor Spoiler",
                                                "description":"URL, custom title",
                                                "input_message_content":{"message_text":"<i>Minor Spoiler:</i> <pre>" + title + "</pre>","parse_mode":"HTML"},
                                                "thumb_url":"http://i.imgur.com/xFbwNIp.png",
                                                "thumb_width":512,
                                                "thumb_height":512,
                                                "reply_markup":{"inline_keyboard":[[{"text":("Show spoiler"),"url":iqq2}]]}})
                                    linkd = True
                                except:
                                    pass
                            if not linkd:
                                results.append({"type":"article",
                                            "id":randid,
                                            "title":"Custom Major Spoiler",
                                            "description":"Text only, custom title, double tap",
                                            "input_message_content":{"message_text":"<b>Major Spoiler:</b> <pre>" + title + "</pre>","parse_mode":"HTML"},
                                            "thumb_url":"http://i.imgur.com/kuIyXod.png",
                                            "thumb_width":512,
                                            "thumb_height":512,
                                            "reply_markup":{"inline_keyboard":[[{"text":("Double tap to show spoiler"),"callback_data":key}]]}})
                                results.append({"type":"article",
                                            "id":minorid2,
                                            "title":"Custom Minor Spoiler",
                                            "description":"Text only, custom title, single tap",
                                            "input_message_content":{"message_text":"<i>Minor Spoiler:</i> <pre>" + title + "</pre>","parse_mode":"HTML"},
                                            "thumb_url":"http://i.imgur.com/xFbwNIp.png",
                                            "thumb_width":512,
                                            "thumb_height":512,
                                            "reply_markup":{"inline_keyboard":[[{"text":("Show spoiler"),"callback_data":key}]]}})
                        except BaseException as ex:
                            pass
                    if iqq.startswith("http:") or iqq.startswith("https:"):
                        try:
                            results.append({"type":"article",
                                            "id":random_id(),
                                            "title":"Major Spoiler!",
                                            "description":"URL, single-tap",
                                            "input_message_content":{"message_text":"<b>Major Spoiler!</b>","parse_mode":"HTML"},
                                            "thumb_url":"http://i.imgur.com/3qqCZZk.png",
                                            "thumb_width":512,
                                            "thumb_height":512,
                                            "reply_markup":{"inline_keyboard":[[{"text":"Show spoiler","url":iqq}]]}})
                            results.append({"type":"article",
                                            "id":minorid,
                                            "title":"Minor Spoiler",
                                            "description":"URL, single-tap",
                                            "input_message_content":{"message_text":"<i>Minor Spoiler</i>","parse_mode":"HTML"},
                                            "thumb_url":"http://i.imgur.com/csh5H5O.png",
                                            "thumb_width":512,
                                            "thumb_height":512,
                                            "reply_markup":{"inline_keyboard":[[{"text":"Show spoiler","url":iqq}]]}})
                            bot.answerInlineQuery(inline_query_id=iqi,
                                                  results=results,
                                                  cache_time=1,
                                                  is_personal=True,
                                                  switch_pm_text="Advanced spoiler (media etc.)...",
                                                  switch_pm_parameter=key)
                            TSPOILERS[key] = iqq[:1024]
                            TSPOILERU[iqu] = key
                            TSPOILERM[iqu] = minorid
                            continue
                        except:
                            pass
                    results.append({"type":"article",
                                "id":random_id(),
                                "title":"Major Spoiler!",
                                "description":"Text only, double-tap",
                                "input_message_content":{"message_text":"<b>Major Spoiler!</b>","parse_mode":"HTML"},
                                "thumb_url":"http://i.imgur.com/3qqCZZk.png",
                                "thumb_width":512,
                                "thumb_height":512,
                                "reply_markup":{"inline_keyboard":[[{"text":"Double tap to show spoiler","callback_data":key}]]}})
                    minorid = random_id()
                    results.append({"type":"article",
                                "id":minorid,
                                "title":"Minor Spoiler",
                                "description":"Text only, single-tap",
                                "input_message_content":{"message_text":"<i>Minor Spoiler</i>","parse_mode":"HTML"},
                                "thumb_url":"http://i.imgur.com/csh5H5O.png",
                                "thumb_width":512,
                                "thumb_height":512,
                                "reply_markup":{"inline_keyboard":[[{"text":"Show spoiler","callback_data":key}]]}})
                    TSPOILERM[iqu] = minorid
                TSPOILERS[key] = iqq[:1024]
                TSPOILERU[iqu] = key
                bot.answerInlineQuery(inline_query_id=iqi,
                                      results=results,
                                      cache_time=1,
                                      is_personal=True,
                                      switch_pm_text="Advanced spoiler (media etc.)...",
                                      switch_pm_parameter=key)
            elif update.has("chosen_inline_result"):
                iqu = update.chosen_inline_result["from"].id
                if iqu in TSPOILERU.keys():
                    key = TSPOILERU[iqu]
                    if key in TSPOILERS.keys() and key not in SPOILERS.keys():
                        temp = TSPOILERS[key]
                        if key in TSPOILERC.keys() and update.chosen_inline_result.result_id in TSPOILERC[key]:
                            temp = temp.split(":::",1)[1]
                        SPOILERS[key] = temp
                        SPOILERD[key] = time.time()
                        if iqu in TSPOILERM.keys() and TSPOILERM[iqu] == update.chosen_inline_result.result_id:
                            SPOILERM[key] = True
                        if iqu in TCSPOILERM.keys() and TCSPOILERM[iqu] == update.chosen_inline_result.result_id:
                            SPOILERM[key] = True
                        del TSPOILERS[key]
                    del TSPOILERU[iqu]
            elif update.has("callback_query"):
                cq = update.callback_query
                cqd = cq.data
                if cqd not in SPOILERS.keys():
                    bot.answerCallbackQuery(callback_query_id=cq.id,
                                            text="Spoiler not found. Too old?",
                                            show_alert=False)
                    continue
                double = True
                if cqd in SPOILERM.keys() and SPOILERM[cqd]:
                    double = False
                if double:
                    tuplex = (cq["from"].id, cq.data)
                    if tuplex not in DSPOILER.keys():
                        DSPOILER[tuplex] = time.time()
                        bot.answerCallbackQuery(callback_query_id=cq.id,
                                                text="Please tap again to see the spoiler")
                        continue
                    if (time.time()) >= (DSPOILER[tuplex] + 3):
                        DSPOILER[tuplex] = time.time()
                        bot.answerCallbackQuery(callback_query_id=cq.id,
                                                text="Please tap again to see the spoiler")
                        continue
                    del DSPOILER[tuplex]
                uid = cq["from"].id
                if type(SPOILERS[cqd]) == list and len(SPOILERS[cqd][0]) <= 200:
                    bot.answerCallbackQuery(callback_query_id=cq.id,
                                            text=SPOILERS[cqd][0],
                                            show_alert=True)
                elif type(SPOILERS[cqd]) == list:
                    try:
                        bot.sendMessage__UNSAFE(chat_id=uid,
                                                text=SPOILERS[cqd][0])
                        bot.answerCallbackQuery(callback_query_id=cq.id,
                                                text="The spoiler has been sent to you as a direct message.")
                    except:
                        LSPOILERV[cq["from"].id] = cqd
                        bot.answerCallbackQuery(callback_query_id=cq.id,
                                            text="Please open @SpoileroBot and type /show to see the spoiler")
                elif type(SPOILERS[cqd]) == dict and "file_id" in SPOILERS[cqd].keys():
                    try:
                        if True:
                                obj = SPOILERS[cqd]
                                if obj["type"] == "Photo":
                                    bot.sendPhoto__UNSAFE(chat_id=uid,
                                                  photo=obj["file_id"],
                                                  caption=None if "caption" not in obj.keys() else obj["caption"])
                                elif obj["type"] == "Audio":
                                    bot.sendAudio__UNSAFE(chat_id=uid,
                                                  audio=obj["file_id"],
                                                  duration=None if "duration" not in obj.keys() else obj["duration"],
                                                  performer=None if "performer" not in obj.keys() else obj["performer"],
                                                  title=None if "title" not in obj.keys() else obj["title"])
                                elif obj["type"] == "Document":
                                    bot.sendDocument__UNSAFE(chat_id=uid,
                                                  document=obj["file_id"],
                                                  caption=None if "caption" not in obj.keys() else obj["caption"])
                                elif obj["type"] == "Sticker":
                                    bot.sendSticker__UNSAFE(chat_id=uid,
                                                  sticker=obj["file_id"])
                                elif obj["type"] == "Video":
                                    bot.sendVideo__UNSAFE(chat_id=uid,
                                                  video=obj["file_id"],
                                                  duration=None if "duration" not in obj.keys() else obj["duration"],
                                                  width=None if "width" not in obj.keys() else obj["width"],
                                                  height=None if "height" not in obj.keys() else obj["height"],
                                                  caption=None if "caption" not in obj.keys() else obj["caption"])
                                elif obj["type"] == "Voice":
                                    bot.sendVoice__UNSAFE(chat_id=uid,
                                                  voice=obj["file_id"],
                                                  duration=None if "duration" not in obj.keys() else obj["duration"])
                                bot.answerCallbackQuery(callback_query_id=cq.id,
                                                        text="The media has been sent to you as a direct message.")
                    except BaseException as ex:
                        print(str(ex))
                        LSPOILERV[cq["from"].id] = cqd
                        bot.answerCallbackQuery(callback_query_id=cq.id,
                                            text="Please open @SpoileroBot and type /show to see the spoiler")
                elif len(SPOILERS[cqd]) > 200:
                    try:
                        bot.sendMessage__UNSAFE(chat_id=uid,
                                                text=SPOILERS[cqd])
                        bot.answerCallbackQuery(callback_query_id=cq.id,
                                                text="The spoiler has been sent to you as a direct message.")
                    except:
                        LSPOILERV[cq["from"].id] = cqd
                        bot.answerCallbackQuery(callback_query_id=cq.id,
                                            text="Please open @SpoileroBot and type /show to see the spoiler")
                else:
                    bot.answerCallbackQuery(callback_query_id=cq.id,
                                            text=SPOILERS[cqd],
                                            show_alert=True)
            elif update.has("message"):
                if update.message.has("text"):
                    umt = update.message.text
                    worked = False
                    chat_id = update.message.chat.id
                    if umt[0:7].lower() == "/start ":
                        I = umt[7:]
                        if len(I.split("_")) == 2:
                            if str(I.split("_")[0]) == str(update.message["from"].id):
                                if len(I) < 50:
                                    if I not in SPOILERS.keys():
                                        try:
                                            worked = True
                                            PSPOILERU[update.message["from"].id] = I
                                            PPHASE[update.message["from"].id] = 0
                                            bot.sendMessage(chat_id=chat_id,
                                                text="Preparing a spoiler. To cancel, type /cancel.\n\nFirst type the content to be spoiled. It can be text, photo, or any other media.\n\nCurrently unsupported: Locations, Venues, Contacts, Games",
                                                parse_mode="HTML")
                                        except:
                                            pass
                    if worked:
                        continue
                    if umt.lower() == "/start" or umt.lower() == "/help" or umt.lower().startswith("/help "):
                        bot.sendMessage(chat_id=chat_id,
                                        text="You can use @SpoileroBot in inline mode:\n\n<pre>@SpoileroBot spoiler here...</pre>\nYou can type quick spoilers, or prepare an advanced spoiler with additional details such as type, how big of a spoiler and a small title for the spoiler.\n\nCustom spoilers can also be done from inline mode as follows:\n\n<pre>@SpoileroBot title for the spoiler ::: contents of the spoiler</pre>\nNote that the title will be immediately visible! Also make sure you tap Custom Spoiler to get the title.\n\nSpoilers last at least 30 days, but probably a lot longer.",
                                        parse_mode="HTML")
                    elif umt.lower() == "/show":
                        uid = update.message["from"].id
                        if uid not in LSPOILERV.keys():
                            bot.sendMessage(chat_id=chat_id,
                                            text="You haven't tried to view a spoiler yet.")
                        else:
                            key = LSPOILERV[uid]
                            del LSPOILERV[uid]
                            if type(SPOILERS[key]) == list:
                                bot.sendMessage(chat_id=chat_id, text=SPOILERS[key][0])
                            elif type(SPOILERS[key]) == str:
                                bot.sendMessage(chat_id=chat_id, text=SPOILERS[key])
                            else:
                                try:
                                    obj = SPOILERS[key]
                                    if obj["type"] == "Photo":
                                        bot.sendPhoto(chat_id=chat_id,
                                                      photo=obj["file_id"],
                                                      caption=None if "caption" not in obj.keys() else obj["caption"])
                                    elif obj["type"] == "Audio":
                                        bot.sendAudio(chat_id=chat_id,
                                                      audio=obj["file_id"],
                                                      duration=None if "duration" not in obj.keys() else obj["duration"],
                                                      performer=None if "performer" not in obj.keys() else obj["performer"],
                                                      title=None if "title" not in obj.keys() else obj["title"])
                                    elif obj["type"] == "Document":
                                        bot.sendDocument(chat_id=chat_id,
                                                      document=obj["file_id"],
                                                      caption=None if "caption" not in obj.keys() else obj["caption"])
                                    elif obj["type"] == "Sticker":
                                        bot.sendAudio(chat_id=chat_id,
                                                      sticker=obj["file_id"])
                                    elif obj["type"] == "Video":
                                        bot.sendVideo(chat_id=chat_id,
                                                      video=obj["file_id"],
                                                      duration=None if "duration" not in obj.keys() else obj["duration"],
                                                      width=None if "width" not in obj.keys() else obj["width"],
                                                      height=None if "height" not in obj.keys() else obj["height"],
                                                      caption=None if "caption" not in obj.keys() else obj["caption"])
                                    elif obj["type"] == "Voice":
                                        bot.sendVoice(chat_id=chat_id,
                                                      voice=obj["file_id"],
                                                      duration=None if "duration" not in obj.keys() else obj["duration"])
                                except:
                                    bot.sendMessage(chat_id=chat_id,
                                                text="Sorry, an error occurred. Please report this to " + BOT_OWNER_TAG + " if the error persists.")
                    elif umt.lower() == "/clear":
                        bot.sendMessage(chat_id=chat_id,
                                        text=(250*".\n"))
                    elif umt.lower() == "/cancel" and update.message["from"].id in PPHASE.keys():
                        del PPHASE[update.message["from"].id]
                        del PSPOILERU[update.message["from"].id]
                        bot.sendMessage(chat_id=chat_id,
                                        text="The spoiler preparation has been cancelled.",
                                        reply_markup={"inline_keyboard":[[{"text":"OK","switch_inline_query":""}]]})
                    elif update.message["from"].id in PPHASE.keys():
                        uid = update.message["from"].id
                        phase = PPHASE[uid]
                        if phase == 0:
                            if len(umt) > 1024:
                                bot.sendMessage(chat_id=chat_id,
                                        text="This spoiler is too long.")
                            else:
                                XSPOILERS[uid] = umt
                                bot.sendMessage(chat_id=chat_id,
                                        text="Next, specify the amount of taps needed.\n\nIf you just want to send a standard spoiler with no extra details (requiring 2 taps), type a dash (-) now.",
                                        reply_markup={"keyboard":[[{"text":"-"}],[{"text":"1"},{"text":"2"}]],"resize_keyboard":True,"one_time_keyboard":True})
                                PPHASE[uid] = 1
                        elif phase == 1:
                            checklist = ["1","2"]
                            if umt in checklist:
                                key = PSPOILERU[uid]
                                SPOILERM[key] = (umt == "1")
                                bot.sendMessage(chat_id=chat_id,
                                        text="Now send a title for the spoiler (maximum 100 characters). It will be immediately visible and can be used to add a small description for your spoiler.",
                                        reply_markup={"hide_keyboard":True})
                                PPHASE[uid] = 2
                            elif umt.lower() in [".","-","none"]:
                                key = PSPOILERU[uid]
                                if type(XSPOILERS[uid]) == dict:
                                    XSPOILERS[uid]["_"] = "Spoiler!"
                                    SPOILERS[key] = XSPOILERS[uid]
                                else:
                                    SPOILERS[key] = [XSPOILERS[uid], "Spoiler!"]
                                SPOILERD[key] = time.time()
                                TSPOILERU[uid] = key
                                del XSPOILERS[uid]
                                del PPHASE[update.message["from"].id]
                                del PSPOILERU[update.message["from"].id]
                                bot.sendMessage(chat_id=chat_id,
                                        text="Done! Your advanced spoiler is ready.",
                                        reply_markup={"inline_keyboard":[[{"text":"Send it","switch_inline_query":"Spoiler!?:"+key}]]})
                            else:
                                bot.sendMessage(chat_id=chat_id,
                                        text="Unknown spoiler type.")
                        elif phase == 2:
                            if len(umt) > 100:
                                bot.sendMessage(chat_id=chat_id,
                                        text="The given title is too long.")
                            else:
                                PSPOILERS[uid] = "\n\n<pre>" + html_escape(umt) + "</pre>"
                                key = PSPOILERU[uid]
                                if type(XSPOILERS[uid]) == dict:
                                    XSPOILERS[uid]["_"] = PSPOILERS[uid]
                                    SPOILERS[key] = XSPOILERS[uid]
                                else:
                                    SPOILERS[key] = [XSPOILERS[uid], PSPOILERS[uid]]
                                SPOILERD[key] = time.time()
                                TSPOILERU[uid] = key
                                del XSPOILERS[uid]
                                del PPHASE[update.message["from"].id]
                                del PSPOILERU[update.message["from"].id]
                                bot.sendMessage(chat_id=chat_id,
                                        text="Done! Your advanced spoiler is ready.",
                                        reply_markup={"inline_keyboard":[[{"text":"Send it","switch_inline_query":"Spoiler!?:"+key}]]})
                elif update.message["from"].id in PPHASE.keys():
                    uid = update.message["from"].id
                    chat_id = update.message.chat.id
                    phase = PPHASE[uid]
                    if phase == 0:
                        # a file was sent?
                        obj = None
                        if update.message.has("document"):
                            obj = update.message.document
                            obj["type"] = "Document"
                            if update.message.has("caption"):
                                obj["caption"] = update.message.caption
                        elif update.message.has("photo"):
                            objs = update.message.photo
                            obj = None
                            mw, mh = 0, 0
                            for photo in objs:
                                if photo.width > mw and photo.height > mh:
                                    obj = photo
                                    mw = photo.width
                                    mh = photo.height
                            obj["type"] = "Photo"
                            if update.message.has("caption"):
                                obj["caption"] = update.message.caption
                        elif update.message.has("video"):
                            obj = update.message.video
                            obj["type"] = "Video"
                            if update.message.has("caption"):
                                obj["caption"] = update.message.caption
                        elif update.message.has("audio"):
                            obj = update.message.audio
                            obj["type"] = "Audio"
                        elif update.message.has("sticker"):
                            obj = update.message.sticker
                            obj["type"] = "Sticker"
                        elif update.message.has("voice"):
                            obj = update.message.voice
                            obj["type"] = "Voice"
                        if obj != None:
                            key = PSPOILERU[uid]
                            XSPOILERS[uid] = dictify(obj)
                            bot.sendMessage(chat_id=chat_id,
                                        text="Next, specify the amount of taps needed.\n\nIf you just want to send a standard spoiler with no extra details (requiring 2 taps), type a dash (-) now.",
                                        reply_markup={"keyboard":[[{"text":"-"}],[{"text":"1"},{"text":"2"}]],"resize_keyboard":True,"one_time_keyboard":True})
                            PPHASE[uid] = 1
                        else:
                            print(update)
                            bot.sendMessage(chat_id=chat_id,
                                    text="Unrecognized media type.")                            
        saferes = True
        time.sleep(0.1)
except KeyboardInterrupt as e:
    save("Quit")
except BaseException as e:
    save("Exception")
    traceback.print_exc()
