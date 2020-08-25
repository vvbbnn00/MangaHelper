from proj_manga import mod_dmzjsearch, mod_init
from proj_manga.mod_imports import *

if __name__ == '__main__':
    mod_init.init()
    mod_dmzjsearch.Analyze_dmzj("http://manhua.dmzj.com/weilenverjidaomowang/", "pdf", [33, 37], False)
    mod_dmzjsearch.Analyze_dmzj("https://manhua.dmzj.com/huiyedaxiaojiexiangrangwogaobaitiancaimendelianait/", "pdf", [24, 25, 26, 44], False)
    mod_dmzjsearch.printerrorlist()

