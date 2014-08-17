from src.services import sort_transactions

if __name__ == '__main__':
    # ## Results will be in ../sort_result directory
    sort_transactions(["../inputs/sort_problem/sample_input.csv"], "out")
    print "Finished"