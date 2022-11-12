from LexicalAnalysis import *
from SLRAnalysis import *

def main():
    filePath = "test1.txt"
    symbols = lexicalAnalysis(filePath)
    itemSets = ItemSets()
    itemSets.grammar.printFIRST()
    print("--------------------------------------------")
    itemSets.grammar.printFOLLOW()
    slr = SLR(itemSets)
    result, seq = slr.analysis(symbols)
    print(result)


if __name__ == '__main__':
    main()
