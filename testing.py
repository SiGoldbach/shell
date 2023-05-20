import os

x = os.open("testfile.txt", os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
print(x)
print(os.getcwd())
os.write(x,"hats".encode('utf-8'))
x=os.open("testfile.txt",os.O_RDONLY)
x = os.open("testfile.txt", os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
os.write(x,"bigger".encode('utf-8'))
x=os.open("testfile.txt",os.O_RDONLY)


print(os.read(x,100,))
