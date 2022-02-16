import sys
command = sys.argv
df = "e2"
if "-d" in command:
    p_d = command.index("-d") + 1
    df = command[p_d]
if "-data" in command:
    p_f = command.index("-data") + 1
    p_c_s = command.index("-data") + 2
    file = command[p_f]
    cen = command[p_c_s:]
centroids = []
for cend in cen:
    mid_each = []
    cend = cend.split(",")
    for ch in cend:
        chang = float(ch)
        mid_each.append(chang)
    centroids.append(mid_each)

#centroids = [[0,0],[200,200],[500,500]]
#centroids = [[0,0,0],[200,200,200],[500,500,500]]


#read file
input_file = open(file,"r")
i = 0 #get the number of lines in file
text = []
for line in input_file.readlines():
  line = line.strip()
  each = line.split(",")
  for i in range(0,len(each)-1):
    each[i] = float(each[i])
  text.append(each)


def classify(centroids):
  classify_result = []
  for point in text:
    calculate_result = []
    for ce in centroids:
      result = 0
      for i in range(0,len(ce)):
        if df == "e2":
          result += pow((point[i] - ce[i]),2)
        elif df == "manh":
          result += abs(point[i] - ce[i])
      calculate_result.append(result)
    min_value = min(calculate_result)
    min_place = calculate_result.index(min_value)
    classify_result.append(cluster[min_place])
  return classify_result

def find_centroids(classify_result):
  point_classify = []
  test_classify = []
  for ce in cluster:
    each_cluster = []
    each_test = []
    for i in range(0,len(classify_result)):
      if classify_result[i] == ce:
        each_cluster.append(text[i])
        each_test.append(text[i][-1])
    point_classify.append(each_cluster)
    test_classify.append(each_test)
  new_centroids = []
  for clu in point_classify:
    denominator = len(clu)
    if denominator == 0:
      point_average = [0] * len(centroids[0])
      new_centroids.append(point_average)
    else:
      sum_clu = []
      for ca in range(0,len(centroids[0])):
        sum = 0
        for t in range(0,denominator):
          sum += clu[t][ca]
        sum_clu.append(sum)
      point_average = sum_clu.copy()
      for mu in range(0,len(point_average)):
       point_average[mu] = float(sum_clu[mu]/denominator)
      new_centroids.append(point_average)
  return new_centroids


cluster = []
for i in range(1, len(centroids) + 1):
    mid = []
    mid.append("c")
    mid.append(str(i))
    addmid = "".join(mid)
    cluster.append(addmid)
get_result = False
while not (get_result):
    classify_result = classify(centroids)
    new_centroids = find_centroids(classify_result)
    new_classify_result = classify(new_centroids)
    for j in range(0, len(new_classify_result)):
        if new_classify_result[j] == classify_result[j]:
            get_result = True
            continue
        else:
            get_result = False
            break
    centroids = new_centroids

final_classify = []
for ce in cluster:
    mid_class = []
    for k in range(0, len(classify_result)):
        if classify_result[k] == ce:
            mid_class.append(text[k][-1])
    final_classify.append(mid_class)

for p in range(0, len(cluster)):
    mid_print = []
    mid_print.append(cluster[p])
    mid_print.append(" = ")
    mid_print.append("{")
    final = " , ".join(final_classify[p])
    mid_print.append(final)
    mid_print.append("}")
    print_out = "".join(mid_print)
    print(print_out)

for ce in centroids:
    mi_print = []
    mi_print.append("(")
    mi_print.append("[")
    fin = []
    for ch in ce:
        fin.append(str(ch))
    fina = "   ".join(fin)
    mi_print.append(fina)
    mi_print.append("]")
    mi_print.append(")")
    print_c = "".join(mi_print)
    print(print_c)

