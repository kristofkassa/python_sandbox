from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


def plot_channels(image):
    red = image[:, :, 0]
    green = image[:, :, 1]
    blue = image[:, :, 2]

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3, figsize=(18, 6))

    ax1.imshow(red, cmap="Reds_r")
    ax1.axis(False)
    ax4.hist(red.ravel(), bins=256, color="red")
    ax4.set_ylim([0, 2000])

    ax2.imshow(green, cmap="Greens_r")
    ax2.axis(False)
    ax5.hist(green.ravel(), bins=256, color="green")
    ax5.set_ylim([0, 2000])

    ax3.imshow(blue, cmap="Blues_r")
    ax3.axis(False)
    ax6.hist(blue.ravel(), bins=256, color="blue")
    ax6.set_ylim([0, 2000])


def get_std_mean(image):
    for ii in range(3):
        extracted = image[:, :, ii]
        print(f"channel {ii} - mean: {extracted.mean()}, standard deviation: {extracted.std()}")
        x_normed = (extracted - extracted.mean()) / (extracted.std())
        print(f"mean / std: {x_normed}")


pictures = {
    1: 'http://people.csail.mit.edu/brussell/research/LabelMe/Images/static_animal1200_256x256/B_N802036.jpg',
    2: 'http://people.csail.mit.edu/brussell/research/LabelMe/Images/static_animal1200_256x256/B_N825055.jpg',
    3: 'http://people.csail.mit.edu/brussell/research/LabelMe/Images/static_animal1200_256x256/Mda_archi100.jpg'
}

for i in pictures:
    picture = imread(pictures[i])
    print(f"type: {type(picture)}, size: {picture.size}, shape: {picture.shape}, ndim: {picture.ndim}")
    plot_channels(picture)
    print(f"Picture {i}: ")
    get_std_mean(picture)


# 2


def audio_norm(data):
    max_data = int(np.max(data))
    min_data = int(np.min(data))
    data = (data - min_data) / (max_data - min_data)
    return data - 0.5


drums_file = 'C:/Users/Kristóf/Downloads/drums.wav'
storm_rate, drum_data = wavfile.read(drums_file)
normalized_drum = audio_norm(drum_data)

print(normalized_drum)
