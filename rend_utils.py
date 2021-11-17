#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os
import re

from fluidfoam import readmesh
from fluidfoam import readvector

def plot_contour(x,y,quant,n=12,show = False,filled=True,fname=''):
    '''
    Makes contour plots of different quantities.
    '''
    plt.figure()
    levels = np.linspace(np.min(quant), np.max(quant), n)
    if filled:
        plt.contourf(x[:, :, nz//2], y[:, :, nz//2], quant,
                 levels=levels)
    else:
        plt.contour(x[:, :, nz//2], y[:, :, nz//2], quant,
                 levels=levels)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    if fname:
        plt.savefig(fname)
    if show:
        plt.show()
    plt.close()

def plot_velVect(x,y,n=10,fname=''):
    '''
    Plots the velocity vectors
    '''
    levels = n
    plt.figure()
    plt.contourf(x[:, :, nz//2], y[:, :, nz//2], vel[1, :, :, nz//2],
                 levels=levels)
    # Setting axis labels
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')

    plt.quiver(x[:, :, nz//2], y[:, :, nz//2],vel[0, :, :, nz//2], vel[1, :, :, nz//2])
    if fname:
        plt.savefig(fname)
    plt.show()
    plt.close()

def gif_maker(gfname,levels_n=10,im_show=False):
    '''
    Makes a .gif file to allow for better understanding of the time-evolution.
    '''
    filenames = []
    for fname in os.listdir(sol):
        if re.search(r'^[0-9]+[.0-9]+$',fname) is not None:
            filenames.append(float(fname))
        elif re.search(r'^[0-9]+$',fname) is not None:
            filenames.append(int(fname)) 
    filenames.sort()
    png_fnames = []
    for i,fname in enumerate(filenames[1:]):
        timename = str(fname)
        vel = readvector(sol, timename, 'U', True)

        vel_x = vel[0, :, :, nz//2]
        vel_y = vel[1, :, :, nz//2]
        vel_z = vel[2, :, :, nz//2]
        vel_magn = np.sqrt(np.power(vel_x,2) + np.power(vel_y,2) + \
                       np.power(vel_z,2))
        png_fname = f'{i}.png'
        plot_contour(x,y,vel_magn,n=levels_n,filled=True,show=im_show,fname=png_fname)
        png_fnames.append(png_fname)

    with imageio.get_writer(gfname+'.gif', mode='I') as writer:
        for filename in png_fnames:
            image = imageio.imread(filename)
            writer.append_data(image)
    # Remove files
    for filename in png_fnames:
        print(filename)
        os.remove(filename)

# Testing...
if __name__ == '__main__':
    # full path of the simulation results - change this to the location where your results are
    sol = '/home/fotis/OpenFOAM/fotis-v2106/run/tutorials/incompressible/icoFoam/cavity/cavityHighRe/'
    # set a particular time step, just for comparison
    timename = '1.5'
    # Load grid data
    x, y, z = readmesh(sol, True)
    nx, ny, nz = x.shape
    print("Nx = ", nx, "Ny = ", ny, "Nz = ", nz)
    # Load results for the velocity
    vel = readvector(sol, timename, 'U', True)
    vel_x = vel[0, :, :, nz//2]
    vel_y = vel[1, :, :, nz//2]
    vel_z = vel[2, :, :, nz//2]
    vel_magn = np.sqrt(np.power(vel[0, :, :, nz//2],2) + np.power(vel[1, :, :, nz//2],2) + \
                   np.power(vel[2, :, :, nz//2],2))
    plot_contour(x,y,vel_magn,show=True)
    plot_contour(x,y,vel_x,show=True)
    plot_contour(x,y,vel_y,show=True)