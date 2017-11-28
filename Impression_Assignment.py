from cvxpy import *
from scipy.optimize import *
import numpy

def impression_assignment(s, s_total_user, s_total, Z, f, theta, p, d, tau, tau_t, L, s_user):#参数为分配问题的参数，分别对应于s，Z，theta，a, b, p, r, s^, 二分图的邻接矩阵, N，, 用户的类别
    x = []
    u = []
    for i in range(len(s)):
        x.append([])
        for j in range(len(d)):
            if j in tau[i]:
                x[i].append(Variable(1,1,'x' + str(i) + '_' +str(j)))
            else:
                x[i].append(None)

    #print(x)
    for j in range(len(theta)):
       u.append(Variable(1,1,'u' + str(j)))
    part1 = 0
    part2 = 0

    #print(tau)
    #print(tau_t)
    # for j in range(len(theta)):#生成优化目标的第一个terms
    #     #print(len(tau_t[j]))
    #     for i in tau_t[j]:
    #             part1 += s_total[i]*Z[j]/theta[j] * (x[i][j]- theta[j])**2

    for j in range(len(theta)):#生成目标的第二个term
        part2 += p[j] * u[j]
        #sprint(part2)
    #print('start')
    #print(part2)
    obj = part1 / 2 + part2#生成目标函数

    const = []
    count = 0
    for j in range(len(theta)):#生成限制1
        con = 0
        for i in tau_t[j]:
            con += x[i][j] * s_total[i]
        #print(con)
        const.append(con + u[j] >= d[j])
    #print('start')
    for i in range(len(s)):#生成限制2
        con = 0
        for j in range(len(tau)):
            if j in tau[i]:
                con += x[i][j]
                #print(i,j)
        #print(con)
        const.append(con <= 1)

    for i in range(len(tau)):#生成限制3
        for j in range(len(d)):
            if j in tau[i]:
                const.append(s_total[i]*x[i][j] <= sum([L[v]*(int(s_user[i][v]+0.5)) for v in range(len(L)) if L[v]<=f[j]])+sum([f[j]*(int(s_user[i][v]+0.5)) for v in range(len(L)) if L[v]>f[j]]))
                #print(sum([L[v]*(int(s_user[i][v]+0.5)) for v in range(len(L)) if L[v]<=f[j]])+sum([f[j]*(int(s_user[i][v]+0.5)) for v in range(len(L)) if L[v]>f[j]]))
    for i in range(len(s)):
        x.append([])
        for j in range(len(d)):
            if j in tau[i]:
                const.append(x[i][j] >= 0)
            else:
                x[i].append(None)
    for j in range(len(theta)):#变量非负限制
        const.append(u[j] >= 0)

    #print(const)
    problem = Problem(Minimize(obj), const)
    result = problem.solve()
    print('problem: ', problem.status, ' result = ', result)
    # alpha = []
    # beta = []

  #   for j in range(len(theta)):#得到对偶变量alpha_j
  #       alpha.append(const[j].dual_value)
  # #      print(const[j].dual_value)
  #   for i in range(len(tau)):#得到对偶变量beta_wi
  #       beta.append([])
  #       for w in range(len(W)):
  #           beta[i].append(const[len(theta)+i*len(N)+w].dual_value)
  #         #  print(const[len(theta)+i*len(N)+w].dual_value)
  #
    for i in range(len(tau)):#得到原始变量v
        for j in range(len(d)):
            if j in tau[i]:
                x[i][j] = x[i][j].value
    return x