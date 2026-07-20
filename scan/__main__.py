import argparse
from pathlib import Path
from batch import proc_batch
from single import proc_file
from helper import validate_fs


def main():    
    parser = argparse.ArgumentParser(description="Reorder, crop, and optionally split scanned test papers.")

    parser.add_argument("-f", "--file", type=str, nargs=1, default=None,
                        metavar="FILENAME",
                        help="Filepath of the singular PDF to process. Leave out for batch processing.")
    
    parser.add_argument("-s", "--split", type=int, nargs="+", default=None,
                        metavar="PAGE NOs",
                        help="Space separated page numbers(exclusive) to split on.")
    
    parser.add_argument("-c","--crop",type=int,nargs=4,default=None,
                        metavar=("LEFT","RIGHT","TOP","BOTTOM"),
                        help="Space separated margin values (px) in order.")
    
    parser.add_argument("-fs","--format-string",type=validate_fs,nargs=1,dest="fs")
    
    args = parser.parse_args()

    if args.file:
        proc_file(args.file,args.split,args.crop,args.fs)            
    else:
        proc_batch(args.crop,args.fs)

main()