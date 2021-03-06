from weis.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper, runFAST_pywrapper_batch
from weis.aeroelasticse.CaseGen_IEC       import CaseGen_IEC
from wisdem.commonse.mpi_tools              import MPI
import sys

eagle = True

if MPI:
    from wisdem.commonse.mpi_tools import map_comm_heirarchical, subprocessor_loop, subprocessor_stop
    if eagle:
        comm_map_down, comm_map_up, color_map = map_comm_heirarchical(1, 246)
    else:
        comm_map_down, comm_map_up, color_map = map_comm_heirarchical(1, 3)


iec = CaseGen_IEC()
iec.Turbine_Class = 'III' # I, II, III, IV
iec.Turbulence_Class = 'A'
iec.D = 206.
iec.z_hub = 140.
TMax   = 720.
Vrated = 8.3
Ttrans = TMax - 60.
TStart = max([0., TMax - 600.])

# Turbine Data
iec.init_cond = {} # can leave as {} if data not available
iec.init_cond[("ElastoDyn","RotSpeed")] = {'U':[3., 5., 7., 8.3, 25.]}
iec.init_cond[("ElastoDyn","RotSpeed")]['val'] = [2.92, 4.88, 6.81, 7.835, 7.88]
iec.init_cond[("ElastoDyn","BlPitch1")] = {'U':[3., 8.2,  9., 11.,  13.,  15.,  17., 19., 21., 23., 25]}
iec.init_cond[("ElastoDyn","BlPitch1")]['val'] = [0., 0., 2.93, 8.76, 12.01, 14.82, 17.37, 19.73, 21.96, 24.08, 26.10]
iec.init_cond[("ElastoDyn","BlPitch2")] = iec.init_cond[("ElastoDyn","BlPitch1")]
iec.init_cond[("ElastoDyn","BlPitch3")] = iec.init_cond[("ElastoDyn","BlPitch1")]

# DLC inputs
iec.dlc_inputs = {}
iec.dlc_inputs['DLC']   = [1.1, 1.3, 1.4, 1.5, 5.1, 6.1, 6.3]
iec.dlc_inputs['U']     = [[3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25.], [3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25.],[Vrated - 2., Vrated, Vrated + 2.],[3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25.], [Vrated - 2., Vrated, Vrated + 2., 25.], [], []]
iec.dlc_inputs['Seeds'] = [range(1,7), range(1,7),[],[], range(1,7), range(1,7), range(1,7)]
iec.dlc_inputs['Yaw']   = [[], [], [], [], [], [], []]
iec.PC_MaxRat           = 2.
iec.TStart              = Ttrans
iec.TMax                = TMax    # wind file length

iec.transient_dir_change        = 'both'  # '+','-','both': sign for transient events in EDC, EWS
iec.transient_shear_orientation = 'both'  # 'v','h','both': vertical or horizontal shear for EWS

# Naming, file management, etc
iec.wind_dir = 'outputs/wind'
iec.case_name_base = 'BAR4'
if eagle:
    iec.Turbsim_exe = '/projects/weis/multifidelity/WEIS/local/bin/turbsim'
    iec.cores = 246
else:
    iec.Turbsim_exe = '/Users/pbortolo/work/2_openfast/TurbSim/bin/TurbSim_glin64'
    if MPI:
        iec.cores = 4
    else:
        iec.cores = 1

iec.debug_level = 2
if MPI:
    iec.parallel_windfile_gen = True
    iec.mpi_run               = True
    iec.comm_map_down         = comm_map_down
else:
    iec.parallel_windfile_gen = False
    iec.mpi_run               = False
iec.run_dir = 'outputs/OpenFAST_BAR4'

