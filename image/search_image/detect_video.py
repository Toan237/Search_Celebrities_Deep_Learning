from keras_facenet import FaceNet
import cv2
import numpy as np
from mtcnn import MTCNN
import pickle
import os
import json
import time
from collections import OrderedDict
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity



detector = MTCNN()
embedder = FaceNet()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
embed_root = os.path.join(BASE_DIR, 'search_image/embed_blob_faces.pkl')
label_root = os.path.join(BASE_DIR, 'search_image/y_labels.pkl')
data_json =  os.path.join(BASE_DIR, 'search_image/data.json')

def _load_pickle(file_path):
  with open(file_path, 'rb') as f:
    obj = pickle.load(f)
  return obj

embed_faces = _load_pickle(embed_root)
y_labels = _load_pickle(label_root)
embed_faces = np.squeeze(embed_faces, axis = 1)

threshold=float(0.79)
name = []

save = 0
i = 0
j = 0
skip = int(20)
end = int(300)
# end = int(200)
embs = []
list_name = []
def _most_similarity(embed_vecs, vec, labels, threshold):
 
 for i in range(len(vec)):
  sim = cosine_similarity(embed_vecs, vec[i].reshape(1,-1))  
  sim = np.squeeze(sim, axis = 1)
  if float(sim.max()) < threshold:
   label = 'Unknown'   
   name.append(label)
  else:
   argmax = np.argsort(sim)[::-1][:1]
   print(argmax)
   label = [labels[idx] for idx in argmax][0] 
   name.append(label)
   list_name.append(label)
   
   
 return name



def _detect_video(video):
    start_time = time.time()
    list_name.clear()
    
    box = []
    embe = []
    success = True
    start_frame_number = skip
    
    vid_capture = cv2.VideoCapture(video)
    while(success):
        vid_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)
        success, image = vid_capture.read()   
        detection = detector.detect_faces(image)
        for i in range(len(detection)):
            bounding_box= detection[i]['box']
            roi_color = image[bounding_box[1]:bounding_box[1] + bounding_box[3], bounding_box[0]:bounding_box[0] + bounding_box[2]]
            box.append(roi_color)
        for i in box:
            k = [i]
            embedding = embedder.embeddings(k)
            embe.append(embedding)

        vec = embe
        v = _most_similarity(embed_faces, vec, y_labels,threshold)
        embs.clear()
        
        box.clear()
        embe.clear()
        name.clear() 
        start_frame_number += skip
        if start_frame_number > end:                   
            break 
    
    
    lst_name = list(set(list_name))

    data = {}
    name_video = {}
    data['1'] = []
    _key = []
    filename = os.path.basename(video)
    filename_link = '/media/video/' + filename 
    video = {'video': filename_link}
    
    sum_face = len(list_name)
    label_faces = "-".join(sorted(set(list_name)))
    faces = {'sum_face': sum_face}
    label_face = {'label_face': label_faces}
    if not os.path.exists(data_json):
        file = open(data_json, "w") 
        string = '{}'
        file.write(string)
        file.close() 
    with open(data_json, 'r') as json_file:
        data = json.load(json_file)
    
    if len(data) == 0:
        index = int(1)
    else:
        for key,value in data.items():
            _key.append(int(key))
        index = max(_key) + int(1)
    
    
    
    
    name_video.update(video)
    
    str = Counter(list_name)
    b = dict(str)
    b.update(name_video)
    b.update(faces)
    b.update(label_face)
    b = OrderedDict(reversed(list(b.items())))
    b = dict(b)
    c = {index : b}
    data.update(c)
    with open(data_json, 'w') as outfile:
        json.dump(data, outfile, indent = 4)
    
    
    end_time = time.time()

    elapsed_time = end_time - start_time
    
    return  lst_name