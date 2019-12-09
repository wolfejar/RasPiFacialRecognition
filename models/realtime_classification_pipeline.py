import cv2
import face_recognition
from create_embeddings import create_embeddings_for_single_face
from classify_embeddings import EmbeddingsClassifier
from sql import SQL


def classify_image_from_client(home_id, model_name, image):
    print('classifying image from client')
    # rgb = cv2.imdecode(image, cv2.COLOR_BGR2RGB)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb, model='hog')
    cropped_images = []
    for box in boxes:
        top, right, bottom, left = box
        print("{},{},{},{}".format(top, right, bottom, left))
        crop_img = image[top: bottom, left: right]
        cropped_images.append(crop_img)

    classifications = []
    for crop_img in cropped_images:
        embeddings = create_embeddings_for_single_face(crop_img)
        print(embeddings)
        classifier = EmbeddingsClassifier(home_id, model_name)
        classifications.append(classifier.classify_embeddings(embeddings).tolist())
    if len(classifications) == 0:
        return 'unknown'
    else:
        return classifications


def get_info_for_unknown_user(home_user_id):
    sql_instance = SQL()
    return sql_instance.get_unknown_user(home_user_id)
