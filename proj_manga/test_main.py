from proj_manga import init
from proj_manga.mod_dmzjsearch import printerrorlist, Analyze_dmzj

if __name__ == '__main__':
    init()
    Analyze_dmzj("http://manhua.dmzj.com/weilenverjidaomowang/", "pdf", [33, 37], False)
    Analyze_dmzj("https://manhua.dmzj.com/huiyedaxiaojiexiangrangwogaobaitiancaimendelianait/", "pdf",
                                [24, 25, 26, 44], False)
    printerrorlist()
