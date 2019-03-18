def BSearch(arr, val, left=0, right=-1):
  if right < 0: right = len(arr) - 1
  while left <= right:
    mid = (left + right) / 2
    if val == arr[mid]:
      return mid          # found val
    elif val < arr[mid]:
      right = mid - 1     # val is in left side
    else:
      left = mid + 1      # val is in right side
  return -1               # cannot find val

def FindFense(arr):
  left = 0
  right = len(arr) - 1
  while left < right:
    mid = (left + right) / 2
    if arr[mid] < arr[left]:
      right = mid
    elif arr[mid] > arr[left]:
      left = mid
    elif arr[mid] < arr[right]:
      right = mid
    elif arr[mid] > arr[right]:
      left = mid
    else:
      left = mid
      right = mid
  return left

def CycleBSearch1(arr, val):
  fense = FindFense(arr)
  if arr[fense] == val:
    return fense
  elif arr[fense] < val:
    return
  else:
    return

g_showInfo = False

def CycleBSearch(arr, val):
  left = 0
  right = len(arr) - 1
  while left <= right:
    mid = (left + right) / 2
    if g_showInfo: print '%d(%d)\t%d(%d)\t%d(%d)' % (
        left, arr[left], mid, arr[mid], right, arr[right])
    if val == arr[mid]:
      return mid          # found val

    if arr[left] <= arr[mid]:
      if arr[left] <= val < arr[mid]:
        right = mid - 1   # val is in left side
      else:
        left = mid + 1    # val is in right side
    else:
      if arr[left] > val > arr[mid]:
        left = mid + 1    # val is in right side
      else:
        right = mid - 1   # val is in left side
  return -1               # cannot find val

from random import Random
rand = Random()
l = range(rand.randint(1, 100))
f = rand.randint(0, len(l) - 1)
li = []
li.extend(l[f:])
li.extend(l[:f])
#li = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 2, 3, 4, 5, 5]
#li = [0, 1, 2, 3]
#li = [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
for i in xrange(len(li)):
  g_showInfo = False
  j = CycleBSearch(li, li[i])
  if j < 0 or li[i] != li[j]:
    print 'Failed for list', li
    print 'CycleBSearch(li, li[%d]=%d) = %d' % (i, li[i], j)
    g_showInfo = True
    CycleBSearch(li, li[i])
    break
