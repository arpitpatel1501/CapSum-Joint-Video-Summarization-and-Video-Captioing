#!/usr/bin/python
import sys
#import cv2
import imageio
import pylab
import numpy as np
#sys.path.insert(1,'/home/arpit/Downloads/caffe/python/')
#print(sys.path)
import skimage.transform
import caffe


def extract_feats(file,batch_size):
    #caffe.set_mode_gpu()
    #caffe.set_device(0)

    """Function to extract VGG-16 features for frames in a video.
       Input:
            filenames:  List of filenames of videos to be processes
            batch_size: Batch size for feature extraction
       Writes features in .npy files"""
    model_file = './caption/VGG_ILSVRC_16_layers.caffemodel'
    deploy_file = './caption/VGG16_deploy.prototxt'
    net = caffe.Net(deploy_file,model_file,caffe.TEST)
    layer = 'fc7'
    mean_file = './caption/ilsvrc_2012_mean.npy'
    transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
    transformer.set_mean('data',np.load(mean_file).mean(1).mean(1))
    transformer.set_channel_swap('data', (2,1,0))
    transformer.set_transpose('data',(2,0,1))
    transformer.set_raw_scale('data',255.0)
    net.blobs['data'].reshape(batch_size,3,224,224)
    print ("VGG Network loaded")
    #Read videos and extract features in batches
    #for file in filenames:
    print(file)
    vid = imageio.get_reader(file,'ffmpeg')
    curr_frames = []
    for frame in vid:
        frame = skimage.transform.resize(frame,[224,224])
        if len(frame.shape)<3:
            frame = np.repeat(frame,3).reshape([224,224,3])
        curr_frames.append(frame)
    curr_frames = np.array(curr_frames)
    print ("Shape of frames: {0}".format(curr_frames.shape))
    idx = map(int,np.linspace(0,len(curr_frames)-1,80))
    idx = [round(x) for x in idx]
    #print('\n curr_frames_shape:', curr_frames.shape, ', curr_frames_type:', type(curr_frames), ', idx:', idx, '\n') 
    #curr_frames = curr_frames[idx,:,:,:]
    print ("Captured 80 frames: {0}".format(curr_frames.shape))
    curr_feats = []
    for i in range(0,curr_frames.shape[0],batch_size):
        caffe_in = np.zeros([batch_size,3,224,224])
        curr_batch = curr_frames[i:i+batch_size,:,:,:]
        #print('cur_frames: ')
        #print(curr_frames[i:i+batch_size,:,:,:])
    
        for j in range(batch_size):
            caffe_in[j] = transformer.preprocess('data',curr_batch[j])
        out = net.forward_all(blobs=[layer],**{'data':caffe_in})
        curr_feats.extend(out[layer])
        print ("Appended {} features {}".format(j+1,out[layer].shape))
    curr_feats = np.array(curr_feats)
    #np.save('Data/Features_VGG/'+file[:-4] + '.npy',curr_feats)
    #np.save(file[:-4] + '.npy',curr_feats)
    #print ("Saved file {}\nExiting".format('Data/Features_VGG/'+file[:-4] + '.npy'))
    

    return curr_feats
        

'''
import os
import pandas as pd
data=pd.read_csv('data_3.csv')
cnt=0
clips=[]
for id,row in data.iterrows():
    if not os.path.exists('Data/Features_VGG/'+row['id']+'.npy'):
        if os.path.exists('Data/YouTubeClips/'+row['id']+'.mp4'):
            print('Data/YouTubeClips/'+row['id']+'.mp4')
            clips.append(row['id']+'.mp4')
            cnt+=1
print(cnt)
print(clips)
'''
#extract_feats('/home/gegs/Downloads/vid_test3.mp4',10)
