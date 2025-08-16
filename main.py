import yaml
import EmailPush
import WechatBotPush
from flask import Flask, request, jsonify
app = Flask(__name__)
with open('config.yaml','r',encoding='UTF-8') as config:
     config= yaml.load(config,Loader=yaml.FullLoader)
@app.route('/send/wyemail',methods=['POST'])
def WyEmailPush():
    data=request.get_json()
    try:
        response=EmailPush.WYsend_email(data,config['WYEmail'])
        return    jsonify({"code": 200, "message": "发送成功"})
    except Exception as e:
        return jsonify({"code": 500, "message":e})
@app.route('/send/wechatbot',methods=['POST'])
def WechatBot():
    data=request.get_json()
    try:
        response=WechatBotPush.PushBot(data,config['WechatBot'])
        return    jsonify({"code": 200, "message": "发送成功"})
    except Exception as e:
        return jsonify({"code": 500, "message":e})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1992)