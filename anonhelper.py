import cv2
from datetime import datetime


def show_and_save(image, title="Output", save=True, time=0):
    """
    Show and save an image.
    Parameters
    ----------
    time
    image: np.array
    arrays with pixels
    title: str
    The tithe of the window
    save: Bool
    Indicate if you want to save the image.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    cv2.imshow(title, image)
    if save:
        file = f"{title}-{datetime.now().strftime('%y-%m-%d %H:%M:%S')}"
        cv2.imwrite(f"{file}.jpg", image)
        print(f"[INFO] image saved as: {file}.jpg")
    cv2.waitKey(time)
    return True

def convert_and_trim_bb(image, rect):
    """

    Parameters
    ----------
    image
    rect

    Returns
    -------

    """
    # extract the starting and ending (x, y)-coordinates of the
    # bounding box
    startX = rect.left()
    startY = rect.top()
    endX = rect.right()
    endY = rect.bottom()
    # ensure the bounding box coordinates fall within the spatial
    # dimensions of the image
    startX = max(0, startX)
    startY = max(0, startY)
    endX = min(endX, image.shape[1])
    endY = min(endY, image.shape[0])
    # compute the width and height of the bounding box
    w = endX - startX
    h = endY - startY
    # return our bounding box coordinates
    return (startX, startY, w, h)
