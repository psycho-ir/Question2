from src.services import sort_transactions

if __name__ == '__main__':
    # ## Results will be in ../sort_result directory
    sort_transactions(["../inputs/sort_problem/sample_input.csv","../inputs/sort_problem/sample_input1.csv","../inputs/sort_problem/sample_input2.csv"], "out")
    print "Finished"