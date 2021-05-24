ALPHA = 0.4
THRESHOLD = 0.5
IMAGE_SIZE= 96
LAYERS_TO_FREEZE= 60
NUM_EPOCHS=50
STEPS_PER_EPOCH= 100
BATCH_SIZE= 200

trn_img="rsz" #ftr = features; rsz = resized
TARGET_IMAGES_DIR = '../images/fin_features_'+str(IMAGE_SIZE)
#TARGET_IMAGES_DIR = TARGET_IMAGES_DIR+trn_img
MAX_FILES = 5000

IMG_DIR = '../images/'
IMAGES_DIR = IMG_DIR+'final_pigmentation_catalogue_2016'

MODEL_DIR="../models/darknet"
FINMODEL_DIR="../models/finnet"
INPUT_DIR="../input2match"
DICTPATH = 'dictmodel.dat'