import operator

def ScheduleTasks(R, O, n, s):
  # R: request
  # O: occupancy
  # T: temporal
  tasks = [(i, R[i], O[i], R[i] - O[i]) for i in xrange(n)]
  tasks.sort(key=operator.itemgetter(-1), reverse=True)
  for i in xrange(n):
    (taskId, req, occ, temp) = tasks[i]
    if req > s or occ > s:
      return (False, tasks)
    s -= occ
  return (True, tasks)

R = [10, 9]
O = [5, 1]
s = 10
n = len(R)
print ScheduleTasks(R, O, n, s)
