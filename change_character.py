import os
import pathlib


p_temp = pathlib.Path('thesis/miyaken_txt')
txtList = list(p_temp.glob('*.txt'))
for txtFile in txtList:
    print(txtFile)
    command = 'nkf -w --overwrite ' + str(txtFile)
    os.system(command)


