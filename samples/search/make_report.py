assert __name__ == "__main__"

import argparse

from dotsearch import report

from simpleai.search import breadth_first, astar, beam, simulated_annealing

parser = argparse.ArgumentParser(description="Runs graph search "
                                 "algorithms over a .dot graph file.")
parser.add_argument("dotfile", action="store")
cfg = parser.parse_args()


print "Running algorithms and writting report.html..."
report(infile=cfg.dotfile,
       algorithms=[
           breadth_first,
           astar,
           beam,
           simulated_annealing,
           ],
       outfile="report.html",
       with_images=True)
