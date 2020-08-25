from proj_manga.mod_pic2pdf import *
from proj_manga.mod_imports import *
import logging
ua = UserAgent()
errorlist = list()
import time

class html_logclass():
    def __init__(self, filename):
        self.logpath = filename

    def info(self,message):
        datetime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        level = 'INFO'
        printdata = "<div id='log'>[%s] %s %s</div>"%(level, datetime, message)
        with open(self.logpath, 'a') as file_obj:
            file_obj.write(printdata)

    def warning(self,message):
        datetime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        level = 'WARN'
        printdata = "<div id='log'>[%s] %s %s</div>"%(level, datetime, message)
        with open(self.logpath, 'a') as file_obj:
            file_obj.write(printdata)

    def critical(self,message):
        datetime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        level = 'CRITICAL'
        printdata = "<div id='log'>[%s] %s %s</div>"%(level, datetime, message)
        with open(self.logpath, 'a') as file_obj:
            file_obj.write(printdata)

    def error(self,message):
        datetime = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        level = 'ERROR'
        printdata = "<div id='log'>[%s] %s %s</div>"%(level, datetime, message)
        with open(self.logpath, 'a') as file_obj:
            file_obj.write(printdata)



def Search_dmzj(text, page):
    output = ""
    tempdir = get_value("Temp_Dir")
    outdir = get_value("Output_Dir")
    url = "https://manhua.dmzj.com/tags/search.shtml?" + "s=" + text + "&p=" + page
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    output += "<br>" + "<a href=\"\\user\">返回</a>"
    output += "<br>" + "尝试获取网页数据,这可能需要较长的时间"
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)
    driver.get(url)
    time.sleep(1)
    html = driver.execute_script('return document.documentElement.outerHTML')
    driver.close() #记得关闭，否则占用内存资源
    soup = BeautifulSoup(html, "html.parser")
    category = soup.find("div", class_="tcaricature_new").find("div", class_="tcaricature_block tcaricature_block2")
    list = category.find_all("ul")
    for item in list:
        subitem = item.find_all("li")
        title = subitem[0]
        detail = subitem[1]
        output += "<br>" + ("------作品------")
        output += "<br>" + (title.find("a").getText())
        output += "<br>" + ("封面：<a href=\""+ title.find("img").__getitem__("src")+"\">"+
                           title.find("img").__getitem__("src")+"</a>")
        output += "<br>" + ("观看链接：<a href=\"https:" + title.find("a").__getitem__("href")+"\">"+"https:" +
                           title.find("a").__getitem__("href")+"</a>")
        author = detail.find_all("div")[0].getText()
        latest = detail.find_all("div")[1].getText()
        output += "<br>" + (author)
        output += "<br>" + (latest)
        output += "<br>" + ("----------------")
    output += "<br>" + ("您正在浏览第" + str(page) + "页的搜索结果")
    output += "<br> <a href=/search?text="+text+"&page="+str(int(page)+1)+">点击浏览第"+str(int(page)+1)+"页</a>"
    return output

def Analyze_dmzj(url, ext, downloadlist, downloadall, logid):
    logmini = html_logclass(get_value("Log_Dir") + logid)
    print(get_value("Log_Dir") + logid)
    tempdir = get_value("Temp_Dir")
    outdir = get_value("Output_Dir")
    logmini.info("正在下载地址"+url)
    logging.info(url)
    headers = {"User-Agent": ua.random}
    logging.info("尝试获取网页数据")
    logmini.info("尝试获取网页数据")
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        logmini.error("您输入的URL地址不合法！")
        logging.error("您输入的URL地址不合法！")
        logmini.error("响应状态" + str(response.status_code))
        logging.error("响应状态" + str(response.status_code))
        return
    html = response.text
    response.close()
    rooturl = url.split('/')[2]
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("span", class_="anim_title_text")
    logmini.info("作品名称：" + title.getText())
    logging.info("作品名称：" + title.getText())
    category = soup.find_all("div", class_="cartoon_online_border")
    id = 0
    for subcategory in category:
        id += 1
        logmini.info("第" + str(id) + "页")
        logging.info("第" + str(id) + "页")
        list = subcategory.find_all("li")
        sid = 0
        for item in list:
            sid += 1
            logmini.info("Sid:"+str(sid)+"  "+item.find("a").getText())
            logging.info("Sid:"+str(sid)+"  "+item.find("a").getText())
            referlink = "https://" + rooturl + item.a['href']
            logmini.info("链接：" + referlink)
            logging.info("链接：" + referlink)
            if (sid in downloadlist) or (downloadall):
                Watch_dmzj(title.getText(), item.find("a").getText(), referlink, ext, logmini)

def Watch_dmzj(title, chapter, url, ext, logmini):
    tempdir = get_value("Temp_Dir")
    outdir = get_value("Output_Dir")
    folderpath = ""
    oriurl = url
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    logmini.info("尝试获取网页数据,这可能需要较长的时间")
    logging.info("尝试获取网页数据,这可能需要较长的时间")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html = driver.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, "html.parser")
    urls = soup.find_all("option")
    page = 0
    driver.close() #记得关闭，否则占用内存资源
    for url in urls:
        page += 1
        logmini.info(url.getText())
        logging.info(url.getText())
        imgurl = "https:" + url.__getitem__('value')
        logmini.info(imgurl)
        logging.info(imgurl)
        folderpath = title + "_" + chapter
        try:
            if not os.path.exists(tempdir):
                os.mkdir(tempdir)
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            if not os.path.exists(tempdir + folderpath):
                os.mkdir(tempdir + folderpath)
        except Exception as e:
            logmini.warning(e)
            logging.warning(e)
        filepath = str(page).zfill(3)
        response = Downpic(ua.random, oriurl, imgurl, tempdir + folderpath + "/" + filepath)
        if response == 1:
            logmini.info("第" + str(page) + "页图片下载成功")
            logging.info("第" + str(page) + "页图片下载成功")
        else:
            logmini.error("第" + str(page) + "页图片下载失败")
            logging.error("第" + str(page) + "页图片下载失败")
            errortxt = "Title:"+str(title) + "_Chapter:" + str(chapter) + "_URL:" + str(oriurl)
            errorlist.append(errortxt)
            return -1
    if ext == "pdf":
        folder2pdf(folderpath)

def printerrorlist():
    if len(errorlist) == 0:
        return 0
    logdir = get_value("Log_Dir")
    file = open(logdir+"ErrorList "+time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))+".txt", "w+")
    for item in errorlist:
        print(item, file=file)
    file.close()
    return 0