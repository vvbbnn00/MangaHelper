from proj_manga import *
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from proj_manga.mod_imports import *
import random

def randomSecretKey(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+='
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return salt

#32位的密钥用于解密邮件服务器密码
private_key = "3fke7pmOGLPcscWYpdBJKDnMbyaIuFQi"

def pass_hash(passwd):
    #加盐用于安全储存密码
    salt1 = "5sGyrWPwWKm4N11GAZd1cNqoRWGYnG9H"
    salt2 = "674zL4jlOCwYsH5klImKVI8GNvWcA09i"
    passwd = salt1 + passwd + salt2
    hash = hashlib.sha256()
    hash.update(passwd.encode("utf8"))
    return hash.hexdigest()

#由于邮件服务器密码需要二次使用，故使用可逆加密
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
