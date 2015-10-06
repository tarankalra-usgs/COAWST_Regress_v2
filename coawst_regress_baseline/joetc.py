import util
import os
import sys 
import shutil
import subprocess
import time  

""" Out of the FOR loop and special treatment for Inlet_test and JOE_TC """
def regress_joetc(code_path):
    case_name='JOE_TC'
    base_bashfile   ='coawst.bash' 
    base_runfile    ='run_nemo'
    couple_flag     ='3way'
    ntilex          = 4
    ntiley          = 2
    nocn            = ntilex*ntiley
    nwav            = 4
    nprocx_atm      = 2
    nprocy_atm      = 2
    natm            = nprocx_atm*nprocy_atm
    tot_nproc       = nocn+nwav+natm  
    executable      = 'coawstM'
    buildfile       = 'Build.txt'

    ignored     = ["namelist.input","wrfbdy_d01","wrfinput_d01",".svn"]
    path_inputs = os.path.join(code_path,'Projects/JOE_TC')
    joetc_tests = [x for x in os.listdir(path_inputs) if x not in ignored]
    print "----------------------------------------------"
    print " The JOE_TC testcases included:", joetc_tests

    os.chdir(path_inputs)
    util.edit_wrfinfile('namelist.input',nprocx_atm,nprocy_atm)
    wrffiles=['namelist.input','wrfbdy_d01','wrfinput_d01']
    for filename in wrffiles:
        shutil.copy(filename,code_path)

    os.chdir(code_path)
    for each_joetc_case in joetc_tests: 
        project_str='Projects/JOE_TC'+'/'+each_joetc_case
        project_subpath=os.path.join(code_path,project_str)

        bashfile  = base_bashfile + '_joetc_' + each_joetc_case
        shutil.copy2(base_bashfile,bashfile)

        runfile   = base_runfile + '_joetc_' + each_joetc_case
        shutil.copy2(base_runfile,runfile)

        """ Edit 'coawst.bash' for each case """
        util.edit_bashfile(bashfile,case_name,code_path,project_subpath)     
         
        """ Compile the COAWST code """
        print "------------------------------------------"
        print "Compiling JOE TC test :", each_joetc_case
        os.system('./%(bashfile)s >>Build.txt' %locals() )

        case_subname="JOE_TC_" + each_joetc_case
        logfile     ='log.out_'+ each_joetc_case 

        if each_joetc_case == 'Coupled': 
            inputfile       ='coupling_joe_tc.in' 
            couplefile      = inputfile
            oceaninfile     = 'ocean_joe_tc.in' 
            util.edit_jobscript(runfile,inputfile,case_subname,project_str,code_path,tot_nproc)    

            os.chdir(project_subpath)
            util.edit_couplefile(couplefile,natm,nwav,nocn,couple_flag)
            util.edit_oceaninfile(oceaninfile,ntilex,ntiley)

            os.chdir(code_path)

            print "------------------------------------------"
            print "Executing JOE TC test :", each_joetc_case 
            p=subprocess.Popen("qsub %(runfile)s" %locals(),shell=True,stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            stdout,stderr=p.communicate()
            time.sleep(32400) # sleep for 18 hours 

            #   Moving output files to each projects folder
            util.move_casefiles(project_subpath,case_subname,bashfile,runfile,buildfile,executable,stdout,logfile)

        elif each_joetc_case == 'DiffGrid': 
            inputfile       ='coupling_joe_tc.in' 
            couplefile      = inputfile
            oceaninfile     = 'ocean_joe_tc_coarse.in' 
            util.edit_jobscript(runfile,inputfile,case_subname,project_str,code_path,tot_nproc)    

            os.chdir(project_subpath)
            util.edit_couplefile(couplefile,natm,nwav,nocn,couple_flag)
            util.edit_oceaninfile(oceaninfile,ntilex,ntiley)

            os.chdir(code_path)

            print "------------------------------------------"
            print "Executing JOE TC test :", each_joetc_case 
            p=subprocess.Popen("qsub %(runfile)s" %locals(),shell=True,stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            stdout,stderr=p.communicate()
            time.sleep(32400) # sleep for 9 hours 

            #   Moving output files to each projects folder
            util.move_casefiles(project_subpath,case_subname,bashfile,runfile,buildfile,executable,stdout,logfile)

    #   Remove WRF files from the code path
    for filename in wrffiles:
        os.remove(filename)
