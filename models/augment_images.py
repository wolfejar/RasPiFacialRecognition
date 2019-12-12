import numpy as np
import cv2
import os


def augment_images(user_id):
    images_dir = os.path.abspath('./static/img/data/' + str(user_id))
    image_paths = [os.path.join(images_dir, f) for f in os.listdir(images_dir)
                   if os.path.isfile(os.path.join(images_dir, f))]
    images = []
    for path in image_paths:
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        images.append(cv2.flip(image, 1))
        images.append(noisy(image))
        images.append(cv2.flip(noisy(image), 1))

    for i, image in enumerate(images):
        cv2.imwrite(images_dir + '/augment_' + str(i) + '.jpg', image)


def noisy(image):
    row, col, ch = image.shape
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    noisy = image + gauss
    return noisy