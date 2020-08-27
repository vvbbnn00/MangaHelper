
from PyPDF2 import PdfFileMerger, PdfFileReader
import codecs
from proj_manga.mod_file import delfile, delfolder
from proj_manga.mod_imports import *
from proj_manga.mod_mysql import SetLogStatus
from proj_manga.mod_settings import get_value
maxsize = 51904512 #单位Byte 换算49.5MB 0.5MB用于信件本身

def mergefiles(path, output_filename, logmini):
        # 遍历目录下的所有pdf将其合并输出到一个pdf文件中，输出的pdf文件默认带书签，书签名为之前的文件名
        filelist = os.listdir(path)
        merger = PdfFileMerger()
        id = 0
        total_size = 0
        for filename in filelist:
            f_path = path + filename
            logmini.info('合并文件：%s' % (filename))
            if total_size + os.path.getsize(f_path) > maxsize:
                if os.path.getsize(f_path) > maxsize:
                    logmini.warning('文件%s过大，已跳过合并，稍后可以自行下载。' % (filename))
                    continue
                total_size = os.path.getsize(f_path)
                out_filename = os.path.join(path, "[%s]" % str(id) + output_filename)
                merger.write(out_filename)
                id += 1
                merger.close()
                merger = PdfFileMerger()
                logmini.warning('合并文件过大，已分段处理。%s' % filename)
                f = codecs.open(f_path, 'rb')
                file_rd = PdfFileReader(f)
                short_filename = os.path.basename(os.path.splitext(filename)[0])
                merger.append(file_rd, bookmark=short_filename, import_bookmarks=True)
                f.close()

            else:
                total_size += os.path.getsize(f_path)
                f = codecs.open(f_path, 'rb')
                file_rd = PdfFileReader(f)
                short_filename = os.path.basename(os.path.splitext(filename)[0])
                merger.append(file_rd, bookmark=short_filename, import_bookmarks=True)
                f.close()
            logmini.info("清理PDF %s" % filename)
            result = delfile(path + filename)
            if result != 0:
                logmini.warning("清理PDF失败 %s" % (result))
        if id == 0:
            out_filename = os.path.join(path, output_filename)
            merger.write(out_filename)
            merger.close()
        else:
            out_filename = os.path.join(path, "[%s]" % str(id) + output_filename)
            merger.write(out_filename)
            merger.close()
        return 0

def Downpic(ua, referer, oripath, targetpath, logmini, logid):
    exts = oripath.split(".")
    ext = exts[len(exts) - 1]
    headers = {"User-Agent": ua, "Referer": referer}
    response = requests.get(url=oripath, headers=headers, timeout=20)
    if response.status_code != 200:
        logmini.error("图片下载失败：" + oripath)
        logmini.error("响应状态 %s" % (str(response.status_code)))
        logmini.error("Thread-图片下载失败")
        SetLogStatus(logid, "uncompleted")
        return -1
    try:
        pic = Image.open(BytesIO(response.content))
        pic.save(targetpath + "." + ext)
        response.close()
    except IOError as e:
        logmini.error("无法保存文件。" + str(e))
        logmini.error("Thread-图片下载失败")
        SetLogStatus(logid, "uncompleted")
        response.close()
        return -1
    except:
        logmini.error("未知错误 " + str(sys.exc_info()))
        logmini.error("Thread-图片下载失败")
        SetLogStatus(logid, "uncompleted")
        response.close()
        return -1
    logmini.info("Thread: 图片下载成功")
    return 1


def folder2pdf(folderpath, logmini, logid):
    outdir = get_value("Output_Dir")
    tempdir = get_value("Temp_Dir")
    pdf_name = folderpath
    path = tempdir + folderpath
    ori_file_list = os.listdir(path)
    file_list = []
    for item in ori_file_list:
        file_list.append(item.lower())
    pic_name = []
    im_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)
    pic_name.sort()
    im1 = Image.open(os.path.join(path, pic_name[0]))
    pic_name.pop(0)
    for i in pic_name:
        img = Image.open(os.path.join(path, i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        elif img.mode == "P":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    try:
        if not os.path.exists(outdir + logid):
            os.mkdir(outdir + logid)
    except Exception as e:
        logmini.error("无法创建文件夹！%s" % e)
    if get_value("GenerateBookMark") == "True":
        try:
            im1.save(tempdir + pdf_name + "_ori.pdf", "PDF", resolution=100.0, save_all=True, append_images=im_list)
            logmini.info("PDF初步创建完成：" + tempdir + pdf_name + "_ori.pdf，生成书签...")
            bookmarks = []
            for i in range(0, len(pic_name) + 1):
                bookmark = {"ID": i, "Title": str(i + 1), "Page": i, "Parent": -1}
                bookmarks.append(bookmark)
            result = pdfbookmark(tempdir + pdf_name + "_ori.pdf", outdir + logid + "/" + pdf_name + ".pdf", bookmarks, logmini)
            if result == 0:
                logmini.info("成功生成PDF")
            else:
                logmini.warning("PDF生成失败 %s" % (result))
            if get_value("CleanOriPDF") == "True":
                logmini.info("清理PDF缓存")
                result = delfile(tempdir + pdf_name + "_ori.pdf")
                if result != 0:
                    logmini.warning("清理PDF缓存失败 %s" % (result))
        except Exception as e:
            print(e)
    else:
        try:
            im1.save(outdir + logid + "/" + pdf_name + ".pdf", "PDF", resolution=100.0, save_all=True,
                     append_images=im_list)
            logmini.info("PDF创建完成：", pdf_name + ".pdf")
        except Exception as e:
            logmini.error(e)
    if get_value("CleanOriPic") == "True":
        logmini.info("清理图片缓存")
        result = delfolder(path)
        if result != 0:
            logmini.warning("清理图片缓存失败 %s" % (result))
    return 0



def pdfbookmark(orifile, outputfile, bookmarks, logmini):
    try:
        logmini.info("为文件 %s 添加书签，保存至 %s " % (orifile, outputfile))
        file = open(orifile, 'rb')
        reader = PyPDF2.PdfFileReader(file)
        outer = PyPDF2.PdfFileWriter()
        for i in range(0, reader.getNumPages()):
            outer.addPage(reader.getPage(i))
        parents = {}
        for item in bookmarks:
            if parents.__contains__(item["Parent"]):
                a = outer.addBookmark(title=item['Title'], pagenum=item["Page"], parent=parents[item["Parent"]])
            else:
                logmini.warning("书签 %s 的Parent项不存在，已自动忽略" % item["Title"])
                a = outer.addBookmark(title=item['Title'], pagenum=item["Page"], parent=None)
            parents[item['ID']] = a
        outerfile = open(outputfile, "wb")
        outer.write(outerfile)
        outerfile.close()
        file.close()
        return 0
    except Exception as e:
        return str(e)
