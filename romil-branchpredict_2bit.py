import sys, os, winsound

def tags(addr):
        bits = bin(int(addr,16))[2:]
        bits = '0'*(64-len(bits))+bits
        idx = bits[-5:]
        tag = bits[0:-5]
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
                history = BHT[int(idxOld,2)][1]
                if diff<0 or diff>15:
                        if history==2:
                                history += 1
                                p += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                        elif history==3:
                                p += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                        elif history==1:
                                history += 1
                                mp += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                        elif history==0:
                                history += 1
                                mp += 1
                                BHT[int(idxOld,2)] = [tagOld,history] 
                else:
                        if history==2:
                                history -= 1
                                mp += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                        elif history==3:
                                history -= 1
                                mp += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                        elif history==1:
                                history -= 1
                                p += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                        elif history==-0:
                                p += 1
                                BHT[int(idxOld,2)] = [tagOld,history] 
        else:
                if diff<0 or diff>15:
                        history = 1
                        BHTmiss += 1
                        BHT[int(idxOld,2)] = [tagOld,history]
                        #print(i)
                else:
                        BHTnomiss += 1

        idxOld = idx
        tagOld = tag

print('Total predictions: ' + str(p))
print('Total miss-predictions: ' + str(mp))
print('Total buffer misses: ' + str(BHTmiss))
print('Performance accuracy: ' + str((p)*100/(p+mp+BHTmiss)))
winsound.Beep(2500,400)
