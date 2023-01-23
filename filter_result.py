import argparse
from collections import Counter
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np

from non_dominated_sorting import fast_non_dominated_sort
from max_hv_dp import get_solutions_with_max_hv

def get_args():
    parser = argparse.ArgumentParser(description='TTP-MORL')
    # GENERAL
    parser.add_argument('--dataset-name',
                        type=str,
                        default="a280-n279",
                        help="dataset's name for real testing")
    parser.add_argument('--title',
                        type=str,
                        default="att_phn",
                        help="title for experiment")
    parser.add_argument('--num-target-solutions',
                        type=int,
                        default=100,
                        help="number of target nondom solutions")
    
    return parser.parse_args(sys.argv[1:])


def filter_result(title, dataset_name, num_target_solutions):
    results_dir = pathlib.Path(".")/"results"
    model_result_dir = results_dir/title
    model_result_dir.mkdir(parents=True, exist_ok=True)
    nondom_result_dir = model_result_dir/"cleaned"
    y_file_path = model_result_dir/(title+"_"+dataset_name+".f")
    with open(y_file_path.absolute(), "r") as y_file:
        solution_list = []
        lines = y_file.readlines()
        for i, line in enumerate(lines):
            strings = line.split()
            tour_length = float(strings[0])
            profit = float(strings[1])
            solution_list += [tuple([tour_length, -profit])]
    unique_solution_counter = Counter(solution_list)
    unique_solution_list = []
    for k,v in enumerate(unique_solution_counter):
        unique_solution_list += [[v[0], v[1]]]
    unique_solution_list = np.asanyarray(unique_solution_list)
    nondom_idx = fast_non_dominated_sort(unique_solution_list)[0]
    nondom_solution_list = unique_solution_list[nondom_idx, :]
    if len(nondom_solution_list)>num_target_solutions:
        best_idx = get_solutions_with_max_hv(nondom_solution_list, num_target_solutions)
        nondom_solution_list = nondom_solution_list[best_idx]
    nondom_result_dir.mkdir(parents=True, exist_ok=True)
    nondom_y_file_path = nondom_result_dir/(title+"_"+dataset_name+".f")
    with open(nondom_y_file_path.absolute(), "w") as nondom_y_file:
        for i in range(len(nondom_solution_list)):
            tour_length = "{:.16f}".format(nondom_solution_list[i,0].item())
            total_profit = "{:.16f}".format(-nondom_solution_list[i,1].item())
            nondom_y_file.write(tour_length+" "+total_profit+"\n")

    # plt.scatter(unique_solution_list[:, 0], unique_solution_list[:, 1], c='b')
    # plt.scatter(nondom_solution_list[:, 0], nondom_solution_list[:, 1], c='r', marker="v")
    # plt.show()

if __name__ == "__main__":
    # read from results based on dataset name and title
    args = get_args()
    filter_result(args.title, args.dataset_name, args.num_target_solutions)
    