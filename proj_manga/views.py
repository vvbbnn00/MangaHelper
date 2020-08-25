from flask import *
from proj_manga import app
from proj_manga.mod_dmzjsearch import *
from proj_manga.mod_init import init
from proj_manga.mod_imports import *
from proj_manga import mod_email
from .mod_mysql import *
#<!--在这里总共用到了一下变量 emailmd5 username authorization email s_host s_port s_pass kindle_email-->

html_index = "index.html"
html_logout = "logout.html"
html_loginform = "login.html"
html_loginformerr = "loginfail.html"
html_user = "user.html"
html_log = "log.html"

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
        token = CheckUser(user,passwd)
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
            return "<meta http-equiv=\"refresh\" content=\"2;url='user'\" > Failed:%s"%(result)
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
    #try:
    token = session['token']
    url = request.args['url']
    start = request.args['from']
    end = request.args['to']
    all = request.args['all']
    sendmail = request.args['sendmail']
    merge = request.args['merge']
    logid = CreateTask(url, start, end, all, sendmail, merge, token)
    return redirect('/getlog?logid=%s' % (logid))
    #return str(all)
    #except Exception as e:
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
        except Exception as e:
            return "请求日记失败: %s" % (e)

#"/download?url="+url+"&from="+from+"&to="+to+"&all="+all+"&sendmail="+sendmail+"&merge="+merge