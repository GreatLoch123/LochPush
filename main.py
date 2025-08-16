import yaml
import EmailPush
import WechatBotPush
from flask import Flask, request, jsonify
import sqlite3
import os
if os.path.exists("data.db")!=True:
    sq1 ="""  alter table SMS add (sendtime)
"""
    sq2 =""" alter table Email (sendtime)
"""
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cur.execute(sq1)
    cur.execute(sq2)
    conn.commit()
    print(cur.fetchall())
# sq1 =""" create table Email (email,content)
# """
# sq2=""" select * from Email
# """
# sq3="""insert into  Email values ('1320911762@qq.com','测试')
# """
# conn=sqlite3.connect('data.db')
# cur=conn.cursor()
# #cur.execute(sq1)
# # cur.execute(sq3)
# cur.execute(sq3)
# conn.commit()
# cur.execute(sq2)
# rows=cur.fetchall()
# print(rows)
# 
def UpdateDB(sql):
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.execute('select * from bot')
    print(cur.fetchall())
app = Flask(__name__)
with open('config.yaml','r',encoding='UTF-8') as config:
     config= yaml.load(config,Loader=yaml.FullLoader)
@app.route('/send/wyemail',methods=['POST'])
def WyEmailPush():
    data=request.get_json()
    email =data['email']
    content=data['content']
    try:
        response=EmailPush.WYsend_email(data,config['WYEmail'])
        sql=f"insert into Email values ('{email}','{content}', datetime(CURRENT_TIMESTAMP,'localtime'))"
        print(sql)
        UpdateDB(sql)
        return    jsonify({"code": 200, "message": "发送成功"})
    except Exception as e:
        return jsonify({"code": 500, "message":e})
@app.route('/send/wechatbot',methods=['POST'])
def WechatBot():
    data=request.get_json()
    content=data['text']['content']
    try:
        response=WechatBotPush.PushBot(data,config['WechatBot'])
        sql=f"insert into bot values('{content}',datetime(CURRENT_TIMESTAMP,'localtime'),'')"
        UpdateDB(sql)
        return    jsonify({"code": 200, "message": "发送成功"})
    except Exception as e:
        return jsonify({"code": 500, "message":e})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1992)


