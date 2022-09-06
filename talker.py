from pyrogram import Client , filters
import sqlite3

#Set Sqlite modules
con = sqlite3.connect("database.db")
c = con.cursor()


app = Client(
  "my_account",
  api_id=2334910,
  api_hash="2281750d57b5a4fe5b5f2014bc5ce7e8"
  )



class TalkBot:
  #Create DataBse
  def __init__(self):
    sql = """CREATE TABLE words(
      id INTEGER PRIMARY KEY,
      word Text(200) ,
      answer Text(200)
      )"""
    try:
      c.execute(sql)
      con.commit()
    except:
      con.rollback()
    return True
  

  #add word & answer to DB
  def add(self,word,answer):
    sql = f"INSERT INTO words(word,answer) VALUES (\"{word}\",\"{answer}\""
    try:
      c.execute(sql)
      con.commit()
    except:
      con.rollback()
      return False
    return True
  
  
  #set the answer for messages
  def talker(self,text):
    answer = False
    results = []
    sql = "SELECT * FROM words"
    c.execute(sql)
    r = c.fetchall()
    for i in r:
      if i[1] in text:
        results.append(i[2])
        answer = True
    if answer == True:return random.choice(results)
    else:return False
  
  
  #list of all words
  def full(self):
    sql = "SELECT * FROM words"
    c.execute(sql)
    r = c.fetchall()
    nums = str(len(r))
    result = f"{nums} word was found:\n\n"
    for i in r:
      text = f"{i[0]}) {i[1]} -> {i[2]}"
      result = result+text
    return result
  
  
  #search in db to many answers of word
  def find(self,word):
    sql = f"SELECT * FROM words WHERE word=\"{word}\""
    c.execute(sql)
    r = c.fetchall()
    nums = str(len(r))
    result = f"{nums} word was found:\n\n"
    for i in r:
      text = f"{i[0]}) {i[1]} -> {i[2]}"
      result = result+text
    return result
  
  
  #delete word&answer from db
  def delete(self,row):
    sql = f"DELETE FROM words WHERE id={row}"
    try:
      c.execute(sql)
      con.commit()
      return True
    except:
      con.rollback()
      return False



bot =TalkBot()


@app.on_message(filters.command("add","/"))
def add(cli,msg):
  text = str(msg.text).replace("/add ","").split(" ; ")
  bot.add(text[0],text[1])
  msg.reply("ok")


@app.on_message(filters.command("all","/"))
def full(cli,msg):
  msg.reply(bot.full())


@app.on_message(filters.command("find","/"))
def find(cli,msg):
  word = str(msg.text).replace("/find  ","")
  result = bot.find(word)
  msg.reply(result)


@app.on_message(filters.command("delete","/"))
def delete(cli,msg):
  word = str(msg.text).replace("/delete ","")
  bot.delete(word)
  msg.reply("ok")


@app.on_message(~filters.me & ~filters.group)
def speak(cli,msg):
      data = bot.talker(msg.text)
      if data != False:
        msg.reply(data)



app.run()