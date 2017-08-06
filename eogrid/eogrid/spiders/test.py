import os










with open('links.txt') as f:
    lines = f.read().splitlines()

ASA_APG_1P = []

for i in lines:
    if "ASA_APG_1P" in i:
        ASA_APG_1P.append(i)
        print i

print len(lines)
print len(ASA_APG_1P)

