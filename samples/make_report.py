assert __name__ == "__main__"
from dotsearch import report
import argparse
parser = argparse.ArgumentParser(description="Runs graph search "
"algorithms over a .dot graph file.")
parser.add_argument("dotfile", action="store")
cfg = parser.parse_args()


from ai.methods import (breadth_first_search,
                        astar_search,
                        beam_search_best_first,
                        beam_search_breadth_first,
                        simulated_annealing,
                       )


print "Running algorithms and writting report.html..."
report(infile=cfg.dotfile,
       algorithms=[
            breadth_first_search,
            astar_search,
            beam_search_best_first,
            beam_search_breadth_first,
            simulated_annealing,
           ],
       outfile="report.html",
       with_images=True)
