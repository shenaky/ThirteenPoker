# -*- coding:utf-8 -*-

import requests
import json



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
        self.registered = False
        self.logged = False
        self.id = None
        self.cards = None

    def show(self):
        print()
        print(self.user)
        print(self.psw)
        print(self.user_id)
        print(self.token)
        print(self.register)
        print(self.logged)
        print(self.id)
        print(self.cards)
        print()
    # 注册

    def register(self):
        # 访问api
        r = register_(self.user, self.psw)
        status = r.json()['status']
        if status == 0 and 'user_id' in r.json()['data']:
            self.user_id = r.json()['data']['user_id']
            self.registered = True
            print('register may be successful')
            print(r.text)
        else:
            print('register fialed!')
            status_display(status)
            print(r.text)
            

    # 登录
    def login(self):
        r = login_(self.user, self.psw)
        status = r.json()['status']
        if status == 0 and 'user_id' in r.json()['data']:
            self.token = r.json()['data']['token']
            print(self.logged)
            self.logged = True
            print(self.logged)
            print('Login may be successful')
            print(r.text)
            self.show()
        else:
            print('login fialed!')
            status_display(status)
            print(r.text)

    # 注销
    def logout(self):
        r = logout_(self.token)
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
        r = validate_(self.token)
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
        return self.logged

    # 开局
    def game_open(self):
        r = game_open_(self.token)
        status = r.json()['status']
        if status == 0:
            self.id = r.json()['data']['id']
            self.cards = r.json()['data']['card']
        else:
            print('game_open fialed!')
            status_display(status)
            print(r.text)
        return self.cards

    # 出牌
    def game_submit(self, submit_card):
        r = game_submit_(self.token, self.id, submit_card)
        status = r.json()['status']
        if status != 0:
            print('game_submit fialed!')
            status_display(status)
            print(r.text)

    # 历史
    def get_history(self, page, limit, play_id):
        data = []
        r = history(self.taken, page, limit, play_id)
        status = r.json()['status']
        if status == 0:
            data = r.json()['data']
        else:
            print('get_history fialed!')
            status_display(status)
            print(r.text)
        return data

    def get_history_detail(self, id):
        r = history_detail(self.taken, id)
        status = r.json()['status']
        if status == 0:
            data = r.json()['data']
        else:
            print('get_history_detail fialed!')
            status_display(status)
            print(r.text)

    def get_rank(self):
        pass


# 注册


def register_(user, psw):
    url = 'https://api.shisanshui.rtxux.xyz/auth/register'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'username': user,
        'password': psw
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r

# 登录验证


def validate_(token):
    url = 'https://api.shisanshui.rtxux.xyz/auth/validate'
    headers = {
        'X-Auth-Token': token
    }
    r = requests.get(url, headers=headers)
    return r

# 注销


def logout_(token):
    url = "https://api.shisanshui.rtxux.xyz/auth/logout"
    headers = {
        'x-auth-token': token
    }
    r = requests.post(url, headers=headers)
    return r

# 登录


def login_(user, psw):
    url = "https://api.shisanshui.rtxux.xyz/auth/login"
    headers = {
        'content-type': 'application/json'
    }
    data = {
        "username": user,
        "password": psw
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r

# 开启战局


def game_open_(token):
    url = "https://api.shisanshui.rtxux.xyz/game/open"
    headers = {
        'x-auth-token': token
    }
    r = requests.post(url, headers=headers)
    return r

# 出牌


def game_submit_(token, user_id, card):
    url = "https://api.shisanshui.rtxux.xyz/game/submit"
    payload = {
        'id': user_id,
        'card': card
    }
    headers = {
        'content-type': "application/json",
        'x-auth-token': token
    }
    r = requests.post(url, data=payload, headers=headers)
    return r

# 历史战局列表


def history(token, page, limit, play_id):
    url = "https://api.shisanshui.rtxux.xyz/history"
    querystring = {
        "page": page,
        "limit": limit,
        "player_id": play_id
    }
    headers = {
        'x-auth-token': token
    }
    r = requests.get(url, headers=headers, params=querystring)
    return r

# 历史战局详情


def history_detail(token, id):
    url = "https://api.shisanshui.rtxux.xyz/history/" + id
    headers = {
        'x-auth-token': token
    }
    r = requests.get(url, headers=headers)
    return r


def main():
    p1 = Player('te222d3', '12345678')

 #   p1.register()

    p1.login()

    p1.validate_token()

    p1.logout()

    p1.show()

if __name__ == '__main__':
    main()
