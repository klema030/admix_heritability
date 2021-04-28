#simulate 400hap 100MB genotype and get local ancestry for each person
import msprime, sys
from math import log
from math import exp

# simulated genotype model
#seed = int(sys.argv[1]) # input the seed
seed=1
mu=1.25e-8 # mutation rate per bp
rho=1e-8 # recombination rate per bp
nbp=1e8 # generate 100Mb
#nbp=1e7 # generate 10Mb
N0=7310 # initial population size
Thum=5920 # time (gens) of advent of modern humans
Naf=14474 # size of african population
Tooa=2040 # number of generations back to Out of Africa
Nb=1861 # size of out of africa population
mafb=1.5e-4 # migration rate Africa and Out-of-Afica
Teu=920 # number generations back to Asia-Euroupe split
Neu=1032; Nas=554 # bottleneck population sizes
mafeu=2.5e-5;mafas=7.8e-6;meuas=3.11e-5 #mig.rates
reu=0.0038 #growth rate per generation in Europe
ras=0.0048 #growth rate per generation in Asia
Tadmix=16 # time of admixture
Nadmix=30000 # initial size of admixed population
radmix=.05 # growth rate of admixed population
Tcencus=17

# pop0 is Africa, pop1 is Europe,  pop2 is admixed
refsamplesize=100
#admsamplesize=1000 #sample size of admixted pop
admsamplesize=400
pop_config = [
    msprime.PopulationConfiguration(sample_size=refsamplesize, initial_size=Naf), #growth_rate=0.0),
    msprime.PopulationConfiguration(sample_size=refsamplesize, initial_size=Neu*exp(reu*Teu)), #growth_rate=reu),
    msprime.PopulationConfiguration(sample_size=admsamplesize, initial_size=Nadmix*exp(radmix*Tadmix), )]#growth_rate=radmix)]
mig_mat=[
    [0,mafeu,0],
    [mafeu,0,0],
    [0,0,0]]

# Admixture event, 0.76517 Africa, rest Europe
# change the AFR prop according to the 10deme model avg anc
admixture_event = [
    msprime.MigrationRateChange(time=Tadmix, rate=0.0), #newly added, change the migration rate to 0
    msprime.MassMigration(time=Tadmix, source=2, destination=0, proportion=0.76517), # African came to America        
    msprime.MassMigration(time=Tadmix+0.0001, source=2, destination=1, proportion=1.0)] # European came to America

# cencus events
census_event = [
    msprime.CensusEvent(time=Tcencus)
]

# Out of Africa event
ooa_event = [
    msprime.MigrationRateChange(time=Tooa, rate=0.0),
    msprime.MassMigration(time=Tooa+0.0001, source=1, destination=0, proportion=1.0)
]

# initial population size
init_event=[msprime.PopulationParametersChange(time=Thum, initial_size=N0, population_id=0)]

#events = admixture_event + eu_event + ooa_event + init_event
events = admixture_event + census_event + ooa_event + init_event

ts = msprime.simulate(
    population_configurations=pop_config,
    migration_matrix=mig_mat,
    demographic_events=events,
    length=nbp,
    recombination_rate=rho, 
    mutation_rate=mu,
    #record_migrations=True, # newly added, Needed for tracking segments.
    random_seed=seed)

#export to diploid to validate simulated global anc
filename=f'AA_100Mb_random_{admsamplesize}hap_chr{seed}.vcf'
n_dip_indv = int(ts.num_samples / 2)
indv_names = [f"AA_{str(i)}indv" for i in range(n_dip_indv)]
with open(filename, "w") as vcf_file:
    ts.write_vcf(vcf_file, ploidy=2, contig_id=str(seed), individual_names=indv_names)

import tskit
import numpy as np
import msprime 

# replace the parent to population label
def get_population_id(node, ts):
    return ts.tables.nodes.population[node]

def local_ancestry(Tcencus, ts):
    # select nodes that are Tcencus generations ago
    ancestors_Tcencus_gens = np.where(ts.tables.nodes.time == Tcencus)[0]
    # which of your samples descend from which ancestors
    ancestrytable_Tcencus_gens = ts.tables.link_ancestors(
    samples=ts.samples(), ancestors=ancestors_Tcencus_gens)
    # replace the parent to population label
    #nodeTable = ts.tables.nodes
    import pandas as pd
    ancestry_table = pd.DataFrame(
        data = {
            'left': ancestrytable_Tcencus_gens.left,
            'right': ancestrytable_Tcencus_gens.right,
            'populations': [get_population_id(u, ts) for u in ancestrytable_Tcencus_gens.parent],
            'child': ancestrytable_Tcencus_gens.child
        }
    )
    #return ancestry_table
    # output the ancestry table to a file
    ancestry_table.to_csv(f'loc_anc_{filename}.txt', sep='\t', encoding='utf-8', index=False)

# run the function
local_ancestry(Tcencus, ts)

