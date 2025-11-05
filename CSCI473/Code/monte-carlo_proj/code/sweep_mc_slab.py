#Tester file to sweep across multiple values and run simulations
"""
Usage: python ./sweep_mc_slab.py [-h] [--exe EXE] --C C --Cc CC --H-min H-MIN --H-max H-MAX --H-step H-STEP
                                --N N [--seed SEED] [--timeout TIMEOUT] [--trace] [--trace-every TRACE-EVERY]
                                [--make-convergence-plots] [--dpi DPI] [--title TITLE]

        Sweep H for mc_slab and plot results
        -h --help               Show this help message and exit
        --exe EXE               Path to mc_slab (default: ./mc_slab)
        --C C
        --Cc CC
        --H-min H-MIN 
        --H-max H-MAX 
        --H-step H-STEP
        --N N 
        --seed SEED
        --timeout TIMEOUT
        --trace                 Enable per iteration tracing to CSV
        --trace-every TRACE-
                                Record every mth iteration
        --make-convergence-plots
                                When tracing also render convergence plots per H
        --dpi DPI
        --title TITLE

"""