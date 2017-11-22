from Impression_Assignment import impression_assignment
import random
import numpy

s = []#曝光数二维数组，对应于s_wi
s_total = []#对应于 s_i
d = []#订单请求数，对应于d_j
tau = []#图的邻接矩阵
theta = []#对应于theta_j
Z = []#对应于Z_j = 1
V = []#对应于W用户类别
s_user = []#不同的用户数，对应于s^_vi
s_total_user = []#对应于s^i
tau_t = []#tau矩阵的转置矩阵
L = []#每一类用户的曝光数
f = []
p = []#惩罚系数 p_j=1
d_sum = 0
s_sum = 0
random.seed(0)

for v in range(5):
    V.append('length = ' + str(v + 1))
    L.append(v + 1)
for i in range(7):  # 生成7个槽，随机生成每个槽曝光数
    s.append([])
    s_user.append([])
    s_total.append(0)
    s_total_user.append(0)
    for v in range(5):# 每个槽内曝光分为5类
        rand = random.uniform(1, 7)
        s[i].append(int((v + 1) * rand))
        s_total[i] += int((v + 1) * rand)
        s_sum += s[i][v]
        s_user[i].append(s[i][v] /  (v + 1))
        s_total_user[i] += s[i][v] / (v + 1)
print('s_sum = ', s_sum)
print(s)
print(s_user)
print(s_total_user)
print(s_total)
for j in range(5):
    rand = int(random.uniform(95,105))
    d.append(rand)  # 生成5个订单，随机生成每个订单的需求量
    d_sum += rand
print('d_sum = ', d_sum)
for i in range(7):  # 随机生成二分图的邻接矩阵
    tau.append([])

for j in range(5):
    tau_t.append([])

for j in range(5):
    temp = random.randint(2,6)
    count = 0
    while count < temp:
        rand = random.randint(0, 6)
        #print(tau[rand].count(j))
        if tau[rand].count(j) == 0:
            tau[rand].append(j)
            #print(count)
            tau_t[j].append(rand)
        count += 1
print('tau =' + str(len(tau)))
#print('tau_t = ' + str(tau_t))

# 生成邻接矩阵的转置矩阵以获取tau_j
for j in range(5):
    sum = 0
    for i in range(len(tau_t[j])):
        for w in range(5):
            sum += s[i][w]
    temp = d[j] / sum
    theta.append(temp)
    Z.append(1)


for j in range(5):
    f.append(2)
    p.append(10000)
print('Column Generation')
impression_assignment(s, s_total_user, s_total, Z,f, theta, p, d, tau, tau_t)
