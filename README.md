# Protein-glycan docking with HADDOCK3

This repository contains all data and analysis necessary to reproduce the results reported in [this paper]().

The repository contains the following directories

- **analysis**, with all the analysis scripts to generate the figures present in the paper

- **data**, with all the data generated in this study

- **pdb_files**. This directory contains subdirectories for each PDB (relative to the protein-glycan complex). In each pdb_files/PDB/ subdirectory the following files are available:

  - **154L_r_b.pdb**: protein bound structure
  - **154L_l_b.pdb**: glycan bound structure
  - **154L_r_u.pdb**: protein unbound structure
  - **154L_l_u.pdb**: glycan unbound structure
  - **154L_l_ensemble.pdb**: glycan ensemble, obtained with [mdref](https://www.bonvinlab.org/haddock3/modules/refinement/haddock.modules.refinement.mdref.html)
  - **154L_analysis.pdb**: reference structure
  - **154L_ti-aa.tbl**: AIRs file, ti-aa restraints (true interface on both protein and glycan)
  - **154L_tip-ap.tbl**: AIRs file, tip-ap restraints (true-interface-protein, glycan fully passive)

- **cfg_files**. It contains subdirectories for each PDB (relative to the protein-glycan complex). In each cfg_files/PDB/ subdirectory the following files are available:
 
  - **bound_default_ti-aa.toml**: bound docking, default haddock scoring function, ti-aa AIRs
  - **bound_vdw_ti-aa.toml**: bound docking, vdW haddock scoring function, ti-aa AIRs
  - **bound_vdw_tip-ap.toml**: bound docking, vdW haddock scoring function, tip-ap AIRs

  - **unbound_vdw_tip-ap_clust.toml**: unbound docking, vdW haddock scoring function, tip-ap AIRs
  - **unbound_ens_vdw_tip-ap_clust.toml**: ensemble docking, vdW haddock scoring function, tip-ap AIRs
  - **mdref-glycans-sf400x16.toml**: sampling of glycan conformations using mdref
