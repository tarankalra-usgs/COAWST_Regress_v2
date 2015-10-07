import os            # issues system commands
import sys           # system commands 
import errno         # raise errors if files exist 
import time          # internal module to get time
import shutil        # file copying 
import fileinput     # replacing string in files
import os.path       # to copy files after checking if they exist on this path

def get_coawst():
    """ get the coawst source code """
    timestr = time.strftime("%Y%m%d")  
    srcdirname = "COAWST_src_"+timestr  
    code_path=os.path.abspath(srcdirname)
    try:
        os.makedirs(srcdirname)
        os.chdir(srcdirname)  
        os.system('svn checkout https://coawstmodel.sourcerepo.com/coawstmodel/COAWST .' %locals())

        src_wrf_make = os.path.abspath('../coawst_regress_baseline/WRF_config_file/makefile')
        src_wrf_conf = os.path.abspath('../coawst_regress_baseline/WRF_config_file/configure.wrf')
        dest2 = os.path.join(code_path, 'WRF')
        shutil.copy(src_wrf_make,code_path)
        shutil.copy(src_wrf_conf,dest2)

        return code_path

    except Exception, OSError:
        code_path=os.path.abspath(srcdirname)
        return code_path
        if exception.errno !=errno.EEXIST:
            print "COAWST source directory for this day already exists"
            raise  

def get_testcaselist(code_path):
    """ get a list of test cases from code path """ 
    """ Always include Inlet_test and JOE_TC in the ignored list """
    ignored = ['.svn']
    path=os.path.join(code_path,'Projects')
    testcase= [x for x in os.listdir(path) if x not in ignored]
 
    return testcase 

def edit_bashfile(bashfile,each_case,code_path,project_path): 
    """ edit the bashfile for each case """ 
    upper_testcase=each_case.upper()
    for line in fileinput.input([bashfile],inplace=True): 
        oldinput = "COAWST_APPLICATION=INLET_TEST"
        newinput = "COAWST_APPLICATION=" + upper_testcase
        line = line.replace(oldinput,newinput)
  
        oldinput = "MY_PROJECT_DIR=${MY_ROOT_DIR}"
        newinput = "MY_PROJECT_DIR="+project_path
        line = line.replace(oldinput,newinput)

        oldinput = "MY_ROOT_DIR=/cygdrive/e/data/models/COAWST"
        newinput = "MY_ROOT_DIR=" + code_path 
        line = line.replace(oldinput,newinput)

        oldinput=  "MY_HEADER_DIR=${MY_PROJECT_DIR}/Projects/Inlet_test/Coupled"
        newinput=  "MY_HEADER_DIR=" + project_path
        line = line.replace(oldinput,newinput)

        oldinput= "MY_ANALYTICAL_DIR=${MY_PROJECT_DIR}/Projects/Inlet_test/Coupled"
        newinput= "MY_ANALYTICAL_DIR=" + project_path 
        line = line.replace(oldinput,newinput)

        oldinput= "USE_MPIF90=  "
        newinput= "USE_MPIF90=on"
        line = line.replace(oldinput,newinput)

        oldinput= "export         which_MPI=openmpi"
        newinput= "#export         which_MPI=openmpi"
        line = line.replace(oldinput,newinput)

        oldinput="export              FORT=ifort"
        newinput= "#export              FORT=     "
        line = line.replace(oldinput,newinput)

        oldinput="#export              FORT=pgi"
        newinput=" export              FORT=pgi"
        line = line.replace(oldinput,newinput)

        sys.stdout.write(line)

def edit_jobscript(runfile,inputfile,each_case,project_str,code_path,tot_nproc):
    """edit the job script for each case  """ 
    for line in fileinput.input([runfile],inplace=True): 
        oldinput = "-N cwstv3"
        newinput = "-N " + each_case
        line = line.replace(oldinput,newinput)

        oldinput = "-e isabel_105.err"
        newinput = "-e " + each_case + ".err"
        line = line.replace(oldinput,newinput)

        oldinput = "-o isabel_105.out"
        newinput = "-o " + each_case + ".out"
        line = line.replace(oldinput,newinput)

        oldinput = "PBS -M jcwarner@usgs.gov"
        newinput = "##PBS -M jcwarner@usgs.gov"
        line = line.replace(oldinput,newinput)

        oldinput = "cd /raid3/jcwarner/Projects/coawst_v3.1/coawst_v3.1_114/"
        newinput = "cd " + code_path 
        line = line.replace(oldinput,newinput)

        oldinput = "-np 8"
        newinput = "-np %s"  % (tot_nproc)
        line = line.replace(oldinput,newinput)

        oldinput = "Projects/Sandy/coupling_sandy1.in"
        newinput =  project_str + '/'+ inputfile
        line = line.replace(oldinput,newinput)

        oldinput = "cwstv3.out"
        newinput =  'log.out_' + each_case
        line = line.replace(oldinput,newinput)

        sys.stdout.write(line)

