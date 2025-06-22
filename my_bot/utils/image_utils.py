import cv2 as cv


def image_cut(
    file_name_old: str,
    file_name_new: str,
    frames: tuple[tuple[int, int], tuple[int, int]] = ((125,1250), (570, 2220)),
    is_markup: bool = False,
) -> None:
    '''
        Фукнция обрезает изображение по указанным координатам левого верхнего и нежнего правого угла,
        is_markup - режим разметки изображения, выделяет указанную область, не сохраняет новое изображение.((y1,x1)(y2,x2))
        file_name_old - файл источник
        file_name_new - новый обрезанный файл
    '''
    if not file_name_old:
        raise Exception("Необходимо указать название файла источника")

    if not file_name_new:
        raise Exception("Необходимо указать название файла для записи обрезанного изображения")

    file_name_new = file_name_new.strip()
    file_name_old = file_name_old.strip()

    image = cv.imread(file_name_old, cv.COLOR_RGB2BGR)
    cv.namedWindow("image", cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty("image", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    image =cv.resize(image, (3000, 1400))

    if is_markup:
        cv.rectangle(image, (frames[1][0], frames[0][0]), (frames[1][1], frames[0][1]), (0, 0, 255), 5)
        cv.imshow("image", image)
        cv.waitKey(0)
    else:
        new_image = image[frames[0][0]:frames[0][1], frames[1][0]:frames[1][1]]
        cv.imwrite(file_name_new, new_image)
    cv.destroyAllWindows()


if __name__ == '__main__':
    'Для тестирования'
    # image_cut(file_name_old="screenshot.png", file_name_new='new.png', is_markup=False)
    pass