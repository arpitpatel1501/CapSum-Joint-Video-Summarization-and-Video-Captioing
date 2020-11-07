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


def extract_feats(filename,output_path):
    """Function to extract VGG-16 features for frames in a video.
       Input:
            filenames:  List of filenames of videos to be processes
            batch_size: Batch size for feature extraction
       Writes features in .npy files"""
    
    if not os.path.exists(output_path):
        os.system('mkdir '+output_path)
        print('mkdir '+output_path)

    #Read videos and extract features in batches
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    model1 = googlenet(pretrained=True)
    #model1.cuda()
    #CHANGED
    lenet = nn.Sequential(*list(model1.children())[:-2])
    
    
    vid = imageio.get_reader(filename,'ffmpeg')
    curr_frames = []
    features = []
    pathOut=output_path+'/frames'
    print(pathOut)
    if not os.path.exists(pathOut):
        print('in fe mkdir '+pathOut)
        os.system('mkdir '+pathOut)
    count=0
    print(pathOut)
    print('extracting features')
    try:
        for frame in vid:
            #frame = skimage.transform.resize(frame,[224,224])
            #if len(frame.shape)<3:
                #frame = np.repeat(frame,3).reshape([224,224,3])
            #curr_frames.append(frame)
            name = os.path.join(pathOut, "frame{:d}.jpg".format(count)) 
            
            #print('Read %d frame: ' % count, ret) 
            #print("filename:",name) 
            cv2.imwrite(name, frame)
            #os.system('ffmpeg -i pot_painting/source_video.mkv frames/frame%d.jpg')
            #save frame as JPEG file 
            
            count+=1 
            print(count)
    except Exception as e:
        print(e)
    count2=0
    for name in os.listdir(output_path+'/frames'):
        print(count2)
        name=output_path+'/frames/'+name
        input_image = Image.open(name) 
        input_tensor = preprocess(input_image) 
        input_batch = input_tensor.unsqueeze(0)
        #input_batch=input_batch.to('cuda:0')
        #CHANGED
        #create a mini-batch as expected by the model 
        #os.remove(name)
        fe = lenet(input_batch)
        fe = torch.reshape(fe, (1, 1024)) 
        fe=fe[0]
        fe=fe.detach().cpu().numpy()
        features.append(fe)
        count2+=1
    print(features)
    df = pd.DataFrame(features)
    df.to_csv(output_path+'/feature.csv')
    curr_frames = []
    features = []
    return output_path+'/feature.csv'

#extract_feats(['vid13.mp4'],10)
#output_path = './seed_video/'
#extract_feats('./seed_video/source.mp4',output_path)