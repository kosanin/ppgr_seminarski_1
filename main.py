import cv2
import modifikovani_dlt



def img_transformation(path, algorithm, width=100, height=100):
    def get_pixels(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(selected_points) < 4:
                cv2.circle(img, (x, y), radius=3, color=(0, 153, 255), thickness=2)
                selected_points.append([x, y, 1])
                cv2.imshow('image', img)
            if len(selected_points) == 4:
                transform_image()
                cv2.destroyWindow('image')

    selected_points = []

    img = cv2.imread(path, 1)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', get_pixels)

    def transform_image():
        points_dests = [[200, 200, 1],
                        [200 + width, 200, 1],
                        [200, 200 + height, 1],
                        [200 + width, 200 + height, 1]]

        # naivna provera
        # unaprediti tako da proverava da li je uneto smece
        if algorithm.lower() == "mdlt":
            mat_transformacije = modifikovani_dlt.normDLT(selected_points, points_dests)
        else:
            mat_transformacije = modifikovani_dlt.dlt(selected_points, points_dests)

        dst = cv2.warpPerspective(img, mat_transformacije, dsize=(img.shape[1], img.shape[0]))
        cv2.imshow(algorithm, dst)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
