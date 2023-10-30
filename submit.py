import sys
from backend.genome import Genome

if len(sys.argv) == 1:
    print("You need to specify filenames of files, you want to submit.")
else:
    for file in sys.argv[1:]:
        try:
            with open(file,"r") as f:
                dna : str = ''.join(f.readlines())
                genome : Genome = Genome(dna)
                try:
                    genome.save()
                    print(f"{file} saved succesfully. You can access it with key: {genome.hash()}")
                except:
                    print(f"{file} could not be saved",file=sys.stderr)
        except Exception as e:
            print(e)