import cv2

pt_start = (-1, -1)
pt_end = (-1, -1)
label_counter = 0


def on_mouse(event, x, y, flags, param):
    global pt_start, pt_end, label_counter
    if event == cv2.EVENT_LBUTTONDOWN:
        pt_start = (x, y)
    if event == cv2.EVENT_LBUTTONUP:
        if abs(x - pt_start[0]) > 5 and abs(y - pt_end[1]) > 5:
            pt_end = (x, y)
            label_counter += 1


def labeling(filename):
    global label_counter
    img = cv2.imread(filename)
    copy_img = img.copy()
    h, w = img.shape[:2]
    cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("test", on_mouse, 0)
    prev_count = label_counter
    labels = []
    while True:
        cv2.imshow("test", img)
        if cv2.waitKey(10) == ord('q'):
            label_counter = 0
            break
        if prev_count != label_counter:
            cv2.rectangle(img, pt_start, pt_end, (0, 0, 255), int(h / 150))
            prev_count = label_counter
            label_pt = list(pt_start)
            width = pt_start[0] - pt_end[0]
            height = pt_start[1] - pt_end[1]
            if width < 0:
                label_pt[0] -= width
                width = -width
            if height < 0:
                label_pt[1] -= height
                height = -height
            print(label_pt, width, height)
            labels.append([tuple(label_pt), width, height])
    print(labels)


if __name__ == "__main__":
    labeling("test2.png")

