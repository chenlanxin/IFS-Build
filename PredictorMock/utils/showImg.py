import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def show_npy_3d(npd_3d, interval=5, cmap='gray', vmin=None, vmax=None, title=None):
    for i in range(0, npd_3d.shape[0], interval):
        npd_2d = np.squeeze(npd_3d[i, ...])
        title_show = '{0}-{1}'.format(title, i)
        show_npy(npd_2d, cmap, vmin, vmax, title_show)

def show_npy(npd_2d, cmap='gray', vmin=None, vmax=None, title=None):
    plt.imshow(npd_2d, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.title(title) 
    plt.axis('off')
    plt.show()

def show_npy_2imgs(npd_2d_1st, npd_2d_2nd, cmap='gray', vmin=None, vmax=None, title=None):
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(npd_2d_1st, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.subplot(1,2,2)
    plt.imshow(npd_2d_2nd, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.show()

def show_curve(y, x=None):
    if not x:
        x = range(len(y))
    plt.plot(x, y)
    plt.show()


def display_rgb():
    file_name = '/Users/chenjiwen/Desktop/8.11-1.png'
    img = mpimg.imread(file_name)
    print(img.shape)
    plt.imshow(img)
    plt.axis('off')
    # plt.show()

    for i in range(4):
        img_1 = img[:,:,i]
        plt.imshow(img_1)
        plt.show()

if __name__ == '__main__':
    # display_rgb()
    y = np.array([2,5,20,18,45,6])
    show_curve(y)
