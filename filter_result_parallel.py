import multiprocessing as mp

from filter_result import filter_result


title = "nds-brkga_bi"

num_target_solutions=100
if __name__ == "__main__":
    graph_name_list = [
                    "ch150",
                    "eil76",
                    "ch130",
                    "d657",
                    "eil51",
                    "eil101",
                    "gil262",
                    
                    "kroA100",
                    "kroA150",
                    "kroA200",
                    "kroB100",
                    "kroB150",
                    
                    "kroB200",
                    "kroC100",
                    "kroD100",
                    "kroE100"
                    ]
    num_nodes_list = []
    for graph_name in graph_name_list:
        num_nodes = 0
        for c in graph_name:
            if c in "0123456789":
                num_nodes = num_nodes*10+int(c)
        num_nodes_list += [num_nodes]
    num_items_list = [1,3,5,10]
    instance_type_list = [
        "bounded-strongly-corr",
        "uncorr",
        "uncorr-similar-weights"]
    dataset_name_list = []
    for gi, graph_name in enumerate(graph_name_list):
        num_nodes = num_nodes_list[gi]
        for num_items in num_items_list:
            total_num_items = num_items*(num_nodes-1)
            for instance_type in instance_type_list:
                for idx in ["01","02","03","04","05","06","07","08","09","10"]:    
                    dataset_name = graph_name+"_n"+str(total_num_items)+"_"+instance_type+"_"+idx
                    dataset_name_list += [dataset_name]
    config_list = [(title, dataset_name_list[i], num_target_solutions) for i in range(len(dataset_name_list))]
        # run(config_list[0])
    # filter_result_args = [(title, dataset_name, num_target_solutions) for dataset_name in dataset_name_list]
    with mp.Pool(processes=4) as pool:
        L = pool.starmap(filter_result, config_list)