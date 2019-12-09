# USAGE
# When encoding on laptop, desktop, or GPU (slower, more accurate):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn
# When encoding on Raspberry Pi (faster, more accurate):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# import the necessary packages
from imutils import paths
import face_recognition
import pickle
import cv2
import os


def encode_faces(friends):
    for fr in friends:
        input_path = './static/img/out/training/'

        faces_dir = os.path.abspath(input_path + str(fr.user_id) + '/')
        image_paths = list(paths.list_images(faces_dir))
        output_path = os.path.abspath('./static/img/out/embeddings/' + str(fr.user_id) + '/')
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        for i, imagePath in enumerate(image_paths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(image_paths)))

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            height, width, channels = image.shape

            box = (0, height, width, 0)
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, [box])

            print("[INFO] serializing encodings...")
            data = {"encodings": encodings, "user_id": fr.username}

            f = open(output_path + '/' + str(i) + '.pickle', "wb+")
            f.write(pickle.dumps(data))
            f.close()


def create_embeddings_for_single_face(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, channels = image.shape

    box = (0, height, width, 0)
    # compute the facial embedding for the face
    return face_recognition.face_encodings(rgb, [box])
