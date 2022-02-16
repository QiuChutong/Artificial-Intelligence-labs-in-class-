import sys
import math
import numpy as np
#read order
verbose = False
if sys.argv[1] == '-v':
  verbose = True
if verbose:
  if sys.argv[8] == '-depth':
    start = sys.argv[2]
    startnode = sys.argv[3]
    goal = sys.argv[4]
    goalnode = sys.argv[5]
    alg = sys.argv[6]
    algchoice = sys.argv[7]
    depth = sys.argv[8]
    depthchoice = sys.argv[9]
    graphfile = sys.argv[10]
  else:
    start = sys.argv[2]
    startnode = sys.argv[3]
    goal = sys.argv[4]
    goalnode = sys.argv[5]
    alg = sys.argv[6]
    algchoice = sys.argv[7]
    graphfile = sys.argv[8]
else:
  if sys.argv[7] == '-depth':
    start = sys.argv[1]
    startnode = sys.argv[2]
    goal = sys.argv[3]
    goalnode = sys.argv[4]
    alg = sys.argv[5]
    algchoice = sys.argv[6]
    depth = sys.argv[7]
    depthchoice = sys.argv[8]
    graphfile = sys.argv[9]
  else:
    start = sys.argv[1]
    startnode = sys.argv[2]
    goal = sys.argv[3]
    goalnode = sys.argv[4]
    alg = sys.argv[5]
    algchoice = sys.argv[6]
    graphfile = sys.argv[7]

file = open(graphfile,"r")
i = 0 #get the number of lines in file
text = []
for line in file.readlines():
  line = line.strip()
  each = line.split()
  text.append(each)
length = len(text)


#Locate two blank rows to determine where the information of coordinate and relationship begin
new_text = []
t = 0
for i in range(0,length):
  if '#' in text[i]:
    i = i+1
    t = t+1
  else:
    if not len(text[i]):
      i= i+1
      t = t+1
    else:
      new_text.append(text[i])
new_length = len(new_text)

#get all the node

na = []
nx = []
ny = []
for tp in range(0,new_length):
  element = new_text[tp]
  node = element[0]
  if node not in na:
    na.append(node)
node = np.array(na) #get all the nodes
nodenumber=len(node)


nx = []
ny = []
for xy in range(0,nodenumber):
  element = new_text[xy]
  x = element[1]
  y = element[2]
  nx.append(x)
  ny.append(y)
x = np.array(nx)
y = np.array(ny)

for a in range(nodenumber,new_length):
  element1 = new_text[a]
  el1 = element1[0]
  el2 = element1[1]
  if el1 not in node:
    sys.exit("error: an edge referencing a vertex not in the file")
  if el2 not in node:
    sys.exit("error: an edge referencing a vertex not in the file")
if startnode not in node:
  sys.exit("error: startnode not in the file")
if goalnode not in node:
  sys.exit("error: goalnode not in the file")


relation = []
for line1 in range(nodenumber,new_length):
  relation.append(new_text[line1])
relation = np.array(relation)
rl = len(relation)

#create an adjacency matrix, adjacency[i] have all the adjacency nodes of node[i]
adjacency = []
adjacency_matrix = np.matrix([0])
for t1 in range(0,nodenumber-1):
  adjacency_matrix = np.insert(adjacency_matrix,1,0,axis=1) #create a matrix
for h in range(0,nodenumber):
  adjacency = np.matrix([node[h]])
  line_number = 0
  for d in range(0,rl):
    if node[h] in relation[d]:
      element2 = np.split(relation[d],2)
      ell1 = np.array(element2[0])
      ell2 = np.array(element2[1])
      if ell1 != node[h]:
        adjacency = np.insert(adjacency,1,ell1,axis=1)
        line_number = line_number+1
      if ell2 != node[h]:
        adjacency = np.insert(adjacency,1,ell2,axis=1)
        line_number = line_number+1
  adjacency = np.delete(adjacency,0)
  adjacency = np.sort(adjacency,axis=1) #sort the adjacencies of a node
  for e in range(line_number,nodenumber):
    adjacency = np.insert(adjacency,line_number,"0")
  adjacency_matrix = np.concatenate((adjacency_matrix,adjacency),axis=0)
adjacency_matrix = np.delete(adjacency_matrix,0,axis=0)

#adjacency matrix
adja_use = adjacency_matrix
adja_use = np.insert(adja_use,0,node.T,axis=1)
adja_use = np.delete(adja_use,nodenumber,axis=1)

h_matrix = []
for a1 in range(0,nodenumber):
  #find the position of goalnode
  if node[a1] == goalnode:
    goal_position = a1
for a2 in range(0,nodenumber):
  x2 = math.pow((int(x[a2])-int(x[goal_position])),2)
  y2 = math.pow((int(y[a2])-int(y[goal_position])),2)
  distance = math.sqrt(x2+y2)
  distance = round(distance,2)
  h_matrix.append(distance)
