
from Offline_Test import  *
import math
import random
import numpy
import  datetime
def main():
    t = datetime.datetime.now()
    random.seed()
    I = []#online 曝光顺序
    real_pattern = {}
    for i in range(len(s)):
        real_pattern[i] = {}

    for i in range(len(s)):#初始化在线曝光
        I.append([])
        for imp in range(s_total[i]):
            I[i].append(-1)
    for i in range(len(s)):
        for v in range(len(L)):
            for u in range(int(s_user[i][v]+0.5)):
                for l in range(L[v]):
                    ran = random.randint(0, s_total[i] - 1)
                    r = ran
                    while I[i][ran] != -1:
                        ran = (1 + ran) % s_total[i]
                        if r == ran:
                            break
                    if v == 0:
                        I[i][ran] = u
                    else:
                        su = 0
                        for v1 in range(v):
                            su += int(s_user[i][v1]+0.5)
                        I[i][ran] = u + su
    #print(I)
    total_allocated = []
    under_delivery = 0
    total_j = []
    for i in range(len(s)):
        total_allocated.append([])
        for j in range(len(tau[i])):
            total_allocated[i].append(0)
    for i in range(len(s)):
        for imp in range(len(I[i])):
            arrival_imp = I[i][0:imp + 1]
            count_u = arrival_imp.count(arrival_imp[-1])
            if  arrival_imp[-1] != -1:
                if count_u == 1:
                    ran = random.randint(0, int(s_total_user[i]+0.5)-len(set(arrival_imp))+1)
                    v = 0
                    su = pattern_pool[i]['type'+str(0)][v]['count']
                    while ran > su :
                        v += 1
                        su += pattern_pool[i]['type'+str(0)][v]['count']
                    st = pattern_pool[i]['type'+str(0)][v]['name']
                    p = st.split('_')
                    p = count_min(i, p)
                    real_pattern[i]['user'+str(arrival_imp[-1])] = p[0:-1]
                    pattern_pool[i]['type' + str(0)][v]['count'] += -1
                    for j in range(len(tau[i])):
                        total_allocated[i][j] += p[0:-1].count(str(tau[i][j])) 
                else:
                    for l in range(len(L[1:])):
                        if count_u == L[l] + 1:
                            phi = []
                            for pattern in pattern_pool[i]['type'+str(l+1)]:
                                if pattern['count'] == 0:
                                    phi.append(-10000000000000)
                                else:
                                    pc = pattern['name'].split('_')
                                    pc = pc[0:-1]
                                    #print(real_pattern[i]['user'+str(arrival_imp[-1])])
                                    pl = real_pattern[i]['user'+str(arrival_imp[-1])] + pc
                                    phi.append(pi_diversity(pl) - pi_pacing(pl) - 10000*psi(pl))
                                    pc_index = numpy.argmax(phi)
                            pc = pattern_pool[i]['type'+str(l+1)][pc_index]['name'].split('_')
                            pl = real_pattern[i]['user'+str(arrival_imp[-1])] + pc
                            pl = count_min(i,pl)
                            real_pattern[i]['user'+str(arrival_imp[-1])] = pl[0:-1]
                            pc = pl[-(L[-1] - L[-2])-1:-1]
                           # print(pc)
                            for j in range(len(tau[i])):
                                total_allocated[i][j] += pc.count(str(tau[i][j]))
        #print(real_pattern)
        #print(total_allocated)
        under_delivery_i = 0
        #for j in range(len(tau[i])):
          #  under_delivery_i += max(int(s_total[i]*x[i][tau[i][j]]+0.5) - total_allocated[i][j], 0)
        #under_delivery += under_delivery_i
        #print(real_pattern[i])
    for j in range(len(d)):
        total_j.append([])
        total_j[-1] = 0
        for i in tau_t[j]:
            total_j[-1] += total_allocated[i][tau[i].index(j)]
        #print(d[j] - total_j[-1])
        under_delivery += max(d[j] - total_j[-1],0)
    print(under_delivery)
    print((datetime.datetime.now() - t).microseconds)

def pi_diversity(p):
    set_p = set(p)
    if 'null' in set_p:
        diversity = len(set_p) - 1
    else:
        diversity = len(set_p)
    return diversity

def pi_pacing(p):
    sum_pacing = 0
    for l in range(len(p)):
        for l1 in range(l):
            if p[l] == p[l1]:
                sum_pacing += 4*pow(math.e, l1 - l)
            else:
                sum_pacing += pow(math.e, l1 - l)
    return sum_pacing

def psi(p):
    set_p = set(p)
    sum_psi = 0
    for item in set_p:
        if item != 'null':
            sum_psi += max(p.count(item) - f[int(item)], 0)
    return sum_psi

def count_min(i, p):
    for e in range(len(p) - 1):
        subp = p[0:e+1]
        if (subp[-1] != 'null') and (subp.count(subp[-1]) >= f[int(subp[-1])]):
           p[e] = 'null'
    while p.count('null') != 0:
        ind = p.index('null')
        p1 = p[0:ind+1]
        count_j = []
        for j in tau[i]:
            count_j.append(p1.count(j))
        min_j = numpy.argmin(count_j)
        p[ind] = str(tau[i][min_j])
    return p

if __name__ == '__main__':
    main()