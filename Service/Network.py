import re
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

from bs4 import BeautifulSoup
from requests import get as rget

from Service.utils import getConfig

__doc__ = """提供网络服务"""


class Mail:
    """不使用Flask自带的邮件功能，使用smtplib+emails完成邮件发送(主要是发验证码)"""

    def __init__(self):
        info = getConfig('E-Mail')
        self._host = info['Host']  # 邮件服务器
        self._port = info['Port']  # 服务器端口
        self._username = info['Username']  # 邮箱账号
        self._password = info['Password']  # 邮箱密码
        self._sender = info['Sender']  # 发件人
        self.captchaPattern = """
        <h1>尊敬的用户：</h1>
        <p>您正在请求重设密码，为保证您的账号安全，需要根据邮箱验证码确定是您本人操作。</p>
        <p>您的验证码为：</p>
        <br><h2>{}</h2>
        <p>验证码10分钟内有效，请及时操作。</p>
        <p>如果这不是您本人的操作，请忽略此邮件。</p>
        <p></p>
        <p align="right">此致</p>
        <p align="right">墨韵平台 Steven</p>"""

    def sendCaptcha(self, receiver: str, captcha: str or int) -> bool:
        """发送验证码"""
        if isinstance(captcha, int):
            captcha = str(captcha)
        content = self.captchaPattern.format(captcha)
        message = MIMEText(content, 'html', 'utf-8')
        message['Subject'] = "墨韵 - 验证码"
        message['From'] = self._sender
        message['To'] = receiver
        return self._send(receiver, message)

    def _send(self, receivers: str or list, message: MIMEText) -> bool:
        try:
            smtpObj = SMTP_SSL(self._host, self._port)
            smtpObj.set_debuglevel(1)
            # 登录到服务器
            smtpObj.login(self._username, self._password)
            # 发送
            smtpObj.sendmail(self._sender, [receivers], message.as_string())
            # 退出
            smtpObj.quit()
            return True
        except SMTPException as e:
            print(e)
            return False


class API:
    """调用第三方API"""

    def __init__(self):
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 ' \
                  'Safari/537.36 Edg/113.0.1774.57'

    @staticmethod
    def getWeather_YiKeTianQi(IP: str) -> dict:
        """
        调用一刻天气API，获取用户当地的天气。
        返回举例：{'city': '昆明', 'weather': '晴', 'temperature': '28', 'temperature_range': ('26', '31'), 'wind': '东北风3级'}
        :param IP: 用户请求的IP地址
        :return: {'city': str, 'weather': str, 'temperature': int, 'temperature_range': (int, int), 'wind': str}
        """
        config = getConfig('YiketianqiAPI')
        r = rget("https://v0.yiketianqi.com/api",
                 params={"unescape": 1, "ip": IP,
                         "version": config["version"], "appid": config["appid"], "appsecret": config["appsecret"]})

        r = r.json()
        return {'city': r['city'],
                'weather': r['wea'],
                'temperature': r['tem'],
                'temperature_range': (r['tem2'], r['tem1']),
                'wind': r['win'] + r['win_speed']}

    def getBookInfo_Douban(self, doubanID) -> dict:
        """
        调用豆瓣API，获取图书信息
        :param doubanID: 豆瓣图书的ID
        :return: 图书信息
        """
        if not isinstance(doubanID, str):
            doubanID = str(doubanID)
        r = rget(f"https://book.douban.com/subject/{doubanID}", headers={"User-Agent": self.UA})
        HTML = r.text
        r.close()
        soup = BeautifulSoup(HTML, 'html.parser')

        title = soup.find('span', attrs={'property': 'v:itemreviewed'}).text  # 标题
        score = soup.find('strong', attrs={'class': 'll rating_num'}).text.strip()  # 豆瓣评分
        # 图书元信息
        metaInfo = {}
        htmlInfo = soup.find('div', id='info').text.split('\n')
        htmlInfo = [i.strip() for i in htmlInfo if not re.fullmatch(' *', i)]

        i, j = 0, 0
        while i < len(htmlInfo):
            if re.fullmatch('.+:', htmlInfo[i]):  # 一个单独的key
                k = htmlInfo[i][:-1]
                v = ""
                j = i + 1  # value从下一个段开始
                while j < len(htmlInfo) and not re.fullmatch('.+:.*', htmlInfo[j]):  # 找到下一个key
                    v += htmlInfo[j]
                    j += 1
                metaInfo[k] = v
                i = j
            elif re.fullmatch('.+:.+', htmlInfo[i]):  # key:value形式的内容
                k, v = htmlInfo[i].split(':')
                metaInfo[k] = v.strip()
                i += 1
            else:
                i += 1

        # 图书简介
        intro = soup.find('span', attrs={'class': 'all hidden'})
        introduction = [i.text.strip() for i in intro.find_all('p')]
        introduction = '\n'.join(introduction)

        return {'isbn': metaInfo.get('ISBN'),
                'title': title,
                'originTitle': metaInfo.get('原作名'),
                'author': metaInfo.get('作者'),
                'page': metaInfo.get('页数'),
                'publishDate': metaInfo.get('出版年'),
                'publisher': metaInfo.get('出版社'),
                'description': introduction,
                'doubanScore': score,
                'doubanID': doubanID}
