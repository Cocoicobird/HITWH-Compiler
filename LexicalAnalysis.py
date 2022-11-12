from Alphabet import *

"""
识别Token
file_str:文件字符序列
pos:指针
返回值为识别出的一个单词与指针
"""
def getToken(file_str, pos):
    # 过滤字符
    while file_str[pos] == ' ' or file_str[pos] == '\t' or file_str[pos] == '\n':
        pos += 1
    ch = file_str[pos]
    # 识别标识符或关键字
    if ch.isalpha():
        token = ch
        pos += 1
        ch = file_str[pos]
        while ch.isalpha() or ch.isdigit() or ch == '_':
            token = token + ch
            pos += 1
            ch = file_str[pos]
        if token in Alphabet[1]:
            return token, pos
        else:
            return 'id', pos
    # 识别常数值
    elif ch.isdigit():
        token = ch
        pos += 1
        ch = file_str[pos]
        hasDot = False
        while ch == '.' or ch.isdigit():
            if ch == '.':
                # 后一个字符不是数字或空
                if not file_str[pos - 1].isdigit() or not file_str[pos + 1].isdigit():
                    return 'error', pos
                if hasDot:
                    return 'error', pos
                else:
                    hasDot = True
            token = token + ch
            pos += 1
            ch = file_str[pos]
        if hasDot:
            return 'float_value', pos
        else:
            return 'int_value', pos
    # 识别操作符和分隔符
    else:
        if ch in Alphabet[3]:
            if file_str[pos + 1] in Alphabet[3]:
                return ch + file_str[pos + 1], pos + 2
            else:
                return ch, pos + 1
        elif ch in Alphabet[4]:
            return ch, pos + 1
        else:
            return 'error', pos

def lexicalAnalysis(filePath):
    tokens = []
    success = True
    with open(filePath, 'r', encoding='utf-8') as f:
        file_str = f.read()
    pos = 0
    while pos < len(file_str):
        token, pos = getToken(file_str, pos)
        if token == 'error':
            success = False
            break
        tokens.append(token)
    if success:
        print("词法分析成功")
        return tokens
    print("词法分析结果有误")
    return []
def main():
    filePath = 'test1.txt'
    tokens = lexicalAnalysis(filePath)
    print(tokens)


if __name__ == '__main__':
    main()