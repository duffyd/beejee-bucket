#!/usr/bin/env python
import argparse
import os
from pathlib import Path
import re
import subprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Word documents to Markdown files.')
    parser.add_argument(
        'docx_path',
        help='Absolute directory path containing the Word documents'
    )
    parser.add_argument(
        'md_path',
        help='Absolute directory path in which create Markdown files'
    )
    parser.add_argument(
        '-s',
        help='Include subdirectories (Y by default)',
        default='Y',
        choices=('Y', 'N')
    )
    args = parser.parse_args()
    if args.s == 'N':
        glob_str = '/*.docx'
    else:
        glob_str = '**/*.docx'
    idx = 0
    conv_errors = 0
    conv_done = 0
    for match in Path(args.docx_path).glob(glob_str):
        #if idx == 3:
        #    break
        print(f'Processing {match}')
        subdir = str(match.joinpath().parent)[str(match.joinpath().parent).find(args.docx_path)+len(str(args.docx_path)):]
        if subdir != '':
            Path(args.md_path+subdir).mkdir(parents=True, exist_ok=True)
        mdfile = f"{args.md_path}{subdir}/{match.stem}.md"
        result = subprocess.run(
            ["pandoc",
             "-f",
             "docx",
             "-t",
             "gfm",
             "--extract-media=.",
             match,
             "-o",
             mdfile],
            capture_output=True,
            text=True
        )
        if result.stderr == '':
            conv_done += 1
            print(f'Successfully created {mdfile}')
        else:
            conv_errors += 1
            print(f'Error processing {match} as follows {result.stderr}')
        idx += 1
    print(f'Finished processing {idx} Word documents (converted:{conv_done}; errors:{conv_errors})')