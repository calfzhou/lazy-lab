#/usr/bin/python
# Filename: full_arrange_swap.py

def full_arrange(l):
    if l == []: return
    length = len(l)
    count = range(1, length+1)
    count.reverse()
    curr = 0
    check = 0
    while (curr >= 0):
        #print curr, ": ", l
        if curr == length:
            # print l
            check += 1
            curr -= 1
        elif count[curr] == length-curr: # first time, no swap
            count[curr] -= 1
            curr += 1
        elif count[curr] == 0: # last time, back trace
            l[curr], l[length-1] = l[length-1], l[curr]
            count[curr] = length-curr
            curr -= 1
        else:
            l[curr], l[length-count[curr]-1] = l[length-count[curr]-1], l[curr]
            count[curr] -= 1
            l[curr], l[length-count[curr]-1] = l[length-count[curr]-1], l[curr]
            curr += 1
    return check

def test_full_arrange():
    total = 1
    for i in range(1, 10):
        l = []
        item = 'a'
        for j in range(i):
            l += item
            item = chr(ord(item)+1)
        total *= i
        check = full_arrange(l)
        if check == total:
            print "total %d sequences composed by length %d list, full arrange check OK." %(total, i)

if __name__ == "__main__":
    test_full_arrange()
