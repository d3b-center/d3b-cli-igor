import os, sys, pathlib
import click, yaml
import d3b_cli_igor.common

logger = d3b_cli_igor.common.get_logger(
    __name__, testing_mode=False, log_format="detailed"
)


def diff_files(file1, file2):
    file1 = open(file1, "r")
    Lines_1 = file1.readlines()
    file2 = open(file2, "r")
    Lines_2 = file2.readlines()
    count_1 = 0
    for line1 in Lines_1:
        print("PROGRESS: " + str(count_1) + " out of " + str(len(Lines_1)))
        count_1 = count_1 + 1
        count = 1
        found = 0
        for line2 in Lines_2:
            if line1 == line2:
                found = 1
                break
            if count == len(Lines_2) and found == 0:
                print(line1)
            count = count + 1


def split_files(file_to_split, num_of_lines):
    file_to_split = open(file_to_split, "r")
    Lines = file_to_split.readlines()
    count = 0
    count_files = 0
    total_lines = len(Lines)
    number_of_lines_per_file = total_lines // int(num_of_lines)
    f = open("sublist" + str(count_files) + ".txt", "a")
    for line in Lines:
        f.write(line)
        if count == number_of_lines_per_file:
            f.close()
            count_files = count_files + 1
            f = open("sublist" + str(count_files) + ".txt", "a")
            count = 0
        count = count + 1
