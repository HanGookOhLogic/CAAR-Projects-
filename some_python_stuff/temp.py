l = open("evolution results.txt",'r').read().split("\n")
rs = 0
bgs = 0
ths = 0

for e in l:
    r = float(e[2:20])
    bg = float(e[24:42])
    th = float(e[46:64])
    rs+=r
    bgs+=bg
    ths+=th

print(rs/20,bgs/20,ths/20)
