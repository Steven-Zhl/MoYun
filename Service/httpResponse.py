from flask import Flask, abort, render_template

from Service.File.File import FileMgr

__doc__ = """自定义HTTP响应，主要包括自定义错误页面等"""


def customizeHttpResponse(app: Flask, fileMgr: FileMgr,db):
    @app.route("/errorSample/<int:errorCode>", methods=["GET"])
    def errorSample(errorCode):
        """演示自定义错误页面而创建的路由，可以通过/errorSample/<int:errorCode>访问，其中errorCode为自定义的错误码"""
        abort(errorCode)  # 抛出异常，对应的异常将会触发

    @app.errorhandler(404)
    def page_not_found(error):
        content = db.getError(error.code)
        author = db.getUser(content['authorID'])
        profilePhoto = fileMgr.getProfilePhotoPath(author['id'])
        errorImage = fileMgr.getErrorImagePath(error.code)
        return render_template('error.html', content=content, author=author, profilePhoto=profilePhoto,
                               errorCode=error.code, errorImage=errorImage), 404

    @app.errorhandler(418)
    def im_a_teapot(error):
        content = db.getError(error.code)
        author = db.getUser(content['authorID'])
        profilePhoto = fileMgr.getProfilePhotoPath(author['id'])
        errorImage = fileMgr.getErrorImagePath(error.code)
        return render_template('error.html', content=content, author=author, profilePhoto=profilePhoto,
                               errorCode=error.code, errorImage=errorImage), 418

    @app.errorhandler(500)
    def internal_server_error(error):
        content = db.getError(error.code)
        author = db.getUser(content['authorID'])
        profilePhoto = fileMgr.getProfilePhotoPath(author['id'])
        errorImage = fileMgr.getErrorImagePath(error.code)
        return render_template('error.html', content=content, author=author, profilePhoto=profilePhoto,
                               errorCode=error.code, errorImage=errorImage), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        content = db.getError(error.code)
        author = db.getUser(content['authorID'])
        profilePhoto = fileMgr.getProfilePhotoPath(author['id'])
        errorImage = fileMgr.getErrorImagePath(error.code)
        return render_template('error.html', content=content, author=author, profilePhoto=profilePhoto,
                               errorCode=error.code, errorImage=errorImage), 503