def edit_oceaninfile(inputfile,ntilex,ntiley): 
    """ edit the input file for each case """ 
    for line in fileinput.input([inputfile],inplace=True): 
            oldinput = "NtileI == 1"
            newinput = "NtileI == %s" % (ntilex)
            line = line.replace(oldinput,newinput)
  
            oldinput = "NtileJ == 1"
            newinput = "NtileJ == %s" % (ntiley)
            line = line.replace(oldinput,newinput)

            sys.stdout.write(line)

def edit_couplefile(couplefile,natm,nwav,nocn,couple_flag): 
    """ edit the input file for each case """ 
    for line in fileinput.input([couplefile],inplace=True):
        if couple_flag=='2way':
            oldinput = "NnodesATM =  0"
            newinput = "NnodesATM =  %s" %(natm) 
            line = line.replace(oldinput,newinput)
  
            oldinput = "NnodesWAV =  1"
            newinput = "NnodesWAV =  %s" %(nwav)
            line = line.replace(oldinput,newinput)

            oldinput = "NnodesOCN =  1"
            newinput = "NnodesOCN =  %s" %(nocn)
            line = line.replace(oldinput,newinput)

            sys.stdout.write(line)
        
        elif couple_flag=='3way':
            oldinput = "NnodesATM =  1"
            newinput = "NnodesATM =  %s" %(natm)
            line = line.replace(oldinput,newinput)
  
            oldinput = "NnodesWAV =  1"
            newinput = "NnodesWAV =  %s" %(nwav)
            line = line.replace(oldinput,newinput)

            oldinput = "NnodesOCN =  1"
            newinput = "NnodesOCN =  %s" %(nocn)
            line = line.replace(oldinput,newinput)

            sys.stdout.write(line)

def edit_ref_oceaninfile(inputfile,ntilex,ntiley,couple_flag):
    """ edit the input file for each case """
    for line in fileinput.input([inputfile],inplace=True):

        if couple_flag=='2way':
            oldinput= "NtileI == 1 1"
            newinput= "NtileI == %s %s"  %(ntilex)
            line = line.replace(oldinput,newinput)

            oldinput= "NtileJ == 1 1"
            newinput= "NtileJ == %s %s"  %(ntiley)
            line = line.replace(oldinput,newinput)

            sys.stdout.write(line)

def edit_wrfinfile(wrfinput,nprocx_atm,nprocy_atm):
    """ edit the input file for each case """
    for line in fileinput.input([wrfinput],inplace=True):
            oldinput= "nproc_x                             = 1"
            newinput= "nproc_x                             = %s" %(nprocx_atm)
            line = line.replace(oldinput,newinput)
         
            oldinput= "nproc_y                             = 1"
            newinput= "nproc_y                             = %s" %(nprocy_atm)
            line = line.replace(oldinput,newinput)

            sys.stdout.write(line)

def move_casefiles(project_path,case_name,bashfile,runfile,buildfile,execute,stdout,logfile):
#   Moving output files to each projects folder
    outfile1=case_name+'.e'+stdout[:5]
    outfile2=case_name+'.o'+stdout[:5]
   
#   Move the build folder first
    src_dir='Build'
    dst_dir=os.path.join(project_path,'Build')
    try: 
        shutil.copytree(src_dir,dst_dir)
    except:
        print"-------------------------------------"
        print"Build folder for this case already exists"
        print"-------------------------------------"
     
#   Now move output files
    outputfilelist= [outfile1,outfile2,bashfile,runfile,buildfile,execute,logfile]

    for filename in outputfilelist:
        if (os.path.isfile(filename)):
            shutil.move(filename,project_path)

#   Now move all the files with these extensions or prefixes
    for filename in os.listdir('.'):
         if filename.endswith('.nc'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.endswith('.mat'):
             shutil.move(filename,project_path)
    
    for filename in os.listdir('.'):
         if filename.startswith('swaninit'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('wrfout'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('PRINT'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('Sandy_'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('depth'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('force'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('qb'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('hsig'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('dissip'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('tmbot'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('rtp'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('vel'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('ubot'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('wdir'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('wlen'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('botlev'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('fric'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('vel'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('point1'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('watlev'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('swan_inlet_rst'):
             shutil.move(filename,project_path)

    for filename in os.listdir('.'):
         if filename.startswith('swan_intest_ref1_rst'):
             shutil.move(filename,project_path)

    outputfilelist2=['namelist.output','nodes.list']
    for filename in outputfilelist2:
        if (os.path.isfile(filename)):
            shutil.move(filename,project_path)
