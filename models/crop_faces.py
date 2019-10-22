from imutils import paths
import face_recognition
import cv2
import os


def crop_and_review_faces(user_name, input_path, output_path):
    # clear existing images in ouput directory
    input_path = input_path + '/' + user_name
    image_paths = list(paths.list_images(input_path))

    images_to_review = []

    # loop over the image paths
    for (i, imagePath) in enumerate(image_paths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
                                                     len(image_paths)))
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
                                                model='hog')

        cropped_images = []
        for box in boxes:
            top, right, bottom, left = box
            print("{},{},{},{}".format(top, right, bottom, left))
            crop_img = image[top: bottom, left: right]
            cropped_images.append(crop_img)
            # if multiple images found, we need to just save the largest image?
            # or send multiple images back up to webpage and let the user choose which one is them.
        if len(boxes) > 1:
            images_to_review.append(cropped_images)
        else:
            top, right, bottom, left = boxes[0]
            crop_img = image[top: bottom, left: right]
            if not os.path.exists(output_path + '/' + user_name):
                os.mkdir(output_path + '/' + user_name)
            cv2.imwrite(output_path + '/' + user_name + '/' + str(i) + '.png', crop_img)
    return images_to_review


crop_and_review_faces('jared_wolfe', '../static/img/data', '../static/img/out')
