import numpy as np

from hv import Hypervolume
from normalization import normalize

def get_area(p1, p2):
  max_x = max(p1[0],p2[0])
  max_y = max(p1[1],p2[1])
  min_x = min(p1[0],p2[0])
  min_y = min(p1[1],p2[1])
  area = (max_x-min_x)*(max_y-min_y)
  return area

def dp(n, m, N, A, memo, memoi, is_visited, maxR=1.1):
  if m==0:
    return 0, []
  r = np.asanyarray([maxR, A[n,1]])
  if is_visited[n][m]:
    return memo[n][m], memoi[n][m]
  num_solutions_eq_m = (N-(n+1) == m)
  if num_solutions_eq_m:
    HV = Hypervolume(r)
    hv = HV.calc(A[n+1:], is_nondom=True)
    is_visited[n][m]=True
    memo[n][m]=hv
    memoi[n][m]=[n+1+i for i in range(m)]
    return hv, memoi[n][m]
  
  hv = 0
  best_sol_idx = []
  for i in range(n+1,N-m+1):
    area = get_area(A[i], r)
    next_hv_, sol_idx = dp(i, m-1, N, A, memo, memoi, is_visited, maxR)
    hv_ = area + next_hv_
    if hv_>hv:
      hv = hv_
      best_sol_idx = [i] + sol_idx 
  is_visited[n][m]=True
  memo[n][m]=hv
  memoi[n][m]= best_sol_idx
  return hv, memoi[n][m]


def get_solutions_with_max_hv(solution_list, num_solutions):
  #input must be nondominated points
  s_ = solution_list.copy()
  s_ = normalize(s_)   
  idx_list = np.arange(len(s_))
  sort_idx = np.argsort(s_[:,0])
  s_ = s_[sort_idx]
  idx_list = idx_list[sort_idx]
  N, M = len(s_), num_solutions
  if N==M:
    return idx_list
  max_hv, best_idx = 0, []
  memo = [[0]*M for i in range(N)]
  is_visited = [[False]*M for i in range(N)]
  # memo, is_visited = np.zeros((N+1,M+1)), np.zeros((N+1,M+1), dtype=bool)
  memoi = [[[] for i in range(M)] for j in range(N)]
  r = np.asanyarray([1.1,1.1])  
  for i in reversed(range(N-M)):
    area = get_area(r, s_[1])
    max_hv_, best_idx_ = dp(i, M-1, N, s_, memo, memoi, is_visited)
    if area+max_hv_>max_hv:
      max_hv = area+max_hv_
      best_idx = [i]+best_idx_
  return idx_list[best_idx]
