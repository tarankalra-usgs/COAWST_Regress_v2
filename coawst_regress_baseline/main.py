import util
import os
import sys 
import shutil 
#import trench
#import ducknc 
import speclight
import sedbed_toy 
import sedfloc_toy 
#import sandy
#import ripcurrent
#import inlettest
#import joetc

def setup_testcase():
    """Create everything needed to run a testcase

    Takes testcase name and creates compiled exe and new bash script
    """
    code_path = util.get_coawst()
    print "----------------------------------------------"
    print " The source code is located in:", code_path

#    trench.regress_trench(code_path) 
#    ducknc.regress_ducknc(code_path) 
    speclight.regress_speclight(code_path) 
    sedbed_toy.regress_sedbed_toy(code_path) 
    sedfloc_toy.regress_sedfloc_toy(code_path) 
#    sandy.regress_sandy(code_path) 
#    ripcurrent.regress_ripcurrent(code_path) 
#    inlettest.regress_inlet(code_path) 
#    joetc.regress_joetc(code_path) 
