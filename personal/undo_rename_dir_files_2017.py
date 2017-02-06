

import os
fname = "/home/tle/Desktop/undocommandline"

with open(fname) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

i = 0
cont = True
while cont == True:
    for item in content:
        try:
            print item.split(' -> ')[1].replace("'", "").replace("./", "/home/tle/"), " -> ", item.split(' -> ')[0].replace(
                "'", "").replace("./", "/home/tle/")
            os.rename(item.split(' -> ')[1].replace("'", "").replace("./", "/home/tle/"),
                      item.split(' -> ')[0].replace("'", "").replace("./", "/home/tle/"))
        except Exception as e:
            #print "Error! ", e  # TODO : delete later
            i+=1
            if i == len(content):
                print "ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!ENOUGH!"
                cont = False
                break
            continue









'''

    for i in  item.split('->'):

        i = i.replace("'","")
        print os.path.dirname(i), os.path.basename(i)
'''
