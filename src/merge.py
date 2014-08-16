from multiprocessing import Queue, Process
from uuid import uuid4

__author__ = 'soroosh'
import os

orders = {'Payment': 1,
          'Deposit': 2,
          'Transfer': 3}


def find_all_files(dir_path):
    return os.listdir(dir_path)


def _compare(line1, line2):
    line1_parts = line1.split(' ')
    line2_parts = line2.split(' ')
    if orders[line1_parts[0]] < orders[line2_parts[0]]:
        return 1
    if orders[line1_parts[0]] > orders[line2_parts[0]]:
        return 2
    else:
        if float(line1_parts[2].strip()) > float(line2_parts[2].strip()): return 1
        return 2


def merge_file(queue):
    while True:
        try:
            item = queue.get(timeout=5)
            print 'reading %s and %s' %(item.file1,item.file2)
            with open(item.file1, 'r') as file1:
                with open(item.file2, 'r') as file2:
                    with open(item.merge_name, 'w') as out:
                        line1 = file1.readline()
                        line2 = file2.readline()
                        while line1 and line2:

                            cmp_reuslt = _compare(line1, line2)
                            if cmp_reuslt == 1:
                                out.write(line1)
                                line1 = file1.readline()
                            else:
                                out.write(line2)
                                line2 = file2.readline()
                        else:
                            if not line1:
                                for f in file2:
                                    out.write(f)
                            else:
                                for f in file1:
                                    out.write(f)

            os.remove(item.file1)
            os.remove(item.file2)

        except Exception as e:
            break


from datetime import datetime


class ReduceCommand:
    def __init__(self, file1, file2, merge_name):
        self.file1 = file1
        self.file2 = file2
        self.merge_name = merge_name


if __name__ == '__main__':
    q = Queue()
    path = '/home/soroosh/projects/schallenge/projects/Question2/outputs/sort_problem/sorted'
    os.chdir(path)
    start_time = datetime.now()
    all_files = find_all_files(path)
    counter = 0
    while True:
        all_files = find_all_files(path)
        if len(all_files) == 1:
            print 'Finished'
            break

        for i in range(len(all_files) / 2):
            f1 = '/home/soroosh/projects/schallenge/projects/Question2/outputs/sort_problem/sorted/' + all_files[i * 2]
            f2 = '/home/soroosh/projects/schallenge/projects/Question2/outputs/sort_problem/sorted/' + all_files[i * 2 + 1]
            merged_name = '/home/soroosh/projects/schallenge/projects/Question2/outputs/sort_problem/sorted/merge-' + str(uuid4()) + '.txt'
            q.put(ReduceCommand(f1, f2, merged_name))
            # merge_file(f1, f2, merged_name

        processes = [Process(target=merge_file, args=(q,), name='P-' + str(i)) for i in range(5)]

        for p in processes:
            p.start()
        for p in processes:
            p.join()









            # result = merge_file('/home/soroosh/projects/schallenge/projects/Question2/outputs/sort_problem/sorted/sort_output_sample_output_10.txt',
            # '/home/soroosh/projects/schallenge/projects/Question2/outputs/sort_problem/sorted/sort_output_sample_output_11.txt')
            #
            # end_time = datetime.now()
            # print end_time - start_time
            # with open('merge1.txt', 'a') as f:
            # f.writelines(result)

