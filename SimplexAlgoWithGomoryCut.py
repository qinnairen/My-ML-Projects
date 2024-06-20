import numpy as np
# np.set_printoptions(suppress=True)
# np.set_printoptions(precision=3)
def true_if_int(a):
    if (abs(round(a)-a)<0.00001):
        return True
    else:
        return False
def simplex_algo(filename="input.txt"):
    with open(filename, 'r') as file:
        sections = file.read().split('[')

    sections=sections[1:]
    for i in range(len(sections)):
        sections[i]='['+sections[i]

    A = np.array([list(map(float, line.split(','))) for line in sections[1][3:].strip().split('\n')])
    b = np.array(list(map(float, sections[2][3:].strip().split('\n'))))
    c = np.array(list(map(float, sections[4][3:].strip().split(','))))

    constraint_types = sections[3].strip().split('\n')
    constraint_types.pop(0)
    for i in range(len(constraint_types)-1):
        constraint_types[i]=constraint_types[i].lstrip()
        constraint_types[i]=constraint_types[i].rstrip()
    objective = sections[0].strip().split('\n')
    objective.pop(0)
    objective=objective[0]
    if (objective=="maximize"):
        c=c*(-1)
    for i in range(len(b)):
        if (b[i]<0):
            b[i]=b[i]*(-1)
            A[i]=A[i]*(-1)
            if (constraint_types[i]=='>='):
                constraint_types[i]='<='
            elif (constraint_types[i]=='<='):
                constraint_types[i]='>='
    count1=0
    count2=0
    count3=0
    for i in range(len(constraint_types)):
        if (constraint_types[i]=='='):
            count1+=1
        elif (constraint_types[i]=='>='):
            count2+=1
        elif (constraint_types[i]=='<='):
            count3+=1
    numzero=count1+2*(count2+count3)
    result = np.zeros((len(b),len(A[0])+numzero))
    modc=np.zeros(len(c)+count2+count3)
    for i in range(len(c)):
        modc[i]=c[i]
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j]=A[i][j]
    temp=len(A[0])
    for i in range(len(constraint_types)):
        if (constraint_types[i]=="="):
            continue
        elif (constraint_types[i]==">="):
            result[i][temp]=-1
            temp+=1
        else:
            result[i][temp]=1
            temp+=1
    for i in range(len(constraint_types)):
        result[i][temp]=1
        temp+=1
    initialtable=np.zeros((len(b),(len(result[0])+1)))
    for i in range(len(b)):
        initialtable[i][0]=b[i]
    for i in range(len(result)):
        for j in range(len(result[0])):
            initialtable[i][j+1]=result[i][j]
    numvar=len(result[0])
    numbasic=len(b)
    n=numvar-numbasic
    cost=(-1*np.sum(b))
    basicvarindex=np.zeros(numbasic)
    for i in range(numvar-numbasic+1,numvar+1):
        basicvarindex[i-(numvar-numbasic+1)]=i
    reduced_cost=np.zeros(numvar)
    for i in range(numvar - numbasic):
        reduced_cost[i] = -1 * np.sum(result[:, i]) 
    while True:
        result=np.round(result,6)
        reduced_cost=np.round(reduced_cost,6)
        cost=np.round(cost,6)
        b=np.round(b,6)
        if np.any(reduced_cost<0):
            pivotcol = np.where(reduced_cost < 0)[0][0]
            column_positive = np.any(result[:,pivotcol] > 0)
            if column_positive:
                mini=2**30-1
                for j in range(0,len(b)):
                    if result[:,pivotcol][j]>0:
                        mini=min(mini,b[j]/result[:,pivotcol][j])
                for j in range(0,len(b)):
                    if result[:,pivotcol][j]>0:
                        if b[j]/result[:,pivotcol][j]==mini:
                            index1=j
                            break
                for i in range(0,numbasic):
                    if (i!=index1):
                        alpha=-1*(result[:,pivotcol][i]/result[:,pivotcol][index1])
                        result[i]=result[i]+(alpha)*result[index1]
                        b[i]=b[i]+alpha*b[index1]
                alpha1=(-1*(reduced_cost[pivotcol])/result[:,pivotcol][index1])
                reduced_cost=reduced_cost+alpha1*result[index1]
                cost=cost+alpha1*b[index1]
                b[index1]=b[index1]/result[:,pivotcol][index1]
                result[index1]=result[index1]/result[:,pivotcol][index1]
                basicvarindex[index1]=pivotcol+1
            else:
                statusofsol="Infeasible"
                finaltable=np.zeros((len(b),len(result[0])+1))
                for i in range(len(b)):
                    finaltable[i][0]=b[i]
                for i in range(len(result)):
                    for j in range(len(result[0])):
                        finaltable[i][j+1]=result[i][j]
                optimalvalue="Does Not Exist"
                optimal_sol="Does Not Exist"
                my_dict={}
                my_dict['Initial Tableau']=initialtable
                my_dict['Final Tableau']=finaltable
                my_dict['Status of Solution']=statusofsol
                my_dict['Optimal Solution Vector']=optimal_sol
                my_dict['Optimal Value']=optimalvalue
                my_dict['Basicvarindex']=basicvarindex
                my_dict['finalc']=modc
                my_dict['objective']=objective
                ##########################
                my_dict['rc']=reduced_cost
                my_dict['inter_cost']=cost
                ##############################
                return my_dict
        elif cost!=0:
            statusofsol="Infeasible"
            finaltable=np.zeros((len(b),len(result[0])+1))
            for i in range(len(b)):
                finaltable[i][0]=b[i]
            for i in range(len(result)):
                for j in range(len(result[0])):
                    finaltable[i][j+1]=result[i][j]
            optimalvalue="Does Not Exist"
            optimal_sol="Does Not Exist"
            my_dict={}
            my_dict['Initial Tableau']=initialtable
            my_dict['Final Tableau']=finaltable
            my_dict['Status of Solution']=statusofsol
            my_dict['Optimal Solution Vector']=optimal_sol
            my_dict['Optimal Value']=optimalvalue
            my_dict['Basicvarindex']=basicvarindex
            my_dict['finalc']=modc
            my_dict['objective']=objective
            ##########################
            my_dict['rc']=reduced_cost
            my_dict['inter_cost']=cost
            ##############################
            return my_dict
        else:

            flag=False
            y=len(basicvarindex)
            for l in range(y):
                if basicvarindex[l]>n:
                    for j in range(n):
                        if (result[l][j]!=0):
                            flag=True
                            for u in range(len(result)):
                                if (u!=l):
                                    result[u,:]=result[u,:]-result[l,:]*result[u,j]/result[l,j]
                            basicvarindex[l]=j+1
                            reduced_cost=reduced_cost-result[l,:]*reduced_cost[j]/result[l,j]
                            result[l,:]=result[l,:]/result[l,j]
                            break
                    if flag==False:
                        continue
                else:
                    continue

            while(True):
                flag=True
                for l in range(len(basicvarindex)):
                    if basicvarindex[l]>n:
                        flag=False
                        result = np.delete(result, l, axis=0)
                        basicvarindex = np.delete(basicvarindex, l, axis=0)
                        b = np.delete(b, l, axis=0)
                        break
                if flag==True:
                    break
            reduced_cost_new=np.zeros(n)

            for i in range(0,n):
                reduced_cost_new[i]=reduced_cost[i]
                
            result = np.delete(result, np.s_[-(len(reduced_cost)-n):], axis=1)
            reduced_cost=reduced_cost_new

            x=np.zeros(n)
            for i in range(0,len(basicvarindex)):
                x[int(basicvarindex[i]-1)]=b[i]
            cost=-1* np.dot(x,modc)
            cb=np.zeros(len(basicvarindex))
            for i in range(len(basicvarindex)):
                cb[i]=modc[int(basicvarindex[i])-1]
            for i in range(0,n):
                if i+1 in basicvarindex:
                    reduced_cost[i]=0
                else:
                    reduced_cost[i]=modc[i]-np.dot(cb,result[:,i])

            numvar=len(result[0])
            numbasic=len(b)
            while True:
                result=np.round(result,6)
                reduced_cost=np.round(reduced_cost,6)
                cost=np.round(cost,6)
                b=np.round(b,6)
                if np.any(reduced_cost<0):
                    pivotcol = np.where(reduced_cost < 0)[0][0]
                    column_positive = np.any(result[:,pivotcol] > 0)
                    if column_positive:
                        mini=2**30-1
                        for j in range(0,len(b)):
                            if result[:,pivotcol][j]>0:
                                mini=min(mini,b[j]/result[:,pivotcol][j])
                        for j in range(0,len(b)):
                            if result[:,pivotcol][j]>0:
                                if b[j]/result[:,pivotcol][j]==mini:
                                    index1=j
                                    break
                        for i in range(0,numbasic):
                            if (i!=index1):
                                alpha=-1*(result[:,pivotcol][i]/result[:,pivotcol][index1])
                                result[i]=result[i]+(alpha)*result[index1]
                                b[i]=b[i]+alpha*b[index1]
                        alpha1=(-1*(reduced_cost[pivotcol])/result[:,pivotcol][index1])
                        reduced_cost=reduced_cost+alpha1*result[index1]
                        cost=cost+alpha1*b[index1]
                        b[index1]=b[index1]/result[:,pivotcol][index1]
                        result[index1]=result[index1]/result[:,pivotcol][index1]
                        basicvarindex[index1]=pivotcol+1
                    else:
                        statusofsol="Unbounded"
                        finaltable=np.zeros((len(b),len(result[0])+1))
                        for i in range(len(b)):
                            finaltable[i][0]=b[i]
                        for i in range(len(result)):
                            for j in range(len(result[0])):
                                finaltable[i][j+1]=result[i][j]
                        if (objective=="maximize"):
                            optimalvalue="inf"
                        else:
                            optimalvalue="-inf"
                        optimal_sol="Does Not Exist"
                        my_dict={}
                        my_dict['Initial Tableau']=initialtable
                        my_dict['Final Tableau']=finaltable
                        my_dict['Status of Solution']=statusofsol
                        my_dict['Optimal Solution Vector']=optimal_sol
                        my_dict['Optimal Value']=optimalvalue
                        my_dict['Basicvarindex']=basicvarindex
                        my_dict['finalc']=modc
                        my_dict['objective']=objective
                        ##########################
                        my_dict['rc']=reduced_cost
                        my_dict['inter_cost']=cost
                        ##############################
                        return my_dict
                else:
                    statusofsol="Optimal"
                    finaltable=np.zeros((len(b),len(result[0])+1))
                    for i in range(len(b)):
                        finaltable[i][0]=b[i]
                    for i in range(len(result)):
                        for j in range(len(result[0])):
                            finaltable[i][j+1]=result[i][j]
                    if objective=='minimize':
                        optimalvalue=-1*cost
                    else:
                        optimalvalue=cost
                    final_bfs=np.zeros(len(A[0]))
                    for i in range(len(basicvarindex)):
                        if (basicvarindex[i]-1<len(A[0])):
                            final_bfs[int(basicvarindex[i]-1)]=b[i]
                    optimal_sol=final_bfs
                    my_dict={}
                    my_dict['Initial Tableau']=initialtable
                    my_dict['Final Tableau']=finaltable
                    my_dict['Status of Solution']=statusofsol
                    my_dict['Optimal Solution Vector']=optimal_sol
                    my_dict['Optimal Value']=optimalvalue
                    my_dict['Basicvarindex']=basicvarindex
                    my_dict['finalc']=modc
                    my_dict['objective']=objective
                    ##########################
                    my_dict['rc']=reduced_cost
                    my_dict['inter_cost']=cost
                    ##############################
                    return my_dict
                    # break


