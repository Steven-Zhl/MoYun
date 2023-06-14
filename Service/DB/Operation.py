from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from Service.DB.ExtractInfo import *
from Service.utils import getConfig


class Database:
    """
    基本函数类别：get__(), getAll__(), add__(), modify__(), delete__()
    如果是添加或者修改信息时需要时间，允许传入datetime对象，否则会自动获取当前时间
    """

    def __init__(self, app: Flask):
        info = getConfig("Database")
        client = f"{info['Type'].lower()}+{info['Driver']}"
        host = info["Host"]
        port = info["Port"]
        account = info["Account"]
        password = info["Password"]
        database = info["Database"]
        URI = f"{client}://{account}:{password}@{host}:{port}/{database}"
        app.config["SQLALCHEMY_DATABASE_URI"] = URI
        self.db = SQLAlchemy(app)
        self._attachModel()

    """用户相关"""

    def addUser(self, account, password, email, telephone, role="student") -> int:
        """
        添加用户
        :param account: 用户名
        :param password: 密码(注意此时是明文，需要在函数内部进行加密)
        :param email: 邮箱
        :param telephone: 电话
        :param role: 角色
        :return:
        """
        email = None if email == "" else email
        telephone = None if telephone == "" else telephone
        user = User(account=account, password=generate_password_hash(password), signature="",
                    email=email, telephone=telephone, role=role,
                    lastLoginTime=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
        self.db.session.add(user)
        self.db.session.commit()
        return user.id

    def modifyUser(self, userID: int, **kwargs):
        """
        修改用户信息
        :param userID:
        :param kwargs:
        :return:
        """
        user = User.query.filter_by(id=userID).first()
        if not user:
            return False
        for key in kwargs:
            if hasattr(user, key):
                setattr(user, key, kwargs[key])
        self.db.session.commit()
        return True

    def modifyUserByAccount(self, account: str, password):
        """
        重置用户密码
        :param account: 用户名
        :param password: 密码
        :return:
        """
        user = User.query.filter_by(account=account).first()
        user._password = generate_password_hash(password)
        self.db.session.commit()

    @staticmethod
    def getUser(userID, withPasswd=False) -> dict or None:
        """
        根据id或account获取单个用户信息(若有多个符合，只会返回第一条)
        :return: 用户信息
        """
        info = User.query.filter_by(id=userID).first()
        if not info:
            return None
        else:
            return extractUser(info, withPasswd)

    @staticmethod
    def searchUser(keyword, withPasswd=False) -> list[dict]:
        """
        搜索用户
        :param keyword:
        :param withPasswd:
        :return:
        """
        users = User.query.filter(User.account.like(f"%{keyword}%")).all()
        if not users:
            return []
        else:
            return [extractUser(info, withPasswd) for info in users]

    @staticmethod
    def getAllUser(withPasswd=False) -> list[dict]:
        """
        获取全部用户信息
        :return: 用户信息
        """
        infoList = User.query.all()
        if not infoList:
            return []
        else:
            return [extractUser(info, withPasswd) for info in infoList]

    @staticmethod
    def getUserByAccount(account: str, withPasswd=False) -> dict or None:
        info = User.query.filter_by(account=account).first()
        if not info:
            return None
        else:
            return extractUser(info, withPasswd)

    @staticmethod
    def getAllUserByAccount(account: str, withPasswd=False) -> list[dict]:
        """
        根据id或account获取单个用户信息(返回全部)
        :return: 用户信息
        """
        infoList = User.query.filter_by(account=account).all()
        if not infoList:
            return []
        else:
            return [extractUser(info, withPasswd) for info in infoList]

    def checkLogin(self, account, password):
        usersInfo = self.getAllUserByAccount(account, withPasswd=True)
        if len(usersInfo) == 0:
            return False
        else:
            for info in usersInfo:
                if check_password_hash(info["password"], password):
                    return info["id"]
            else:
                return False

    """日志相关"""

    @staticmethod
    def getJournal(journalID: int):
        """
        根据journalID获取单个书评信息(若有多个符合，只会返回第一条)
        :return: 书评和用户信息
        """
        journal = Journal.query.filter_by(id=journalID).first()
        likeNum = JournalLike.query.filter_by(journalID=journal.id).count()
        commentNum = JournalComment.query.filter_by(journalID=journal.id).count()
        return extractJournal(journal, likeNum, commentNum)

    @staticmethod
    def getAllJournalByID(journalID: list) -> dict[dict]:
        """
        根据journalID获取单个书评信息(若有多个符合，只会返回第一条)
        :return: 书评和用户信息
        """
        journals = Journal.query.filter(Journal.id.in_(journalID)).all()
        res = {}
        for journal in journals:
            likeNum = JournalLike.query.filter_by(journalID=journal.id).count()
            commentNum = JournalComment.query.filter_by(journalID=journal.id).count()
            res[journal.id] = extractJournal(journal, likeNum, commentNum)
        return res

    @staticmethod
    def getAllJournalByAuthorID(authorID: int = None, limit=None) -> list[dict]:
        """
        根据account和authorID中的任一个获取书评信息
        :param authorID: 用户名或用户id，若为None则不限制作者
        :param limit: 限制返回的数量，0为不限制
        :return: 用户信息
        """
        if authorID is None and limit is None:  # 按时间降序排列
            journals = Journal.query.order_by(Journal.publishTime.desc()).all()
        elif authorID is None and limit is not None:
            journals = Journal.query.order_by(Journal.publishTime.desc()).limit(limit).all()
        elif authorID is not None and limit is None:
            journals = Journal.query.filter_by(authorID=authorID).order_by(Journal.publishTime.desc()).all()
        else:
            journals = Journal.query.filter_by(authorID=authorID).order_by(Journal.publishTime.desc()).limit(
                limit).all()
        res = []
        for journal in journals:
            likeNum = JournalLike.query.filter_by(journalID=journal.id).count()
            commentNum = JournalComment.query.filter_by(journalID=journal.id).count()
            res.append(extractJournal(journal, likeNum, commentNum))
        return res

    @staticmethod
    def getAllJournal():
        """
        直接获取所有书评信息
        :return:
        """
        res = []
        journals = Journal.query.order_by(Journal.publishTime.desc()).all()
        for journal in journals:
            likeNum = JournalLike.query.filter_by(journalID=journal.id).count()
            commentNum = JournalComment.query.filter_by(journalID=journal.id).count()
            res.append(extractJournal(journal, likeNum, commentNum))
        return res

    @staticmethod
    def searchJournal(keyword: str) -> list[dict]:
        """
        根据关键字搜索书评信息
        :param keyword:
        :return:
        """
        journalsInfo = Journal.query.filter(
            Journal.title.like("%" + keyword + "%") | Journal.content.like("%" + keyword + "%")).all()
        res = []
        for journal in journalsInfo:
            likeNum = JournalLike.query.filter_by(journalID=journal.id).count()
            commentNum = JournalComment.query.filter_by(journalID=journal.id).count()
            res.append({"id": journal.id,
                        "title": journal.title,
                        "firstParagraph": journal.firstParagraph,
                        "content": journal.content,
                        "publishTime": journal.publishTime,
                        "authorID": journal.authorID,
                        "bookID": journal.bookID,
                        "likeNum": likeNum,
                        "commentNum": commentNum})
        return res

    def addJournal(self, title: str, content: list, publishTime: str, authorID: int, bookID: int) -> int:
        """
        添加日志
        :return: journalID
        """
        journal = Journal(title=title,
                          firstParagraph=content[0],
                          content="\n".join(content),
                          publishTime=publishTime,
                          authorID=authorID,
                          bookID=bookID)
        self.db.session.add(journal)
        self.db.session.commit()
        return Journal.query.filter_by(title=title, authorID=authorID).first().id

    def markAllJournalCommentAsRead(self, journalID: int):
        """
        将Journal的所有Comments都标记为已读
        :param journalID:
        :return:
        """
        JournalComment.query.filter_by(journalID=journalID).update({"isRead": True})
        self.db.session.commit()

    @staticmethod
    def getJournalComments(journalID) -> list[dict]:
        """
        根据journalID获取全部关于这个书评的评论
        :return: 书评和用户信息
        """
        comments = JournalComment.query.filter_by(journalID=journalID).order_by(JournalComment.publishTime.desc()).all()
        if not comments:
            return []
        else:
            return [extractJournalComment(comment) for comment in comments]

    def addJournalComment(self, journalID, content, authorID, publishTime: str = None):
        """
        根据journalID获取单个书评信息(若有多个符合，只会返回第一条)
        :return: 书评和用户信息
        """
        if not publishTime:
            publishTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment = JournalComment(content=content, publishTime=publishTime, authorID=authorID, journalID=journalID)
        self.db.session.add(comment)
        self.db.session.commit()
        return True

    @staticmethod
    def getJournalLikeNum(journalID) -> int:
        """
        根据journalID获取点赞数
        :return: 点赞数
        """
        return JournalLike.query.filter_by(journalID=journalID).count()

    def addJournalLike(self, journalID, authorID) -> bool:
        """
        根据journalID和authorID添加点赞记录
        :return: 是否成功添加点赞记录(False说明已经存在该点赞记录)
        """
        publishTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if JournalLike.query.filter_by(journalID=journalID, authorID=authorID).first():
            return False
        else:
            like = JournalLike(journalID=journalID, authorID=authorID, publishTime=publishTime)
            self.db.session.add(like)
            self.db.session.commit()
            return True

    """书籍相关"""

    @staticmethod
    def searchBook(keyword: str) -> list[dict]:
        """
        根据关键字搜索书籍信息
        :param keyword:
        :return:
        """
        booksInfo = Book.query.filter(
            Book.title.like(f"%{keyword}%") | Book.author.like(f"%{keyword}%")).order_by(
            Book.doubanScore.desc()).all()

        return [extractBook(book) for book in booksInfo]

    @staticmethod
    def getBook(bookID: int):
        """
        根据bookID获取单个书籍信息(若有多个符合，只会返回第一条)
        :return: 书籍信息
        """
        book = Book.query.filter_by(id=bookID).first()
        return extractBook(book)

    def modifyBook(self, bookID: int, **kwargs):
        """
        根据bookID修改书籍信息
        :param bookID: bookID
        :return:
        """
        book = Book.query.filter_by(id=bookID).first()
        if not book:
            return False
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        self.db.session.commit()
        return True

    @staticmethod
    def getAllBook(limit=0) -> list[dict]:
        """
        获取全部书籍的信息
        :param limit: 限制返回的数量
        :return:
        """
        if not limit:
            books = Book.query.filter_by().order_by(Book.publishDate.desc()).all()
        else:
            books = Book.query.filter_by().order_by(Book.publishDate.desc()).limit(limit).all()
        return [extractBook(book) for book in books]

    """圈子相关"""

    def addGroup(self, name: str, description: str, founderID: int, establishTime: str = None) -> int:
        """
        添加圈子
        :return: groupID
        """
        if not establishTime:
            establishTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        group = Group(name=name, description=description, founderID=founderID, establishTime=establishTime)
        self.db.session.add(group)
        self.db.session.commit()
        return Group.query.filter_by(name=name, founderID=founderID, establishTime=establishTime).first().id

    @staticmethod
    def getGroup(groupID: int) -> dict:
        """
        根据groupID获取圈子信息(若有多个符合，只会返回第一条)
        :param groupID:
        :return:
        """
        group = Group.query.filter_by(id=groupID).first()
        return extractGroup(group)

    def modifyGroup(self, groupID: int, **kwargs):
        """
        根据groupID修改圈子信息
        :param groupID: groupID
        :return:
        """
        group = Group.query.filter_by(id=groupID).first()
        if not group:
            return False
        for key, value in kwargs.items():
            if hasattr(group, key):
                setattr(group, key, value)
        self.db.session.commit()
        return True

    @staticmethod
    def getAllGroup() -> list[dict]:
        groups = Group.query.filter_by().all()
        return [extractGroup(group) for group in groups]

    @staticmethod
    def searchGroup(keyword: str) -> list[dict]:
        """
        根据关键字搜索圈子信息
        :param keyword:
        :return:
        """
        groups = Group.query.filter(
            Group.name.like(f"%{keyword}%") | Group.description.like(f"%{keyword}%")).all()
        return [extractGroup(group) for group in groups]

    """圈子内的帖子"""

    @staticmethod
    def getGroupAllDiscussion(groupID: int) -> list[dict]:
        """
        根据groupID获取圈子内所有帖子的信息
        :param groupID:
        :return:
        """
        discussions = GroupDiscussion.query.filter_by(groupID=groupID).order_by(GroupDiscussion.postTime.desc()).all()
        return [extractGroupDiscussion(discussion) for discussion in discussions]

    def markAllDiscussionAsRead(self, groupID: int):
        """
        标记所有帖子为已读
        :param groupID:
        :return:
        """
        GroupDiscussion.query.filter_by(groupID=groupID).update({"isRead": True})
        self.db.session.commit()

    def addGroupDiscussion(self, posterID: int, groupID: int, postTime: str, title: str, content: str)->int:
        """
        添加帖子
        :param posterID:
        :param groupID:
        :param postTime:
        :param title:
        :param content:
        :return:
        """
        discussion = GroupDiscussion(posterID=posterID, groupID=groupID, postTime=postTime, title=title,
                                     content=content)
        self.db.session.add(discussion)
        self.db.session.commit()
        return GroupDiscussion.query.filter_by(posterID=posterID, groupID=groupID, postTime=postTime).first().id

    @staticmethod
    def getGroupDiscussion(discussID: int) -> dict:
        """
        根据discussID获取帖子信息
        :param discussID:
        :return:
        """
        discussion = GroupDiscussion.query.filter_by(id=discussID).first()
        return extractGroupDiscussion(discussion)

    def deleteGroupDiscussion(self, discussID: int) -> bool:
        """
        根据discussID删除帖子
        :param discussID:
        :return:
        """
        discussion = GroupDiscussion.query.filter_by(id=discussID).first()
        if not discussion:
            return False
        self.db.session.delete(discussion)
        self.db.session.commit()
        return True

    """帖子的回复相关"""

    def addGroupDiscussionReply(self, discussionID: int, authorID: int, content: str, replyTime: str = None) -> bool:
        if not replyTime:
            replyTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reply = GroupDiscussionReply(authorID=authorID, discussionID=discussionID, replyTime=replyTime, content=content)
        self.db.session.add(reply)
        self.db.session.commit()
        return True

    @staticmethod
    def getGroupDiscussionReplies(discussionID: int) -> list[dict]:
        reply = GroupDiscussionReply.query.filter_by(discussionID=discussionID).order_by(
            GroupDiscussionReply.replyTime.asc()).all()
        return [extractGroupDiscussionReply(reply) for reply in reply]

    @staticmethod
    def getGroupDiscussionRepliesNum(discussionID: int) -> int:
        return GroupDiscussionReply.query.filter_by(discussionID=discussionID).count()

    def markAllDiscussionReplyAsRead(self, discussionID: int):
        """
        标记所有回复为已读
        :param discussionID:
        :return:
        """
        GroupDiscussionReply.query.filter_by(discussionID=discussionID).update({"isRead": True})
        self.db.session.commit()

    @staticmethod
    def getGroupReplies(groupID: int, limit=5) -> list[dict]:
        """
        按照时间降序获取圈子内所有回复
        :param groupID:
        :return:
        """
        discussionID = [discussion.id for discussion in GroupDiscussion.query.filter_by(groupID=groupID).all()]
        replies = GroupDiscussionReply.query.filter(GroupDiscussionReply.discussionID.in_(discussionID)).order_by(
            GroupDiscussionReply.replyTime.desc()).limit(limit).all()
        return [extractGroupDiscussionReply(reply) for reply in replies]

    """圈子成员相关"""

    @staticmethod
    def getAllGroupUser(groupID: int) -> list[dict]:
        user = GroupUser.query.filter_by(groupID=groupID).order_by(GroupUser.joinTime.desc()).all()
        return [extractGroupUser(user) for user in user]

    @staticmethod
    def getGroupUserNum(groupID: int) -> int:
        return GroupUser.query.filter_by(groupID=groupID).count()

    @staticmethod
    def getGroupDiscussionNum(groupID: int) -> int:
        return GroupDiscussion.query.filter_by(groupID=groupID).count()

    """错误响应相关"""

    @staticmethod
    def getError(errorCode: int) -> dict:
        """
        根据errorCode获取错误信息
        :param errorCode: 错误码
        :return: 错误信息
        """
        error = Error.query.filter_by(errorCode=errorCode).first()
        return {"errorCode": error.errorCode,
                "title": error.title,
                "title_en": error.title_en,
                "content": error.content,
                "publishTime": error.publishTime,
                "authorID": error.authorID,
                "referenceLink": error.referenceLink}

    """消息相关"""

    def getAllUnreadMessage(self, userID: int) -> dict[str, list[dict]]:
        """
        获取用户的所有未读消息(各类消息，包括书评回复、帖子回复、新私信、圈子新帖)
        :param userID:
        :return:
        """
        # 书评回复
        journalComments = JournalComment.query.filter_by(authorID=userID, isRead=False).all()
        journalComments = [extractJournalComment(comment) for comment in journalComments]
        for comment in journalComments:
            comment["account"] = self.getUser(comment["authorID"])['account']
        # 圈子新帖
        groupID = [item.id for item in Group.query.filter_by(founderID=userID).all()]
        groupDiscussions = GroupDiscussion.query.filter(GroupDiscussion.groupID.in_(groupID),
                                                        GroupDiscussion.isRead == False).all()
        groupDiscussions = [extractGroupDiscussion(discussion) for discussion in groupDiscussions]
        for discussion in groupDiscussions:
            discussion["account"] = self.getUser(discussion["posterID"])['account']
        # 帖子回复
        discussionID = [item.id for item in GroupDiscussion.query.filter_by(posterID=userID).all()]
        discussionReplies = GroupDiscussionReply.query.filter(
            GroupDiscussionReply.discussionID.in_(discussionID), GroupDiscussionReply.isRead == False).all()
        discussionReplies = [extractGroupDiscussionReply(reply) for reply in discussionReplies]
        for reply in discussionReplies:
            reply["account"] = self.getUser(reply["authorID"])['account']
        # 私信
        chats = Chat.query.filter_by(receiverID=userID, isRead=False).all()
        chats = [extractChat(chat) for chat in chats]
        for chat in chats:
            chat["account"] = self.getUser(chat["senderID"])['account']
        return {"journalComment": journalComments,
                "groupDiscussion": groupDiscussions,
                "discussionReply": discussionReplies,
                "chat": chats}

    @staticmethod
    def getAllUnreadMessageNum(userID: int) -> dict[str, int]:
        """
        获取用户的所有未读消息数量(各类消息，包括书评回复、帖子回复、新私信、圈子新帖)
        :param userID:
        :return:
        """
        # 书评回复
        journalCommentsNum = JournalComment.query.filter_by(authorID=userID, isRead=False).count()
        # 圈子新帖
        groupID = [item.id for item in Group.query.filter_by(founderID=userID).all()]
        groupDiscussionsNum = GroupDiscussion.query.filter(
            GroupDiscussion.groupID.in_(groupID), GroupDiscussion.isRead == False).count()
        # 帖子回复
        discussionID = [item.id for item in GroupDiscussion.query.filter_by(posterID=userID).all()]
        discussionRepliesNum = GroupDiscussionReply.query.filter(
            GroupDiscussionReply.discussionID.in_(discussionID), GroupDiscussionReply.isRead == False).count()
        # 私信
        chatsNum = Chat.query.filter_by(receiverID=userID, isRead=False).count()
        return {"journalComment": journalCommentsNum,
                "groupDiscussion": groupDiscussionsNum,
                "discussionReply": discussionRepliesNum,
                "chat": chatsNum}

    """数据模型"""

    def _attachModel(self):
        global User, Book, Journal, JournalComment, JournalLike, Group, GroupDiscussion, GroupUser, GroupDiscussionReply
        global Error, Chat

        class User(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            account = self.db.Column(self.db.String(24), unique=True)
            password = self.db.Column(self.db.String(128), unique=False)
            signature = self.db.Column(self.db.String(128), unique=False)
            email = self.db.Column(self.db.String(120), unique=False)
            telephone = self.db.Column(self.db.String(11), unique=False)
            lastLoginTime = self.db.Column(self.db.DateTime, unique=False)
            role = self.db.Column(self.db.Enum("student", "teacher", "admin"), unique=False)

            def __init__(self, account, password, signature, email, telephone, lastLoginTime, role):
                self.account = account
                self.password = password
                self.signature = signature
                self.email = email
                self.telephone = telephone
                self.lastLoginTime = lastLoginTime
                self.role = role

        class Book(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            isbn = self.db.Column(self.db.String(32), unique=True)
            title = self.db.Column(self.db.String(128), unique=False)
            originTitle = self.db.Column(self.db.String(128), unique=False)
            subtitle = self.db.Column(self.db.String(128), unique=False)
            author = self.db.Column(self.db.String(128), unique=False)
            page = self.db.Column(self.db.Integer, unique=False)
            publishDate = self.db.Column(self.db.String(24), unique=False)
            publisher = self.db.Column(self.db.String(32), unique=False)
            description = self.db.Column(self.db.Text, unique=False)
            doubanScore = self.db.Column(self.db.Float, unique=False)
            doubanID = self.db.Column(self.db.String(24), unique=False)
            type = self.db.Column(
                self.db.Enum("马列主义、毛泽东思想、邓小平理论", "哲学、宗教", "社会科学总论", "政治、法律", "军事", "经济",
                             "文化、科学、教育、体育", "语言、文字", "文学", "艺术", "历史、地理", "自然科学总论",
                             "数理科学和化学", "天文学、地球科学", "生物科学", "医药、卫生", "农业科学", "工业技术",
                             "交通运输", "航空、航天", "环境科学、安全科学", "综合性图书"), unique=False)

            def __init__(self, isbn, title, originTitle, subtitle, author, page, publishDate, publisher, description,
                         doubanScore, doubanID, type):
                self.isbn = isbn
                self.title = title
                self.originTitle = originTitle
                self.subtitle = subtitle
                self.author = author
                self.page = page
                self.publishDate = publishDate
                self.publisher = publisher
                self.description = description
                self.doubanScore = doubanScore
                self.doubanID = doubanID
                self.type = type

        class Journal(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            title = self.db.Column(self.db.String(128), unique=False)
            firstParagraph = self.db.Column(self.db.Text, unique=False)
            content = self.db.Column(self.db.Text, unique=False)
            publishTime = self.db.Column(self.db.DateTime, unique=False)
            authorID = self.db.Column(self.db.Integer, unique=False)
            bookID = self.db.Column(self.db.Integer, unique=False)

            def __init__(self, title, firstParagraph, content, publishTime, authorID, bookID):
                self.title = title
                self.firstParagraph = firstParagraph
                self.content = content
                self.publishTime = publishTime
                self.authorID = authorID
                self.bookID = bookID

        class JournalComment(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            publishTime = self.db.Column(self.db.DateTime, unique=False)
            authorID = self.db.Column(self.db.Integer, unique=False)
            journalID = self.db.Column(self.db.Integer, unique=False)
            content = self.db.Column(self.db.Text, unique=False)
            isRead = self.db.Column(self.db.Boolean, nullable=False, default=False)

            def __init__(self, publishTime, authorID, journalID, content):
                self.publishTime = publishTime
                self.authorID = authorID
                self.journalID = journalID
                self.content = content

        class JournalLike(self.db.Model):
            authorID = self.db.Column(self.db.Integer, unique=False)
            journalID = self.db.Column(self.db.Integer, unique=False)
            __table_args__ = (self.db.PrimaryKeyConstraint('authorID', 'journalID'),)  # 让authorID和journalID作为联合主键
            publishTime = self.db.Column(self.db.DateTime, unique=False)

            def __init__(self, authorID, journalID, publishTime):
                self.authorID = authorID
                self.journalID = journalID
                self.publishTime = publishTime

        class Group(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            name = self.db.Column(self.db.String(32), unique=True)
            founderID = self.db.Column(self.db.Integer, unique=False)
            description = self.db.Column(self.db.Text, unique=False)
            establishTime = self.db.Column(self.db.DateTime, unique=False)

            def __init__(self, name, founderID, description, establishTime):
                self.name = name
                self.founderID = founderID
                self.description = description
                self.establishTime = establishTime

        class GroupDiscussion(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            posterID = self.db.Column(self.db.Integer, unique=False)
            groupID = self.db.Column(self.db.Integer, unique=False)
            postTime = self.db.Column(self.db.DateTime, unique=False)
            title = self.db.Column(self.db.String(256), unique=False)
            content = self.db.Column(self.db.Text, unique=False)
            isRead = self.db.Column(self.db.Boolean, nullable=False, default=False)

            def __init__(self, posterID, groupID, postTime, title, content):
                self.posterID = posterID
                self.groupID = groupID
                self.postTime = postTime
                self.title = title
                self.content = content

        class GroupUser(self.db.Model):
            userID = self.db.Column(self.db.Integer, unique=False)
            groupID = self.db.Column(self.db.Integer, unique=False)
            __table_args__ = (self.db.PrimaryKeyConstraint('userID', 'groupID'),)  # 联合主键
            joinTime = self.db.Column(self.db.DateTime, unique=False)

            def __init__(self, userID, groupID, joinTime):
                self.userID = userID
                self.groupID = groupID
                self.joinTime = joinTime

        class GroupDiscussionReply(self.db.Model):
            authorID = self.db.Column(self.db.Integer, unique=False)
            discussionID = self.db.Column(self.db.Integer, unique=False)
            replyTime = self.db.Column(self.db.DateTime, unique=False)
            __table_args__ = (self.db.PrimaryKeyConstraint('authorID', 'discussionID', 'replyTime'),)  # 联合主键
            content = self.db.Column(self.db.Text, unique=False)
            isRead = self.db.Column(self.db.Boolean, nullable=False, default=False)

            def __init__(self, authorID, discussionID, replyTime, content):
                self.authorID = authorID
                self.discussionID = discussionID
                self.replyTime = replyTime
                self.content = content

        class Error(self.db.Model):
            errorCode = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            title = self.db.Column(self.db.String(128), unique=False)
            title_en = self.db.Column(self.db.String(128), unique=False)
            content = self.db.Column(self.db.Text, unique=False)
            publishTime = self.db.Column(self.db.DateTime, unique=False)
            authorID = self.db.Column(self.db.Integer, unique=False)
            referenceLink = self.db.Column(self.db.String(128), unique=False)

            def __init__(self, title, title_en, content, publishTime, authorID, referenceLink):
                self.title = title
                self.title_en = title_en
                self.content = content
                self.publishTime = publishTime
                self.authorID = authorID
                self.referenceLink = referenceLink

        class Chat(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True, autoincrement=True)
            senderID = self.db.Column(self.db.Integer, nullable=False)
            receiverID = self.db.Column(self.db.Integer, nullable=False)
            content = self.db.Column(self.db.Text, nullable=False)
            sendTime = self.db.Column(self.db.DateTime, nullable=False)
            isRead = self.db.Column(self.db.Boolean, nullable=False, default=False)

            def __init__(self, senderID, receiverID, content, sendTime):
                self.senderID = senderID
                self.receiverID = receiverID
                self.content = content
                self.sendTime = sendTime
