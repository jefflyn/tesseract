import os

print("working path: " + os.getcwd())

os.chdir("../..")
print(os.getcwd())