import sys
verbose_df = False
verbose_min = False
verbose_tol = False
verbose_iter = False
command = sys.argv
df = 1
tol = 0.01
iter = 100
file = command[-1]
if "-df" in command:
    verbose_df = True
    po_df = command.index("-df") + 1
    df = float(command[po_df])
if "-min" in command:
    verbose_min = True
if "-tol" in command:
    verbose_tol = True
    po_tol = command.index("-tol") + 1
    tol = float(command[po_tol])
if "-iter" in command:
    verbose_iter = True
    po_iter = command.index("-iter") + 1
    iter = int(command[po_iter])
def get_reward_list(line):
  splited_line = line.split("=")
  reward_line = []
  reward_line.append(splited_line[0].strip())
  num = splited_line[1].strip()
  reward_line.append(float(num))
  return reward_line

def get_edge_list(line):
  edge_line = []
  split_m = line.split(":")
  edge_line.append(split_m[0].strip())
  no_left = split_m[1].split("[")
  no_right = no_left[1].split("]")
  no_dou = no_right[0].split(",")
  for nod in no_dou:
    edge_line.append(nod.strip())
  return edge_line

def get_probability_list(line):
  prob_line = []
  no_percentage = line.split("%")
  prob_line.append(no_percentage[0].strip())
  no_space = no_percentage[1].split(" ")
  if not(no_space[0]):
    for p in no_space[1:]:
      prob_line.append(float(p))
    return prob_line
  else:
    for p in no_space:
      prob_line.append(float(p))
    return prob_line

file = open(file,"r")
rewardc = []
value_edge = []
probability = []
for line in file.readlines():
  if "#" not in line and len(line)!=1:
    line = line.strip()
    if "=" in line:
      splited_reward = get_reward_list(line)
      rewardc.append(splited_reward) #this is not a full reward list
    elif ":" in line:
      splited_edge = get_edge_list(line)
      value_edge.append(splited_edge)
    elif "%" in line:
      splited_percentage = get_probability_list(line)
      probability.append(splited_percentage) #this is not a full prob list

#first column of value_edge is the start node of edge
#value_edge is for calculate value, contains chance node

#fill the case that have edge but not have prob with p = 1
prob_value = []
csp = []
for p in probability:
  csp.append(p[0])
for pv in value_edge:
  if pv[0] in csp:
    ind = csp.index(pv[0])
    prob_value.append(probability[ind])
  else:
    new_pro = []
    new_pro.append(pv[0])
    new_pro.append(float(1))
    prob_value.append(new_pro)

#get terminal chance and decision nodes
#terminal
reward_node = []
reward_reward = []
terminal_node = []
terminal_reward = []
value_edge_node = []
all_node = []
reward = []
for r in rewardc:
  reward_node.append(r[0])
  reward_reward.append(r[1])
#get reward and node from rewardc, only contains those give reward.
#find all the node in value_edge
for vn in value_edge:
  value_edge_node.append(vn[0])

#if a node in reward_node but not in value_edge_node, then it is a terminal
#if a node not in reward_node but in value_edge_node, then it need to be add to reward_node to be all node
for nod in value_edge_node:
  if nod in reward_node:
    index_reward_node = reward_node.index(nod)
    this_reward = reward_reward[index_reward_node]
    all_node.append(nod)
    reward.append(this_reward)
  else:
    all_node.append(nod)
    reward.append(float(0))
for nos in reward_node:
  if nos not in value_edge_node:
    terminal_node.append(nos)
    this_index = reward_node.index(nos)
    terminal_reward.append(reward_reward[this_index])
    all_node.append(nos)
    reward.append(reward_reward[this_index])

#reward is the full list of reward



#chance node and decision node
chance_node = []
chance_edge = []
decision_node = []
chance_prob = []
chance_reward = []
chance_prob = []
decision_edge = []
decision_reward = []
decision_prob = []
for i in range(0,len(value_edge)):
  a = prob_value[i]
  b = a[0]
  if len(prob_value[i]) == len(value_edge[i]):
    chance_node.append(b)
    chance_edge.append(value_edge[i])
    ind = all_node.index(b)
    chance_reward.append(reward[ind])
    chance_prob.append(prob_value[i])
  else:
    decision_node.append(b)
    decision_edge.append(value_edge[i])
    ind = all_node.index(b)
    decision_reward.append(reward[ind])
    decision_prob.append(prob_value[i])
#decision node and decision edge can be used to select policy

#initial value
initial_value = [0]*len(all_node)
for i in range(0,len(all_node)):
  if all_node[i] in terminal_node:
    initial_value[i] = reward[i]
  else:
    continue
#initial policy
#select the first edge of each decision node as the initial policy
initial_policy = []
for start in decision_edge:
  trp = []
  st = start[0]
  trp.append(st)
  sd = start[1]
  trp.append(sd)
  initial_policy.append(trp)

