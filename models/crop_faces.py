from imutils import paths
import face_recognition
import cv2
import os
import create_embeddings as ce
import classify_embeddings as cle
import model_train_pipeline as mtp
import classification as c
import pickle
import models.friend
from datetime import datetime


def crop_and_review_faces(user_id, input_path, output_path):
    # clear images in needs_review directory
    folder = os.path.abspath('./static/img/out/needs_review/')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    input_path = os.path.abspath(input_path + user_id + '/')
    output_path = os.path.abspath(output_path + user_id + '/')
    print('Input: ' + input_path)
    print('Output: ' + output_path)
    image_paths = list(paths.list_images(input_path))
    images_need_review = False

    file_num = 1
    needs_review_indexes = []
    index_of_index = 0
    # loop over the image paths
    for i, imagePath in enumerate(image_paths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i+1, len(image_paths)))

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb, model='hog')
        print(boxes)
        if len(boxes) == 0:
            boxes = face_recognition.face_locations(rgb, model='cnn')
        cropped_images = []
        images_to_review = []
        for box in boxes:
            top, right, bottom, left = box
            print("{},{},{},{}".format(top, right, bottom, left))
            crop_img = image[top: bottom, left: right]
            cropped_images.append(crop_img)
            # if multiple images found, send multiple images back up to page
            # and let the user choose which ones are correct
        if len(cropped_images) > 1:
            images_need_review = True
            images_to_review.append(cropped_images)
            for k in range(len(cropped_images)):
                needs_review_indexes.append(file_num + k)
        elif len(cropped_images) == 0:
            continue
        else:
            top, right, bottom, left = boxes[0]
            crop_img = image[top: bottom, left: right]
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            cv2.imwrite(output_path + '/' + str(file_num) + '.png', crop_img)
        for images in images_to_review:
            for image in images:
                print('../static/img/out/needs_review/' + str(needs_review_indexes[index_of_index]) + '.png')
                cv2.imwrite(folder + '/' + str(needs_review_indexes[index_of_index]) + '.png', image)
                index_of_index += 1
        file_num += len(cropped_images)
    return images_need_review


def save_reviewed_faces(images_indeces, user_id,  output_path):
    output_path = os.path.abspath(output_path + user_id + '/')
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for file_num in images_indeces:
        in_path = os.path.abspath('./static/img/out/needs_review/' + file_num + '.png')
        crop_img = cv2.imread(in_path)
        cv2.imwrite(output_path + '/' + str(file_num) + '.png', crop_img)


def crop_and_classify(image_path, home_user_id):
    print("cropping image from client")
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,
                                            model='hog')
    cropped_images = []
    for box in boxes:
        top, right, bottom, left = box
        crop_img = image[top: bottom, left: right]
        cropped_images.append(crop_img)
        # if multiple images found, send multiple images back up to page
        # and let the user choose which ones are correct

    embeddings = []
    for image in cropped_images:
        embeddings.append(ce.create_embeddings_for_single_face(image))

    model_name = mtp.get_active_name(home_user_id)
    print(model_name)
    classifier = cle.EmbeddingsClassifier(home_user_id, model_name)
    results = []
    for e in embeddings:
        results.append(classifier.classify_embeddings(e).tolist())

    # friends = classifier.get_friend_ids_for_classifier()
    friends = pickle.loads(open(os.path.abspath('./static/models/' + str(home_user_id) + '/' + model_name + '.pickle'),
                                "rb").read())
    print(friends)

    for i, result in enumerate(results):
        if len(result) > 1:
            result = result[0]
        print(result)
        classified_friend_id = friends[result.index(max(result))]
        friend = models.friend.load_by_id_with_home_id(home_user_id, classified_friend_id)
        out_image_path = os.path.abspath('./static/img/out/training/' + str(friend.user_id) + '/' +
                                         datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f') + '.png')
        cv2.imwrite(out_image_path, cropped_images[i])
        '''
        classification = c.Classification(friend.user_id, friend.first_name, friend.last_name, max(result),
                                          datetime.now(), out_image_path)
        c.save_classification(model_id=classifier.get_model_id(), classification=classification)
        '''
