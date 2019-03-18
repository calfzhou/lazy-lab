import random

def Sit(n):
  seats = [i for i in xrange(n)]
  mad_seat = random.choice(seats)
  if mad_seat == 0: return True
  if mad_seat == n - 1: return False
  seats.remove(mad_seat)
  for i in xrange(1, n - 1):
    if i in seats: seat = i
    else: seat = random.choice(seats)
    seats.remove(seat)
  assert(len(seats) == 1)
  last_seat = seats.pop()
  return (last_seat == n - 1) and True or False

def Sit2(n):
  seats = [i for i in xrange(n)]
  mad_seat = random.choice(seats)
  #if mad_seat == 0: return True
  if mad_seat == n - 1: return False
  seats.remove(mad_seat)
  for i in xrange(1, n - 1):
    #if i in seats: seat = i
    #else:
    seat = random.choice(seats)
    seats.remove(seat)
  assert(len(seats) == 1)
  last_seat = seats.pop()
  return (last_seat == n - 1) and True or False

play_cnt = 10000
last_inplace = 0
for i in xrange(play_cnt):
  if Sit2(100): last_inplace += 1
print 'Inplace:', last_inplace, '/', play_cnt
