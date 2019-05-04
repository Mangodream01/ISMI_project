import matplotlib.pyplot as plt
import numpy as np

def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)

def multi_slice_viewer(volume, view='axial',
                        overlay_1=None, overlay_1_cmap='RdYlGn', overlay_1_alpha=0.5, overlay_1_thres=0.5,
                        overlay_2=None, overlay_2_cmap='Wistia', overlay_2_alpha=0.5, overlay_2_thres=0.5,
                        title=''):

    assert view in ['axial', 'sagittal', 'coronal']
    remove_keymap_conflicts({'j', 'k'})

    # change view
    rotation = None
    if view == 'axial':
        rotation = lambda img : img.copy()
    elif view == 'sagittal':
        rotation = lambda img : np.rot90(np.rot90(img.copy(), axes=(0,2)), axes=(1,2))
    elif view == 'coronal':
        rotation = lambda img : np.rot90(img.copy(), axes=(1,0))

    fig, ax = plt.subplots()
    plt.xticks([], [])
    plt.yticks([], [])
    ax.volume = rotation(volume)
    ax.index = ax.volume.shape[0] // 2
    ax.imshow(ax.volume[ax.index], cmap='gray', vmin=np.min(ax.volume), vmax=np.max(ax.volume), interpolation='bilinear')
    if overlay_1 is not None:
        ax.volume_2 = np.ma.masked_where(rotation(overlay_1) < overlay_1_thres, rotation(overlay_1))
        ax.imshow(ax.volume_2[ax.index], vmin=np.min(ax.volume_2) , vmax=np.max(ax.volume_2), cmap=overlay_1_cmap, alpha=overlay_1_alpha)
    if overlay_2 is not None:
        ax.volume_3 = np.ma.masked_where(rotation(overlay_2) < overlay_2_thres, rotation(overlay_2))
        ax.imshow(ax.volume_3[ax.index], vmin=np.min(ax.volume_3) , vmax=np.max(ax.volume_3), cmap=overlay_2_cmap, alpha=overlay_2_alpha)
    plt.title(title)
    plt.xlabel(ax.index)
    fig.canvas.mpl_connect('key_press_event', process_key)
    fig.canvas.mpl_connect('scroll_event', process_scroll)

def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'j':
        previous_slice(ax)
    elif event.key == 'k':
        next_slice(ax)
    fig.canvas.draw()

def process_scroll(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.button == 'down':
        previous_slice(ax)
    elif event.button == 'up':
        next_slice(ax)
    fig.canvas.draw()

def previous_slice(ax):
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[0]  # wrap around using %
    plt.xlabel(ax.index)
    ax.images[0].set_array(volume[ax.index])
    if ax.volume_2 is not None:
        volume_2 = ax.volume_2
        ax.images[1].set_array(volume_2[ax.index])
    if ax.volume_3 is not None:
        volume_3 = ax.volume_3
        ax.images[2].set_array(volume_3[ax.index])

def next_slice(ax):
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[0]
    plt.xlabel(ax.index)
    ax.images[0].set_array(volume[ax.index])
    if ax.volume_2 is not None:
        volume_2 = ax.volume_2
        ax.images[1].set_array(volume_2[ax.index])
    if ax.volume_3 is not None:
        volume_3 = ax.volume_3
        ax.images[2].set_array(volume_3[ax.index])
