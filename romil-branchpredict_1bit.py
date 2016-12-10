import sys, os, winsound

def tags(addr):
        bits = bin(int(addr,16))[2:]
        bits = '0'*(64-len(bits))+bits
        idx = bits[-6:]
        tag = bits[0:-6]
        return idx, tag

fname = 'hw1trace2.out'
addr = [line.rstrip('\n') for line in open(fname)]
BHT = [[None,None]]*64

p,mp,BHTmiss,BHTnomiss = 0.0,0.0,0.0,0.0

idxOld ,tagOld = tags(addr[0][2:])

for i in range(1,len(addr)-1):
        idx ,tag = tags(addr[i][2:])
        diff = int(addr[i],16)-int(addr[i-1],16)

        if ([tagOld,1] in BHT) or ([tagOld,0] in BHT):
                if diff<0 or diff>15:
                        if BHT[int(idxOld,2)][1]==1:
                                history = 1
                                p += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                        elif BHT[int(idxOld,2)][1]==0:
                                history = 1
                                mp += 1
                                BHT[int(idxOld,2)] = [tagOld,history]      
                else:
                        if BHT[int(idxOld,2)][1]==0:
                                history = 0
                                p += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                        elif BHT[int(idxOld,2)][1]==1:
                                history = 0
                                mp += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
        else:
                if diff<0 or diff>15:
                        history = 1
                        BHTmiss += 1
                        BHT[int(idxOld,2)] = [tagOld,history]
                else:
                        BHTnomiss += 1

        idxOld = idx
        tagOld = tag

print('Total predictions: ' + str(p))
print('Total miss-predictions: ' + str(mp))
print('Total buffer misses: ' + str(BHTmiss))
print('Performance accuracy: ' + str((p)*100/(p+mp+BHTmiss)))
winsound.Beep(2500,400)
