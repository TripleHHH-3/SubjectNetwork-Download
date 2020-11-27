import os

dic = {1: None, 2: 3}
dic[1] = "1"
dic[2] = [1, 2, "3"]
for valus in dic.values():
    print(valus)

fileList = os.listdir("E:/")
for file in fileList:
    li = 11
    print(os.path.splitext(file)[0])

if True:
    l2 = 22

print(l2)

dit = {1: None}
dit[1] = [1, 3, 4]
for v in dit.values():
    print(v[0])

print (os.getcwd()) #获取当前工作目录路径
print (os.path.abspath('.')) #获取当前工作目录路径
print (os.path.abspath('test.txt')) #获取当前目录文件下的工作目录路径
print( os.path.abspath('..') )#获取当前工作的父目录 ！注意是父目录路径
print (os.path.abspath(os.curdir)) #获取当前工作目录路径
# with open("./test.txt", "a", encoding="utf-8") as file:
#     file.write("hi!")

