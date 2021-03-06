import numpy as np
import cv2

# ------------------------------------------------------------------------------
# draw circle and get coordinate
class PointList():
    def __init__(self, npoints):
        self.npoints = npoints
        self.pts = np.empty((npoints, 2), dtype=int)
        self.pos = 0

    def add(self, x, y):
        if self.pos < self.npoints:
            self.pts[self.pos, :] = [x, y]
            self.pos += 1
            return True
        return False
# ------------------------------------------------------------------------------
def onMouse(event, x, y, flag, params):
    wname, img, pts = params
    # if move the mouse, x and y line is edited
    if event == cv2.EVENT_MOUSEMOVE:
        img2 = np.copy(img)
        h, w = img2.shape[0], img2.shape[1]
        cv2.line(img2, (x, 0), (x, h - 1), (255, 0, 0))
        cv2.line(img2, (0, y), (w - 1, y), (255, 0, 0))
        cv2.imshow(wname, img2)

    # if left button is clicked,
    if event == cv2.EVENT_LBUTTONDOWN:
        if pts.add(x, y):
            print(type(pts))
            # print('[%d] ( %d, %d )' % (pts.pos - 1, x, y))
            # print((pts.pos - 1, x, y))
            print((x,y))
            cv2.circle(img, (x, y), 3, (0, 0, 255), 3)
            cv2.imshow(wname, img)
            X.append((x,y))
            print(X)
            Num_X = np.array(X) # list to numpy

            #
            if len(Num_X) == 4:
                rect = np.zeros((4,2), dtype="float32")
                s = Num_X.sum(axis = 1)

                # top-left point will have the smallest sum
                rect[0] = Num_X[np.argmin(s)]
                rect[2] = Num_X[np.argmax(s)]
                # bottom-right point will have the largest sum
                diff = np.diff(Num_X, axis = 1)
                rect[1] = Num_X[np.argmin(diff)]
                rect[3] = Num_X[np.argmax(diff)]
                # return rect

                if len(rect) == 4:
                    print(rect)
                    (tl, tr, br, bl) = rect # 4 points of rectangle
                    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                    print(widthA)
                    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                    print(widthB)
                    maxWidth = max(int(widthA), int(widthB))
                    print(maxWidth)
                    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                    print(heightA)
                    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                    print(heightB)
                    maxHeight = max(int(heightA), int(heightB))
                    print(maxHeight)
                    dst = np.array([
                        [0,0],
                        [maxWidth - 1, 0],
                        [maxWidth - 1, maxHeight - 1],
                        [0, maxHeight - 1]], dtype = "float32")
                    print(dst)
                    M = cv2.getPerspectiveTransform(rect, dst)
                    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

                    # return warped
                    cv2.imshow("warped", warped)
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    img = cv2.imread('analog.jpg') # 入力画像
    wname = "MouseEvent" # Window name
    cv2.namedWindow(wname)
    npoints = 4 # 座標の数
    pts = PointList(npoints)
    X = []
    # print(type(pts)) # class __main__.PointList()
    cv2.setMouseCallback(wname, onMouse, [wname, img, pts])
    cv2.imshow(wname, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # warped= four_point_transform(img, pts)
    # cv2.imshow("Warped", warped)
    # k = cv2.waitKey(0)
    # if k == 27:
    #     cv2.destroyAllWindows()
    # elif k == ord('s'):
    #     # cv2.imwrite("get", warped)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
