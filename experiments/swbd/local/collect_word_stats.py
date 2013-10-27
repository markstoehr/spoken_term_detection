#!/usr/bin/python

import numpy as np
import argparse, sys

def main(args):
    """
    Extract the words from the corpus
    and get the locations in which files 
    """
    words = dict(tuple( (w.strip().split()[-1],[])
                        for w in open(args.w,'r').read().strip().split('\n')))
    
    for line in sys.stdin:
        line =  line.strip().split()
        identifier = line[0]
        start = float(line[1])
        end = float(line[2])
        duration = end-start
        word = line[3]
        if words.has_key(word):
            words[word].append(
                (identifier,start,end,duration))

    fl_durations = open('%s/av_durations.txt' % args.o,'w')
    for word in np.sort(words.keys()):
        fl_durations.write('%s %d %g %g\n' % (word,
                            len(words[word]),
                            np.mean([duration for identifier,start,end,duration in words[word]]),
                            np.median([duration for identifier,start,end,duration in words[word]])))

        fl_word_times = open('%s/%s' % (args.o, word),'w')
        for identifier,start,end,duration in words[word]:
            fl_word_times.write('%s %g %g\n' % (identifier, start,end))
        
        fl_word_times.close()

    fl_durations.close()



    # import pdb; pdb.set_trace()
    # words = []
    # use_cur_line = False
    # keyphrase = "# normal lexical items"
    # for line in open(args.d,'r'):
    #     if line[:len(keyphrase)] == keyphrase:
    #         use_cur_line = True
        
    #     if not use_cur_line: continue

    #     split_line = line.strip().split()
    #     if len(split_line) == 0 or split_line[0][:1] == '#': continue
        
    #     words.append(split_line[0])
    #     words.sort()

    # open(args.o,'w').write('\n'.join( '%d %s' % (i,w) for i,w in enumerate(words)))
            
    
    

if __name__=="__main__":
    parser = argparse.ArgumentParser("""
    Get the vocabulary from the `normal lexical items`
    contained in the switchboard ms98 vocabulary
""")
    parser.add_argument('-w',type=str,default='data/local/words.txt',
                        help='location to find the words.txt containing all the words we are tracking')
    parser.add_argument('-o',type=str,default='data/local/word_stats',
                        help='path to the output directory `av_duration`, `occurrence_times`')
    main(parser.parse_args())
