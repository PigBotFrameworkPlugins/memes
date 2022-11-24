import sys, time
sys.path.append("../..")
from bot import bot

class memes(bot):
    def add(self):
        if '\r\n' in self.args[2]:
            self.args[2] = self.args[2].replace("\r\n", "")
        self.commonx("INSERT INTO `botMemes` (`keyword`, `url`, `uid`, `time`) VALUES (%s, %s, %s, %s)", (self.args[1], self.args[2], self.se.get("user_id"), time.time()))
        self.send("face54[|已添加！|]")
        
    def messageListener(self):
        memesList = self.selectx("SELECT * FROM `botMemes` WHERE `uid`=%s", (self.se.get("user_id")))
        for i in memesList:
            if self.keywordPair(i.get("keyword"), self.message):
                self.send(i.get("url"), coinFlag=False, insertStrFlag=False)
                self.CallApi('delete_msg', {'message_id':self.se.get('message_id')})
                return 
    
    def listMemes(self):
        arr = []
        memesList = self.selectx("SELECT * FROM `botMemes` WHERE `uid`=%s", (self.se.get("user_id")))
        for i in memesList:
            arr.append({"type": "node", "data": {"name": self.botSettings.get("name"), "uin": self.botSettings.get("myselfqn"), "content": "{} => {}".format(i.get("keyword"), i.get("url"))}})
        self.CallApi("send_group_forward_msg", {"group_id":self.se.get("group_id"), "messages":arr})
    
    def rmMemes(self):
        self.commonx("DELETE FROM `botMemes` WHERE `keyword`=%s and `uid`=%s", (self.args[1], self.se.get("user_id")))
        self.send("face54[|已删除！|]")