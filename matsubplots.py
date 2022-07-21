import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import Grid, ImageGrid


def axesgrid(shape=1, size=3, pad=0, close=False, image_grid=False, return_grid=False, **kwargs):
    """Extend mpl_toolkits.axes_grid1.Grid."""
    if np.isscalar(shape):
        shape = shape, 1
    if np.isscalar(size):
        size = np.repeat(size, 2)
    if np.isscalar(pad):
        pad = np.repeat(pad, 2)
    xticks = kwargs.pop('xticks', None)
    yticks = kwargs.pop('yticks', None)
    frameon = kwargs.pop('frameon', None)
    if image_grid:
        kwargs.setdefault('cbar_pad', pad[0])
        kwargs.setdefault('cbar_size', size[0] * 0.1)
        if kwargs.get('cbar_mode') == 'each':
            size = size[0] + kwargs.get('cbar_pad') + kwargs.get('cbar_size'), size[1]
    figsize = [size[x] * shape[x] + pad[x] * (shape[x] + 1) for x in range(2)]
    if image_grid:
        if kwargs.get('cbar_mode') in ('edge', 'single'):
            figsize = figsize[0] + kwargs.get('cbar_pad') + kwargs.get('cbar_size'), figsize[1]
    fig = plt.figure(figsize=figsize)
    if close:
        plt.close(fig)
    padr = [pad[x] / figsize[x] for x in range(2)]
    rect = padr[0], padr[1], 1 - padr[0] * 2, 1 - padr[1] * 2
    grid = (ImageGrid if image_grid else Grid)(fig, rect, shape[::-1], axes_pad=pad, **kwargs)
    axs = np.asarray(grid.axes_row)
    for ax in axs.ravel():
        if xticks is not None:
            ax.set_xticks(xticks)
        if yticks is not None:
            ax.set_yticks(yticks)
        if frameon is not None:
            ax.set_frame_on(frameon)
    returned = fig, axs
    if return_grid:
        returned += grid,
    return returned


def imagegrid(*args, **kwargs):
    """Extend mpl_toolkits.axes_grid1.ImageGrid."""
    kwargs['image_grid'] = True
    kwargs.setdefault('aspect', False)
    return axesgrid(*args, **kwargs)


def subplots(shape=1, size=3, pad=0, close=False, label_mode='L', **kwargs):
    """Extend matplotlib.pyplot.subplots."""
    if np.isscalar(shape):
        shape = shape, 1
    if np.isscalar(size):
        size = np.repeat(size, 2)
    if np.isscalar(pad):
        pad = np.repeat(pad, 2)
    figsize = [size[x] * shape[x] + pad[x] * (shape[x] + 1) for x in range(2)]
    fig = plt.figure(figsize=figsize)
    if close:
        plt.close(fig)
    axs = np.empty(shape[::-1], dtype=np.object)
    for i in range(shape[0]):
        for j in range(shape[1]):
            offset = [pad[x] + (i,j)[x] * (size[x] + pad[x]) for x in range(2)]
            axs[j,i] = _add_axes_inches(fig, size, offset, origin='top left', **kwargs)
    if label_mode == 'L':
        for ax in axs[:-1,:].ravel():
            ax.set_xticklabels(())
        for ax in axs[:,1:].ravel():
            ax.set_yticklabels(())
    else:
        raise NotImplementedError(label_mode)
    return fig, axs


def _add_axes_inches(fig, size, offset=0, origin='middle center', **kwargs):
    figsize = fig.get_size_inches()
    if np.isscalar(size):
        size = np.repeat(size, 2)
    elif len(size) != 2:
        raise NotImplementedError(size)
    if np.isscalar(offset):
        offset = np.repeat(offset, 2)
    elif len(offset) != 2:
        raise NotImplementedError(offset)
    origin = origin.split()
    if len(origin) != 2:
        raise NotImplementedError(origin)
    if origin[1] == 'left':
        left = offset[0]
    elif origin[1] == 'right':
        left = figsize[0] - size[0] - offset[0]
    elif origin[1] == 'center':
        left = (figsize[0] - size[0]) / 2 + offset[0]
    else:
        raise NotImplementedError(origin[1])
    if origin[0] == 'bottom':
        bottom = offset[1]
    elif origin[0] == 'top':
        bottom = figsize[1] - size[1] - offset[1]
    elif origin[0] == 'middle':
        bottom = (figsize[1] - size[1]) / 2 + offset[1]
    else:
        raise NotImplementedError(origin[0])
    width, height = size
    left /= figsize[0]
    bottom /= figsize[1]
    width /= figsize[0]
    height /= figsize[1]
    return fig.add_axes((left, bottom, width, height), **kwargs)