def atleast_one_not_int(optimal_sol):
    for i in optimal_sol:
        if abs(round(i)-i)>0.0001:
            return True
    return False
def gomory_cut_algo():
    my_dict=simplex_algo("input_ilp.txt")      
    finaltable=my_dict['Final Tableau']
    num_of_var=len(finaltable[0])-1
    statusofsol=my_dict['Status of Solution']
    optimal_sol=my_dict['Optimal Solution Vector']
    objective=my_dict['objective']
    basicvarindex=my_dict['Basicvarindex']   
    c1=my_dict['finalc']     
    rc_1=my_dict['rc']
    # print(rc_1)
    cost1=my_dict['inter_cost']
    # print(cost1)
    r=len(finaltable)
    c=len(finaltable[0])
    my_tableau=np.zeros((r+1,c))
    # print(my_tableau)
    my_tableau[0][0]=cost1
    for i in range(1,c):
        my_tableau[0][i]=rc_1[i-1]
    for i in range(r):
        for j in range(c):
            my_tableau[i+1][j]=finaltable[i][j]
    my_tableau=np.round(my_tableau,6)
    # print(finaltable)
    # print(cost1)
    # print(rc_1)
    # print(my_tableau)
    # return
    # objective_row=np.zeros(len(finaltable[0]))
    # for i in range(len(basicvarindex)):
    #     objective_row[0]=objective_row[0]-c1[int(basicvarindex[i])-1]*finaltable[int(i)][0]
    # cb=np.zeros(len(basicvarindex))
    # for i in range(len(basicvarindex)):
    #     cb[i]=c1[int(basicvarindex[i])-1]
    
    # for i in range(1,len(finaltable[0])):
    #     objective_row[i]=c1[i-1]-np.dot(cb,finaltable[:,i])
    # my_tableau = np.vstack((objective_row, finaltable))
    if (statusofsol=='Unbounded'): #string mein likhdena
        print('intitial_solution: does not exist')
        print('final_solution: does not exist')
        print('solution_status: unbounded')
        print('number_of_cuts: N.A.')
        if objective=='maximize':
            print('optimal_value: inf')
        else:
            print('optimal_value: -inf')
        return
    elif (statusofsol=='Infeasible'):
        print('intitial_solution: does not exist')
        print('final_solution: does not exist')
        print('solution_status: infeasible')
        print('number_of_cuts: N.A.')
        print('optimal_value: does not exist')
        return
    else:
        statusofsol="Feasible"
        cuts=0
        # print(finaltable)
        x_=my_tableau[1:,0]
        while(atleast_one_not_int(x_) and statusofsol=="Feasible"):   #my_tableau[1:,0] is BFS
            # print(my_tableau)
            cuts+=1
            num_of_var+=1
            # basicvarindex = np.concatenate((basicvarindex, [num_of_var]))
            source_row=0        # 0 indexing
            for i in range(len(x_)):
                if (true_if_int(x_[i])==False):##################################################################################
                    source_row=i         ####         
                    break
            # print(x_)
            # print(source_row)
            new_tableau = np.zeros((my_tableau.shape[0] + 1, my_tableau.shape[1] + 1))
            for i in range(len(my_tableau)):
                for j in range(len(my_tableau[0])):
                    new_tableau[i][j]=my_tableau[i][j]
            
            new_tableau[-1,-1]=1
            new_tableau[-1,0]= -1*(round(x_[source_row]%1,6))#################################################################################

            arr=np.zeros(len(new_tableau[0]))
            arr[0]=new_tableau[-1,0]
            arr[-1]=new_tableau[-1,-1]
            for j in range(len(arr)):
                if (j not in basicvarindex and j!=len(arr)-1 and j!=0):
                    arr[j]=-1*round(new_tableau[source_row+1][j]%1,6)##########################################################################
            
            for i in range(len(arr)):
                new_tableau[-1][i]=arr[i]
            my_tableau=new_tableau
            # basicvarindex = np.concatenate((basicvarindex, [num_of_var]))
            newbasicvarindex = np.zeros(basicvarindex.shape[0] + 1)
            for i in range(len(basicvarindex)):
                newbasicvarindex[i]=int(basicvarindex[i])
            newbasicvarindex[-1]=num_of_var
            basicvarindex=newbasicvarindex
            
            # print(my_tableau)
            # return
            # my_tableau=np.round(my_tableau,3)
            ##################################################################################################################
            # print(dual_simplex(my_tableau,basicvarindex))
            # my_tableau,basicvarindex,res=dual_simplex(my_tableau,basicvarindex)
            
            pivot_row_index=-1
            my_tableau=np.round(my_tableau,6)
            for i in range(1,len(my_tableau)):
                if (my_tableau[i][0]<0):###########################################
                    pivot_row_index=i
                    break
            pivot_column_index=-1

            while(pivot_row_index!=-1):
                mini=2**31-1
                res=False
                for i in range(1,len(my_tableau[0])):
                    if (my_tableau[pivot_row_index][i])<0:
                        res=True
                        break
                if res==False:
                    statusofsol='Infeasible'
                    print('intitial_solution:',', '.join(map(str,optimal_sol)))
                    print('final_solution: does not exist')
                    print('solution_status: infeasible')
                    print('number_of_cuts:',cuts)
                    print('optimal_value: does not exist')
                    return
                else:
                    for i in range(1,len(my_tableau[0])):
                        if (my_tableau[pivot_row_index][i])<0:
                            mini=min(mini,-1*my_tableau[0][i]/my_tableau[pivot_row_index][i])
                    for i in range(1,len(my_tableau[0])):
                        if (my_tableau[pivot_row_index][i])<0:
                            if (-1*my_tableau[0][i]/my_tableau[pivot_row_index][i]==mini):
                                pivot_column_index=i
                                break
                basicvarindex[pivot_row_index-1] = pivot_column_index
                my_tableau[pivot_row_index, :] /= my_tableau[pivot_row_index][pivot_column_index]
                my_tableau[pivot_row_index,:]=np.round(my_tableau[pivot_row_index,:],6)
                my_tableau=np.round(my_tableau,6)
                for row_index in range(my_tableau.shape[0]):
                    if(row_index != pivot_row_index):
                        my_tableau[row_index, : ] -= my_tableau[pivot_row_index, :] * my_tableau[row_index][pivot_column_index]
                        my_tableau[row_index, : ]=np.round(my_tableau[row_index, : ],6)
                pivot_row_index=-1
                for i in range(1,len(my_tableau)):
                    if (my_tableau[i][0]<0):
                        pivot_row_index=i
                        break
            x_=my_tableau[1:,0]
            
            ###################################################################################################################
            # if res==False:
            #     #dual is unbounded
            #     statusofsol='Infeasible'
            #     print('intitial_solution: ',optimal_sol)
            #     print('final_solution: does not exist')
            #     print('solution_status: infeasible')
            #     print('number_of_cuts: ',cuts)
            #     print('optimal_value: does not exist')
            #     return
            # else:
            #     continue
        with open("input_ilp.txt", 'r') as file:
            sections1 = file.read().split('[')

        sections1=sections1[1:]
        for i in range(len(sections1)):
            sections1[i]='['+sections1[i]

        A = np.array([list(map(float, line.split(','))) for line in sections1[1][3:].strip().split('\n')])
        # b = np.array(list(map(float, sections1[2][3:].strip().split('\n'))))
        # c = np.array(list(map(float, sections1[4][3:].strip().split(','))))
        ans=np.zeros(len(A[0]))
        for i in range(len(basicvarindex)):
            if (int(basicvarindex[i])-1<len(ans)):
                ans[int(basicvarindex[i])-1]=my_tableau[i+1][0]
        print('intitial_solution:',', '.join(map(str, optimal_sol)))
        print('final_solution:',', '.join(map(str, np.round(ans).astype(int))))
        print('solution_status: optimal')
        print('number_of_cuts:',cuts)
        if objective=='maximize':
            print('optimal_value:',round(my_tableau[0][0]))
        else:
            print('optimal_value:',round(-1*my_tableau[0][0]))
gomory_cut_algo()
