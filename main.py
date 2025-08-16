import yaml
import EmailPush
import WechatBotPush
with open('config.yaml','r',encoding='UTF-8') as config:
     config= yaml.load(config,Loader=yaml.FullLoader)
data={'email':'1320911762@qq.com','content':'测试短信'}
data2={
    "msgtype": "text",
    "text": {
                "content": "机房大门打开"
        }
}
print(config)
EmailPush.WYsend_email(data,config['WYEmail'])
WechatBotPush.PushBot(data2,config['WechatBot'])