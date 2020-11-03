__author__ = 'Jiri Fajtl'
__email__ = 'ok1zjf@gmail.com'
__version__= '3.6'
__status__ = "Research"
__date__ = "1/12/2018"
__license__= "MIT License"



from torchvision import transforms
import numpy as np
import time
import glob
import random
import argparse
import h5py
import json
import torch.nn.init as init
import pandas as pd
from pandas.core.common import flatten

from config import  *
from sys_utils import *
from vsum_tools import generate_summary
from vasnet_model import  *
from feat_extract import extract_feats
from generate_summarized_vid import generate_summarized_vid
from cpd_auto import cpd_auto
from cpd_nonlin import cpd_nonlin




def weights_init(m):
    classname = m.__class__.__name__
    if classname == 'Linear':
        init.xavier_uniform_(m.weight, gain=np.sqrt(2.0))
        if m.bias is not None:
            init.constant_(m.bias, 0.1)

def parse_splits_filename(splits_filename):
    # Parse split file and count number of k_folds
    spath, sfname = os.path.split(splits_filename)
    sfname, _ = os.path.splitext(sfname)
    dataset_name = sfname.split('_')[0]  # Get dataset name e.g. tvsum
    dataset_type = sfname.split('_')[1]  # augmentation type e.g. aug

    # The keyword 'splits' is used as the filename fields terminator from historical reasons.
    if dataset_type == 'splits':
        # Split type is not present
        dataset_type = ''

    # Get number of discrete splits within each split json file
    with open(splits_filename, 'r') as sf:
        splits = json.load(sf)

    return dataset_name, dataset_type, splits

def lookup_weights_splits_file(path, dataset_name, dataset_type, split_id):
    dataset_type_str = '' if dataset_type == '' else dataset_type + '_'
    weights_filename = path + '/models/{}_{}splits_{}_*.tar.pth'.format(dataset_name, dataset_type_str, split_id)
    weights_filename = glob.glob(weights_filename)
    if len(weights_filename) == 0:
        print("Couldn't find model weights: ", weights_filename)
        return ''

    # Get the first weights file in the dir
    weights_filename = weights_filename[0]
    splits_file = path + '/splits/{}_{}splits.json'.format(dataset_name, dataset_type_str)

    return weights_filename, splits_file


class AONet:

    def __init__(self, hps: HParameters):
        self.hps = hps
        self.model = None
        self.log_file = None
        self.verbose = hps.verbose


    def load_model(self, model_filename):
        self.model.load_state_dict(torch.load(model_filename, map_location=lambda storage, loc: storage), strict=False)
        return


    def initialize(self, cuda_device=None):
        rnd_seed = 12345
        random.seed(rnd_seed)
        np.random.seed(rnd_seed)
        torch.manual_seed(rnd_seed)

        self.model = VASNet()
        self.model.eval()
        self.model.apply(weights_init)
        #print(self.model)

        #cuda_device = cuda_device or self.hps.cuda_device

        if self.hps.use_cuda:
            print("Not! Setting CUDA device: ",cuda_device)
            #torch.cuda.set_device(cuda_device)
            #torch.cuda.manual_seed(rnd_seed)

        if self.hps.use_cuda:
            print("Not! Setting CUDA device: ",cuda_device)
            #self.model.cuda()

        return

    def lookup_weights_file(self, data_path):
        dataset_type_str = '' if self.dataset_type == '' else self.dataset_type + '_'
        weights_filename = data_path + '/models/{}_{}splits_{}_*.tar.pth'.format(self.dataset_name, dataset_type_str, self.split_id)
        weights_filename = glob.glob(weights_filename)
        if len(weights_filename) == 0:
            print("Couldn't find model weights: ", weights_filename)
            return ''

        # Get the first weights filename in the dir
        weights_filename = weights_filename[0]
        splits_file = data_path + '/splits/{}_{}splits.json'.format(self.dataset_name, dataset_type_str)

        return weights_filename, splits_file

def centering(K):
    """Apply kernel centering"""
    mean_rows = np.mean(K, 1)[:, np.newaxis]
    return K - mean_rows - mean_rows.T + np.mean(mean_rows)

