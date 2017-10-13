import glob
import os
import pickle
from PIL import Image
from extract_features import ExtractFeature

fe = ExtractFeature()

dict_feature = "static/feature/"  # set new path

if not os.path.exists(dict_feature):
    os.makedirs(dict_feature)

for img_path in sorted(glob.glob('static/img/*.jpg')):
    print(img_path)
    img = Image.open(img_path)  # PIL image
    feature = fe.extract(img)
    feature_path = dict_feature + os.path.splitext(os.path.basename(img_path))[0] + '.pkl'
    pickle.dump(feature, open(feature_path, 'wb'))