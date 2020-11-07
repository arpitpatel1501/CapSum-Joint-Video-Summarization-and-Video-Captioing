#!/usr/bin/python
import sys
import cv2
import imageio
import pylab
import numpy as np
#sys.path.insert(1,'/home/arpit/Downloads/caffe/python/')
#print(sys.path)
import skimage.transform
from torchvision import models 
from torchvision.models import googlenet 
from PIL import Image 
import torch 
from torchvision import transforms 
import torch.nn as nn 
import os
import pandas as pd


def extract_feats(filenames,batch_size):
    """Function to extract VGG-16 features for frames in a video.
       Input:
            filenames:  List of filenames of videos to be processes
            batch_size: Batch size for feature extraction
       Writes features in .npy files"""
    
    #Read videos and extract features in batches
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    model1 = googlenet(pretrained=True)
    #model1.cuda()
    lenet = nn.Sequential(*list(model1.children())[:-2])
    for file in filenames:
        vid = imageio.get_reader(file,'ffmpeg')
        curr_frames = []
        features = []
        pathOut='./VASNet-master/frames'
        count=0
        try:
          for frame in vid:
              
              #frame = skimage.transform.resize(frame,[224,224])
              #if len(frame.shape)<3:
                  #frame = np.repeat(frame,3).reshape([224,224,3])
              curr_frames.append(frame)
              name = os.path.join(pathOut, "frame{:d}.jpg".format(count)) 
              
              #print('Read %d frame: ' % count, ret) 
              #print("filename:",name) 
              cv2.imwrite(name, frame) 
              #save frame as JPEG file 
              input_image = Image.open(name) 
              input_tensor = preprocess(input_image) 
              input_batch = input_tensor.unsqueeze(0) 
              #create a mini-batch as expected by the model 
              os.remove(name)
              fe = lenet(input_batch) 
              fe = torch.reshape(fe, (1, 1024)) 
              fe=fe[0]
              fe=fe.cpu().detach().numpy() 
              features.append(fe) 
              count+=1
              
          print(features)
          #df = pd.DataFrame(features)
          #df.to_csv('/feature.csv')
        

        except Exception as e:
            print(e) 

        
        curr_frames = np.array(curr_frames)
        print ("Shape of frames: {0}".format(curr_frames.shape))
        #idx = map(int,np.linspace(0,len(curr_frames)-1,80))
        #idx = [round(x) for x in idx]
        #print('\n curr_frames_shape:', curr_frames.shape, ', curr_frames_type:', type(curr_frames), ', idx:', idx, '\n') 
        #curr_frames = curr_frames[idx,:,:,:]
        print ("Captured 80 frames: {0}".format(curr_frames.shape))
        curr_feats = []
        
        '''
        for i in range(0,80,batch_size):
            caffe_in = np.zeros([batch_size,3,224,224])
            curr_batch = curr_frames[i:i+batch_size,:,:,:]
            for j in range(batch_size):
                caffe_in[j] = transformer.preprocess('data',curr_batch[j])
            out = net.forward_all(blobs=[layer],**{'data':caffe_in})
            curr_feats.extend(out[layer])
            print ("Appended {} features {}".format(j+1,out[layer].shape))
        
        curr_feats = np.array(curr_feats)
        np.save('Data/Features_VGG/'+file[:-4] + '.npy',curr_feats)
        print ("Saved file {}\nExiting".format('Data/Features_VGG/'+file[:-4] + '.npy'))
       '''
    return curr_feats

#extract_feats(['vid13.mp4'],10)
extract_feats(['/home/gegs/Downloads/test_video.mp4'],10)