import itertools
def Remove_Duplicate(List, Dict):
  return list(set(List) - set(Dict[0] + Dict[1]))

def FullSituation(same_extra_element):
  same_extra_points = list(same_extra_element.keys())
  new_dict = {}
  for point in same_extra_points:
    new_dict[(point,)] = Remove_Duplicate(same_extra_points, same_extra_element[point])
  return [[]] +[list(i) for i in ChoosePoint(same_extra_element,new_dict)]

def ChoosePoint(same_extra_element, new_dict, n = 1):
  l = [i for i in list(new_dict.keys())[:] if len(i) == n]
  if len(l) == 0:
    return list(new_dict.keys())
  Closed_points = []
  for p1 in l:
    for p2 in new_dict[p1]:
      Points_Chosen = list(p1) + [p2]
      if set(Points_Chosen) not in Closed_points:
        Closed_points.append(set(Points_Chosen))
        nl = Remove_Duplicate(new_dict[p1], same_extra_element[p2])
        new_dict[tuple(Points_Chosen)] = nl
  return ChoosePoint(same_extra_element, new_dict, n+1)

def Cartesian_product(list_sets):
  # Hàm cũ : CombineList
  # speed x5.3(đã test)
  list_tranform = []
  for i in list_sets:
    Set = [k for j in i for k in j]
    list_tranform.append(Set)
  return list(itertools.product(*list_tranform))