h_matrix = np.array(h_matrix)

hmatrix = adja_use.copy()
for hm1 in range(0,nodenumber):
  for hm2 in range(0,nodenumber):
    find = adja_use[hm1,hm2]
    if find == "0":
      hmatrix[hm1,hm2] = "0"
    else:
      for fin1 in range(0,nodenumber):
        #find the position of startnode
        if node[fin1] == find:
          find_position = fin1
      hmatrix[hm1,hm2] = h_matrix[find_position]


transi = np.matrix(['0'])
ASTAR_value = np.matrix([])
for astr in range(0,nodenumber+1):
  ASTAR_value = np.insert(ASTAR_value,0,0) #创建一个全0行避免insert出现问题
for v1 in range(0,nodenumber): #通过v1限制在adja_use的第几行（即计算哪一个node的邻接点距离）
  count = 0
  if node[v1] == adja_use[v1,0]: #找到node的index，等会计算它与其他邻接点的距离
    node1_position = v1  #node1_position存放index
  v2 = 0
  while adja_use[node1_position,v2] != "0": #如果取到0就停止
    for v3 in range(0,nodenumber):
      if node[v3] == adja_use[node1_position,v2]: #得到各个对应坐标
        node2_position = v3
    x3 = math.pow((float(x[node1_position])-float(x[node2_position])),2)
    y3 = math.pow((float(y[node1_position])-float(y[node2_position])),2)
    value2 = float(round(math.sqrt(x3+y3),2))
    transi = np.append(transi,[[value2]],axis=1)
    count = count+1
    v2 = v2+1
  for v5 in range(0, nodenumber-count):
    transi = np.insert(transi,v2+1,0)
  ASTAR_value=np.concatenate((ASTAR_value,transi))
  transi = np.matrix(['0'])
ASTAR_value = np.delete(ASTAR_value,0,0)
ASTAR_value = np.delete(ASTAR_value,0,1)


def BFS(startnode,goalnode):
  import warnings
  import numpy as np
  for i4 in range(0, nodenumber):
    if node[i4] == goalnode:
      end_index = i4
  if adja_use[end_index, 1] == "0":
    print("No solution")
  node_position = 0  # store the position of startnode in node matrix
  parent = np.matrix([])  # create a matrix to store the parent of each node in path
  for pp in range(0, nodenumber):
    parent = np.insert(parent, 0, 0)
  BFS_visited = np.matrix(["0"])  # visited nodes
  length_visit = len(BFS_visited)  # make sure whether visited all the nodes
  start_node = np.array([startnode])  # store the nodes wait for expanding
  line = 0
  warnings.simplefilter(action="ignore", category=FutureWarning)
  while goalnode != startnode:
    if verbose:
      print('Expanding:', startnode)
    count = 1
    if startnode not in BFS_visited:
      transition = np.matrix([startnode])
      for p1 in range(0, nodenumber):
        if node[p1] == startnode:
          node_position = p1
      for p2 in range(0, nodenumber):
        adja = adjacency_matrix[node_position, p2]
        if adja == "0":
          break
        else:
          if adja not in parent:
            start_node = np.insert(start_node, 0, adja, axis=0)
            transition = np.insert(transition, count, adja, axis=1)
            count = count + 1
      for p3 in range(count, nodenumber):
        transition = np.insert(transition, count, "0")
      st_p = len(start_node) - 1
      BFS_visited = np.insert(BFS_visited, 0, start_node[st_p])
      parent = np.concatenate((parent, transition))
      start_node = np.delete(start_node, st_p)
      startnode = np.array(start_node[st_p - 1])
      line = line + 1

  parent = np.delete(parent, 0, axis=0)
  path = np.array([goalnode])
  p4 = line - 1
  picture = str("->")
  while p4 >= 0:
    if goalnode in parent[p4, :]:
      path = np.append(path, picture)
      path = np.append(path, np.array(parent[p4, 0]))
      goalnode = parent[p4, 0]
      p4 = p4 - 1
    else:
      p4 = p4 - 1
  final_path = " ".join(path[::-1])
  print("Solution: " + final_path)

