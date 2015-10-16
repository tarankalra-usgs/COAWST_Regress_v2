import util
import os
import sys 
import shutil 
import subprocess 
import time

def regress_sandy(code_path):
    case_name       ='Sandy'
    base_bashfile   ='coawst.bash' 
    base_runfile    ='run_nemo'
    oceaninfile     ='ocean_%s.in' % (case_name.lower())
    couplefile      = 'coupling_%s.in'  % (case_name.lower())
    project_str     ='Projects'+'/'+case_name
    project_path    =os.path.join(code_path,project_str)
    couple_flag     ='3way'
    ntilex          = 2
    ntiley          = 2
    nocn            = ntilex*ntiley  
    nwav            = 2 
    nprocx_atm      = 2
    nprocy_atm      = 1
    natm            = nprocx_atm*nprocy_atm
    tot_nproc       = nocn+nwav+natm 
    nodes           = 1                    # for NEMO ppn=8
    execute         = 'coawstM'
    logfile         = 'log.out_' + case_name 
    buildfile       = 'Build.txt'

    os.chdir(project_path)
    util.edit_wrfinfile('namelist.input',nprocx_atm,nprocy_atm)
    wrffiles=['namelist.input','wrfbdy_d01','wrfinput_d01','wrfinput_d02', \
              'wrflowinp_d01','wrflowinp_d02'] 
    for filename in wrffiles:
        shutil.copy(filename,code_path)
      
    os.chdir(code_path)

    """ Make local copies for each case """
    bashfile  = base_bashfile + "_" + case_name 
    shutil.copy2(base_bashfile,bashfile)
      
    runfile   = base_runfile + "_" + case_name
    shutil.copy2(base_runfile,runfile)
 
    util.edit_bashfile(bashfile,case_name,code_path,project_path)
 
    print "------------------------------------------"
    print "Compiling:", case_name,"case"
    os.system('./%(bashfile)s >>Build.txt' %locals() )

    util.edit_jobscript(runfile,couplefile,case_name,project_str,code_path,\
                        tot_nproc,nodes)

    os.chdir(project_path)
    util.edit_oceaninfile(oceaninfile,ntilex,ntiley)
    util.edit_couplefile(couplefile,natm,nwav,nocn,couple_flag)

    os.chdir(code_path)
    print "------------------------------------------"
    print "Executing case:", case_name
    p=subprocess.Popen("qsub %(runfile)s" %locals(),shell=True,stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE) 
    stdout,stderr=p.communicate()

#check every ten mins
    stdout_case=stdout
    util.check_queue(stdout_case)

#   Moving output files to each projects folder
    util.move_casefiles(project_path,case_name,bashfile,runfile,buildfile,\
                        execute,stdout,logfile)

#   Remove WRF files from the code path 
    for filename in wrffiles:
        os.remove(filename)
