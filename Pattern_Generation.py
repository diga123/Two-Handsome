from pulp import *


def pattern_generation(s, x, f, V, s_user, L, tau):  # 参数分别对应于列生成中的已知量，其中lambda_i 表示变量a_j的系数
    prob = LpProblem('CG', LpMaximize)  # 定义列生成线性规划
    y = []
    l = locals()
    obj = 1
    #print(L)
    count = 0
    print(len(tau))
    for v in range(len(V)):
        y.append([])
        for p in range(int(s_user[v]+0.5)):
            y[v].append([])
            for k in range(L[v]):
                y[v][p].append([])
                for j in tau:
                    count += 1
                    y[v][p][k].append(LpVariable('y' + str(v) + '_' + str(p) + '_' +str(k) +'_'+str(j), 0, 1, LpInteger))
    #print(count)
    #for j in range(len(tau)):
        #print(s*x[tau[j]])
    for j in range(len(tau)):#限制1
        con = 0
        for v in range(len(V)):
            for p in range(int(s_user[v]+0.5)):
                for k in range(L[v]):
                    con += y[v][p][k][j]
        #print(con)
        prob += con == int(s*x[tau[j]]-0.5)

    for v in range(len(V)):
        for p in range(int(s_user[v]+0.5)):
            for k in range(L[v]):
                con = 0
                for j in range(len(tau)):
                    con += y[v][p][k][j]
                prob += con <= 1

    for v in range(len(V)):
        for p in range(int(s_user[v]+0.5)):
            for j in range(len(tau)):
                con = 0
                for k in range(L[v]):
                    con += y[v][p][k][j]
                prob += con <= f[tau[j]]
    #print(prob)

    prob.solve()#解线性规划
    print("Status:", LpStatus[prob.status])
    for v in range(len(V)):
        for p in range(int(s_user[v]+0.5)):
            for k in range(L[v]):
                for j in range(len(tau)):
                    y[v][p][k][j] = value(y[v][p][k][j])
    #print(y)
    return y
