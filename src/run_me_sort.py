from src.services import sort_transactions

if __name__ == '__main__':
    # ## Results will be in ../sort_result directory
    sort_transactions(["../inputs/sort_problem/sample_input.csv", "../inputs/sort_problem/sample_input1.csv", "../inputs/sort_problem/sample_input2.csv"], "out_sample_1")
    sort_transactions(["../inputs/sort_problem/sample_input.json"], "out_sample_2")
    print "Finished"