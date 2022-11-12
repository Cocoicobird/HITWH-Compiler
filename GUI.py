from tkinter import *
from LexicalAnalysis import *
from SLRAnalysis import *

import tkinter.filedialog as fd

def selectFile():
    filePath = fd.askopenfilename()
    if filePath != '':
        inputFilePath.delete(0, END)
        inputFilePath.insert(END, filePath)

def analyze():
    filePath = inputFilePath.get()
    if filePath != '':
        lexicalAnalysisText.delete("1.0", "end")
        SLRAnalysisText.delete("1.0", "end")
        sequence = lexicalAnalysis(filePath)
        s = ''
        for token in sequence:
            s = s + token + '\n'
        lexicalAnalysisText.insert(END, s)
        s = '分析开始\n\n'
        itemSets = ItemSets()
        slr = SLR(itemSets)
        result, seq = slr.analysis(sequence)
        s = s + seq + "\n" + "分析结束\n" + result
        SLRAnalysisText.insert(END, s)

root = Tk()
root.title('SLR语法分析器')
root.geometry('720x480')
filePathLabel = Label(root, text='请输入或选择所要分析的文件路径')
filePathLabel.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.05)
inputFilePath = Entry(root)
inputFilePath.place(relx=0.25, rely=0.06, relwidth=0.5, relheight=0.05)
fileButton = Button(root, text='选择文件', command=selectFile)
fileButton.place(relx=0.25, rely=0.12, relwidth=0.2, relheight=0.05)
analyzeButton = Button(root, text='开始分析', command=analyze)
analyzeButton.place(relx=0.55, rely=0.12, relwidth=0.2, relheight=0.05)
# 词法分析
lexicalAnalysisLabel = Label(root, text='词法分析')
lexicalAnalysisLabel.place(relx=0.1, rely=0.18, relwidth=0.2, relheight=0.05)
lexicalAnalysisText = Text(root)
lexicalAnalysisText.place(relx=0.05, rely=0.23, relwidth=0.3, relheight=0.7)
lexicalAnalysisScroll = Scrollbar()
lexicalAnalysisScroll.place(relx=0.35, rely=0.23, relwidth=0.02, relheight=0.7)
lexicalAnalysisScroll.config(command=lexicalAnalysisText.yview)
lexicalAnalysisText.config(yscrollcommand=lexicalAnalysisScroll.set)
# 语法分析
SLRAnalysisLabel = Label(root, text='语法分析')
SLRAnalysisLabel.place(relx=0.575, rely=0.18, relwidth=0.2, relheight=0.05)
SLRAnalysisText = Text(root)
SLRAnalysisText.place(relx=0.4, rely=0.23, relwidth=0.55, relheight=0.7)
SLRAnalysisScroll = Scrollbar()
SLRAnalysisScroll.place(relx=0.95, rely=0.23, relwidth=0.02, relheight=0.7)
SLRAnalysisScroll.config(command=SLRAnalysisText.yview)
SLRAnalysisText.config(yscrollcommand=SLRAnalysisScroll.set)
root.mainloop()