import sys
command = sys.argv
df = "e2"
k = 3
voting = "1/d"
if "-k" in command:
    p_k = command.index("-k") + 1
    k = int(command[p_k])
if "-d" in command:
    p_d = command.index("-d") + 1
    df = command[p_d]
if "-unitw" in command:
    p_u = command.index("-unitw") + 1
    voting = command[p_u]
if "-train" in command:
    p_t = command.index("-train") + 1
    f_train = command[p_t]
if "-test" in command:
    p_e = command.index("-test") + 1
    f_test = command[p_e]


#read file
file_train = open(f_train,"r")
file_test = open(f_test,"r")
i = 0 #get the number of lines in file
train = []
test = []
for line in file_train.readlines():
  line = line.strip()
  each = line.split(",")
  for i in range(0,len(each)-1):
    each[i] = float(each[i])
  train.append(each)
for line in file_test.readlines():
  line = line.strip()
  each = line.split(",")
  for i in range(0,len(each)-1):
    each[i] = float(each[i])
  test.append(each)

category_number = 0
category = []
for t in train:
  if t[-1] not in category:
    category.append(t[-1])
    category_number += 1
category = sorted(category)

distance = []
classify_result = []

for cp in test:

  classify_point = cp[:-1]
  calculate_result = []
  for tp in train:
    train_point = tp[:-1]
    result = 0
    for c in range(0,len(train_point)):
      if df == "e2":
        result += pow(classify_point[c] - train_point[c],2)
      elif df == "manh":
        result += abs(classify_point[c] - train_point[c])
    calculate_result.append(result)
  find_copy = calculate_result.copy()
  find_k = []
  index_list = []
  train_classify = []
  for fd in range(0,k):
    min_value = min(find_copy)
    find_k.append(min_value)
    k_place = find_copy.index(min_value)
    index_list.append(k_place)
    find_copy[k_place] = 1000000000
    train_classify.append(train[k_place][-1])
  category_score = [0] * category_number
  if voting == "unit":
    for c in train_classify:
      place = category.index(c)
      category_score[place] += 1
    max_score = max(category_score)
    max_score_place = category_score.index(max_score)
    classify_result.append(category[max_score_place])
  elif voting == "1/d":
    for h in range(0,len(train_classify)):
      place = category.index(train_classify[h])
      category_score[place] += 1/max(find_k[h],0.0001)
    max_score = max(category_score)
    max_score_place = category_score.index(max_score)
    classify_result.append(category[max_score_place])


true_classify = []
for tc in test:
  true_classify.append(tc[-1])
for ou in range(0,len(classify_result)):
  midd = []
  midd.append("want = ")
  midd.append(true_classify[ou])
  midd.append("  ")
  midd.append("got = ")
  midd.append(classify_result[ou])
  classify_print = "".join(midd)
  print(classify_print)

#precision
precision = []
recall = []
for c in category:
  true_positive = 0
  false_positive = 0
  false_negative = 0
  m_p = []
  m_r = []
  for f in range(0,len(true_classify)):
    if c != true_classify[f]:
      if c == classify_result[f]:
        false_positive += 1
    elif c == true_classify[f]:
      if c == classify_result[f]:
        true_positive += 1
      elif c != classify_result[f]:
        false_negative += 1
  mp_denominator = true_positive + false_positive
  mr_denominator = true_positive + false_negative
  m_p.append(str(true_positive))
  m_p.append("/")
  m_p.append(str(mp_denominator))
  m_r.append(str(true_positive))
  m_r.append("/")
  m_r.append(str(mr_denominator))
  mp = "".join(m_p)
  mr = "".join(m_r)
  precision.append(mp)
  recall.append(mr)


for p in range(0,len(category)):
  mid = []
  mid.append("Label = ")
  mid.append(category[p])
  mid.append("  ")
  mid.append("Precision = ")
  mid.append(str(precision[p]))
  mid.append("  ")
  mid.append("Recall = ")
  mid.append(str(recall[p]))
  evaluation_print = "".join(mid)
  print(evaluation_print)


