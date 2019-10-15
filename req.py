# -*- coding:utf-8 -*-

import requests
import json
import card_order

def status_display(key):
    dict = {
        0: '成功',
        1001: '用户名已被使用',
        1002:	'学号已绑定',
        1003:	'教务处认证失败',
        1004:	'Token过期',
        2001:	'未结束战局过多',
        2002:	'出千！！！',
        2003:	'不合法墩牌',
        2003:	'战局不存在或已结束',
        3001:	'战局不存在或未结束',
        3002:	'玩家不存在'
    }
    if key in dict:
        print(dict[key])
    else:
        print('KeyError %d' % key)

# 玩家类
class Player(object):
    def __init__(self, user, psw):
        self.user = user
        self.psw = psw
        self.user_id = None
        self.token = None
        self.is_register = None
        self.is_log = None
        self.id = None
        self.cards = None

    def show(self):
        print()
        print(self.user)
        print(self.psw)
        print(self.user_id)
        print(self.token)
        print(self.is_register)
        print(self.is_log)
        print(self.id)
        print(self.cards)
        print()
    # 注册

    def register(self):
        url = 'https://api.shisanshui.rtxux.xyz/auth/register'
        headers = {'Content-Type': 'application/json'}
        data = {
            'username': self.user,
            'password': self.psw
        }
        r = requests.post(url, headers=headers, data=json.dumps(data))

        status = r.json()['status']
        if status == 0 and 'user_id' in r.json()['data']:
            self.user_id = r.json()['data']['user_id']
            self.is_register = True
            print('register may be successful')
            print(r.text)
        else:
            print('register fialed!')
            status_display(status)
            print(r.text)
            
    # 登录
    def login(self):
        url = "https://api.shisanshui.rtxux.xyz/auth/login"
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "username": self.user,
            "password": self.psw
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)

        status = r.json()['status']
        if status == 0 and 'user_id' in r.json()['data']:
            self.user_id = r.json()['data']['user_id']
            self.token = r.json()['data']['token']
            self.is_log = True
            print('Login may be successful')
            print(r.text)
        else:
            print('login fialed!')
            status_display(status)
            print(r.text)

    # 注销
    def logout(self):
        url = "https://api.shisanshui.rtxux.xyz/auth/logout"
        headers = {
            'x-auth-token': self.token
        }
        r = requests.post(url, headers=headers)

        status = r.json()['status']
        if status == 0:
            self.logged = False
            print('Logout may be successful')
            print(r.text)
        else:
            print('logout fialed!')
            status_display(status)
            print(r.text)

    # 登录验证
    def validate_token(self):
        url = 'https://api.shisanshui.rtxux.xyz/auth/validate'
        headers = {
            'X-Auth-Token': self.token
        }
        r = requests.get(url, headers=headers)

        status = r.json()['status']
        if status == 0 and 'user_id' in r.json()['data']:
                if 'token' in r.json()['data']:
                    self.token = r.json()['data']['token']
                print('validate may be successful')
                print(r.text)
        else:
            print('validate fialed!')
            status_display(status)
            print(r.text)

    # 返回登陆状态
    def check_login_status(self):
        return self.is_log

    # 开局
    def game_open(self):
        url = "https://api.shisanshui.rtxux.xyz/game/open"
        headers = {
            'x-auth-token': self.token
        }
        r = requests.post(url, headers=headers)

        status = r.json()['status']
        if status == 0:
            self.id = r.json()['data']['id']
            self.cards = r.json()['data']['card']
            print('game_open may be successful')
            print(r.text)
        else:
            print('game_open fialed!')
            status_display(status)
            print(r.text)
        return self.cards

    # 出牌
    def game_submit(self, submit_card):
        url = "https://api.shisanshui.rtxux.xyz/game/submit"
        data = {
            'id': self.id,
            'card': submit_card
        }
        headers = {
            'content-type': "application/json",
            'x-auth-token': self.token
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        status = r.json()['status']
        print('game_submit may be successful')
        print(r.text)
        if status != 0:
            print('game_submit fialed!')
            status_display(status)
            print(r.text)

    # 历史
    def get_history(self, page, limit, play_id):
        url = "https://api.shisanshui.rtxux.xyz/history"
        querystring = {
            "page": page,
            "limit": limit,
            "player_id": play_id
        }
        headers = {
            'x-auth-token': self.token
        }
        r = requests.get(url, headers=headers, params=querystring)
        data = []
        status = r.json()['status']
        if status == 0:
            data = r.json()['data']
            print('get_history may be successful')
            print(r.text)
        else:
            print('get_history fialed!')
            status_display(status)
            print(r.text)
        return data

    def get_history_detail(self, id):
        url = "https://api.shisanshui.rtxux.xyz/history/" + str(id)
        headers = {
            'x-auth-token': self.token
        }
        r = requests.get(url, headers=headers)

        data = []
        status = r.json()['status']
        if status == 0:
            data = r.json()['data']['detail']
            print('get_history_detail may be successful')
            status_display(status)
            print(r.text)
        else:
            print('get_history_detail fialed!')
            status_display(status)
            print(r.text)
        return data

    def get_rank(self):
        url = "https://api.shisanshui.rtxux.xyz/rank"
        headers = {
            'x-auth-token': self.token
        }
        r = requests.get(url, headers=headers)
        data = []
        data = r.json()
        print('get_rank may be successful')
        return data

def main():
    p1 = Player('sddd12', '87654321')

    # p1.register()

    p1.login()

    card = p1.game_open()
    s = card_order.AI(card) 
    p1.game_submit(s)

    data = p1.get_history(0, 20, p1.user_id)

    # data = p1.get_rank()
    # print(data)

    data = p1.get_history_detail(14785)
    # print(data)

    p1.validate_token()
    p1.logout()

if __name__ == '__main__':
    main()
