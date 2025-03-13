import os
from nipype.interfaces import spm

def realign_data(data_descrip: dict , method : str):
  
    print(f"{method.upper()}: Realign {method.upper()} data...")
    
    if method.lower() == "mricloud":
      register_to_mean = False
      interp = 4
    
    elif method.lower() == "asltbx":
      register_to_mean = True
      interp = 1
      
    else:
      raise ValueError("Invalid method")
        

    for key, value in data_descrip["Images"].items():
        key = key.replace("rawdata", "derivatives")
        for asl_file in value["asl"]:
            P = os.path.join(key, "perf", f"{asl_file}.nii")

            realign = spm.Realign()
            realign.inputs.in_files = P
            realign.inputs.quality = 0.9  # SPM default
            realign.inputs.fwhm = 5
            realign.inputs.register_to_mean = register_to_mean  # realign to the first timepoint
            realign.inputs.jobtype = "estwrite"
            realign.inputs.interp = interp  # SPM default
            realign.inputs.wrap = [0, 0, 0]  # SPM default
            realign.inputs.write_mask = True
            realign.inputs.write_which = [
                2,
                1,
            ]  # which_writerealign = 2, mean_writerealign = 1
            realign.run()
            
