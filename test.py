import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
import matplotlib
from shutil import copyfile

data_temp = np.loadtxt("temp.dat").T
data_temp[13] /= 1e2

data_sun = np.loadtxt("sun.dat").T

data_sun[1] = np.convolve(data_sun[1], np.ones((11,))/11, mode='same')


data_co2 = np.loadtxt("co2.dat").T
data_ice = np.loadtxt("ice.dat").T

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

plt.xkcd()

fig, host = plt.subplots()
fig.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

# placed on the right by twinx above.
par2.spines["right"].set_position(("axes", 1.2))
# Having been created by twinx, par2 has its frame off, so the line of its
# detached spine is invisible.  First, activate the frame but make the patch
# and spines invisible.
make_patch_spines_invisible(par2)
# Second, show the right spine.
par2.spines["right"].set_visible(True)

p1 = host.plot(data_temp[0], data_temp[13], color="tab:blue", label="Temperatura")
p2 = par1.plot(data_co2[0], data_co2[1], color="tab:red", label="CO2 (Manua Loa)")
p2b = par1.plot(data_ice[0], data_ice[1], color="tab:green", label="CO2 (Ghiacci)")
p3 = par2.plot(data_sun[0], data_sun[1], color="tab:orange", label="Macchie Solari")



host.yaxis.label.set_color(p1[0].get_color())
par1.yaxis.label.set_color(p2[0].get_color())
par2.yaxis.label.set_color(p3[0].get_color())

tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors=p1[0].get_color(), **tkw)
par1.tick_params(axis='y', colors=p2[0].get_color(), **tkw)
par2.tick_params(axis='y', colors=p3[0].get_color(), **tkw)
host.tick_params(axis='x', **tkw)

host.set_ylabel("Anomalia termica / °C")
par1.set_ylabel("Concentrazione CO$_2$ / ppm", rotation=-90, labelpad=20)
par2.set_ylabel("Numero di macchie solari", fontsize=10, rotation=-90)

par2.set_ylim(top=5e2)
par2.spines['right'].set_bounds(0, 200)
par2.set_yticks([0, 5e1, 1e2, 1.5e2, 2e2])
par2.yaxis.set_label_coords(1.36, .2)

#host.spines['top'].set_visible(False)
#par1.spines['top'].set_visible(False)
#par2.spines['top'].set_visible(False)

lns = p1 + p2 + p2b + p3
labs = [l.get_label() for l in lns]
plt.legend(lns, labs, loc="upper left", fontsize=9, ncol=2)

plt.xlim(1950, 2020)

plt.savefig("plot.svg")
