from SLRUtils import *

def main():
    grammar = Grammar()
    grammar.printFIRST()
    grammar.printFOLLOW()
    itemSets = ItemSets()
    print(len(itemSets.C))
    for i in itemSets.C[1]:
        i.print()


if __name__ == '__main__':
    main()