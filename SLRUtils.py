# 产生式
class Production:
    def __init__(self, left, right, number):
        self.left = left
        self.right = right
        # 产生式的序号
        self.number = number
        self.length = len(right)

    # 比较
    def __eq__(self, other):
        if other.number == self.number:
            return True
        else:
            return False

    def __hash__(self):
        return hash(str(self.number))

    def __str__(self):
        return str(self.number)

    def print(self):
        print(self.left[0], '->', self.right)
# 文法
class Grammar:
    # 非终结符
    V = []
    # 终结符
    T = []
    # 产生式
    P = []
    # 文法开始符号
    S = 'S'
    # FIRST集
    FIRST = {}
    # FOLLOW集
    FOLLOW= {}

    def __init__(self):
        self.initProduction()
        self.initV()
        self.initT()
        self.initFIRST()
        self.initFOLLOW()

    def initProduction(self):
        """
        初始化产生式
        :return:
        """
        prodcutions = []
        prodcution = Production(["S"], ["A"], 0)
        prodcutions.append(prodcution)
        prodcution = Production(["A"], ["E", "I", "(", ")", "{", "D", "}"], 1)
        prodcutions.append(prodcution)
        prodcution = Production(["E"], ["int"], 2)
        prodcutions.append(prodcution)
        prodcution = Production(["E"], ["float"], 3)
        prodcutions.append(prodcution)
        prodcution = Production(["D"], ["D", ";", "B"], 4)
        prodcutions.append(prodcution)
        prodcution = Production(["B"], ["F"], 5)
        prodcutions.append(prodcution)
        prodcution = Production(["B"], ["G"], 6)
        prodcutions.append(prodcution)
        prodcution = Production(["B"], ["M"], 7)
        prodcutions.append(prodcution)
        prodcution = Production(["F"], ["E", "I"], 8)
        prodcutions.append(prodcution)
        prodcution = Production(["G"], ["I", "=", "P"], 9)
        prodcutions.append(prodcution)
        prodcution = Production(["P"], ["K"], 10)
        prodcutions.append(prodcution)
        prodcution = Production(["P"], ["K", "+", "P"], 11)
        prodcutions.append(prodcution)
        prodcution = Production(["P"], ["K", "-", "P"], 12)
        prodcutions.append(prodcution)
        prodcution = Production(["I"], ["id"], 13)
        prodcutions.append(prodcution)
        prodcution = Production(["K"], ["I"], 14)
        prodcutions.append(prodcution)
        prodcution = Production(["K"], ["int_value"], 15)
        prodcutions.append(prodcution)
        prodcution = Production(["K"], ["float_value"], 16)
        prodcutions.append(prodcution)
        prodcution = Production(["M"], ["while", "(", "T", ")", "{", "D", ";", "}"], 17)
        prodcutions.append(prodcution)
        prodcution = Production(["N"], ["if", "(", "T", ")", "{", "D", ";", "}", "else", "{", "D", ";", "}"], 18)
        prodcutions.append(prodcution)
        prodcution = Production(["T"], ["K", "L", "K"], 19)
        prodcutions.append(prodcution)
        prodcution = Production(["L"], [">"], 20)
        prodcutions.append(prodcution)
        prodcution = Production(["L"], ["<"], 21)
        prodcutions.append(prodcution)
        prodcution = Production(["L"], [">="], 22)
        prodcutions.append(prodcution)
        prodcution = Production(["L"], ["<="], 23)
        prodcutions.append(prodcution)
        prodcution = Production(["L"], ["=="], 24)
        prodcutions.append(prodcution)
        prodcution = Production(["D"], ["B"], 25)
        prodcutions.append(prodcution)
        prodcution = Production(["B"], ["N"], 26)
        prodcutions.append(prodcution)
        prodcution = Production(["E"], ["void"], 27)
        prodcutions.append(prodcution)

        self.P = prodcutions

    def initV(self):
        """
        初始化非终结符集
        :return:
        """
        for pro in self.P:
            v = pro.left[0]
            if v not in self.V:
                self.V.append(v)

    def initT(self):
        """
        初始化终结符集
        :return:
        """
        for pro in self.P:
            for t in pro.right:
                if t not in self.V and t not in self.T:
                    self.T.append(t)

    def initFIRST(self):
        """
        初始化所有文法符号的FIRST集
        FIRST(X):可以从X推导出的所有串首终结符的集合
        如果X是终结符FIRST(X)={X}
        如果X是非终结符且X->Y1Y2...Yn,如果Y1、Y2、...、Yk-1的FIRST集含有空字符
        那么FIRST(Yk)应在FIRST(X)中,如果Y1、Y2、...、Yn的FIRST集都含有空字符,
        那么FIRST(X)也包含空字符
        如果X->空字符,FIRST(X)包含空字符
        :return:
        """
        # 终结符
        for t in self.T:
            self.FIRST[t] = {t}

        # 非终结符
        for v in self.V:
            self.FIRST[v] = set()
            for pro in self.P:
                # 右部第一个为终结符
                if pro.left[0] == v and pro.right[0] in self.T + [None]:
                    self.FIRST[v] = self.FIRST[v].union({pro.right[0]})
        while True:
            len_old = [len(i) for i in self.FIRST.values()]
            for v in self.V:
                for pro in self.P:
                    # 右部第一个为非终极符
                    if pro.left[0] == v and pro.right[0] in self.V:
                        self.FIRST[v] = self.FIRST[v].union(self.FIRST[pro.right[0]])
                    if pro.left[0] == v and pro.right[0] is None:
                        self.FIRST[v] = self.FIRST[v].union([None])
            len_new = [len(i) for i in self.FIRST.values()]
            success = True
            for i, j in zip(len_old, len_new):
                if i != j:
                    success = False
            if success:
                break

    def getFIRST(self, x):
        """
        获得指定文法符号x的FIRST集
        :param x:
        :return:
        """
        return self.FIRST[x]

    def printFIRST(self):
        print("FIRST集")
        for key in self.FIRST.keys():
            if self.FIRST[key] is None:
                continue
            print(key, end=':')
            for s in self.FIRST[key]:
                print(s, end=' ')
            print()

    def initFOLLOW(self):
        """
        初始化非终结符的FOLLOW集
        FOLLOW(A):在某个句型紧跟在A后面的终结符的集合
        文法开始符号S,$在FOLLOW(S)中
        如果A->aBb,则FIRST(b)中除空字符之外都在B中
        如果A->aB或者A->aBb且FIRST(b)含有空字符,FOLLOW(A)在FOLLOW(B)中
        :return:
        """
        for v in self.V:
            self.FOLLOW[v] = set()
        self.FOLLOW[self.S] = {'#'}

        while True:
            len_old = [len(i) for i in self.FOLLOW.values()]
            for v in self.V:
                for pro in self.P:
                    length = len(pro.right)
                    for i in range(length):
                        if pro.right[i] == v and i < length - 1:
                            self.FOLLOW[v] = self.FOLLOW[v].union(self.FIRST[pro.right[i + 1]])
                        elif pro.right[i] == v and i == length - 1:
                            self.FOLLOW[v] = self.FOLLOW[v].union(self.FOLLOW[pro.left[0]])

            len_new = [len(i) for i in self.FOLLOW.values()]
            success = True
            for i, j in zip(len_old, len_new):
                if i != j:
                    success = False
            if success:
                break

    def getFOLLOW(self, x):
        """
        获得指定文法符号x的FOLLOW集
        :param x:
        :return:
        """
        return self.FOLLOW[x]

    def printFOLLOW(self):
        print("FOLLOW集")
        for key in self.FOLLOW.keys():
            if self.FOLLOW[key] is set():
                continue
            print(key, end=':')
            for s in self.FOLLOW[key]:
                print(s, end=' ')
            print()

    def getProductionFile(self):
        file_str = ''
        for pro in self.P:
            l = pro.left[0]
            r = ''
            for s in pro.right:
                r += s
            file_str += l + '->' + r + '\n'
        with open('production.txt', 'w', encoding='utf-8') as f:
            f.write(file_str)
