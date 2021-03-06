import PIL
import PIL.Image
import torch.nn.functional as F
import torchvision.transforms as transforms
import cv2
import torch

def idx_to_class(class_to_idx):
    idx2class = {}
    for key, val in class_to_idx.items():
        dt = {val:key}
        idx2class.update(dt)
    return idx2class

def get_hand_number(classes, class_to_idx):
    idx2class = idx_to_class(class_to_idx)
    nclass = classes.data.squeeze().numpy().tolist()
    name = []
    for key in nclass:
        name.append(idx2class[key])
    return nclass, name
    
class ResizeCV(object):
    def __init__(self, size):
        self.size = size
    
    def __call__(self, image):
        rs_img = cv2.resize(image, (self.size,self.size))
        return rs_img
        
        
class NumpyToTensor(object):
    def __init__(self):
        pass
    def __call__(self, image):
        return torch.from_numpy(image)
    
        
def preprocess_npimage(img):
    
    mean_val, std_val = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    do_transforms =  transforms.Compose([
        ResizeCV(size=224),
#         transforms.CenterCrop(224),
        NumpyToTensor(),
        transforms.Normalize(mean_val,std_val)
    ])
    im_tfmt = do_transforms(img)
    im_add_batch = im_tfmt.view(1, im_tfmt.shape[0], im_tfmt.shape[1], im_tfmt.shape[2])
    return im_add_batch
    

def process_image(image):
    ''' Scales, crops, and normalizes a PIL image for a PyTorch model,
        returns an Numpy array
    '''
    im = PIL.Image.open(image)
    mean_val, std_val = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    do_transforms =  transforms.Compose([
        transforms.Resize(224),
#         transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean_val,std_val)
    ])
    im_tfmt = do_transforms(im)
    im_add_batch = im_tfmt.view(1, im_tfmt.shape[0], im_tfmt.shape[1], im_tfmt.shape[2])
    return im_add_batch