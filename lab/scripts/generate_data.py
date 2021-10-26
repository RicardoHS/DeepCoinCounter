import os
from os import walk
from typing import Dict

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

import config


def load_random_background(background_folder, base_ratio, mobile_camera_ratio=1.6624):
    # mobile_camera_ratio: 2048 x 1232
    # load background
    # get files
    filenames = next(walk(background_folder), (None, None, []))[2]  # [] if no file
    filename = np.random.choice(filenames)
    back = Image.open(background_folder + filename)

    # compute crop ratios
    back_w, back_h = back.size
    if back_w >= back_h:
        camera_w = base_ratio * mobile_camera_ratio
        camera_h = base_ratio
    else:
        camera_w = base_ratio
        camera_h = base_ratio * mobile_camera_ratio

    # compute crop dimensions
    left = np.random.randint(back_w - camera_w)
    top = np.random.randint(back_h - camera_h)
    right = camera_w + left
    bottom = camera_h + top

    # Crop image
    crop = back.crop((left, top, right, bottom))

    return crop


def compute_area(rectangle):
    dw = rectangle[2] - rectangle[0]
    dh = rectangle[3] - rectangle[1]
    return dw * dh


def compute_overlap_percentage(pos1, pos2):
    left = max(pos1[0], pos2[0])
    top = max(pos1[1], pos2[1])
    right = min(pos1[2], pos2[2])
    bottom = min(pos1[3], pos2[3])
    pos3 = (left, top, right, bottom)

    dw = right - left
    dh = bottom - top
    if (dw >= 0) and (dh >= 0):
        pos1_area = compute_area(pos1)
        pos2_area = compute_area(pos2)
        pos3_area = compute_area(pos3)
        min_area = min(pos1_area, pos2_area)
        return pos3_area / min_area
    else:
        return 0.0


def paste_random_coin(
    background, coin_img, coin_positions=None, max_coin_overlap_percentage=0.1
):
    background_copy = background.copy()
    # get background size
    back_w, back_h = background.size

    # get coin random position
    coin_w, coin_h = coin_img.size
    coin_pos_w = np.random.randint(back_w - coin_w)
    coin_pos_h = np.random.randint(back_h - coin_h)
    coin_pos = (coin_pos_w, coin_pos_h, coin_pos_w + coin_w, coin_pos_h + coin_h)

    if coin_positions:
        for old_coin_pos in coin_positions:
            overlap_percentage = compute_overlap_percentage(coin_pos, old_coin_pos[0])
            if overlap_percentage >= max_coin_overlap_percentage:
                return background_copy, None

    # get coin circle mask
    coin_mask = Image.new("L", coin_img.size, 0)
    draw = ImageDraw.Draw(coin_mask)
    draw.ellipse((0, 0, coin_w, coin_h), fill=255)
    coin_mask.filter(ImageFilter.GaussianBlur(10))

    # random rotate coin imgage
    coin_img = coin_img.rotate(np.random.randint(360))

    # paste coin into background
    background_copy.paste(coin_img, (coin_pos_w, coin_pos_h), coin_mask)

    return background_copy, coin_pos


def draw_bounding(image, pos, text=None):
    image_copy = image.copy()
    draw = ImageDraw.Draw(image_copy)
    draw.rectangle(pos, outline="red")

    if text:
        fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
        draw.text((pos[0], pos[1]), text, font=fnt, fill="red")

    return image_copy


def get_front_coins():
    eur_front = Image.open("../data/coins_raw/euro_front.png")

    coin_pos_dict = {
        "f_1cent": ((30, 30, 205, 207), 0.01),
        "f_2cent": ((340, 30, 540, 230), 0.02),
        "f_5cent": ((661, 30, 890, 259), 0.05),
        "f_10cent": ((9, 324, 229, 539), 0.1),
        "f_20cent": ((320, 312, 564, 551), 0.2),
        "f_50cent": ((641, 300, 909, 563), 0.5),
        "f_1eur": ((161, 593, 414, 846), 1),
        "f_2eur": ((481, 582, 757, 859), 2),
    }

    coin_img_dict = {}
    for name, (pos, value) in coin_pos_dict.items():
        coin_img_dict[name] = (eur_front.crop(pos), value)

    return coin_img_dict


def get_back_coins():
    # TODO: add back coins
    return {}


