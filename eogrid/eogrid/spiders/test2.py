import os

with open('/home/tuan/Desktop/anaapg1p') as f:
    crawler = f.read().splitlines()

with open('/home/tuan/Desktop/query.txt') as f:
    query = f.read().splitlines()


dif1 = set(query) - set(crawler)
dif2 = set(crawler) - set(query)

print dif2

print dif1


thefile = open('dif.txt', 'w')

for item in dif1:
  thefile.write("%s\n" % item)