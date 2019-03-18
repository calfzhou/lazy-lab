from random import Random

class RandomSelector:
  def __init__(self, selectionCount=1):
    self._selectionCount = selectionCount
    self._selectedItems = []
    self._count = 0
    self._rand = Random()

  def SelectedItems(self):
    return self._selectedItems

  def Count(self):
    return self._count

  def AddItem(self, item):
    if len(self._selectedItems) < self._selectionCount:
      self._selectedItems.append(item)
    else:
      idx = self._rand.randint(0, self._count)
      if idx < self._selectionCount:
        self._selectedItems[idx] = item
    self._count += 1

if __name__ == '__main__':
  rs = RandomSelector(10)
  for i in range(100):
    rs.AddItem(i)

  print rs.Count()
  print rs.SelectedItems()
