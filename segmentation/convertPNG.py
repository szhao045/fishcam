import sys,os
from PIL import Image

def convert_png(path):
    '''
    Helper function to convert PNG to TIFF
    '''
    for file in os.listdir(path):
        if file.endswith(".png"):
            image = Image.open(os.path.join(path, file))
            # Make sure image is at 16bit depth
            image.convert('I;16').save(path + '/' + os.path.splitext(file)[0] + '.tif')

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        raise ValueError('Wrong number of arguments!')
    convert_png(path)