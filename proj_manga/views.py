from proj_manga import mod_email
from proj_manga.mod_dmzjsearch import Search_dmzj
from proj_manga.mod_imports import *
from flask import *
from proj_manga import app
# <!--在这里总共用到了一下变量 emailmd5 username authorization email s_host s_port s_pass kindle_email-->
from proj_manga.mod_mysql import *

html_index = "index.html"
html_logout = "logout.html"
html_loginform = "login.html"
html_loginformerr = "loginfail.html"
html_user = "user.html"
html_log = "log.html"
html_loglist = "loglist.html"

def userpage(token):
    user = GetUser(GetUsername(token))
    message = render_template(html_user, username=user['username']
                              , emailmd5=user['emailmd5']
                              , email=user['email']
                              , authorization=user['authorization']
                              , s_host=user['s_host']
                              , s_port=user['s_port']
                              , s_pass=user['s_pass']
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


@app.route('/')
@app.route('/index')
def index():
    return render_template(html_index)


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
def login():
    if checkforlogin():
        return redirect("/user")
    try:
        user = request.args['user']
        passwd = request.args['pass']
        token = CheckUser(user, passwd)
        if token == -1:
            return render_template(html_loginformerr)
        else:
            session['token'] = token
            return redirect("/user")
    except KeyError as e:
        if checkforlogin():
            return redirect("/user")
        return render_template(html_loginform)


@app.route('/logout')
def logout():
    session.pop('token', None)
    return render_template(html_logout)


@app.route('/testemail')
def testmail():
    if not checkforlogin():
        return redirect('/login')
    try:
        t_email = request.args['email']
        s_host = request.args['s_host']
        s_port = request.args['s_port']
        s_pass = request.args['s_pass']
        result = mod_email.sendtestmail(t_email, s_host, s_port, s_pass)
        if result == 0:
            return "<meta http-equiv=\"refresh\" content=\"2;url='user'\" > OK"
        else:
            return "<meta http-equiv=\"refresh\" content=\"2;url='user'\" > Failed:%s" % (result)
    except Exception as e:
        return "<meta http-equiv=\"refresh\" content=\"2;url='user'\" > Failed:%s" % (e)


@app.route('/search')
def search():
    if not checkforlogin():
        return redirect('/login')
    try:
        text = request.args['text']
        page = request.args['page']
        return Search_dmzj(text, page)
    except Exception as e:
        return "Search Failed:%s" % (e)


@app.route('/download')
def download():
    if not checkforlogin():
        return redirect('/login')
    # try:
    token = session['token']
    url = request.args['url']
    start = request.args['from']
    end = request.args['to']
    all = request.args['all']
    sendmail = request.args['sendmail']
    merge = request.args['merge']
    logid = CreateTask(url, start, end, all, sendmail, merge, token)
    if logid == -1:
        return "创建下载任务失败！"
    else:
        return redirect('/getlog?logid=%s' % (logid))
    # return str(all)
    # except Exception as e:
    #    return "Failed: %s" % (e)


@app.route('/getlog')
def getlog():
    if not checkforlogin():
        return redirect('/login')
    else:
        try:
            token = session['token']
            logid = request.args['logid']
            result = GetLog(logid, token)
            return render_template(html_log, logid=logid, log=result)
        except KeyError as e:
            return "请求日记失败: 请求格式错误！"
        except Exception as e:
            return "请求日记失败: Unexpected Error <br> %s" % (e)

@app.route('/getloglist')
def getloglist():
    if not checkforlogin():
        return redirect('/login')
    #try:
    token = session['token']
    list = GetLogListFromToken(token)[::-1]
    text = ""
    for item in list:
        username = item[0]
        logid = item[1]
        datetime = item[2].strftime('%Y-%m-%d %X')
        status = item[3]
        text += """
        <tr>
            <td><div id="%s">%s</div></td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td><a href="/getlog?logid=%s">查看日志</a></td>
		</tr>"""\
                %(status, status, username, logid, datetime, logid)
    return render_template(html_loglist, table=text)
    #except Exception as e:
    #    return e

@app.route('/getdownlist')
def getdownlist():
    if not checkforlogin():
        return redirect('/login')
    #try:
    token = session['token']
    logid = request.args['logid']
    result = GetLogSingle(logid, token)
    text = ""
    if result != -1:
        path = get_value("Output_Dir")+logid
        list = os.listdir(path)
        for item in list:
            text += """
                <dir id="download"> <a href="%s">%s</a> </dir>
            """ % (item, item)
    return text

@app.route('/requestfile')
def requestfile():
    if not checkforlogin():
        return redirect('/login')
    #try:
    token = session['token']
    logid = request.args['logid']
    filename = request.args['file']
    result = GetLogSingle(logid, token)
    try:
        path = os.path.join(os.getcwd(), get_value("Output_Dir").replace('/', '\\')) + logid + "\\" + filename
        return send_file(path, attachment_filename=filename)
    except Exception as e:
        return "下载文件失败"