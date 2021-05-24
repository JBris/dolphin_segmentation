######################################################################################
## Code is based on a facenet implementation: https://github.com/sainimohit23/FaceNet-Real-Time-face-recognition
## Code was amended for the use of this project

import os
import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("tensorflow").addHandler(logging.NullHandler(logging.ERROR))
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'

from keras.models import Model
from keras.callbacks import CSVLogger
# from keras.layers.normalization import BatchNormalization
# from keras.layers.pooling import MaxPooling2D, AveragePooling2D
# from keras.layers.merge import Concatenate
# from keras.layers.core import Lambda, Flatten, Dense
# from keras.initializers import glorot_uniform
#from keras.engine.topology import Layer
#import tensorflow_addons as tfa
from keras import backend as K
K.set_image_data_format('channels_first')

import tensorflow as tf
from fr_utils import *
from inception_blocks_v2 import *


import keras
from generator_utils import *
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
import time
from parameters import *

# from tensorflow.python.framework.ops import disable_eager_execution
# disable_eager_execution()

tf.function(jit_compile=True)
# os.environ['XLA_FLAGS'] = '--tf_xla_disable_xla_devices'
os.environ['XLA_FLAGS'] = '--tf_xla_disable_xla_devices --tf_xla_auto_jit=2 --tf_xla_cpu_global_jit'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
with tf.Graph().as_default():
        gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.7)
        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.compat.v1.Session(config=config)
        
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
with tf.profiler.experimental.Profile('profile'):
    foo = tf.random.normal((100, 100))
    bar = foo * foo        

best_model_path=None
if os.path.exists("./bestmodel.txt"):
    with open('bestmodel.txt', 'r') as file:
        best_model_path = file.read()
        
# remove precalculations
if os.path.exists(DICTPATH):
    os.remove(DICTPATH) 
    
if best_model_path != None and os.path.exists(best_model_path):
    ("Pre trained model found")
    FRmodel = keras.models.load_model(best_model_path, custom_objects={'triplet_loss': triplet_loss})
    
else:
    print('Saved model not found, loading untrained ')
    FRmodel = finRecoModel(input_shape=(3, IMAGE_SIZE, IMAGE_SIZE))
    load_weights_from_FinNet(FRmodel)

for layer in FRmodel.layers[0: LAYERS_TO_FREEZE]:
    layer.trainable  =  False
    
#print("layers: "+str(len(FRmodel.layers)))
    
input_shape=(3, IMAGE_SIZE, IMAGE_SIZE)
A = Input(shape=input_shape, name = 'anchor')
P = Input(shape=input_shape, name = 'anchorPositive')
N = Input(shape=input_shape, name = 'anchorNegative')

#Anchors
enc_A = FRmodel(A)
enc_P = FRmodel(P)
enc_N = FRmodel(N)

#model2
positive_dist = Lambda(euclidean_distance, name='pos_dist')([A, P])
negative_dist = Lambda(euclidean_distance, name='neg_dist')([A, N])
stacked_dists = Lambda(lambda vects: K.stack(vects, axis=1), name='stacked_dists')([positive_dist, negative_dist]) # shape = [batch_size, 2, 1]

# Callbacks
ts = str(int(time.time()))
early_stopping = EarlyStopping(monitor='loss', patience=5, min_delta=0.00005)
STAMP = 'finmod_%d'%(len(paths)) 
checkpoint_dir = FINMODEL_DIR+'/checkpoints/' + ts + '/'

if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

bst_model_path = checkpoint_dir + STAMP + '.h5'
tensorboard = TensorBoard(log_dir=checkpoint_dir + "logs/{}".format(time.time()))

# Model1
tripletModel = Model(inputs=[A, P, N], outputs=[enc_A, enc_P, enc_N])
tripletModel.compile(optimizer = 'adam', loss = triplet_loss)

# Model2
#tripletModel = Model([A, P, N], stacked_dists, name='triple_siamese')
#tripletModel.compile(optimizer = 'adadelta', loss = triplet_loss_v2, metrics = None)

gen = batch_generator(BATCH_SIZE)

if len(labels)==0:
    print("Error >> no training data found in " + TARGET_IMAGES_DIR)
    exit(0)
csv_logger = CSVLogger(FINMODEL_DIR+'/finnet_train_'+ts+'.csv', append=True, separator=',')
tripletModel.fit(gen, epochs=NUM_EPOCHS,steps_per_epoch=STEPS_PER_EPOCH,callbacks=[csv_logger, tensorboard]) #early_stopping

FRmodel.save(bst_model_path)
with open('bestmodel.txt','w') as file:
    file.write(bst_model_path)
