def convert_box(box, img_w, img_h):
    left = float(box.attrib["left"])
    top = float(box.attrib["top"])
    width = float(box.attrib["width"])
    height = float(box.attrib["height"])

    x_center = (left + width / 2) / img_w
    y_center = (top + height / 2) / img_h
    w = width / img_w
    h = height / img_h

    return x_center, y_center, w, h
