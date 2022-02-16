import sys
import copy
verbose = False
if sys.argv[1] == '-v':
  verbose = True
if verbose:
    mode = sys.argv[2]
    modechoice = sys.argv[3]
    inputfile = sys.argv[4]
else:
    mode = sys.argv[1]
    modechoice = sys.argv[2]
    inputfile = sys.argv[3]


#get all the unit-literal
def unit_atoms(sentence):
  unit_literal = []
  trans = []
  for m in sentence:
    if len(m) == 1:
      new_m = m[0]
      if new_m[-1] not in trans:
        trans.append(m[-1])
        unit_literal.append(new_m)
  return unit_literal

#get all the pure-literal
def pure_atoms(sentence):
  pure_literal = []
  all_atoms = []
  for n1 in sentence:
    for n2 in n1:
      if n2 not in all_atoms:
        all_atoms.append(n2)
  for n3 in all_atoms:
    countnumber = 0
    for n4 in all_atoms:
      if n3[-1] == n4[-1]:
        countnumber = countnumber + 1
    if countnumber == 1:
      pure_literal.append(n3)
  return pure_literal

#assign_value
def assign_value(L,atoms_value,sentence):
  for i in range(0,len(L)):
    new_value = L[i]
    if atoms_value[atoms.index(new_value[-1])] == "UNBOUND":
      if len(new_value) == 1:
        assign_position = atoms.index(new_value)
        atoms_value[assign_position] = "True"
      elif len(new_value) > 1:
        assign_position = atoms.index(new_value[-1])
        atoms_value[assign_position] = "False"
  return atoms_value


# dp1
def dp1(atoms, sentence, atoms_value):
    while True:
        if not (sentence):
            # 在cnf为空但仍然有字母没有赋值时，给这些字母直接赋值false
            for a1 in range(0, len(atoms_value)):
                # 查找atoms_value，值仍然为unbound的字母全部赋值false
                if atoms_value[a1] == "UNBOUND":
                    atoms_value[a1] = "False"
                    if verbose:
                        print("Unbound", atoms[a1], "=", atoms_value[a1])
            for j in range(0, len(atoms)):
                print(atoms[j], "=", atoms_value[j])
            return ""
        # easy case
        # if exist pure-Literal
        elif (pure_atoms(sentence)):  # 如果存在pure_atom
            L = pure_atoms(sentence)  # get the list of pure-literal
            atoms_value = assign_value(L, atoms_value, sentence)  # 给pure-literal赋值
            for pure in L:  # 对pure进行赋值
                pure_position = atoms.index(pure[-1])
                pure_value = atoms_value[pure_position]
                if verbose:
                    print("easy case:", atoms[pure_position], "=", pure_value)
                # 对于sentence里的每一行, remove这个clause
                sentence = [clause for clause in sentence if pure not in clause]
            if verbose:
                A = sentence.copy()
                for c in A:
                    c = " ".join(c)
                    print(c)
        # if exist unit-literal
        elif (unit_atoms(sentence)):
            L = unit_atoms(sentence)  # get the list of unit-literal
            atoms_value = assign_value(L, atoms_value, sentence)  # 给unit-literal赋值
            for unit in L:  # 得到unit在atoms_value里的坐标
                unit_position = atoms.index(unit[-1])
                unit_value = atoms_value[unit_position]
                if verbose:
                    print("easy case:", atoms[unit_position], "=", unit_value)  # 输出easy case的值
                for clause in sentence:
                    if len(clause) < 2:
                        if "!" in str(set(clause)) and atoms_value[atoms.index(str(set(clause))[3])] == "True":
                            if verbose:
                                print("".join(clause), "contradiction")
                            return "NIL"
                            break
                        elif "!" not in str(set(clause)) and atoms_value[atoms.index(str(set(clause))[2])] == "False":
                            if verbose:
                                print("".join(clause), "contradiction")
                            return "NIL"
                            break
                sentence = propagate(L, sentence, atoms_value)  # remove所在行和删除反词
        else:
            break
    # hard case
    for t in range(0, len(atoms) - 1):
        if atoms_value[t] == "UNBOUND":
            position = t
            break
    atoms_value[position] = "True"
    if verbose:
        print("hard case, guess:", atoms[position], "=", atoms_value[position])
    s1 = copy.deepcopy(sentence)
    s2 = copy.deepcopy(sentence)
    atoms_value_2 = copy.deepcopy(atoms_value)
    s1 = propagate(atoms[position], s1, atoms_value)
    vnew = dp1(atoms, s1, atoms_value)
    if vnew != "NIL":
        return vnew
    elif vnew == "NIL":
        atoms_value = copy.deepcopy(atoms_value_2)
        atoms_value[position] = "False"
        if verbose:
            print("fail|hard case, try:", atoms[position], "=", atoms_value[position])
        s2 = propagate(atoms[position], s2, atoms_value)
        return dp1(atoms, s2, atoms_value)


#propagate
def propagate(L,sentence,atoms_value):
  for delete_atom in L:
      not_atom = "!" + delete_atom[-1]
      yes_atom = delete_atom[-1]
      p_position = atoms.index(yes_atom)
      if atoms_value[p_position] == "False":
        remove_list = []
        for clause in sentence:
          if not_atom in clause:
            remove_list.append(clause)
          if yes_atom in clause:
            clause.remove(yes_atom)
          if not_atom in clause and yes_atom in clause:
            remove_list.append(clause)
        for remove_c in remove_list:
          sentence.remove(remove_c)
      elif atoms_value[p_position] == "True":
        remove_list = []
        for clause in sentence:
          if yes_atom in clause:
            remove_list.append(clause)
          if not_atom in clause:
            clause.remove(not_atom)
          if not_atom in clause and yes_atom in clause:
            remove_list.append(clause)
        for remove_c in remove_list:
          sentence.remove(remove_c)
  if verbose:
      A = sentence.copy()
      for c in A:
          c = " ".join(c)
          print(c)
  return sentence





if modechoice == "dpll":
    # read CNF file,get list of CNF
    file = open(inputfile, "r")
    cnf_input = []
    for line in file.readlines():
        line = line.strip()
        each = line.split()
        cnf_input.append(each)
    for cnf in cnf_input:
        cnf = " ".join(cnf)
        print(cnf)

    #get atoms
    atoms = []
    s_for_atoms = []
    for i in cnf_input:
        new = [t.strip('!') for t in i]
        s_for_atoms.append(new)
    for j in s_for_atoms:
        for k in j:
            if k not in atoms:
                atoms.append(k)
    atoms = sorted(atoms)

    # dp
    atoms_value = []
    for A in atoms:
        atoms_value.append("UNBOUND")

    result = dp1(atoms, cnf_input, atoms_value)
    print(result)


elif modechoice != "dpll":
  sys.exit("error: you choose a wrong mode")
