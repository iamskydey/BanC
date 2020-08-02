import random  #to generate random value
import numpy as np
from numpy import asarray
from numpy import save
from numpy import load
upd=[[1,2,0],[2,1,0],[3,2,0]]
RSSIth1=50
RSSIth2=60
def becon_F():     #random RSSI generator
    bb=int(random.randint(40,100))
    return bb

def init():        #initialize all nearby AP's RSSI
    AP=np.array([]) 
    AP=load('rssi.npy')
    
    return AP

def dis_rssi(AP):  #displays RSSI
    print(" ")
    print("1st Ap RSSI: ",AP[0])
    print("2nd Ap RSSI: ",AP[1])
    print("3rd Ap RSSI: ",AP[2])
    print(" ")

def active_check(s1,s2,arr):
    if(arr[s2]>arr[s1]):return 1
    else:return 0

def update(s1,s2,s3):
    for i in range(3):
        if(upd[i][0]==s1 and upd[i][1]==s2):
            upd[i][2]=s3
            print("update complete")
    print(upd)
    
def hidden(s1,s2):
    for i in range(3):
        if(upd[i][0]==s1 and upd[i][1]==s2):
            print("Entered hidden")
            if(upd[i][2]==0):
                return 0
            else:
                x=int(upd[i][2])
                return x

def d_prio(hr):    #data prioritisation method
    hrf_def_critical=0.38888   
    hrf_def_emergency=0.66666
    down_critical=-0.23611
    down_emergency=-0.513888
    hrf=(hr-72)/72
    if(hrf>hrf_def_emergency or hrf<=down_emergency or hrf<=down_critical):
        emergency_data= hr
        print("Emergency Data")
        return 2
    elif(hrf>hrf_def_critical):
        critical_data=hr
        print("Critical Data")
        return 1
    else:
        normal_data=hr
        print("Normal Data")
        return 0

def prob(a,b,x):    #probability generator
    count1=0
    count2=0
    for i in range(3):
        for j in range(3): 
            if(x[i][j]== a and x[i][j+1] == b):
                count1+=1
            if(x[i][j] == a and x[i][j+1] != 0 and j!=4):
                count2+=1

    p = count1/count2
    return p

def prediction(dap,temp):    #prediction method with marcov chain
    pm=[[1,2,3,1], [1,3,3,2], [3,3,2,1],[3,3,2,1]]
    g=[0,0,0]
    state=[0,0,0]
    nexts=0
    pr12=prob(1,2,pm)
    pr13=prob(1,3,pm)
    pr21=prob(2,1,pm)
    pr23=prob(2,3,pm)
    pr31=prob(3,1,pm)
    pr32=prob(3,2,pm)
    pr22=prob(2,2,pm)
    pr33=prob(3,3,pm)
    pr11=prob(1,1,pm)

    trans=[[pr11,pr12,pr13],[pr21,pr22,pr23],[pr31,pr32,pr33]]
    max_f=1
    for i in range(3):
        g[i]=trans[dap-1][i]
        
    for i in range(3): 
        for j in range(3): 
            state[i] += trans[i][j] * g[j]

    for p in range(3):
        if(state[p] < max_f):
            max_f=state[p]
            q=p
     #hidden
    check=active_check(dap-1,q,temp)
    if(check==0):   
        q+=1
        print("prediction",q)
        nexts=hidden(dap,q)
        print("nexts is: ",nexts)
        if(nexts==0):
            print("without hidden")
            znexts=q-1
        else:
            znexts=nexts-1   
            
    return znexts

def best_sink(AP_rss):     #best sink selection method(returns AP with Max RSSI)
    BestAP=np.argmax(AP_rss)
    if AP_rss[BestAP] >= RSSIth1 :
        return BestAP+1
        
        #print("Best AP: ", BestAP+1)
    else:
        print("All AP's RSSI is low")
        return 0

def best_sink(AP_rss,d,o_p):     #best sink selection method(returns AP with Max RSSI)
    BestAP=np.argmax(AP_rss)
    print(BestAP)
    if AP_rss[BestAP] >= RSSIth1 :
        b=BestAP+1
        print("updating")
        #print("d",d)
        #print("o_p",o_p)
        update(d,o_p,b)
        return BestAP+1
        
        #print("Best AP: ", BestAP+1)
    else:
        print("All AP's RSSI is low")
        return 0

#main 

while(1):
    temp=init()
    dis_rssi(temp)
    ra=becon_F()
    data=np.array([])
    hr=int(input("Enter Heartrate: "))
    value=d_prio(hr)
    if (ra > RSSIth2):
        print("Connection is STABLE with rssi: ",ra)
        active=load("active.npy")
        data=[active,hr]
        save("data.npy",data)
        print("Data is sent")
        
    else:
        print("Connection is UNSTABLE with rssi: ",ra)
        if (value < 2):
            print("Starting Prediction")
            dap=int(input("Enter current State: "))
            output_p=prediction(dap,temp)
            if(temp[output_p] > RSSIth2):
                print("Prediction Success with AP: ",output_p+1)
                data=[output_p,hr]
                save("data.npy",data)
                print("Data is sent")
                
            else:
                print("Predicted AP's RSSI is less:",temp[output_p])
                print("Starting Best Sink")
                output=best_sink(temp,dap,output_p+1)
                print("Best Sink Success with AP: ",output)
                data=[output-1,hr]
                save("data.npy",data)
                print("Data is sent")
        else:
            print("Starting Best Sink")
            output=best_sink(temp)
            print("Best Sink Success with AP: ",output)
            data=[output-1,hr]
            save("data.npy",data)
            print("Data is sent")


