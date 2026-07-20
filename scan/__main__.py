import argparse
from pathlib import Path
from batch import proc_batch
from single import proc_file
from helper import validate_fs, validate_sm


def main():    
    parser = argparse.ArgumentParser(description="Reorder, crop, and optionally split scanned test papers.")

    parser.add_argument("-f", "--file", type=str, nargs=1, default=None,
                        metavar="FILENAME",
                        help="Filepath of the singular PDF to process. Leave out for batch processing.")
    
    parser.add_argument("-c","--crop",type=int,nargs=4,default=None,
                        metavar=("LEFT","RIGHT","TOP","BOTTOM"),
                        help="Space separated margin values (px) in order.")
    
    parser.add_argument("-sm","--split-mode",type=validate_sm,default=None,dest="sm",
                        metavar="SPLIT MODE",
                        help="Mode to split document by: 'IDX' or 'COUNT'")
    
    parser.add_argument("-s", "--split", type=int, nargs="+", default=None,
                        metavar="SPLIT VALs",
                        help="Space separated values to split by: 1. Page NOs(inclusive) 2. No. of Pages")
    
    parser.add_argument("-g","--group",type=int,nargs="+",default=None,dest="groups",
                        metavar="GROUP COUNTS",
                        help="Space serparated number of documents to group by.")

    parser.add_argument("-fs","--format-string",type=validate_fs,dest="fs",
                        metavar="FORMAT STRING",
                        help="Format string including '{stem}' and '{id}' for file naming convention")
    
    args = parser.parse_args()

    if args.file:
        proc_file(
            in_file=args.file,
            mode=args.sm,
            split_lst = args.split,
            grp_counts= args.groups,
            format_string=args.fs
        )            
    else:
        proc_batch(args.crop,args.fs)

main()