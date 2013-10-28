#!/usr/bin/python

from __future__ import division
import argparse, sys
from template_speech_rec import configParserWrapper
import numpy as np

def main(args):
    """
    """
    config_d = configParserWrapper.load_settings(open(args.config,'r'))


    # get the lengths so that I know the number of frames
    # are going to be used
    num_frames = int((config_d['SPECTROGRAM']['sample_rate'] *np.max(np.loadtxt(args.lengths)) - config_d['SPECTROGRAM']['num_window_samples'])/config_d['SPECTROGRAM']['num_window_step_samples']+1)
    
    

    if args.occurrences is None:
        occurrences = sys.stdin
    else:
        occurrences = open(args.occurrences,'r')

    prev_fl = ''
    start_end_pairs = []
    for line in occurrences:
        split_line = line.strip().split()
        fl = split_line[0]
        if fl != prev_fl:
            out_str = prev_fl
            for i, start_end in enumerate(start_end_pairs):
                out_str += " "
                if i > 0:
                    out_str += "| "

                time_start,time_end = start_end
                out_str += "%d %d : %d %d" % (time_start-(config_d['TRAINING']['shift_window']-1)/2,
                                              time_start + num_frames+(config_d['TRAINING']['shift_window']-1)/2,
                                              time_start,
                                              time_end)
            
            print out_str

            start_end_pairs = []
        
        start_end_pairs.append(
            (int(float(split_line[1])*config_d['SPECTROGRAM']['sample_rate']/config_d['SPECTROGRAM']['num_window_step_samples']+1),
             int(float(split_line[2])*config_d['SPECTROGRAM']['sample_rate']/config_d['SPECTROGRAM']['num_window_step_samples']+1)))
        prev_fl = fl
                               
            
    out_str = prev_fl
    for i, start_end in enumerate(start_end_pairs):
        out_str += " "
        if i > 0:
            out_str += "| "

        time_start,time_end = start_end
        out_str += "%d %d : %d %d" % (time_start-(config_d['TRAINING']['shift_window']-1)/2,
                                      time_start + num_frames+(config_d['TRAINING']['shift_window']-1)/2,
                                      time_start,
                                      time_end)
            
    print out_str

        

if __name__=="__main__":
    parser = argparse.ArgumentParser("""
    extract the occurrences that follow the set of
    utterance identities so that its of the form
    utterance_id time time ( | time time )*
    so that we open up one file can get all the instances
    out of it and use it for later processing
    """)
    parser.add_argument('--uttids',
                        type=str,
                        default=None,
                        help='should contain all of the utterance identifiers that will be used, if None then all of the occurrences are used')
    parser.add_argument('--occurrences',
                        type=str,
                        default=None,
                        help='file containing three column output where the first part indicates the file the example comes from (these should be sorted), second column  is the start time in seconds, and the last column is the end time in seconds, if None this is assumed to be read in from standard input')
    parser.add_argument('--lengths',
                        type=str,
                        help='length data for the examples that we will work with, used for computing how big the context window should be')
    parser.add_argument('--config',
                        type=str,
                        help='configuration file, relevant for getting the sampling rate correct, and for computing statstics about how many frames will appear in each word, as well as the size of the context window to use when we do a shift-tolerant EM algorithm')
    main(parser.parse_args())
