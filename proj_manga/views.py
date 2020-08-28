

from proj_manga import mod_email
from proj_manga.mod_dmzjsearch import Search_dmzj
from flask import *
from proj_manga import app

# <!--在这里总共用到了一下变量 emailmd5 username authorization email s_host s_port s_pass kindle_email-->
from proj_manga.mod_mysql import *

html_introduce = "introduce.html"
html_introduce2 = "introduce2.html"
html_logout = "logout.html"
html_loginform = "login.html"
html_loginformerr = "loginfail.html"
html_user = "user.html"
html_log = "log.html"
html_loglist = "loglist.html"
html_downlist = "downlist.html"
html_mainpage = "mainpage.html"
html_donate = "donate.html"
html_error = "error.html"
html_reg = "register.html"
html_search = "searchlist.html"




def userpage(token):
    user = GetUser(GetUsername(token))
    message = render_template(html_user, username=user['username']
                              , emailmd5=user['emailmd5']
                              , email=user['email']
                              , authorization=user['authorization']
                              , s_host=user['s_host']
                              , s_port=user['s_port']
                              , s_pass=""
                              , kindle_email=user['kindle_email'])
    return message


def checkforlogin():
    try:
        token = session['token']
    except Exception as e:
        return False
    if checkuser(token) == 0:
        return True
    else:
        return False


def checkuser(token):
    if GetUsername(token) == -1:
        return 1
    else:
        return 0


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,  # 根据访问者的IP记录访问次数
    default_limits=["5 per second"]  # 默认限制，一天最多访问200次，一小时最多访问50次
)


@app.errorhandler(429)
def toomanyrequests(e):
    return render_template(html_error, error_code="429", error_description=e), 200


@app.errorhandler(403)
def toomanyrequests(e):
    return render_template(html_error, error_code="403", error_description=e), 200


@app.errorhandler(404)
def toomanyrequests(e):
    return render_template(html_error, error_code="404", error_description=e), 200


@app.errorhandler(500)
def toomanyrequests(e):
    return render_template(html_error, error_code="500", error_description=e), 200


@app.errorhandler(414)
def toomanyrequests(e):
    return render_template(html_error, error_code="414", error_description=e), 200


@app.errorhandler(413)
def toomanyrequests(e):
    return render_template(html_error, error_code="413", error_description=e), 200


@app.errorhandler(412)
def toomanyrequests(e):
    return render_template(html_error, error_code="412", error_description=e), 200


from proj_manga.mod_file import RunCleaner


@app.before_request
def checkfilecleaner():
    RunCleaner()


@app.route('/donate')
def donate():
    return render_template(html_donate)


@app.route('/')
@app.route('/index')
def index():
    if checkforlogin():
        return render_template(html_mainpage)
    else:
        return redirect("/introduce")


@app.route('/introduce')
def introduce():
    if checkforlogin():
        return render_template(html_introduce2)
    else:
        return render_template(html_introduce)


@app.route('/user')
def user():
    try:
        token = session['token']
    except Exception as e:
        return redirect("/login")
    if checkuser(token) == 0:
        return userpage(token)
    else:
        return redirect("/login")


@app.route('/login')
@limiter.limit("3/second")
def login():
    if checkforlogin():
        return redirect("/index")
    try:
        user = request.args['user']
        passwd = request.args['pass']
        token = CheckUser(user, passwd)
        if token == -1:
            return render_template(html_loginformerr)
        else:
            session['token'] = token
            return redirect("/index")
    except KeyError as e:
        if checkforlogin():
            return redirect("/index")
        return render_template(html_loginform)


