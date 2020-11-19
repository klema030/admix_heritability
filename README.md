# admix_simulation

This repo is for simulating the trait correlation under ancestry stratification

### Simulate admixed population - African American, Cape Verdean

* V1: __sim_AfrAmr_20200824.py__  
With ASN admixture, 100Mb chromosome 
* V2: __sim_AfrAmr_20200830.py__  
Delete ASN events, 100Mb chromosome  
* V3: __anc_estimate_10Mb.sh sim_AA_v3_10Mb.py__  
Seeds {1..22} as different chromosomes, 22 10Mb chromosomes
* 10demes: __AA_sim_10demes.ipynb__  
Simulate 10 demes with different admixture proportion,works fine with certain random seeds in 10MB, but tends to error if 100MB. 
Found out the error was caused by the number of admixed individuals, deleted this file because git commit error.
* 10demes/11demes: __AA_sim_10demes_1.ipynb anc_estimate.sh plot_admixture.R__  
Simulate 10 demes with different admixture proportion and different population size. Solved error in last script. 


### Get local ancestry of simulated individuals with msprime

* Initial test the code: __Local_anc_msprime.ipynb__    
  Function credit: https://gist.github.com/rwaples/10336129f75239465279dbfe163bf3c1  
  Test with 11 demes model, 100Mb chromosome, test with AFR,EUR,ADM individuals respectively at 20, 5000 generations
* Test the code with simpler model: __Local_anc_msprime_2.ipynb anc_estimate_2.sh local_to_global.py__  
  Test with 1 admixed deme model, 100Mb chromosome, remove growth rate and migration rate before 16 generations, 200 haplotypes for AFR, EUR, ADM.   
  Export their genotype and estimate global ancestry with ADMIXTURE.  
  Calculate their global ancestry (True) from the local ancestry and compare with the predicted.
* Test the code with 10 demes model: __Local_anc_msprime_3.ipynb anc_estimate_3.sh local_to_global_anc_10deme.py local_anc_10deme_plot.py__  
  Test with 10 admixed (decile, 0.05-0.95) deme model, 100Mb chromosome, remove growth rate and migration rate before 16 generations, 200 haplotypes for AFR, EUR,     2000 ADM.  
  Export their genotype and estimate global ancestry with ADMIXTURE.  
  Since it took too long to calculate local anc for all individuals, pick sample (AFR,EUR,AFR), Calculate their global ancestry (True) from the local ancestry for     each and plot their local anc at generation 20 and 2030 (10generations after AFR-EUR split).
