import os

file_path = 'aloe'
file_names = os.listdir(file_path)
i = 1

for name in file_names:
    src = os.path.join(file_path, name)
    dst = 'aloe_%03d.jpg'%(i)
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    i += 1