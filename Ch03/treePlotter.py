# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 19:18:40 2018

@author: Zhou-Dongliang
"""

import matplotlib.pyplot as plt

# boxstyle为文本框的类型， sawtooth是锯齿类型，fc是边框线粗细
decisionNode = dict(boxstyle='sawtooth', fc='0.8')
leafNode = dict(boxstyle='round4', fc='0.8')
arrow_args = dict(arrowstyle='<-')


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    '''
    nodeTxt:显示的文本
    centerPt:文本的中心点,即箭头的指向点
    parentPt:指向文本的位置，即箭头的出发点
    '''
    
    # annotate是关于一个数据点的文本
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',\
                            xytext=centerPt, textcoords='axes fraction',\
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)


def createPlot():   # python在形式上不支持函数重载，因此本函数会被下面的createPlot(inTree)函数所替代
    # 定义画布，背景色为白色
    fig = plt.figure(1, facecolor='white')
    # clear current figure清除当前figure内容
    fig.clf()
    # createPlot.ax1为全局变量，绘制图像的句柄，subplot定义子图
    # 111表示figure中的1*1的第一个 frameon表示是否会之坐标轴矩形
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode(u'Decision Node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode(u'Leaf Node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()
    
   
def getNumLeaves(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict:
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs = numLeafs + getNumLeaves(secondDict[key])
        else:
            numLeafs = numLeafs + 1
    return numLeafs


def getTreeDepth(myTree):
    # 此处myTree必然是一个字典，因此不必考虑myTree仅为value的特殊情况
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict:
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth
    

def retrieveTree(i):
    listOfTrees = [{'no surfacing':{0:'no', 1:{'flippers':{0:'no',1:'yes'}}}},\
                   {'no surfacing':{0:'no', 1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}]
    return listOfTrees[i]


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] + cntrPt[0]) / 2.0
    yMid = (parentPt[1] + cntrPt[1]) / 2.0
    createPlot.ax1.text(xMid,yMid,txtString)
    

# python中的函数也是object，因此函数也具有attributes，网上称其为不好的编程规范
# 参考: https://stackoverflow.com/questions/22378606/what-kind-of-variable-of-this-definition-in-python/22378691#22378691 
def plotTree(myTree, parentPt, nodeTxt):
    numLeaves = getNumLeaves(myTree)
    # 下面变量treeDepth未使用
    treeDepth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeaves)) / 2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    # 每一次递归画子树时其标签y坐标值每次下降为1/树深度
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict:
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            # 每一次偏移为 1/树宽度
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD
    
    
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    # 以下语句相当于axprops = {'xticks': [], 'yticks': []}
    axprops = dict(xticks=[], yticks=[])
    # python函数中参数传递的顺序为位置参数、默认参数、*args(通过元组传递),**kwargs(通过字典传递)
    createPlot.ax1 = plt.subplot(111,frameon=False,**axprops)
    # 全局变量totalW:宽度, totalD:深度
    plotTree.totalW = float(getNumLeaves(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    # 图形范围 x:0-1 y:0-1 
    plotTree.xOff = -0.5 / plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1), '')
    plt.show()       
     
    
if __name__ == '__main__':
    myTree = retrieveTree(0)
    print(myTree)
    numLeaves = getNumLeaves(myTree)
    treedDepth = getTreeDepth(myTree)
    print(numLeaves, treedDepth)
    createPlot(myTree)