# 项目=产生式+小圆点位置
class Item:
    # 初始项目 小圆点在pos前一个位置
    def __init__(self, production, pos=0):
        self.production = production
        self.pos = pos

    def getNextSymbol(self):
        # 获取小圆点后的符号
        if self.isReduction(): # 归约项目小圆点后无符号
            return None
        return self.production.right[self.pos]

    def getNextItem(self):
        # 获取该项目的后继项目
        return Item(self.production, self.pos + 1)

    def isReduction(self):
        # 是否为归约项目
        return self.pos == self.production.length

    def getProduction(self):
        return self.production

    def getProductionNumber(self):
        return self.production.number

    def __eq__(self, other):
        if other.production == self.production and other.pos == self.pos:
            return True
        return False

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return str(self.production) + ':' + str(self.pos)

    def print(self):
        print(self.production.left[0], '->', self.production.right[:self.pos], ' · ', self.production.right[self.pos:])
# 项目集族
class ItemSets:
    grammar = Grammar()
    # 所有项目集
    C = []

    def __init__(self):
        # 项目集I0
        itemSet0 = []
        # 第一个产生式
        production = self.grammar.P[0]
        # 初始项目
        item = Item(production)
        itemSet0.append(item)
        # 初始项目所在项目集闭包的计算
        I0 = self.CLOSURE(itemSet0)
        self.C.append(I0)
        # 计算所有的项目集
        self.initC()

    def CLOSURE(self, I):
        """
        对于项目集I,求其项目集闭包
        J=I
        repeat
            for(J中的每一项A->a·Bb)
                for(G中的每个B对应的产生式B->y)
                    if(项目B->·y不在J中)
                        加入J中
        until J不再变化
        :param I:
        :return:
        """
        J = I
        while True:
            len_old = len(J)
            # 对于J中的每一项A->a·Bb
            for j in J:
                if not j.isReduction():
                    B = j.getNextSymbol()
                    if B in self.grammar.V:
                        # 对于G中的每个产生式B->·y
                        for pro in self.grammar.P:
                            if pro.left[0] == B:
                                item = Item(pro)
                                # 如果不在J中
                                if item not in J:
                                    J.append(item)
            len_new = len(J)
            if len_old == len_new:
                break
        return J

    def GOTO(self, I, X):
        """
        GOTO函数
        状态I遇到X进入的状态,X就是当前项目·后面的文法符号
        J为空集
        for(I中的每一项A->a·Bb)
            将A->aB·b加入J中
        返回CLOSURE(J)
        :param I:
        :param X:
        :return:
        """
        # I遇到文法符号X进入下一个状态集
        J = []
        # 对于I中的每一项A->a·Xb
        for i in I:
            if not i.isReduction():
                # 将A->aX·b加入J中
                if i.getNextSymbol() == X:
                    J.append(i.getNextItem())
        return self.CLOSURE(J)

    def initC(self):
        """
        repeat
            for(C中的每个项目集)
                for(每个文法符号X)
                    if(GOTO(I,X)不空且不在C中)
                        将GOTO(I,X)放入C中
        until C不再变化
        :return:
        """
        # C初始只有一个状态集
        while True:
            len_old = len(self.C)
            # 对于C里的每个项目集I
            for I in self.C:
                X = self.grammar.V + self.grammar.T
                # 对于每个文法符号x
                for x in X:
                    J = self.GOTO(I, x)
                    # 如果GOTO(I,x)非空且不在C中
                    if J and J not in self.C:
                        self.C.append(J)
            len_new = len(self.C)
            # 直至无新的项目集加入
            if len_old == len_new:
                break

    def getFOLLOW(self, X):
        return self.grammar.getFOLLOW(X)

def getItemState(item):
    x = item.getNextSymbol()
    if item.isReduction():
        return 'reduction', None
    elif x in Grammar.V:
        return 'V', x
    else:
        return 'T', x

def getItemIndex(I):
    n = len(ItemSets.C)
    for i in range(n):
        if len(I) == len(ItemSets.C[i]):
            if I == ItemSets.C[i]:
                return i
    return None