def ASTAR(startnode,goalnode):
  import numpy as np
  for i4 in range(0, nodenumber):
    if node[i4] == goalnode:
      end_index = i4
  if adja_use[end_index, 1] == "0":
    print("No solution")
  compare = []
  path = [[10000000000]]
  gpr = [0]
  transition1 = [0]
  value = [10000000000]
  countast = 1
  g_prior = 0
  final_path = []
  expand_content = startnode
  picture = "->"
  addingString = ""
  while startnode != goalnode:

    for as1 in range(0, nodenumber):

      if node[as1] == startnode:
        startnode_position = as1

    for as2 in range(1, nodenumber):
      if adja_use[startnode_position, as2] == "0":
        break
      else:

        transition1 = [0]
        transition1.extend(expand_content)
        transition1.extend(adja_use[startnode_position, as2])

        g = round(g_prior + float(ASTAR_value[startnode_position, as2]),2)
        h = round(float(hmatrix[startnode_position, as2]),2)
        f = round(g + h, 2)

        gpr.append(g)
        value.append(f)
      transition1.remove(0)
      tempTransition = transition1
      if verbose:
        addingTransition = np.array(transition1)
        if addingTransition.size >= 3:
          addingTransition = addingTransition[:-1]
          tempAddingString = ""
          for index in range(0, addingTransition.size):
            tempAddingString += addingTransition[index]
            if index != addingTransition.size - 1:
              tempAddingString += " -> "
          if addingString != tempAddingString:
            addingString = tempAddingString
            print("adding ", addingString)

        transition1 = transition1[-2:]
        mark1 = transition1.pop()
        mark2 = transition1.pop()

        print(mark2, picture, mark1, ";", "g=", g, " h=", h, " =", f)

      path.append(tempTransition)
      countast = countast + 1
    min_value = min(value)
    min_index = value.index(min_value)

    expand_content = path[min_index]
    g_prior = gpr[min_index]

    value.pop(min_index)
    path.pop(min_index)
    gpr.pop(min_index)
    startnode = expand_content[len(expand_content) - 1]

  prinlen = len(expand_content)
  for plt in range(0, prinlen):
    final_path.append(expand_content[plt])
    final_path.append(picture)
  final_path.pop()
  final_path = " ".join(final_path)
  print("Solution: " + final_path)

def ID(startnode,goalnode,depthchoice):
  import numpy as np
  if depthchoice.isdigit() == False:
    sys.exit("error: please input a number as initial depth")
  if startnode == goalnode:
    print("startnode = goalnode")
    print("Solution: ")
    sys.exit(startnode)
  for i4 in range(0, nodenumber):
    if node[i4] == goalnode:
      end_index = i4
  if adja_use[end_index, 1] == "0":
    print("No solution")
  parent = [""]
  adja_depth = [[startnode]]
  visit_depth = [[startnode]]
  depth_value = [0]
  D = 0
  visit = []
  while goalnode not in visit:
    search = visit_depth[D]  # 取出depth D对应的visit_depth行
    len_search = len(search)  # 找到循环范围
    line = []
    line1 = []
    D = D + 1
    for i1 in range(0, len_search):
      startnode = search[i1]  # 从第一个值开始做startnode
      parent.append(startnode)
      line1 = []
      for i2 in range(0, nodenumber):
        if node[i2] == startnode:
          startnode_position = i2
      for i3 in range(1, nodenumber):
        adja = adja_use[startnode_position, i3]  # 得到逐个邻接点
        if adja == "0":
          break
        elif adja not in parent:
          line.append(adja)
          line1.append(adja)
          visit.append(adja)
        else:
          i3 = i3 + 1
      adja_depth.append(line1)
      depth_value.append(D)
    visit_depth.append(line)

  depth_max = max(depth_value)
  parent.pop(0)
  adja_depth.pop(0)
  depth_value.pop(0)
  pre = []
  if verbose:
    for pl in range(0, len(parent)):
      if depth_value[pl] < int(depthchoice):
        print("Expand:", parent[pl])
      else:
        print("Expand:", parent[pl])
        wait = adja_depth[pl]
        for pl1 in range(0, len(wait)):
          print("hit depth =", depth_value[pl], ":", wait[pl1])
  picture = "->"
  print_path = [goalnode]
  print_path.append(picture)
  for pl4 in range(0, len(adja_depth)):
    if goalnode in adja_depth[pl4]:
      end_position = pl4
      break
  max_depth = depth_value[end_position]
  while max_depth > 1:
    goalnode = parent[end_position]
    print_path.append(goalnode)
    print_path.append(picture)
    end_position = depth_value.index(max_depth)
    max_depth = max_depth - 1
    start_position = depth_value.index(max_depth)
    for pl5 in range(start_position, end_position):
      if goalnode in adja_depth[pl5]:
        end_position = pl5
  print_path.append(parent[0])
  print_path = " ".join(print_path[::-1])
  print("Solution: " + print_path)


if algchoice == 'BFS':
  BFS(startnode,goalnode)
if algchoice == 'ID':
  ID(startnode,goalnode,depthchoice)
if algchoice == 'ASTAR':
  ASTAR(startnode,goalnode)
elif algchoice != 'BFS' and algchoice != 'ID' and algchoice != 'ASTAR':
  sys.exit("error: you choose a wrong algorithm")
