import shutil, os

def generate_summarized_vid(frame_list,path,count,video_path):
    source = path+'/frames/'
    destination = path+'/summary_frames/'
    if not os.path.exists(destination):
        os.system('mkdir '+destination)

    frame_names = []
    for i in frame_list:
        frame_names.append('frame'+str(i)+'.jpg')
    print(frame_names)
    cnt=0
    for f in frame_names:
        try:
            shutil.copy(source+f, destination)
            extension = f.split('.')[1]
            os.rename(destination+f,destination+str(cnt)+'.'+extension)
            cnt+=1
        except Exception as e:
            print(e)
    import cv2
    cap=cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    #print('ffmpeg -framerate 24 -i '+destination+'%d.jpg '+path+'summarized'+str(count)+'.mp4')
    try: 
        os.system('mkdir '+path+'/output')
    except:
        pass
    os.system('ffmpeg -y -framerate '+str(fps)+' -i '+destination+'%d.jpg '+path+'/output/summarized'+str(count)+'.mp4')
    os.system('rm '+destination+'*')