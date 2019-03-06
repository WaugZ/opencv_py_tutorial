import cv2
import numpy as np
import os

pos = (0, 0)
count = 0


def on_mouse(event, x, y, flags, param):
    global count
    global pos
    if event == cv2.EVENT_LBUTTONDOWN:
        pos = (x, y)
        count += 1
    if event == cv2.EVENT_RBUTTONDOWN:
        print()


def distance(pos0, pos1):
    return np.sqrt(np.sum(np.square(np.array(pos0) - np.array(pos1))))


def two_pts2line(pt0, pt1):
    # according to formula: ax + by + c = 0 passes (x0, y0) and (x1, y1)
    # then a = y0 - y1, b = x1 - x0, c = x0y1 - x1y0
    a = pt0[1] - pt1[1]
    b = pt1[0] - pt0[0]
    c = pt0[0] * pt1[1] - pt1[0] * pt0[1]
    return a, b, c


def tow_pts2perpendicular(pt0, pt1):
    # according to formula y = -(x0 - x1) / (y0 - y1) x + c passes ((x0 + x1) / 2, (y0 + y1) / 2)
    # c = ... then the line is (x0 - x1)x + (y0 - y1)y + (y0 ** 2 - y1 ** 2 + x0 ** 2 - x1 ** 2) / 2 = 0
    a = pt0[0] - pt1[0]
    b = pt0[1] - pt1[1]
    c = 1. * (pt0[1] ** 2 - pt1[1] ** 2 + pt0[0] ** 2 - pt1[0] ** 2) / 2
    return a, b, c


def intersection(line0, line1):
    """
    :param line0: tuple(a0, b0, c0) for line a0x + b0y + c0 =0
    :param line1: tuple(a1, b1, c1) for line a1x + b1y + c1 =0
    :return: (x, y) the intersection of this two lines
    """
    # according to formula a0x + b0y + c0 =0 == a1x + b1y + c1 =0
    # then we have x = (b0c1 - b1c0) / (a0b1 - a1b0), y = (a1c0 - a0c1) / (a0b1 - a1b0)
    d = line0[0] * line1[1] - line1[0] * line0[1]
    if d == 0:
        raise Exception("two lines are the same.")
    else:
        x = (line0[1] * line1[2] - line1[1] * line0[2]) / d
        y = (line1[0] * line0[2] - line0[0] * line1[2]) / d
        return x, y


def show_img(img):
    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.imshow("result", img)
    cv2.waitKey(3000)


def write_img(img, path="/"):
    cv2.imwrite(path + "result.jpg", img)


def perspective_with_pts_selected(filename):
    img = cv2.imread(filename)
    h, w = img.shape[:2]
    # img = cv2.resize(img, (int(w / 2), int(h / 2)))
    # h, w = img.shape[:2]
    copy_img = img.copy()
    cv2.namedWindow(filename, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(filename, on_mouse, 0)
    global count
    pre_count = count
    src_rect = []
    while count < 4:
        cv2.imshow(filename, img)
        cv2.waitKey(1)
        if pre_count != count:
            print(pos)
            cv2.circle(img, pos, int(h / 150), (0, 0, 255), int(h / 150))
            src_rect.append(pos)
            pre_count = count
    count = 0

    tmp = src_rect.copy()
    # make sure src_rect made by lefttop, righttop, leftbottom, rightbottom.
    # calculate the pts in up, down, left, right of this pt, to make sure where this point is in
    check = [False] * 4
    for pt in tmp:
        up_count = 0
        down_count = 0
        left_count = 0
        right_count = 0
        for other_pt in tmp:
            if other_pt is pt:
                continue
            if other_pt[0] > pt[0]:
                right_count += 1
            elif other_pt[0] < pt[0]:
                left_count += 1
            if other_pt[1] > pt[1]:
                down_count += 1
            elif other_pt[1] < pt[1]:
                up_count += 1

        if right_count > left_count and down_count > up_count:
            src_rect[0] = pt
            check[0] = True
        elif right_count < left_count and down_count > up_count:
            src_rect[1] = pt
            check[1] = True
        elif right_count > left_count and down_count < up_count:
            src_rect[2] = pt
            check[2] = True
        elif right_count < left_count and down_count < up_count:
            src_rect[3] = pt
            check[3] = True
        else:
            raise Exception("you make a bug.")

    dst_w = distance(src_rect[0], src_rect[1])
    dst_h = distance(src_rect[0], src_rect[2])
    max_width = w - src_rect[0][0]
    max_height = h - src_rect[0][1]
    if dst_w > max_width:
        dst_w = max_width
    if dst_h > max_height:
        dst_h = max_height
    lefttop_x, lefttop_y = src_rect[0]
    dst_rect = [(lefttop_x, lefttop_y), (lefttop_x + dst_w, lefttop_y),
                (lefttop_x, lefttop_y + dst_h), (lefttop_x + dst_w, lefttop_y + dst_h)]

    print(src_rect)
    print(dst_rect)

    if False in check:
        raise Exception("did not solve this situation, maybe there are 2 pts in the same height(or width)")

    trans_m = cv2.getPerspectiveTransform(np.float32(src_rect), np.float32(dst_rect))
    dst_img = cv2.warpPerspective(copy_img, trans_m, (w, h))

    show_img(dst_img)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # img = cv2.imread("C:\\Users\\38345\\Desktop\\map.jpg")
    # for _, _, fs in os.walk('.'):
    #     for f in fs:
    #         if f.endswith(".jpg") or f.endswith(".png"):
    #             perspective_with_pts_selected(f)
    # perspective_with_pts_selected("C:\\Users\\38345\\Desktop\\map.jpg")
    perspective_with_pts_selected("test2.png")

