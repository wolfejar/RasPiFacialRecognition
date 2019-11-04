from imutils import paths
import face_recognition
import cv2
import os


def crop_and_review_faces(user_name, input_path, output_path):
    # clear images in needs_review directory
    folder = os.path.abspath('./static/img/out/needs_review/')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    input_path = os.path.abspath(input_path + user_name + '/')
    output_path = os.path.abspath(output_path + user_name + '/')
    print(input_path)
    print(output_path)
    image_paths = list(paths.list_images(input_path))
    print(image_paths)
    images_need_review = False

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
        images_to_review = []
        for box in boxes:
            top, right, bottom, left = box
            print("{},{},{},{}".format(top, right, bottom, left))
            crop_img = image[top: bottom, left: right]
            cropped_images.append(crop_img)
            # if multiple images found, we need to just save the largest image?
            # or send multiple images back up to webpage and let the user choose which one is them.
        if len(cropped_images) > 1:
            images_need_review = True
            images_to_review.append(cropped_images)
        else:
            top, right, bottom, left = boxes[0]
            crop_img = image[top: bottom, left: right]
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            cv2.imwrite(output_path + str(i) + '.png', crop_img)
        for images in images_to_review:
            for k, image in enumerate(images):
                # cv2.imshow("review", image)
                # cv2.waitKey(0)
                print('../static/img/out/needs_review/' + str(i) + '-' + str(k) + '.png')
                cv2.imwrite('../static/img/out/needs_review/' + str(i) + '-' + str(k) + '.png', image)
    return images_need_review