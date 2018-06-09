# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 19:29:18 2018

@author: Zhou-Dongliang
"""

from numpy import *
import operator
import os


def createDataSet():
    group = array([[1.0, 1.1],
                   [1.0, 1.0],
                   [0, 0],
                   [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    '''
    inX:输入特征向量(d)
    dataSet:训练样本集(nk*d)
    labels:标签向量(nk)
    k:用于选择最近邻居数目
    '''
    
    # 获取数据集行数目nk
    dataSetSize = dataSet.shape[0]
    # tile(A,reps):若A为向量，reps为标量，则结果为向量，上面列重复为reps次
    #              若A为向量，reps为矩阵，则结果为矩阵，形状与reps相同，行上重复reps[0]次,列上重复reps[1]次
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    # 下述axis=1 为按行求和， axis=0为按列求和
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    # 返回数组由小到大的索引值
    sortedDistIndices = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndices[i]]
        # dict.get(key, default=None) 如果键值key不存在，则返回default的值
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 下述若为python2， 则应改为
    #sortedClassCount = sorted(classCount.iteritems(),
    #key = operator.itemgetter(1), reverse = True)
    sortedClassCount = sorted(classCount.items(),
    key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    '''
    filename:datingTextSet2.txt所在路径
    returnMat:nk*3
    classLabelVector:nk
    '''
    
    # python中变量没有块级作用域，但是具有函数作用域
    with open(filename,'r') as fr:
        # readlines函数:返回列表，包含所有的行
        arrayOLines = fr.readlines()
        numberOfLines = len(arrayOLines)
        # 格式为nk*d,此处d为3
        returnMat = zeros((numberOfLines, 3))
        classLabelVector = []
        index = 0
        for line in arrayOLines:
            line = line.strip()
            listFormatLine = line.split('\t')
            returnMat[index,:] = listFormatLine[0:3]
            classLabelVector.append(int(listFormatLine[-1]))
            index = index + 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    '''
    dataSet:nk*d
    normDataSet:nk*d
    ranges:nk
    minVals:nk
    '''
    
    # array.min(axis=0)每列最小值
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet / tile(ranges, (m,1))
    return normDataSet, ranges ,minVals


def datingClassTest():
    hoRatio = 0.40
    datingDataMat, datingLabels = file2matrix('./datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:],\
                                     datingLabels[numTestVecs:m], 3)
        print('the classifier came back with: %d, the real answer is: %d' \
              %(classifierResult, datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount = errorCount + 1.0
    print('the total error rate is: %f' %(errorCount / float(numTestVecs)))
    

def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input('percentage of time spent playing video games?'))
    ffMiles = float(input('frequent flier miles earned per year?'))
    iceCream = float(input('liters of ice cream consumed per year?'))
    datingDataMat, datingLabels = file2matrix('./datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals) / ranges, normMat, datingLabels, 3)
    print('You will probably like this person: ', resultList[classifierResult - 1])
    

def img2vector(filename):
    returnVect = zeros((1,1024))
    with open(filename, 'r') as fr:
        for i in range(32):
            lineStr = fr.readline()
            for j in range(32):
                returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('./trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumber = fileStr.split('_')[0]
        hwLabels.append(classNumber)
        trainingMat[i,:] = img2vector('./trainingDigits/%s' %fileNameStr)
    testFileList = os.listdir('./testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumber = fileStr.split('_')[0]
        vectorUnderTest = img2vector('./testDigits/%s' %fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print('the classifier came back with: %s, the real answer is: %s' % (classifierResult, classNumber))
        if classifierResult != classNumber:
            errorCount = errorCount + 1.0
    print('\nthe total number of errors is: %d' %errorCount)
    print('\nthe total error rate is:%f' %(errorCount / float(mTest)))
    
    
if __name__ == '__main__':
    handwritingClassTest()