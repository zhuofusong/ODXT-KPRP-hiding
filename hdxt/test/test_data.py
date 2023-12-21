"""
Generate test data
"""

import random

D = 20000 # Number of documents

ids = [str(j+1) for j in range(D)] 

with open("test/ids.txt","w") as f:
    f.writelines([jj + "\n" for jj in ids])

keywords = ["@keyword" + str(i+1) + "@" for i in range(0,101,10)]   # Keyword ID : total 11 keywords

with open("test/keywords.txt","w") as f:
    f.writelines([kk + "\n" for kk in keywords])

updates = []

for kk in keywords:
    i = int(kk.lstrip("@keyword").strip("@"))
    # link i documents with keyword: @keyword + str(i) + @
    for j in range(len(ids)//2-i//2,len(ids)//2+i//2):
        u = "add " + str(j) + " @keyword" + str(i) + "@"
        updates.append(u)

redundant_updates = []
for kk in keywords:
    i = int(kk.lstrip("@keyword").strip("@"))
    # link documents with keyword i+1
    j = random.randint(1,len(ids)//2-i//2)
    u1 = "add " + str(j) + " @keyword" + str(i) + "@"
    u2 = "del " + str(j) + " @keyword" + str(i) + "@"
    for k in range(10): # repeat 10 times
        redundant_updates.append(u1)
        redundant_updates.append(u2)

with open("test/updates.txt","w") as f:
    f.writelines([uu  + "\n" for uu in updates + redundant_updates])