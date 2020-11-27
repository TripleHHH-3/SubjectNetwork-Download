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

print(os.path.splitext("山东省日照第三中学人教版生物必修一6.1细胞增殖学案.doc")[0])
# with open("./test.txt", "a", encoding="utf-8") as file:
#     file.write("hi!")

