# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 19:38:08 2018

@author: Zhou-Dongliang
"""

from math import log
import operator
import pickle
import treePlotter

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    # 统计各类别数目
    for featVec in dataSet:
        currentLabel = featVec[-1]
        # 下述语句也可以写作labelCounts[currentLabel] = labelCounts.get(currentLabel, 0) + 1
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] = labelCounts[currentLabel] + 1
    shannonEnt = 0.0
    # 在使用上，for key in dict.keys() 与 for key in dict完全等价
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt = shannonEnt - prob * log(prob, 2)
    return shannonEnt


def createDataSet():
    dataSet = [[1, 1, 'yes'],\
               [1, 1, 'yes'],\
               [1, 0, 'no'],\
               [0, 1, 'no'],\
               [0, 1, 'no']]
    labels = ['not surfacing', 'flippers']
    return dataSet, labels


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            # 如果axis+1超过索引范围，此时默认返回空list
            # extend指的是后面拼接一个序列 append指的是后面加上一个object
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    '''
    dataSet:(nk+1)*d 并不限制属性的类型，既可以是数字，也可以是字符串
    '''
    
    numFeatures = len(dataSet[0]) - 1
    numExamples = len(dataSet)
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        # 获取属性的不重复属性值
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(numExamples)
            newEntropy = newEntropy + prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
    

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        classCount[vote] = classCount.get(vote, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=False)
    return sortedClassCount[0][0]
    
    
def createTree(dataSet, labels):
    # 获取输出类别全部值
    classList = [example[-1] for example in dataSet]
    # 如果全部样本均为同一输出值则直接返回该标签
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 如果最终遍历完所有样本则返回目前剩余样本输出的最多的类别
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    # 删除选出的最好特征这一标签，因为splitDataSet函数会删除最好属性那一列的值并分割开来
    del labels[bestFeat]
    featValues = [example[bestFeat] for example in dataSet]
    uniqueFeatValues = set(featValues)
    for value in uniqueFeatValues:
        # 之所以复制当前标签列表，是因为递归函数中含有删除操作
        subLabels = labels[:]
        # 通过字典类型递归的构造决策树
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

    
def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    # 将标签字符串转化为索引
    featIndex = featLabels.index(firstStr)
    for key in secondDict:
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


# 下面两个函数在使用pickle里面的读写函数时，必须为二进制格式，因为文本读写只接受字符串str
def storeTree(inputTree, filename):
    with open(filename, 'wb+') as fw:
        pickle.dump(inputTree,fw)


def grabTree(filename):
    with open(filename, 'rb+') as fr:
        return pickle.load(fr)


if __name__ == '__main__':
    with open('lenses.txt', 'r') as fr:
        lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age', 'prescript', 'astigamtic', 'tearRate']
    lensesTree = createTree(lenses, lensesLabels)
    treePlotter.createPlot(lensesTree)