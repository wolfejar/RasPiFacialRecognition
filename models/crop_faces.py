from imutils import paths
import face_recognition
import cv2
import os


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
        boxes = face_recognition.face_locations(rgb,
                                                model='hog')

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
    for file_num in images_indeces:
        in_path = os.path.abspath('./static/img/out/needs_review/' + file_num + '.png')
        crop_img = cv2.imread(in_path)
        cv2.imwrite(output_path + '/' + str(file_num) + '.png', crop_img)
