#!/usr/bin/python

import numpy as np
import tensorflow as tf
import glob
from caption.preprocess import *
#import cv2  ##################

import imageio


from pathlib import Path ######################
"""Utilities for training the video captioning system"""

#Global initializations
n_lstm_steps = 80
DATA_DIR = './caption/Data/'
VIDEO_DIR = DATA_DIR + 'Features_VGG/'
YOUTUBE_CLIPS_DIR = DATA_DIR+'YouTubeClips/'
TEXT_DIR = './caption/text_files/'
Vid2Url = eval(open(TEXT_DIR + 'Vid2Url_Full.txt').read())
Vid2Cap_train = eval(open(TEXT_DIR + 'Vid2Cap_train.txt').read())
Vid2Cap_val = eval(open(TEXT_DIR + 'Video2Caption_test.txt').read())

Url2Vid = eval(open(TEXT_DIR + 'url_to_vidId.txt').read()) #################

word_counts,unk_required = build_vocab(0)
word2id,id2word = word_to_word_ids(word_counts,unk_required)

video_files = list(Vid2Cap_train.keys())   ################################
val_files = list(Vid2Cap_val.keys())

print ("{0} files processed".format(len(video_files)))

##################################
# import os
# all_feature_files = [vid[:-4] for vid in os.listdir(VIDEO_DIR)]


def get_bias_vector():
    """Function to return the initialization for the bias vector
       for mapping from hidden_dim to vocab_size.
       Borrowed from neuraltalk by Andrej Karpathy"""
    bias_init_vector = np.array([1.0*word_counts[id2word[i]] for i in id2word])
    bias_init_vector /= np.sum(bias_init_vector) # normalize to frequencies
    bias_init_vector = np.log(bias_init_vector)
    bias_init_vector -= np.max(bias_init_vector)
    return bias_init_vector

def fetch_data_batch(batch_size):
    """Function to fetch a batch of video features, captions and caption masks
        Input:
                batch_size: Size of batch to load
        Output:
                curr_vids: Features of the randomly selected batch of video_files
                curr_caps: Ground truth (padded) captions for the selected videos
                curr_masks: Mask for the pad locations in curr_caps"""
    curr_batch_vids = np.random.choice(video_files,batch_size)  #####################3
    # curr_batch_vids = np.array(['vid1', 'vid5', 'vid4', 'vid3', 'vid2', 'vid6', 'vid7', 'vid8', 'vid13', 'vid11'])

    # curr_batch_vids = curr_batch_vids[:batch_size]

    # while not (set(curr_batch_vids).issubset(set(all_feature_files))):
    #     curr_batch_vids = np.random.choice(video_files,batch_size)  #####################
    #     print(curr_batch_vids)
    
    video_urls = [Vid2Url[vid] for vid in curr_batch_vids]
    
    curr_vids = np.array([np.load(VIDEO_DIR + vid + '.npy') for vid in curr_batch_vids])  ###########################
    ind_50 = map(int,np.linspace(0,79,n_lstm_steps))
    ind_50 = [round(x) for x in ind_50]     ###########################
    
    curr_vids = curr_vids[:,ind_50,:]
    captions = [np.random.choice(Vid2Cap_train[vid],1)[0] for vid in curr_batch_vids]
    curr_caps,curr_masks = convert_caption(captions,word2id,n_lstm_steps)
    return curr_vids,curr_caps,curr_masks,video_urls

def fetch_data_batch_val(batch_size):
    """Function to fetch a batch of video features from the validation set and its captions.
        Input:
                batch_size: Size of batch to load
        Output:
                curr_vids: Features of the randomly selected batch of video_files
                curr_caps: Ground truth (padded) captions for the selected videos"""

    curr_batch_vids = np.random.choice(val_files,batch_size)
    
    # while not (set(curr_batch_vids).issubset(set(all_feature_files))):
    #     curr_batch_vids = np.random.choice(val_files,batch_size)  #####################
    
    curr_vids = np.array([np.load(VIDEO_DIR + vid + '.npy') for vid in curr_batch_vids]) ###########################
    video_urls = [Vid2Url[vid] for vid in curr_batch_vids]
    ind_50 = map(int,np.linspace(0,79,n_lstm_steps))
    ind_50 = [round(x) for x in ind_50]     ###########################
   
    curr_vids = curr_vids[:,ind_50,:]
    captions = [np.random.choice(Vid2Cap_val[vid],1)[0] for vid in curr_batch_vids]
    curr_caps,curr_masks = convert_caption(captions,word2id,n_lstm_steps)
    return curr_vids,curr_caps,curr_masks,video_urls

def fetch_data_batch_user(feat_vid):
    """Function to fetch a batch of video features from the validation set and its captions.
        Input:
                batch_size: Size of batch to load
        Output:
                curr_vids: Features of the randomly selected batch of video_files
                curr_caps: Ground truth (padded) captions for the selected videos"""

    # curr_batch_vids = np.random.choice(val_files,batch_size)
    
    
    #curr_vids = np.load(VIDEO_DIR + '.npy') ###########################
    curr_vids = np.array([feat_vid]) ###########################
    print(curr_vids.shape)    
    #ind_50 = map(int,np.linspace(0,79,n_lstm_steps))
    ind_50 = map(int,np.linspace(0,curr_vids.shape[1]-1,n_lstm_steps))
    ind_50 = [round(x) for x in ind_50]     ###########################
    
    curr_vids = curr_vids[:,ind_50,:]
    # captions = [np.random.choice(Vid2Cap_val[vid],1)[0] for vid in curr_batch_vids]
    # curr_caps,curr_masks = convert_caption(captions,word2id,n_lstm_steps)
    return curr_vids


def print_in_english(caption_idx):
	"""Function to take a list of captions with words mapped to ids and
		print the captions after mapping word indices back to words."""
	captions_english = [[id2word[word] for word in caption] for caption in caption_idx]
	#print(captions_english)
	for i,caption in enumerate(captions_english):
		if '<EOS>' in caption:
			caption = caption[0:caption.index('<EOS>')]
		#print (str(i+1) + ' ' + ' '.join(caption))
	caption.pop(0)
	return (' '.join(caption))
		#print ('..................................................')
'''
def playVideo(file):
#    video = imageio.get_reader(YOUTUBE_CLIPS_DIR + video_urls[0] + '.avi','ffmpeg')	###################
    video = imageio.get_reader(file,'ffmpeg')
    for frame in video:
        fr = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        cv2.imshow('frame',fr)
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
'''