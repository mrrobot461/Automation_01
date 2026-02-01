
from pathlib import Path
def main():

 folder = Path("C:/Users/Leul/OneDriveالمستندات")
 for py in folder.glob('*.py'):

def opener():
  with open("file2.txt",'w') as f:
    f.write(py)
    print("done")
    


