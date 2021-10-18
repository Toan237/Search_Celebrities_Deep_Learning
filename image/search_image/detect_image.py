import cv2
import numpy as np
import pickle
from mtcnn import MTCNN
from keras_facenet import FaceNet
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from operator import itemgetter

detector = MTCNN()
embedder = FaceNet()
threshold=float(0.7)
l = []

embs = []
i = 0
j = 0
p = 0

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

def _most_similarity(embed_vecs, vec, labels, threshold):
 for i in range(len(vec)):
  sim = cosine_similarity(embed_vecs, vec[i].reshape(1,-1))
  sim = np.squeeze(sim, axis = 1)
  if sim.max() < threshold:
   label = 'Unknow'   
  else:
   argmax = np.argsort(sim)[::-1][:1]
   label = [labels[idx] for idx in argmax][0]
   l.append(label)
 return l  

def _detect_image(image):
    l.clear()
    box = []
    embe = []
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


    with open(data_json, 'r') as json_file:
     data = json.load(json_file)
    
    lst = [] 
    lst1 = []
    lst2 = []
    lst3 = []
    lst4 = []
    lst_name = []
    if len(l) == 0:
     return lst_name, l
    elif len(l) == 1:
     for names in l:
      name = names 
     for i in data:
      lst.append(data[i])
    
     for i in range(len(lst)):
      for j in lst[i]:
       if j == name:
        lst1.append(lst[i])
     newlist = sorted(lst1, key=itemgetter(name), reverse=True)
     
     if newlist:
      lst_name.append(newlist)
    
     lst.clear()
     lst1.clear()
     new_l = sorted(l)
     return lst_name, new_l

    elif len(l) == 2:
      for i in data:
       lst.append(data[i])
      n = "-".join(sorted(l))
      t = "-"
      for i in range(len(lst)):
       if lst[i]["label_face"] == n:
        lst2.append(lst[i])
      if len(lst2) == 0: 
       for i in range(len(lst)):
        for j in lst[i]:
         if j == l[0]:
          lst3.append(lst[i])
       for i in range(len(lst3)):
        if t in lst3[i]["label_face"]:
         lst3[i]["sum_face"] = lst3[i][l[0]]
 

       for i in range(len(lst)):
        for j in lst[i]:
         if j == l[1]:
          lst3.append(lst[i])
       for i in range(len(lst4)):
        if t in lst4[i]["label_face"]:
         lst4[i]["sum_face"] = lst4[i][l[1]]
 
       for i in lst4:
        lst3.append(i)
       lst3 = sorted(lst3, key=itemgetter("sum_face"), reverse=True)
       lst.clear()
       lst1.clear()
       new_l = sorted(l)
       return lst3, new_l
      else:
       lst2 = sorted(lst2, key=itemgetter("sum_face"), reverse=True)
       for name in l:
        for i in range(len(lst)):
         if lst[i]["label_face"] == name:
          lst3.append(lst[i])
       lst3 = sorted(lst3, key=itemgetter("sum_face"), reverse=True)
       lst_name = lst2 + lst3
       lst.clear()
       lst1.clear()
       new_l = sorted(l)
       return lst_name, new_l
    else:  
     for i in data:
      lst.append(data[i])
     for name in l: 
      for i in range(len(lst)):
       if lst[i]["label_face"] == name:
        lst3.append(lst[i])

     lst3 = sorted(lst3, key=itemgetter("sum_face"), reverse=True)
    #  lst_name = lst3
     lst.clear()
     lst1.clear()
     new_l = sorted(l)
     return lst3, new_l
      
      
      