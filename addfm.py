#!/usr/bin/env python
import argparse
import os
from pathlib import Path
import re

WOLBIBLE = "https://www.jw.org/finder?wtlocale=E&pub=nwtsty&srctype=wol&bible={}&srcid=share"
BOOKS = [
    'Genesis',
    'Exodus',
    'Leviticus',
    'Numbers',
    'Deuteronomy',
    'Joshua',
    'Judges',
    'Ruth',
    '1Samuel',
    '2Samuel',
    '1Kings',
    '2Kings',
    '1Chronicles',
    '2Chronicles',
    'Ezra',
    'Nehemiah',
    'Esther',
    'Job',
    'Psalms',
    'Proverbs',
    'Ecclesiastes',
    'SongofSolomon',
    'Isaiah',
    'Jeremiah',
    'Lamentations',
    'Ezekiel',
    'Daniel',
    'Hosea',
    'Joel',
    'Amos',
    'Obadiah',
    'Jonah',
    'Micah',
    'Nahum',
    'Habakkuk',
    'Zephaniah',
    'Haggai',
    'Zechariah',
    'Malachi',
    'Matthew',
    'Mark',
    'Luke',
    'John',
    'Acts',
    'Romans',
    '1Corinthians',
    '2Corinthians',
    'Galatians',
    'Ephesians',
    'Philippians',
    'Colossians',
    '1Thessalonians',
    '2Thessalonians',
    '1Timothy',
    '2Timothy',
    'Titus',
    'Philemon',
    'Hebrews',
    'James',
    '1Peter',
    '2Peter',
    '1John',
    '2John',
    '3John',
    'Jude',
    'Revelation'
]
NOTE_TYPES = [
        'CA-br',
        'CA-co',
        'SKE',
        'Pioneer Meeting',
        'Pioneer Session',
        'PSS',
        'Regional Convention',
        'Circuit work',
        'CO Seminar',
        'HQ Representative Visit',
        'Illustration',
        'KMS',
        'Shepherding CO Visit',
        'Tour',
        'Training'
]

def wolUrlRepl(matchobj):
    return WOLBIBLE.format(f"{BOOKS.index(matchobj.group(1))+1}{matchobj.group(2).zfill(3)}{matchobj.group(3).zfill(3)}")

def h1Toh2Repl(matchobj):
    isFirstH1 = False
    for note_type in NOTE_TYPES:
        if matchobj.group(1).find(note_type) > -1:
            isFirstH1 = True
            break
    if isFirstH1:
        return matchobj.group(0)
    else:
        print(f"Changed h1 to h2 for {matchobj.group(1)}")
        return f"## {matchobj.group(1)}"

def tidyContent(tidiedcontent):
    tidiedcontent = re.sub("(?:equipd|equipdbible)://bible/([1-3]?[a-zA-Z]*)(\d+):(\d+)", wolUrlRepl, tidiedcontent)
    tidiedcontent = re.sub("NBImages", "", tidiedcontent)
    tidiedcontent = re.sub("#(?=[^\s#])", "# ", tidiedcontent)
    tidiedcontent = re.sub('<img src=\"(?=[^/])', '<img src="/', tidiedcontent)
    note_title = re.search("\*\*.*\*\*", tidiedcontent)
    if note_title and note_title.start() == 0:
        tidiedcontent = re.sub('(?:\*\*)(.*)(?:\*\*)', '# \g<1>', tidiedcontent, count=1)
    tidiedcontent = re.sub("(?:[^#])# (.*)", h1Toh2Repl, tidiedcontent)
    return tidiedcontent

def genTag(content):
    tag = None
    for searchterm in NOTE_TYPES:
        if re.search(f".*{searchterm}.*\n", content):
            tag = searchterm
            break
    return tag

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add frontmatter to Markdown files.')
    parser.add_argument(
        'path',
        help='Absolute directory path containing the Markdown files'
    )
    parser.add_argument(
        '-s',
        help='Include subdirectories (Y by default)',
        default='Y',
        choices=('Y', 'N')
    )
    parser.add_argument(
        '-r',
        help='Remove frontmatter from files (N by default)',
        default='N',
        choices=('Y', 'N')
    )
    parser.add_argument(
        '-c',
        help='Clean up content (N by default)',
        default='N',
        choices=('Y', 'N')
    )
    parser.add_argument(
        '-t',
        help='Frontmatter tag to assign to every file. N.B. you can only assign one',
        default=None
    )
    args = parser.parse_args()
    if args.s == 'N':
        glob_str = '/*.md'
    else:
        glob_str = '**/*.md'
    for match in Path(args.path).glob(glob_str):
        print(f'Processing {match}')
        with open(match, 'r') as original:
            if args.c == 'Y':
                data = original.read()
                data = tidyContent(data)
                with open(match, 'w') as modified:
                    print(f"Tidied content for:{match}")
                    modified.write(data)
            elif args.r == 'N':
                data = original.read()
                if data[:3] != '---':
                    note_title = re.search("(?:#\s?)(.*)", data)
                    if note_title and note_title.start() != 0 or not note_title:
                        note_title = re.search("(?:\*\*)(.*)(?:\*\*)", data)
                    with open(match, 'w') as modified:
                        if args.t:
                            tag = args.t
                        else:
                            tag = genTag(data)
                        print(f"Writing frontmatter to {note_title and note_title.group(1) or 'No title'}:{match}")
                        modified.write(f"---\ntitle: {note_title and note_title.group(1) or ''}\ntags:\n{tag and '  - '+tag or ''}\n---\n" + data)
            else:
                lines = original.readlines()
                if lines[0][:3] != '---':
                    print(f"No frontmatter to remove in:{match}")
                    continue
                with open(match, 'w') as modified:
                    modified.write(f'{"".join(lines[5:])}')
                    print(f"Finished removing frontmatter from:{match}")