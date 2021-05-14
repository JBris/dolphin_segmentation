from pathlib import Path

def preprocess_images(image_files):
    #images = []
    names = []

    for file in image_files:
        names.append(Path(file).stem)
        # img = cv2.imread(file)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv2.resize(img, (img_size, img_size))
        # img = img.astype('float32')
        # img = cv2.bilateralFilter(img, 9, 50, 50)
    #     #image = cv2.normalize(image, np.zeros((img_size, img_size)), 0, 1, cv2.NORM_MINMAX)
    #     images.append(img)
    # images = np.asarray(images)
    # images = images.reshape((images.shape[0], -1))
    return names
        
class ImagePreprocessor:
    IMG_SIZE = 256

    def preprocess(self, preprocessed_files):
        names = preprocess_images(preprocessed_files["files"])
        #preprocessed_files["preprocessed_images"] = images
        preprocessed_files["preprocessed_names"] = names
        return preprocessed_files