def get_coins():
    coin_dict = {**get_front_coins(), **get_back_coins()}
    return coin_dict


def crop_coins(background, coin_positions, crop_noise):
    back_w, back_h = background.size
    coins = []
    for pos, value in coin_positions:
        noised_pos = np.random.uniform(-crop_noise, crop_noise, 4) * pos
        pos = pos + noised_pos
        pos = (max(0, pos[0]), max(0, pos[1]), min(back_w, pos[2]), min(back_h, pos[3]))
        coins.append((background.crop(pos), value))
    return coins


def generate_image(coins_dict, n_coins):
    back_img = load_random_background(
        background_folder=config.DATA_BACKGROUND_FOLDER,
        base_ratio=config.BACKGROUND_RESIZE_RATIO,
    )

    coin_resize_base = min(
        max(config.COIN_RESIZE_RATIO_MIN, np.random.rand()),
        config.COIN_RESIZE_RATIO_MAX,
    )

    coins = np.empty(len(coins_dict), dtype=object)
    coins[:] = list(coins_dict.values())

    coin_positions = []
    for coin, value in np.random.choice(coins, size=n_coins):
        coin_w, coin_h = coin.size
        coin = coin.resize(
            (int(coin_w * coin_resize_base), int(coin_h * coin_resize_base)),
            resample=Image.LANCZOS,
        )
        back_img, coin_pos = paste_random_coin(
            back_img,
            coin,
            coin_positions=coin_positions,
            max_coin_overlap_percentage=config.MAX_COIN_OVERLAP_PERCENTAGE,
        )
        if coin_pos:
            coin_positions.append([coin_pos, value])

    return back_img, coin_positions


def crop_all_coins(images):
    all_coins = []
    for img, positions in images:
        coins = crop_coins(img, positions, crop_noise=config.INDIVIDUAL_COIN_CROP_NOISE)
        all_coins.extend(coins)
    return all_coins


def generate_all(n_images):
    coin_dict = get_coins()

    images = []
    for i in range(n_images):
        img, positions = generate_image(
            coin_dict, n_coins=config.BACKGROUND_MAX_N_COINS
        )
        images.append([img, positions])

    return images


def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_relative_positions(image, positions):
    """
    Get the relative value of the positions when
    max image width and height equal 1.
    """
    img_w, img_h = image.size
    positions = np.array(positions, dtype=float)
    positions[0] = positions[0] / img_w
    positions[1] = positions[1] / img_h
    positions[2] = positions[2] / img_w
    positions[3] = positions[3] / img_h
    return positions


def save_full_images(images, folder_path):
    create_folder_if_not_exists(folder_path)

    with open(folder_path + "positions.csv", "w") as f:
        f.write("")

    for i, (img, positions) in enumerate(images):
        img_type = np.random.choice(["TRAIN", "VALIDATION", "TEST"], p=[0.8, 0.1, 0.1])
        path = folder_path + "image_{}.jpeg".format(i)
        img.save(path, "JPEG")
        with open(folder_path + "positions.csv", "a") as f:
            for pos, value in positions:
                relative_pos = get_relative_positions(img, pos)
                f.write(
                    f"{img_type},{path},{str(value)}"
                    + ",{},{},,,{},{},,\n".format(*relative_pos)
                )


def save_all_coins(coins, folder_path):
    create_folder_if_not_exists(folder_path)

    for i, (img, value) in enumerate(coins):
        coin_path = folder_path + str(value)
        create_folder_if_not_exists(coin_path)
        try:
            img.save(coin_path + f"/coin_{i}.jpeg", "JPEG")
        except SystemError:
            print(f"INFO: Saving coin_{i} ({value}) failed.")
            os.remove(coin_path + f"/coin_{i}.jpeg")


def main():
    n_images = config.IMAGES_TO_GENERATE
    print(f"Generating full images. ({n_images})")
    images = generate_all(n_images=n_images)
    print("Saving full images.")
    save_full_images(images, folder_path=config.DATA_GENERATED_FOLDER + "full_images/")
    print("Cropping coins.")
    all_coins = crop_all_coins(images)
    print("Saving individual coins.")
    save_all_coins(all_coins, folder_path=config.DATA_GENERATED_FOLDER + "coins/")
    print("Done.")


if __name__ == "__main__":
    main()
