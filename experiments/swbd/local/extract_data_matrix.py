#!/usr/bin/python

import numpy as np
import argparse, itertools
from template_speech_rec import configParserWrapper
from scipy.io import wavfile
import template_speech_rec.get_train_data as gtrd
    


def main(args):
    """
    Get the start and end frame associated to each example
    and then extract the example and save into a matrix

    we make the assumption that all the examples have the exact
    same length as the first
    """
    config_d = configParserWrapper.load_settings(open(args.c,'r'))

    uttid_dict = dict(tuple( (uttid,k) for k,uttid in enumerate(open(args.uttids,'r').read().strip().split('\n'))))

    examples = []
    examples_S = []
    output_info = []

    for line_id, line in enumerate(open(args.transcript,'r')):
        split_line = line.strip().split()
        fpath = split_line[0]
        uttid = '_'.join(fpath.strip('.wav').split('/')[-3:])
        split_line = split_line[1:]
        frame_starts = np.array(tuple(int(k) for k in split_line[::3]), dtype=int)
        frame_ends = np.array( tuple( int(k) for k in split_line[1::3]),dtype=int)
        example_length = int((frame_ends - frame_starts).max())

        sr, x = wavfile.read(fpath)
        S,sample_mapping, sample_to_frames = gtrd.get_spectrogram_use_config(x,config_d['SPECTROGRAM'],return_sample_mapping=True)
        X = gtrd.get_edge_features_use_config(S.T,config_d['EDGES'])
        S = np.vstack( (S[:example_length][::-1],
                        S,
                        S[::-1][:example_length]))
        X = np.vstack( (X[:example_length][::-1],
                        X,
                        X[::-1][:example_length]))

        frame_starts += example_length
        frame_ends += example_length
        for i, s_e in enumerate(itertools.izip(frame_starts,frame_ends)):
            s,e = s_e
            examples.append(X[s:e])
            examples_S.append(S[s:e])
            output_info.append( (uttid_dict[uttid],i,s-example_length,
                                 e-example_length))

        if line_id % 100 == 0:
            print line_id, uttid, line




    examples = np.array(examples,dtype=np.uint8)
    examples_S = np.array(examples_S)
    np.save(args.output, examples)
    if args.output_info is not None:
        np.save(args.output_info,np.array(output_info,dtype=int))
    if args.output_spec is not None:
        np.save(args.output_spec,examples_S)
    

if __name__=="__main__":
    parser = argparse.ArgumentParser("""
    Compute the frame length for the examples (based on the number
    of samples for an example length)
    and then extract the best centered example for each of the 
    data.
    """)
    parser.add_argument('-c',
                        type=str,
                        default='conf/main.config',
                        help='configuration file should contain a section about spectrogram computation')
    parser.add_argument('--uttids',
                        type=str,
                        default='train.uttids',
                        help='utterance ids so that we can map back to integers')
    parser.add_argument('--transcript',
                        type=str,
                        default='aa_train.frame_trans',
                        help='transcript for start and end frames')
    parser.add_argument('--output',
                        type=str,
                        default='aa_train_examples.npy',
                        help='matrix of examples of the phone or phone sequence')
                                 
    parser.add_argument('--output_spec',
                        type=str,
                        default=None,
                        help='If not None then this is the data matrix corresponding to the spectrogram output')
    parser.add_argument('--output_info',
                        type=str,
                        default=None,
                        help='If not None then this is the data matrix corresponding to the output info')
                                 
    main(parser.parse_args())
