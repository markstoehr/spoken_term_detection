#!/usr/bin/python

import numpy as np
import argparse

def main(args):
    """
    Extract the words from the corpus
    we assume that all the words come after
    `normal lexical items`
    """
    words = []
    use_cur_line = False
    keyphrase = "# normal lexical items"
    for line in open(args.d,'r'):
        if line[:len(keyphrase)] == keyphrase:
            use_cur_line = True
        
        if not use_cur_line: continue

        split_line = line.strip().split()
        if len(split_line) == 0 or split_line[0][:1] == '#': continue
        
        words.append(split_line[0])
        words.sort()

    open(args.o,'w').write('\n'.join( '%d %s' % (i,w) for i,w in enumerate(np.sort(np.unique(words)))))
            
    
    

if __name__=="__main__":
    parser = argparse.ArgumentParser("""
    Get the vocabulary from the `normal lexical items`
    contained in the switchboard ms98 vocabulary
""")
    parser.add_argument('-d',type=str,default='swb_ms98_transcripts/sw-ms98-dict.text',help='location of the dictionary provided with the switchboard ms98 transcriptions from ISIP')
    parser.add_argument('-o',type=str,default='data/local/words.txt',
                        help='location to save the words.txt')
    main(parser.parse_args())
