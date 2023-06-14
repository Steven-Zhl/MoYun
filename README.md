# MoYun

> “墨韵”在线读书交流平台项目，是软件工程课程的大作业，也同样打算作为一个长期的个人项目来维护。

## 功能

* 账号管理：注册、登录、登出、找回密码(需要配置邮箱服务)、修改个人信息、查看他人信息
* 书评：写书评、书评点赞、书评回复、书评搜索
* 书籍：书籍搜索、书籍详情
* 圈子：创建圈子、查看圈子详情、修改圈子信息(仅限管理员)
  * 帖子：发表新帖、回帖

### 特色功能

* 自定义Error页面
* 首页引入天气和“今日诗词”API
* 消息中心：整合书评回复、圈子新帖、帖子回复、私信等消息

## 部署指南

* git clone整个项目
* 安装依赖
  ```shell
  pip install -r requirements.txt
  ```
* 按照自身情况修改[`config.yaml`](/config.yaml)(建议将其拷贝一份为`myConfig.yaml`，并在这个文件中修改配置)
* 执行[`init_db.py`](/init_db.py)脚本，初始化数据库
  ```shell
  python init_db.py
  ```
* 执行`app.py`，运行主程序：
  * `python app.py`(常规执行)
  * `nohup python app.py`(仅限Linux，通过SSH远程启动服务器的服务时，使用这种方式可以在断开SSH连接后继续运行)
* 此时便可通过`127.0.0.1:{您预设的端口}`访问网站，如果是服务器端，请自行配置反向代理和DNS解析等服务。

### 运行环境

> 该项目在Windows 11 专业版 22H2和Ubuntu 20.04 LTS上测试通过。

* Python 3.11.3
* Flask 2.0.2
* MySQL 8.0.30

## 注意事项

* 部署路径请全英文，但数据库中的内容允许中文、其他语言甚至Unicode表情。
* `/home`页面使用了2个免费API：[今日诗词](https://www.jinrishici.com/)
  和[一刻天气](https://tianqiapi.com/index/doc?version=v61)
  * 一刻天气可免费试用2000次，需要注册账号后申请，申请后请在`config.yaml`中配置相关参数以使用；
    * 另外，该API通过IP来判断城市，仅限大陆地区，对于其他地区IP则显示北京天气；但我们租用的Azure服务器架设在香港，您如果通过代理访问的话通常只会显示北京的天气。
  * 今日诗词无需申请key，但每秒只能访问1次。

## 后记

* 由于时间和精力有限，有些软件设计说明书中的功能并未实现。比如添加书籍、圈子成员管理、私信等功能......该项目距离完善还有很长的路。
* Flask的数据库连接有两种实现方式，

## Reference

### 资源来源

* HTML模板
  * [Dimension | HTML5 UP](https://html5up.net/dimension)
  * [Future Imperfect | HTML5 UP](https://html5up.net/future-imperfect)
* Logo设计：[AIDesign](https://ailogo.qq.com/guide/brandname)
* 第三方API
  * [今日诗词](https://www.jinrishici.com/)
  * [一刻天气](https://tianqiapi.com/index/doc?version=v61)

### 参考资料

* [欢迎来到 Flask 的世界 — Flask中文文档(2.1.x)](https://dormousehole.readthedocs.io/en/latest/index.html)
* [Flask 教程_w3cschool](https://www.w3cschool.cn/flask/)
* [CSS：层叠样式表 | MDN](https://developer.mozilla.org/zh-CN/docs/Web/CSS)
* [HTTP 响应状态码 - HTTP | MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)