@app.route('/reg')
@limiter.limit("1/second")
def register():
    from proj_manga.mod_safety import requireChapta
    picsrc, c_hash = requireChapta()
    if checkforlogin():
        return redirect("/index")
    try:
        user = request.args['user']
        passwd = request.args['pass']
        email = request.args['email']
        chapta = request.args['chapta']
        pichapta = request.args['pichapta']
        if pass_hash(chapta.upper()) == pichapta:
            if GetUser(user)['username'] != None:
                return render_template(html_reg, errordetail="用户名重复", pichapta=picsrc, question=c_hash)
            result = UpdateUser(user, passwd, email, "", "", "未验证", "", "")
            if result != 0:
                return render_template(html_reg, errordetail="注册失败 %s" % result, pichapta=picsrc, question=c_hash)
            token = CheckUser(user, passwd)
            session['token'] = token
            return redirect("/index")
        else:
            picsrc, c_hash = requireChapta()
            return render_template(html_reg, errordetail="验证码错误", pichapta=picsrc, question=c_hash)
    except KeyError as e:
        if checkforlogin():
            return redirect("/index")
        return render_template(html_reg, errordetail="", pichapta=picsrc, question=c_hash)


@app.route('/logout')
def logout():
    session.pop('token', None)
    return render_template(html_logout)


@app.route('/testemail')
@limiter.limit("1/10second")
def testmail():
    if not checkforlogin():
        return redirect('/login')
    try:
        token = session['token']
        user = GetUser(GetUsername(token))
        s_host = user['s_host']
        s_port = user['s_port']
        s_pass = user['s_pass']
        s_email = user['email']
        result = mod_email.sendtestmail(s_email, s_host, s_port, s_pass)
        if result == 0:
            return "<meta http-equiv=\"refresh\" content=\"3;url='user'\" > 邮件发送成功，三秒后自动返回"
        else:
            return render_template(html_error, error_code="500", error_description="邮件发送失败:%s" % result)
    except Exception as e:
        return render_template(html_error, error_code="500", error_description="邮件发送失败:%s" % e)


@app.route('/search')
@limiter.limit("1/10second")
def search():
    if not checkforlogin():
        return redirect('/login')
    try:
        token = session['token']
        user = GetUser(GetUsername(token))
        auth = user['authorization']
        if auth == "未验证":
            return render_template(html_error, error_code="403",
                                   error_description="您的账号还未通过管理员验证，没有权限使用该功能，请联系管理员。")
        text = request.args['text']
        page = request.args['page']
        result = Search_dmzj(text, page)
        if result == -1:
            return render_template(html_error, error_code="500", error_description="搜索失败")
        return render_template(html_search, search=result['search'], nextpage=result['next_page'],
                               page=result['page'], table=result['table'])
    except Exception as e:
        return render_template(html_error, error_code="500", error_description="搜索失败")

@app.route('/download')
@limiter.limit("1/second")
def download():
    if not checkforlogin():
        return redirect('/login')
    try:
        token = session['token']
        user = GetUser(GetUsername(token))
        auth = user['authorization']
        if auth == "未验证":
            return render_template(html_error, error_code="403",
                                   error_description="您的账号还未通过管理员验证，没有权限使用该功能，请联系管理员。")
        url = request.args['url']
        start = request.args['from']
        end = request.args['to']
        all = request.args['all']
        sendmail = request.args['sendmail']
        merge = request.args['merge']
        logid = CreateTask(url, start, end, all, sendmail, merge, token)
        if logid == -1:
            return render_template(html_error, error_code="500", error_description="创建下载任务失败")
        else:
            return redirect('/getloglist')
    except Exception as e:
        return render_template(html_error, error_code="500", error_description="Failed: %s" % e)


@app.route('/getlog')
def getlog():
    if not checkforlogin():
        return redirect('/login')
    else:
        try:
            token = session['token']
            user = GetUser(GetUsername(token))
            auth = user['authorization']
            if auth == "未验证":
                return render_template(html_error, error_code="403",
                                       error_description="您的账号还未通过管理员验证，没有权限使用该功能，请联系管理员。")
            logid = request.args['logid']
            result = GetLog(logid, token)
            return render_template(html_log, logid=logid, log=result)
        except KeyError as e:
            return render_template(html_error, error_code="400", error_description="请求日记失败: 请求格式错误！")
        except Exception as e:
            return render_template(html_error, error_code="500", error_description="请求日记失败: Unexpected Error %s" % e)


def takeSecond(elem):
    return elem[1]


