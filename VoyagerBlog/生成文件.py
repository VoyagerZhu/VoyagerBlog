import time 
ltime = str(time.time())
address = "blogs\{}.txt".format(ltime)
strf_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
with open(address,"w",encoding='utf-8')as f:
    f.write("helloworld!\n你好编程猫！\n你好\n{}\n似梦".format(strf_time))

import os
files = os.listdir('./blogs')
for file in files:
    print(file)




