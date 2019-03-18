'''Find the least common ancestor (LCA) of two nodes in the bin-tree.
'''

class Node:
  def __init__(self, val=None, left=None, right=None):
    self.val = val
    self.left = left
    self.right = right
    self.parent = None
    if self.left: self.left.parent = self
    if self.right: self.right.parent = self

from sets import Set

class Dir:
  (Undef, Left, Right) = range(3)

def FindNodes(root, nodeSet, findAll=True):
  if not root or not nodeSet:
    return None

  pathDict = {}
  path = []
  curr = root
  while curr or path:
    while curr:   # Go down along left branch
      path.append((curr, Dir.Left))
      if curr in nodeSet:
        pathDict[curr] = list(path)
        nodeSet.remove(curr)
        if not nodeSet or not findAll:
          return pathDict
      curr = curr.left
    (curr, dir) = path.pop()
    while dir == Dir.Right:   # Back from right branch
      if not path: return pathDict
      (curr, dir) = path.pop()
    path.append((curr, Dir.Right))  # Trun to right from left
    curr = curr.right

  return pathDict

# Compare two pathes
def FindLCA_3(root, node1, node2):
  if not root or not node1 or not node2:
    return None
  if node1 is node2:
    return node1

  nodeSet = Set([node1, node2])
  pathDict = FindNodes(root, nodeSet)
  if nodeSet:
    return None

  path1 = [i[0] for i in pathDict[node1]]
  path2 = [i[0] for i in pathDict[node2]]

  lca = None
  minLen = min(len(path1), len(path2))
  for i in xrange(minLen):
    if path1[i] is not path2[i]:
      break
    lca = path1[i]

  return lca


def FindLCA_4(root, node1, node2):
  if not root or not node1 or not node2:
    return None
  if node1 is node2:
    return node1

  nodeSet = Set([node1, node2])
  pathDict = FindNodes(root, nodeSet, False)
  if not pathDict:
    return None

  path1 = [i[0] for i in pathDict.popitem()[1] if i[1] == Dir.Left]
  node = path1.pop()
  if FindNodes(node, nodeSet):
    return node
  while path1:
    node = path1.pop()
    if FindNodes(node.right, nodeSet):
      return node
  return None


# Get two pathes by parent pointer, then compare
def FindLCA_1(node1, node2):
  if not node1 or not node2:
    return None
  if node1 is node2:
    return node1

  path1 = []
  while node1:
    path1.append(node1)
    node1 = node1.parent

  path2 = []
  while node2:
    path2.append(node2)
    node2 = node2.parent

  lca = None
  minLen = min(len(path1), len(path2))
  for i in xrange(minLen):
    i = -1 - i
    if path1[i] is not path2[i]:
      break
    lca = path1[i]

  return lca





# Get one path by parent pointer, then check...
def FindLCA_2(node1, node2):
  if not node1 or not node2:
    return None
  if node1 is node2:
    return node1

  ancestors1 = Set()
  while node1:
    ancestors1.add(node1)
    node1 = node1.parent

  while node2:
    if node2 in ancestors1:
      return node2
    node2 = node2.parent

  return None

from RandomSelector import RandomSelector

def Ex1():
  rs1 = RandomSelector()
  rs2 = RandomSelector()
  nk = Node('K')
  nj = Node('J', None, nk)
  ni = Node('I', None, nj)
  nh = Node('H', ni)
  nl = Node('L')
  ng = Node('G', nh, nl)
  nf = Node('F')
  nd = Node('D')
  nc = Node('C', nf, nd)
  ne = Node('E')
  nb = Node('B', ne, nc)
  na = Node('A', nb, ng)

  for i in xrange(ord('a'), ord('m')):
    node = eval('n%s' % chr(i))
    rs1.AddItem(node)
    rs2.AddItem(node)

  return (na, rs1.SelectedItems()[0], rs2.SelectedItems()[0])

def Ex2():
  rs1 = RandomSelector()
  rs2 = RandomSelector()
  nl = Node('L')
  ni = Node('I', nl)
  nf = Node('F', None, ni)
  nc = Node('C', None, nf)
  nj = Node('J')
  nk = Node('K')
  nh = Node('H', nj, nk)
  ng = Node('G')
  nd = Node('D', ng, nh)
  ne = Node('E')
  nb = Node('B', nd, ne)
  na = Node('A', nb, nc)

  for i in xrange(ord('a'), ord('m')):
    node = eval('n%s' % chr(i))
    rs1.AddItem(node)
    rs2.AddItem(node)

  return (na, rs1.SelectedItems()[0], rs2.SelectedItems()[0])

def Test(root, node1, node2):
  n1 = FindLCA_1(node1, node2)
  n2 = FindLCA_2(node1, node2)
  n3 = FindLCA_3(root, node1, node2)
  n4 = FindLCA_4(root, node1, node2)
  print
  print 'LCA of', node1.val, 'and', node2.val, 'is:',
  print n1 and n1.val or 'None', n2 and n2.val or 'None',
  print n3 and n3.val or 'None', n4 and n4.val or 'None',
  if not n1 == n2 == n3 == n4:
    raise Exception('xxx')


def Main():
  (root, node1, node2) = Ex1()
  Test(root, node1, node2)
  (root, node1, node2) = Ex2()
  Test(root, node1, node2)

if __name__ == '__main__':
  for i in xrange(10000):
    Main()
