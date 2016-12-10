import sys, os

## Function to separate tags and index bits
def tags(addr):
        bits = bin(int(addr,16))[2:]
        bits = '0'*(64-len(bits))+bits
        idx = bits[-6:]
        tag = bits[0:-6]
        return idx, tag

## Perceptron training Function
def train(history,output,BHT,tagOld,idxOld):
        w = [0]*(len(tagOld)+1)
        if output==0:
                if history==1:
                        w[0]=w[0]+1
                else:
                        w[0]=w[0]-1
                for i in range(1,len(BHT)):
                        if BHT[i-1][1]==1:
                                w[i%7]=w[i%7]+1
                        else:
                                w[i%7]=w[i%7]-1
        else:
                for i in range(1,len(BHT)):
                        w[i]=0
        
        return w

## Predictor Function
def predict(w,history,BHT,idx):
        for i in range(len(BHT)):
                thresh = 30
                output = w[0]
                temp = 0
                for i in range(0,len(idx)):
                        temp += w[i+1]*int(idx[i])
                if history==1:
                        output = output + temp
                else:
                        output = output - temp
                if output>=-thresh:
                        pred = 1
                else:
                        pred = 0
        return pred,output
        
                        
## Main Function
fname = 'vpr175.out'
addr = [line.rstrip('\n') for line in open(fname)]
BHT = [[None,None]]*64

p,mp,BHTmiss,BHTnomiss = 0.0,0.0,0.0,0.0

idxOld ,tagOld = tags(addr[0][2:])
W = [[0]*(len(BHT)+1)]
W[0][0] = 1
OUT = [0]

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
                                wtemp = train(history,0,BHT,tagOld,idxOld)
                                W.append(wtemp)
                                OUT.append((history-0.5)*2)
                                pred,val = predict(wtemp,1,BHT,idx)
                                if pred == 0:
                                        p += 1
                                        history = 1
                                        BHT[int(idxOld,2)] = [tagOld,history]
                                else:
                                        mp += 1
                                        history = 0
                                        BHT[int(idxOld,2)] = [tagOld,history]


                else:
                        if BHT[int(idxOld,2)][1]==0:
                                history = 0
                                p += 1
                                BHT[int(idxOld,2)] = [tagOld,history]
                                
                        elif BHT[int(idxOld,2)][1]==1:
                                wtemp = train(history,0,BHT,tagOld,idxOld)
                                W.append(wtemp)
                                OUT.append((history-0.5)*2)
                                pred,val = predict(wtemp,1,BHT,idx)
                                if pred == 0:
                                        p += 1
                                        history = 0
                                        BHT[int(idxOld,2)] = [tagOld,history]
                                else:
                                        mp += 1
                                        history = 1
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