#calculate probability list, contains the prob for chance and decision node
def policy_value_prob(policy):
  policy_prob = []
  #fill the prob, add 1-p
  for i in range(0,len(value_edge)):
    nod = value_edge[i]
    f = len(nod)
    tranp = []
    pnod = prob_value[i]
    d_or_c = nod[0]
    tranp.append(d_or_c)
    if d_or_c in chance_node:
      for i in range(1,f):
        pr = pnod[i]
        tranp.append(pr)
      policy_prob.append(tranp)
    elif d_or_c in decision_node:
      p = pnod[1] #get p
      ind = decision_node.index(d_or_c)
      policy_position = policy[ind]
      p_position = policy_position[1]
      p_p = nod.index(p_position)
      fn = (1-p)/(f-2) #get 1-p
      for i in range(1,f):
        tranp.append(fn)
      tranp[p_p] = p
      policy_prob.append(tranp)
  return policy_prob

#prob is the result of def policy_value_prob
def ValueIteration(value,prob):
  previous_value = value.copy()
  next_value = value.copy()
  for i in range(0,iter):
    for j in range(0,len(value_edge)):
      edge = value_edge[j] #get the edge of this node
      edge_value = []
      rp = all_node.index(edge[0]) #get the node need to be calculated
      next_value[j] = reward[rp] #v𝜋(s) = R(s)
      for e in edge:
        po = all_node.index(e) #find the corresponding index in all node
        edge_value.append(previous_value[po]) #append values to edge_value
      value_prob = prob[j] #get pro list of node
      for k in range(1,len(edge_value)):
        next_value[j] = next_value[j] + df * edge_value[k] * value_prob[k]
      #next_value[j] = round(next_value[j],3)
    next = False
    for c in range(0,len(previous_value)):
        if abs(previous_value[c] - next_value[c]) > tol:
            next = True
            break
    previous_value = next_value.copy()
    if not(next):
        return next_value
    #previous_value = next_value.copy()
  #return next_value


def GreedyPolicyComputation(values):
  new_policy = []
  for i in range(0,len(decision_edge)):
    sub_policy = []
    sub_policy.append(decision_edge[i][0]) #add start node of policy
    p = decision_prob[i][1]
    if len(decision_edge[i]) == 2:
      not_p = 0
    else:
      not_p = (1-p)/(len(decision_edge[i])-2) #get p and 1-p
    change_position = len(decision_edge[i])-1
    #print("decision_edge[i]",decision_edge[i])
    sub_prob = []
    for n in range(0,change_position):
      s_prob = [not_p] * change_position
      s_prob[n] = p
      sub_prob.append(s_prob)  #get sub_prob list, contains all the possible prob case
    #print("sub_prob",sub_prob)
    sub_value = []
    for nod in decision_edge[i][1:]:
      po = all_node.index(nod)
      #print("po",po)
      po_value = values[po]
      #print("po_value",po_value)
      sub_value.append(po_value) #get value list
    #print("sub_value",sub_value)
    result = []
    for h in range(0,len(sub_prob)):
      a = sub_prob[h]
      re = 0
      for m in range(0,len(sub_prob[h])):
        re += df * a[m] * sub_value[m]
      result.append(re) #get the result of all the cases
    #print("result",result)
    if (verbose_min):
        min_value = min(result)
        min_index = result.index(min_value) + 1
        sub_policy.append(decision_edge[i][min_index])
    elif not(verbose_min):
        max_value = max(result)  # find the max result
        # print("max value",max_value)
        max_index = result.index(max_value) + 1
        # print("max index",max_index)
        sub_policy.append(decision_edge[i][max_index])
    #print("sub policy",sub_policy)
    new_policy.append(sub_policy) #choose the max policy as the new policy
  return new_policy


policy = initial_policy
values = initial_value.copy()
if not (decision_node):  # if no policy, just output decision node
    policy_prob = policy_value_prob(policy)
    new_values = ValueIteration(values, policy_prob)
    value_print = []
    for i in range(0, len(all_node)):
        start_node = all_node[i]
        end_value = round(new_values[i],3)
        sub_print = []
        sub_print.append(start_node)
        sub_print.append("=")
        sub_print.append(str(end_value))
        sub_print.append("  ")
        add_value = "".join(sub_print)
        value_print.append(add_value)
    value_result_print = "".join(value_print)
    print(value_result_print)

elif (decision_node):
    get_result = False
    while not (get_result):
        policy_prob = policy_value_prob(policy)
        new_values = ValueIteration(values, policy_prob)
        new_policy = GreedyPolicyComputation(new_values)
        for i in range(0, len(policy)):
            if policy[i][1] == new_policy[i][1]:
                get_result = True
                continue
            else:
                get_result = False
                break
        policy = new_policy
    output_policy = []
    for p in policy:
        if p[0] in chance_node:
            continue
        if p[0] in terminal_node:
            continue
        else:
            output_policy.append(p)

    for pol in output_policy:
        start_p = pol[0]
        end_p = pol[1]
        sub_pol = []
        sub_pol.append(start_p)
        sub_pol.append(" ")
        sub_pol.append("->")
        sub_pol.append(" ")
        sub_pol.append(end_p)
        policy_print = "".join(sub_pol)
        print(policy_print)
    print("")
    value_print = []
    for i in range(0, len(all_node)):
        start_node = all_node[i]
        end_value = round(new_values[i],3)
        sub_print = []
        sub_print.append(start_node)
        sub_print.append("=")
        sub_print.append(str(end_value))
        sub_print.append("  ")
        add_value = "".join(sub_print)
        value_print.append(add_value)
    value_result_print = "".join(value_print)
    print(value_result_print)
