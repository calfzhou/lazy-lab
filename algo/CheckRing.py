class Node:
  def __init__(self, val=None, next=None):
    self.val = val
    self.next = next

def CheckRing(head):
  l1 = 0  # length of the chain before the ring
  l2 = 0  # length of the ring

  # Check if there is a ring.
  pos1 = head
  pos2 = head
  while pos2 and pos2.next:
    pos1 = pos1.next
    pos2 = pos2.next.next
    l1 += 2
    if pos2 and pos1 == pos2:
      l2 = 1
      break
  if not l2:
    if pos2: l1 += 1
    return (l1, l2)  # l2 should be 0

  # Calc the length of the ring.
  pos1 = pos2.next
  while pos1 != pos2:
    pos1 = pos1.next
    l2 += 1

  # Calc the length of the chain before the ring.
  l1 = 0
  pos1 = head
  pos2 = head
  for i in xrange(l2):
    pos2 = pos2.next
  while pos1 != pos2:
    pos1 = pos1.next
    pos2 = pos2.next
    l1 += 1
  return (l1, l2)


from random import Random
r = Random()

def Test(n):
  head = Node()
  curr = head
  sel = None
  selIdx = n
  for i in xrange(n):
    curr.next = Node(i)
    curr = curr.next
    if r.randint(0, i) == 0:
      sel = curr
      selIdx = i
  if r.randint(0, n) == 0:
    selIdx = n
  else:
    curr.next = sel
  print ' n =', n, 'selIdx =', selIdx
  (l1, l2) = CheckRing(head.next)
  print 'l1 =', l1,'    l2 =', l2
  print 'l1 + l2 == n:', l1 + l2 == n
  print 'l2 == n - selIdx:', l2 == n - selIdx

Test(r.randint(0, 100))
