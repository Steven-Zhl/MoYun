__doc__ = """数据库提取服务，所有从数据库提取数据的函数都在这里实现"""


def extractUser(user, withPassword=False):
    """
    提取用户信息
    :param user: 用户对象
    :param withPassword: 是否返回密码
    """
    if withPassword:
        return {"id": user.id,
                "account": user.account,
                "password": user.password,
                "signature": user.signature,
                "email": user.email,
                "telephone": user.telephone,
                "role": user.role}
    else:
        return {"id": user.id,
                "account": user.account,
                "signature": user.signature,
                "email": user.email,
                "telephone": user.telephone,
                "role": user.role}


def extractJournal(journal, likeNum: int, commentNum: int):
    """
    提取日志信息
    :param journal: 日志对象
    :param likeNum: 点赞数
    :param commentNum: 评论数
    """
    return {"id": journal.id,
            "title": journal.title,
            "firstParagraph": journal.firstParagraph,
            "content": journal.content.split("\n"),
            "publishTime": journal.publishTime,
            "authorID": journal.authorID,
            "bookID": journal.bookID,
            "likeNum": likeNum,
            "commentNum": commentNum}


def extractJournalComment(comment):
    """
    提取日志评论信息
    :param comment: 日志评论对象
    """
    return {"id": comment.id,
            "journalID": comment.journalID,
            "authorID": comment.authorID,
            "content": comment.content,
            "publishTime": comment.publishTime,
            "isRead": comment.isRead}


def extractBook(book) -> dict:
    return {"id": book.id,
            "isbn": book.isbn,
            "title": book.title,
            "originTitle": book.originTitle,
            "subtitle": book.subtitle,
            "author": book.author,
            "page": book.page,
            "publishDate": book.publishDate,
            "publisher": book.publisher,
            "description": book.description,
            "doubanScore": book.doubanScore,
            "doubanID": book.doubanID,
            "type": book.type}


def extractGroup(group) -> dict:
    return {"id": group.id,
            "name": group.name,
            "description": group.description,
            "createTime": group.createTime,
            "creatorID": group.creatorID}


def extractGroupUser(groupUser) -> dict:
    return {"userID": groupUser.userID,
            "groupID": groupUser.groupID,
            "joinTime": groupUser.joinTime}


def extractGroupDiscussion(groupDiscussion) -> dict:
    return {"id": groupDiscussion.id,
            "groupID": groupDiscussion.groupID,
            "posterID": groupDiscussion.posterID,
            "postTime": groupDiscussion.postTime,
            "title": groupDiscussion.title,
            "content": groupDiscussion.content,
            "isRead": groupDiscussion.isRead}


def extractGroupDiscussionReply(reply) -> dict:
    return {"authorID": reply.authorID,
            "discussionID": reply.discussionID,
            "replyTime": reply.replyTime,
            "content": reply.content,
            "isRead": reply.isRead}


def extractError(error) -> dict:
    return {"errorCode": error.errorCode,
            "title": error.title,
            "title_en": error.title_en,
            "content": error.content,
            "publishTime": error.publishTime,
            "authorID": error.authorID,
            "referenceLink": error.referenceLink}


def extractChat(char) -> dict:
    return {"id": char.id,
            "senderID": char.senderID,
            "receiverID": char.receiverID,
            "content": char.content,
            "sendTime": char.sendTime,
            "isRead": char.isRead}
