# -*- coding: utf-8 -*-
##############################################################################
#
##############################################################################
#   DATE   | VERSION |  AUTHOR  |  CHANGELOG
#----------|---------|----------|---------------------------------------------
# 26-06-30 |  0.0.1  | asasson  | Initial draft
##############################################################################
#
##############################################################################
# LICENSE                                #
##############################################################################

import argparse
import numpy as np
import math, time
import yaml

parser = argparse.ArgumentParser(prog="pyres",
        description='''Back-calculate resistor combinations to achieve a
        target resistance using standard tolerance parts.''',
        epilog='''Published under a TBD license''')
parser.add_argument("target", type=float, help = "target resistance")
parser.add_argument("tol", type=float, default = 1.0,
                    help = "target tolerance (10, 1, 0.1, etc)%%")
parser.add_argument("-e6", action="store_true",
                    help = "Enable 20%% resistors")
parser.add_argument("-e12", action="store_true",
                    help = "Enable 10%% resistors")
parser.add_argument("-e24", action="store_true",
                    help = "Enable  5%% resistors")
parser.add_argument("-e48", action="store_true",
                    help = "Enable  2%% resistors")
parser.add_argument("-e96", action="store_true",
                    help = "Enable  1%% resistors")
parser.add_argument("-e192", action="store_true",
                    help = "Enable  0.5%% resistors")
parser.add_argument("-c", "--csv", type=str, nargs='?',
                    help = "Write output to csv file")
parser.add_argument("-m", "--maxdevices", type=int, default=0,
                    help = "Max # of parts to consider")
parser.add_argument("-p", "--parallel", action="store_true",
                    help = "enable parallel calculation")
parser.add_argument("-s", "--series", action="store_true",
                    help = "enable series calculation")
parser.print_help()

# Load the YAML file
with open('resistors.yml', 'r') as file:
    resistor_values = yaml.safe_load(file)

def find_series_combos(target, tol, val, md):
    res, sums = [], []
    lower = target * (1 - tol)
    upper = target * (1 + tol)
    print("TARGET: ", lower, upper)
    def rec_search(ind, current_sum, current_combo):
        #print("CURRENT INDEX: ", ind, current_sum, current_combo)
        if(current_sum > upper): return
        if(md > 0 and md < len(current_combo)): return
        if(current_sum > lower):
            if(current_combo in res):
                print("DUPLICATE COMBO FOUND!!!!!!")
                return
            print(current_combo)
            res.append(current_combo[:])
            sums.append(current_sum)
            #print(res)
        for d in range(1, 3):
            for i,v in enumerate(val):
                if i<ind : continue
                #print(i, v, "SUM: ", (current_sum + v))
                if((current_sum + v) > upper): break
                current_combo.append(v)
                #print("RECURSION!")
                rec_search(i, current_sum + v, current_combo)
                #print("POP!")
                current_combo.pop()
                #if(current_sum > upper): return
                #time.sleep(0.5)

    rec_search(0, val[0], [val[0]])
    #print("FINAL LIST\n", res)
    return res, sums

def rev_parallel(res, target):
    t = res * target / (res - target)
    return t

def find_parallel_combos(target, tol, val, md):
    res, adms = [], []
    for e in range(6):
        for i,v in enumerate(val):
            r1 = v ** e
            if r1<target : continue

if __name__ == '__main__':
    values = []
    try:
        if __IPYTHON__:
            print("IPYTHON CONSOLE DETECTED")
            args = parser.parse_args(["666", "5.0", "-e12"])
        else:
            args = parser.parse_args()
    except:
        print("ArgeParse error")

    target = args.target
    tol = args.tol
    mdev = args.maxdevices
    if(args.e192):
        values = resistor_values["E192"][1]["val"]
    elif(args.e96):
        values = resistor_values["E96"][1]["val"]
    elif(args.e48):
        values = resistor_values["E48"][1]["val"]
    elif(args.e24):
        values = resistor_values["E24"][1]["val"]
    elif(args.e12):
        values = resistor_values["E12"][1]["val"]
    elif(args.e6):
        values = resistor_values["E6"][1]["val"]
    dec = np.array(sorted(values)) #/ 100
    for d in range(1,3): dec = np.append(dec, dec*(10**d))
    try:
        print(find_series_combos(target, 0.01*tol, values, mdev))
        print(find_series_combos(target, 0.01*tol, values, 3))
    except:
        pass
