from random import Random

def Shuffle(dataList):
  rand = Random()
  for i in xrange(len(dataList) - 1, 0, -1):
    j = rand.randint(0, i)
    dataList[i], dataList[j] = dataList[j], dataList[i]