def test(hps,weights_filename,fe_csv_path,fe_output_path):
    import torch
    import pandas as pd
    df = pd.read_csv(fe_csv_path)
    fe = df.to_numpy()
    fe=fe[:,1:]
    ao = AONet(hps)
    ao.initialize()
    #weights_filename = "/content/drive/My Drive/Semester_7/AI_CC_Project/Video Summarization/VASNet-master/data/models/summe_aug_splits_1_0.443936558699067.tar.pth"
    ao.load_model(weights_filename)
    seq = fe
    seq = torch.from_numpy(seq).unsqueeze(0)
    if ao.hps.use_cuda:
        seq = seq.float()
    y, att_vec = ao.model(seq, seq.shape[1])
    print(y.shape)
    
    att_vec=att_vec.cpu().detach().numpy()
    y=y.cpu().detach().numpy()
    print(y.shape)
    K = np.dot(y.T, y)
    
    n = K.shape[0]
    num_frames = y.shape[1]
    
    vmax = np.trace(centering(K)/n)
    #cps, scores = cpd_nonlin(K, 4000, lmin=1, lmax=10000)

    cps,scores = cpd_auto(K,num_frames//2,1,vmax)

    #cps, scores = cpd_auto(att_vec, 100, 1)
    
    
    #print(cps)
    
    import pandas as pd
    df=pd.DataFrame(cps)
    df.to_csv(fe_output_path+'/cps.csv')
    df = pd.read_csv(fe_output_path+'/cps.csv')
    df = df.to_numpy()
    #print(type(df))
    print(df[:,1])
    cps=df[:,1]
    start=cps[0]
    cps_pair=[]
    cnt=1
    # 107 108 109 110
    #cps_pair.append([0,1452])
    frame=df[:,1]
    start=frame[0]
    dummy_start=frame[0]
    frame_pair=[]
    cnt=1
    while cnt!=len(cps):
        end = cps[cnt]
        if dummy_start+1!=end:
            cps_pair.append([start,cps[cnt-1]])
            start = end
            dummy_start = start
            cnt=cnt+1
        else:
            dummy_start = end
            cnt=cnt+1
              
    #print(cps_pair[-1][1])
    if cps_pair[-1][1] != y.shape[1]:
        cps_pair.append([cps_pair[-1][1],y.shape[1]])
    positions = range(0,y.shape[1],15)
    positions = np.asarray(positions)
    print(type(positions))

    probs = np.asarray(y)
    
    nfps = []
    for i in cps_pair:
        nfps.append(i[1]-i[0])
    
    cps_pair = np.asarray(cps_pair)
    nfps = np.asarray(nfps)
    print(len(probs[0]))
    
    print(cps_pair)
    machine_summary = generate_summary(probs[0], cps_pair, num_frames, nfps, positions)
    print(machine_summary)
    machine_summary = machine_summary.tolist()
    print(len(machine_summary))
    print(machine_summary.count(1))
    summary_frames = [i for i in range(len(machine_summary)) if machine_summary[i] == 1]
    #print(summary_frames) 
    ##print(cps_pair)
    del sys.modules['torch']
    del torch
    return cps_pair,summary_frames



def run_sum(source_vid):
    #print_pkg_versions()
    #parser = argparse.ArgumentParser("PyTorch implementation of paper \"Summarizing Videos with Attention\"")
    #parser.add_argument('-r', '--root', type=str, default='', help="Project root directory")
    #parser.add_argument('-d', '--datasets', type=str, help="Path to a comma separated list of h5 datasets")
    #parser.add_argument('-s', '--splits', type=str, help="Comma separated list of split files.")
    #parser.add_argument('-t', '--train', default=True,action='store_true', help="Train")
    #parser.add_argument('-v', '--verbose', action='store_true', help="Prints out more messages")
    #parser.add_argument('-o', '--output-dir', type=str, default='data', help="Experiment name")
    #args = parser.parse_args()

    # MAIN
    #======================
    hps = HParameters()	
    print(source_vid.split('./process/')[1].split('.')[0])
    os.system('mkdir ./process/'+source_vid.split('./process/')[1].split('.')[0])
    video_path=source_vid
    fe_output_path='./process/'+source_vid.split('./process/')[1].split('.')[0]
    
    
    fe_csv_path = extract_feats(video_path,fe_output_path)
    #fe_csv_path='./'+source_vid.split('.')[0]+'/feature.csv'
    #hps.load_from_args(args.__dict__)
    weights_filename = "./summarizer/model_weight/summe_aug_splits_1_0.443936558699067.tar.pth"
    #print("Parameters:")
    print("----------------------------------------------------------------------")
    print(hps)
    

    cps_pair,summary_frames = test(hps,weights_filename,fe_csv_path,fe_output_path)
    df=pd.DataFrame(summary_frames)
    df.to_csv(fe_output_path+'/summary_frames.csv')
    
    print(fe_output_path+'/summary_frames.csv')
    df=pd.read_csv(fe_output_path+'/summary_frames.csv')
    #df = pd.read_csv('./summary_frames.csv')
    #print(df.head)
    print(df.head)
    df = df.to_numpy()
    
    frame=df[:,1]
    start=frame[0]
    dummy_start=frame[0]
    frame_pair=[]
    cnt=1
    # 107 108 109 110
    # 101 102 108 108
    #cps_pair.append([0,1452])
    #end = frame[cnt]
  
    while cnt!=len(frame):
        end = frame[cnt]
        if dummy_start+1!=end:
            frame_pair.append([start,frame[cnt-1]])
            start = end
            dummy_start = start
            cnt=cnt+1
        else:
            dummy_start = end
            cnt=cnt+1    
        
    lenFramePair = len(frame_pair)
    #print(lenFramePair)
    count = 0
    cnt=0
    finalFramePair = []
    print(frame_pair)
    frames = list(range(frame_pair[0][0],frame_pair[0][1]+1,1))
    finalFramePair.append(frames)
    count=count+1
    
    while count!=lenFramePair:
        last = frame_pair[count-1][1]
        next_ = frame_pair[count][0]

        if ((next_-last<=40) and (len(finalFramePair[cnt])<=20)):
            frames = list(range(frame_pair[count][0],frame_pair[count][1]+1,1))
            finalFramePair[cnt].append(frames)
            
        else:
            l = finalFramePair[cnt]
            finalFramePair[cnt] = list(flatten(l))
            cnt=cnt+1
            frames = list(range(frame_pair[count][0],frame_pair[count][1]+1,1))
            finalFramePair.append(frames)

        count=count+1

    #print(cps_pair[-1][1])
    
    for count,i in enumerate(finalFramePair):
        #frames = range(i[0],i[1],1)
        print(i)
        frames = np.asarray(i)
        generate_summarized_vid(frames,fe_output_path,count,video_path)
    
if __name__ == "__main__":
    source_vid=sys.argv[1]
    #source_vid = 'hello.mp4'
    run_sum(source_vid)
