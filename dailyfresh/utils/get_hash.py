from hashlib import sha1


def get_hash(str, salt=None): # salt 盐
    '''取一个字符串的hash值'''
    # 提高字符串的复杂度
    str = '!@#$%'+str+'&^**('
    if salt:
        str = str + salt
    # 取str　hash值
    sh = sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()