@app.route('/getloglist')
def getloglist():
    if not checkforlogin():
        return redirect('/login')
    try:
        token = session['token']
        user = GetUser(GetUsername(token))
        auth = user['authorization']
        if auth == "未验证":
            return render_template(html_error, error_code="403",
                                   error_description="您的账号还未通过管理员验证，没有权限使用该功能，请联系管理员。")
        loglist = list(GetLogListFromToken(token))
        loglist.sort(reverse=True, key=takeSecond)
        text = ""
        for item in loglist:
            username = item[0]
            logid = item[1]
            datetime = item[2].strftime('%Y-%m-%d %X')
            status = item[3]
            if (status == "failed") or (status == "running"):
                text += """
                <tr>
                    <td><div id="%s">%s</div></td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td><a href="/getlog?logid=%s">查看日志</a></td>
                    <td><a>暂无下载</a></td>
                </tr>""" \
                        % (status, status, username, logid, datetime, logid)
            elif status == "outdated":
                text += """
                <tr>
                    <td><div id="%s">%s</div></td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td><a>日志过期</a></td>
                    <td><a>暂无下载</a></td>
                </tr>""" \
                        % (status, status, username, logid, datetime)
            elif status == "queuing":
                text += """
                <tr>
                    <td><div id="%s">%s</div></td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td><a>队列中</a></td>
                    <td><a>队列中</a></td>
                </tr>""" \
                        % (status, status, username, logid, datetime)
            else:
                text += """
                <tr>
                    <td><div id="%s">%s</div></td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td><a href="/getlog?logid=%s">查看日志</a></td>
                    <td><a href="/getdownlist?logid=%s">下载</a></td>
                </tr>""" \
                        % (status, status, username, logid, datetime, logid, logid)
        return render_template(html_loglist, table=text)
    except Exception as e:
        return render_template(html_error, error_code="500", error_description="获取目录列表失败")


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    size = round(fsize, 2)
    result = "%.2f MB" % (size)
    return result


@app.route('/getdownlist')
def getdownlist():
    if not checkforlogin():
        return redirect('/login')
    try:
        token = session['token']
        user = GetUser(GetUsername(token))
        auth = user['authorization']
        if auth == "未验证":
            return render_template(html_error, error_code="403",
                                   error_description="您的账号还未通过管理员验证，没有权限使用该功能，请联系管理员。")
        logid = request.args['logid']
        result = GetLogSingle(logid, token)
        if (result['username'] != user['username']) and (user['authorization'] != "管理员"):
            return render_template(html_error, error_code="403", error_description="您没有权限下载他人的文件")
        text = ""
        if result != -1:
            path = get_value("Output_Dir") + logid
            list = os.listdir(path)
            for item in list:
                size = get_FileSize(os.path.join(os.getcwd(), get_value("Output_Dir").replace('/', '\\')) + logid +
                                    "\\" + item)
                text += """
                    <tr>
                        <td><div>
                        <i class="social fa fa-file-pdf-o" style="font-size:25px;font-weight:normal;color:#6F6F6F;"></i>&nbsp;%s
                         </div></td>
                    <td>%s</td>
                    <td><a href="/requestfile?logid=%s&file=%s">点击下载</a></td>
                    <td><a href="/send2kindle?logid=%s&file=%s">发送到kindle</a></td>
                </tr>
                """ % (item, size, logid, item, logid, item)
        return render_template(html_downlist, logid=logid, table=text)
    except Exception as e:
        return render_template(html_error, error_code="500", error_description="获取文件列表失败")


@app.route('/requestfile')
@limiter.limit("5/second")
def requestfile():
    if not checkforlogin():
        return redirect('/login')
    try:
        token = session['token']
        user = GetUser(GetUsername(token))
        auth = user['authorization']
        if auth == "未验证":
            return render_template(html_error, error_code="403",
                                   error_description="您的账号还未通过管理员验证，没有权限使用该功能，请联系管理员。")
        logid = request.args['logid']
        filename = request.args['file']
        result = GetLogSingle(logid, token)
        if (result['username'] != user['username']) and (user['authorization'] != "管理员"):
            return render_template(html_error, error_code="403", error_description="您没有权限下载他人的文件")
        try:
            path = os.path.join(os.getcwd(), get_value("Output_Dir")) + logid + "/" + filename
            return send_file(path, attachment_filename=filename)
        except Exception as e:
            return render_template(html_error, error_code="500", error_description="下载文件失败")
    except Exception as e:
        return render_template(html_error, error_code="500", error_description="下载文件失败")


