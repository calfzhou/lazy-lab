#/usr/bin/python
# Filename: full_arrange.py

def full_arrange(l):
    queue = l[:] # to store current elements left
    length = len(l)
    count = range(1, length+1)
    count.reverse()
    li = [] # the result list
    curr = 0 # pointer
    num = 0 # static
    while (1):
        num += 1
        # print "curr=", curr, ":", li
        if curr == -1: break
        if curr == length:
            # print li
            curr -= 1
            continue
        if count[curr] == 0:
            # print "trace back"
            #traceback
            queue.append(li.pop())
            count[curr] = length-curr
            curr -= 1
        else:
            # print "continue"
            if count[curr] != length-curr: # not first time fill
                queue.append(li.pop()) # pop current
            li.append(queue[0]) # append new one
            queue = queue[1:]
            count[curr] -= 1
            curr += 1
    print num

if __name__ == "__main__":
    l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    full_arrange(l)
