from datetime import datetime, timedelta
import os
import yaml


def getConfig(category: str = None, key: str = None) -> dict or str or int:
    """
    获取配置文件中的配置项(优先读取myConfig.yaml，若不存在则读取config.yaml)
    :param category: 配置项类别
    :param key: 配置项key
    :return:
    """
    if os.path.exists(os.path.join(os.getcwd(), "myConfig.yaml")):
        with open("myConfig.yaml", "r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    else:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    if category is None or category not in config:
        return config
    else:
        if key is None or key not in config[category]:
            return config[category]
        else:
            return config[category][key]


class Time:
    """使用该类处理时间的目的是应对服务器和客户端时区不同的情况。"""
    _host_time_zone = 0  # UTC+0
    _client_time_zone = {'zh-CN': 8}  # UTC+8，东8区

    @classmethod
    def getClientNow(cls, region: str = "zh-CN", time_format: str = "datetime") -> str:
        """
        获取客户端当前时间
        :param region: 地区
        :param time_format: 时间格式
        :return:
        """
        host_now = datetime.utcnow()  # 服务器时间
        client_now = host_now + timedelta(hours=cls._client_time_zone[region])  # 客户端时间
        if time_format == "datetime":
            return client_now.now().strftime("%Y-%m-%d %H:%M:%S")
        elif time_format == "date":
            return client_now.now().strftime("%Y-%m-%d")
        elif time_format == "time":
            return client_now.now().strftime("%H:%M:%S")
        else:
            raise Exception("Invalid format")