@app.route('/send2kindle')
@limiter.limit("1/second")
def send2kindle():
    if not checkforlogin():
        return redirect('/login')
    try:
        token = session['token']
        user = GetUser(GetUsername(token))
        auth = user['authorization']
        if auth == "未验证":
            return render_template(html_error, error_code="403",
                                   error_description="您的账号还未通过管理员验证，没有权限使用该功能，请联系管理员。")
        s_host = user['s_host']
        s_port = user['s_port']
        s_pass = user['s_pass']
        s_email = user['email']
        kindle_email = user['kindle_email']
        valid = (s_host != "") and (s_port != "") and (s_pass != "") and (s_email != "") and (kindle_email != "")
        if not valid:
            return render_template(html_error, error_code="400", error_description="您的电子邮箱信息不正确，请更新后重试")
        logid = request.args['logid']
        filename = request.args['file']
        result = GetLogSingle(logid, token)
        if (result['username'] != user['username']) and (user['authorization'] != "管理员"):
            return render_template(html_error, error_code="403", error_description="您没有权限操作他人的文件")
        try:
            path = os.path.join(os.getcwd(), get_value("Output_Dir")) + logid + "/" + filename
            mail_result = mod_email.sendemail_file(s_email, kindle_email, s_host, s_port, s_pass, path, filename)
            if mail_result == 0:
                return "<meta http-equiv=\"refresh\" content=\"2;url='user'\" > 送信请求已发送"
            else:
                return render_template(html_error, error_code="500", error_description="送信请求发送失败")
        except Exception as e:
            return render_template(html_error, error_code="500", error_description="送信请求发送失败")
    except Exception as e:
        return render_template(html_error, error_code="500", error_description="送信请求发送失败")


def is_valid_email(email):
    ex_email = re.compile(r'^[\w][a-zA-Z1-9.]{4,19}@[a-zA-Z0-9]{2,3}.*')
    result = ex_email.match(email)
    if result:
        return 0
    else:
        return -1


@app.route('/changeemail')
@limiter.limit("1/second")
def changeemail():
    if not checkforlogin():
        return redirect('/login')
    token = session['token']
    email = request.args['email']
    s_host = request.args['s_host']
    s_port = request.args['s_port']
    s_pass = request.args['s_pass']
    kemail = request.args['kemail']
    if not is_valid_email(email) or s_host == "" or s_port == "" or s_pass == "" or not is_valid_email(kemail):
        return render_template(html_error, error_code="400", error_description="请正确且完整地填写邮箱信息。")
    username = GetUsername(token)
    if username == -1:
        return render_template(html_error, error_code="403", error_description="未知的用户token")
    user = GetUser(username)
    result = UpdateUser(username, "", email, s_host, s_pass, user['authorization'], s_port, kemail)
    if result == 0:
        return "<meta http-equiv=\"refresh\" content=\"2;url='user'\" > OK"
    else:
        return render_template(html_error, error_code="500", error_description="Failed:%s" % result)


@app.route('/setauth')
@limiter.limit("1/second")
def setauth():
    if not checkforlogin():
        return redirect('/login')
    token = session['token']
    username = request.args['user']
    auth = request.args['auth']
    if GetUser(GetUsername(token))['authorization'] != "管理员":
        return render_template(html_error, error_code="403", error_description="您没有权限操作用户组。")
    user = GetUser(username)
    if user['username'] == None:
        return render_template(html_error, error_code="400", error_description="用户不存在")
    email = user['email']
    s_host = user['s_host']
    s_port = user['s_port']
    s_pass = user['s_pass']
    k_email = user['kindle_email']
    result = UpdateUser(username, "", email, s_host, s_pass, auth, s_port, k_email)
    if result == 0:
        return "<meta http-equiv=\"refresh\" content=\"2;url='user'\" > OK"
    else:
        return render_template(html_error, error_code="500", error_description="Failed:%s" % result)