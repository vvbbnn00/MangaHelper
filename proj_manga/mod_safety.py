from proj_manga.mod_imports import *

def randomSecretKey(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+='
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return salt


# 32位的密钥用于解密邮件服务器密码
private_key = "3fke7pmOGLPcscWYpdBJKDnMbyaIuFQi"


def pass_hash(passwd):
    # 加盐用于安全储存密码
    salt1 = "5sGyrWPwWKm4N11GAZd1cNqoRWGYnG9H"
    salt2 = "674zL4jlOCwYsH5klImKVI8GNvWcA09i"
    passwd = salt1 + passwd + salt2
    hash = hashlib.sha256()
    hash.update(passwd.encode("utf8"))
    return hash.hexdigest()


# 由于邮件服务器密码需要二次使用，故使用可逆加密
def s_passencrypt(passwd):
    return aes_encrypt(passwd, private_key)


def s_passdecrypt(passwd):
    return aes_decrypt(passwd, private_key)


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def aes_encrypt(text, private_key):
    try:
        key = private_key.encode('utf-8')
        mode = AES.MODE_ECB
        text = add_to_16(text)
        cryptos = AES.new(key, mode)
        cipher_text = cryptos.encrypt(text)
        return b2a_hex(cipher_text)
    except:
        return text


# 解密后，去掉补足的空格用strip() 去掉
def aes_decrypt(text, private_key):
    try:
        key = private_key.encode('utf-8')
        mode = AES.MODE_ECB
        cryptor = AES.new(key, mode)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip('\0')
    except:
        return text



from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import base64

def getRandomColor(dark=False):
    '''获取一个随机颜色(r,g,b)格式的'''
    if dark:
        c1 = random.randint(0, 125)
        c2 = random.randint(0, 125)
        c3 = random.randint(0, 125)
    else:
        c1 = random.randint(125, 255)
        c2 = random.randint(125, 255)
        c3 = random.randint(125, 255)
    # print '=====',(c1,c2,c3)
    return (c1, c2, c3)


def getRandomStr():
    '''获取一个随机字符串，每个字符的颜色也是随机的'''
    random_num = str(random.randint(0, 9))
    random_low_alpha = chr(random.randint(97, 122))
    random_upper_alpha = chr(random.randint(65, 90))
    random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
    return random_char


class ValidCodeImg:
    def __init__(self, width=150, height=30, code_count=5, font_size=24, point_count=20, line_count=3,
                 img_format='png'):
        '''
        可以生成一个经过降噪后的随机验证码的图片
        :param width: 图片宽度 单位px
        :param height: 图片高度 单位px
        :param code_count: 验证码个数
        :param font_size: 字体大小
        :param point_count: 噪点个数
        :param line_count: 划线个数
        :param img_format: 图片格式
        '''
        self.width = width
        self.height = height
        self.code_count = code_count
        self.font_size = font_size
        self.point_count = point_count
        self.line_count = line_count
        self.img_format = img_format

    def getValidCodeImg(self):
        image = Image.new('RGB', (self.width, self.height), getRandomColor())
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("./simsun.ttf", size=30)
        temp = []
        for i in range(self.code_count):
            random_char = getRandomStr()
            draw.text((10 + i * 30, -2), random_char, getRandomColor(dark=True), font=font)
            temp.append(random_char)
        valid_str = "".join(temp)
        for i in range(self.line_count):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=getRandomColor(dark=True))
        for i in range(self.point_count):
            draw.point([random.randint(0, self.width), random.randint(0, self.height)], fill=getRandomColor())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=getRandomColor(dark=True))
        from io import BytesIO
        f = BytesIO()
        image.save(f, self.img_format)
        data = f.getvalue()
        f.close()
        return data, valid_str


def requireChapta():
    img = ValidCodeImg()
    data, valid_str = img.getValidCodeImg()
    base64_data = base64.b64encode(data)
    s = base64_data.decode()
    return pass_hash(valid_str.upper()), 'data:image/jpeg;base64,%s' % s

if __name__ == '__main__':
    requireChapta()