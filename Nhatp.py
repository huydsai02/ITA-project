import itertools
def Remove_Duplicate(List, Dict):
  return set(List) - set(Dict[0] + Dict[1])

def FullSituation(same_extra_element):
  l_key, l_value = [], []
  l_intersect = {}
  result = [[]]
  same_extra_points = list(same_extra_element.keys())
  for i in range(len(same_extra_points)):
    point = same_extra_points[i]
    points = Remove_Duplicate(same_extra_points[:i], same_extra_element[point])
    if len(points) != 0:
      l_key.append([point])
      l_value.append(points)
    l_intersect[point] = points
    
  while True:
    if len(l_key) == 0:
      break
    old_points = l_key.pop()
    points_satisfy = l_value.pop()
    result.append(old_points[:])
    for point in points_satisfy:
      new_points = old_points + [point]
      new_points_satisfy = set.intersection(points_satisfy, l_intersect[point])
      l_key.append(new_points)
      l_value.append(new_points_satisfy)
  return result

def Cartesian_product(list_sets):
  # Hàm cũ : CombineList
  # speed x5.3(đã test)
  list_tranform = []
  for i in list_sets:
    Set = [k for j in i for k in j]
    list_tranform.append(Set)
  return list(itertools.product(*list_tranform))