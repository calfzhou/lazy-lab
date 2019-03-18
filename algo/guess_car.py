import random

def OpenDoor(doors, selection):
  for i in xrange(len(doors)):
    if i == selection: continue
    if doors[i]: continue
    return i

def PlayGame(changeSelection):
  # initialize doors
  doors = ['car', '', '']
  random.shuffle(doors)
  # user 1st selection
  select1 = random.randint(0, len(doors) - 1)
  # operator open an empty door other than the user selected
  open = OpenDoor(doors, select1)
  # use change selection or not
  if changeSelection:
    select2 = 3 - select1 - open
  else:
    select2 = select1
  # done
  return doors[select2]

for changeSelection in (True, False):
  gotCar = 0
  playCnt = 100000
  for i in xrange(playCnt):
    gotCar += PlayGame(changeSelection) and 1 or 0
  print 'Change:', changeSelection, ': Got cars:', gotCar, '/', playCnt
