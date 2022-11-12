from SLRUtils import *


class SLR:
    # ACTION表
    ACTION = {}
    # GOTO表
    GOTO = {}
    # 单词序列
    sequence = {}

    def __init__(self, itemSets):
        self.grammar = Grammar()
        self.itemSets = itemSets
        self.generateForm()

    def generateForm(self):
        """
        分析表生成
        G的项目集族C
        Ik对应状态k
        if(A->m·an属于Ik且GOTO(Ik,a)=Ij)
            ACTION[i,a]=sj
        if(A->m·Bn属于Ik且GOTO(Ik,B)=Ij)
            GOTO[i,B]=j
        if(A->a·属于Ik且A不是文法开始符号)
            遇到任何FOLLOW(A)中的符号a都有ACTION[k,a]=rj,j是A->a的产生式编号
        if(S'->S·)
            ACTION[k,$]=acc
        :return:
        """
        n = len(self.itemSets.C)
        for i in range(n + 1):
            for t in (self.grammar.T + ['#']):
                self.ACTION[(i, t)] = (None, None)

        for i in range(n):
            for v in self.grammar.V:
                self.GOTO[(i, v)] = None

        for k in range(n):
            Ik = self.itemSets.C[k]
            for i in Ik:
                tempSymbol, x = getItemState(i)
                if tempSymbol == 'reduction':
                    print(k, end=':::')
                    i.print()
#s'->s·
                    p = i.getProduction()
                    if p.left[0] == self.grammar.S:
                        self.ACTION[(k, '#')] = ('acc', None)
                    else:
                        j = i.getProductionNumber()
                        for t in self.grammar.T + ['#']:
                            self.ACTION[(k, t)] = ('r', j)
                else:
                    J = self.itemSets.GOTO(Ik, x)
                    j = getItemIndex(J)
                    if tempSymbol == 'V':
                        self.GOTO[(k, x)] = j
                    elif tempSymbol == 'T':
                        self.ACTION[(k, x)] = ('s', j)

    def analysis(self, seq):
        """
        分析过程
        :param seq:词法分析得到的单词序列
        :return:
        """
        grammar = Grammar()
        # 末尾加结束符
        sequence = seq + ['#']
        # 初始化状态栈
        stateStack = [0]
        # 初始化符号栈
        symbolStack = ['#']
        # 返回分析过程序列
        result = ''

        while len(symbolStack) > 0 and len(stateStack) > 0:
            print("当前状态栈为:", stateStack)
            print("当前状态符号栈为:", symbolStack)
            print("当前剩余输入:", sequence)
            print('')
            result = result + "当前状态栈为:" + str(stateStack) + "\n" + "当前状态符号栈为:" + str(symbolStack) + "\n" + "当前剩余输入:" + str(sequence) + "\n"
            # 当前指针所指向的符号
            a = sequence[0]
            # 栈顶状态
            n = stateStack[-1]
            # 状态n遇到a
            (action, i) = self.ACTION[(n, a)]
            # 表格为空
            if not action:
                return "error", result
            # 移入动作
            if action == 's':
                stateStack.append(i)
                symbolStack.append(a)
                sequence = sequence[1:]
            # 归约动作
            elif action == 'r':
                p = None
                for pro in grammar.P:
                    if pro.number == i:
                        p = pro
                p.print()
                A = p.left[0]
                symbolStack = symbolStack[:-len(p.right)]
                stateStack = stateStack[:-len(p.right)]
                if len(stateStack) == 0:
                    return 'error', result
                n = stateStack[-1]
                symbolStack.append(A)
                s = self.GOTO[(n, A)]
                if s is None:
                    return 'error', result
                stateStack.append(s)
            elif action == 'acc':
                return 'acc', result
            else:
                return 'error', result

    def printACTION(self):
        """
        打印ACTION表
        :return:
        """
        S = set()
        T = set()
        for (s, t) in self.ACTION.keys():
            S.add(s)
            T.add(t)
        for t in T:
            print(t, end=' ')
        print()
        for s in S:
            print(s, ':', end='')
            for t in T:
                print(self.ACTION[(s, t)], end=' ')
            print()

    def printGOTO(self):
        """
        打印GOTO表
        :return:
        """
        S = set()
        V = set()
        for (s, v) in self.ACTION.keys():
            S.add(s)
            V.add(v)
        for v in V:
            print(v, end=' ')
        print()
        for s in S:
            print(s, ':', end='')
            for v in V:
                print(self.GOTO[(s, v)], end=' ')
            print()


def main():
    itemSets = ItemSets()
    slr = SLR(itemSets)
    slr.printACTION()
    slr.printGOTO()


if __name__ == '__main__':
    main()