# Run case generator / wind file writing
case_inputs = {}
case_inputs[('Fst','OutFileFmt')]        = {'vals':[2], 'group':0}
case_inputs[("Fst","CompHydro")]         = {'vals':[0], 'group':0}
case_inputs[("Fst","CompSub")]           = {'vals':[0], 'group':0}
case_inputs[("Fst","DT")]                = {'vals':[0.0002], 'group':0}
case_inputs[("Fst","DT_Out")]            = {'vals':[0.2], 'group':0}
case_inputs[("Fst","TMax")]              = {'vals':[TMax], 'group':0}
case_inputs[("Fst","TStart")]            = {'vals':[TStart], 'group':0}
case_inputs[("ElastoDyn","PtfmSgDOF")]   = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmSwDOF")]   = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmHvDOF")]   = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmRDOF")]    = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmPDOF")]    = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmYDOF")]    = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","TwFADOF1")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwFADOF2")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwSSDOF1")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwSSDOF2")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","FlapDOF1")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","FlapDOF2")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","EdgeDOF")]     = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","DrTrDOF")]     = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","GenDOF")]      = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","YawDOF")]      = {'vals':["False"], 'group':0}
case_inputs[("Fst","CompElast")]         = {'vals':[2], 'group':0}
case_inputs[("AeroDyn15","WakeMod")]     = {'vals':[1], 'group':0}
case_inputs[("AeroDyn15","DBEMT_Mod")]   = {'vals':[1], 'group':0}
case_inputs[("AeroDyn15","tau1_const")]  = {'vals':[20], 'group':0}
case_inputs[("AeroDyn15","AFAeroMod")]   = {'vals':[2], 'group':0}
case_inputs[("AeroDyn15","TwrPotent")]   = {'vals':[0], 'group':0}
case_inputs[("AeroDyn15","TwrShadow")]   = {'vals':['True'], 'group':0}
case_inputs[("AeroDyn15","TwrAero")]     = {'vals':['True'], 'group':0}
case_inputs[("AeroDyn15","SkewMod")]     = {'vals':[2], 'group':0}
case_inputs[("AeroDyn15","TipLoss")]     = {'vals':['True'], 'group':0}
case_inputs[("AeroDyn15","HubLoss")]     = {'vals':['True'], 'group':0}
case_inputs[("AeroDyn15","TanInd")]      = {'vals':['True'], 'group':0}
case_inputs[("AeroDyn15","AIDrag")]      = {'vals':['True'], 'group':0}
case_inputs[("AeroDyn15","TIDrag")]      = {'vals':['True'], 'group':0}
case_inputs[("AeroDyn15","UseBlCm")]     = {'vals':['True'], 'group':0}


# Parallel wind file generation with MPI
if MPI:
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
else:
    rank = 0
if rank == 0:
    case_list, case_name_list, dlc_list = iec.execute(case_inputs=case_inputs)


    # Run FAST cases
    fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST',dev_branch = True)
    if eagle:
        fastBatch.FAST_exe = '/home/pbortolo/OpenFAST/build/glue-codes/openfast/openfast'   # Path to executable
        fastBatch.FAST_InputFile = 'BAR4.fst'   # FAST input file (ext=.fst)
        fastBatch.FAST_directory = '/home/pbortolo/BAR_Designs/BAR4/OpenFAST'   # Path to fst directory files
    else:
        fastBatch.FAST_exe = '/Users/pbortolo/work/2_openfast/openfast/build/glue-codes/openfast/openfast'   # Path to executable
        fastBatch.FAST_InputFile = 'OpenFAST_BAR_05.fst'   # FAST input file (ext=.fst)
        fastBatch.FAST_directory = '/Users/pbortolo/work/2_openfast/BAR/OpenFAST_Models/BAR_05'   # Path to fst directory files
    fastBatch.FAST_runDirectory = iec.run_dir
    fastBatch.case_list = case_list
    fastBatch.case_name_list = case_name_list
    fastBatch.debug_level = 2

    if MPI:
        fastBatch.run_mpi(comm_map_down)
    else:
        fastBatch.run_serial()

if MPI:
    sys.stdout.flush()
    if rank in comm_map_up.keys():
        subprocessor_loop(comm_map_up)
    sys.stdout.flush()

# close signal to subprocessors
if rank == 0 and MPI:
    subprocessor_stop(comm_map_down)
sys.stdout.flush()
    
    
    
    
    
