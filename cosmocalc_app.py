# -*- coding: utf-8 -*-
from __future__ import division

import numpy as np
from Tkinter import *
import ttk
from scipy.constants import *
import scipy.integrate as spint

# ========== CONSTANTS ========== # DO NOT CHANGE!
mpc = 1e6 * parsec/1e3 # Mpc to km conversion
H_0 = 69.6
omega_m0 = 0.286
omega_r0 = 8.24e-5
omega_lam0 = 0.714

# calculates age at a given scale factor based on FRW metric
# needs to be multiplied by Mpc * 1e-9 /(seconds_per_year) to convert to time to Gyr
# calculates proper distance at a given scale factor based on FRW metric
# returns distance in Mpc

def calculate_dist_time(*args):

    try:
        z = float(redshift_entry.get())
        scale_factor = 1 / (1 + z)
        f = lambda a: 1/(a*H_0*np.sqrt((omega_m0/a**3) + (omega_r0/a**4) + omega_lam0 + \
                                       ((1 - omega_m0 - omega_r0 - omega_lam0)/a**2)))
        time_bb.set(spint.quadrature(f, 0.0, scale_factor)[0] * mpc * 1e-9 / year)
        p = lambda a: 1/(a*a*H_0*np.sqrt((omega_m0/a**3) + (omega_r0/a**4) + omega_lam0 + \
                                         ((1 - omega_m0 - omega_r0 - omega_lam0)/a**2)))
        dp = spint.quadrature(p, scale_factor, 1.0)[0] * 1e-3 * c
        prop_dist.set(dp)
        lum_dist.set((1+z) * dp)
        
    except ValueError:
        pass

if __name__ == '__main__':

    # Create GUI window
    root = Tk()
    root.title("Cosmology Calculator")

    mainframe = ttk.Frame(root, padding="10 10 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    redshift = StringVar()
    prop_dist = StringVar()
    time_bb = StringVar()
    lum_dist = StringVar()

    redshift_entry = ttk.Entry(mainframe, width=5, textvariable=redshift)
    redshift_entry.grid(column=2, row=1, sticky=(W, E))

    ttk.Label(mainframe, textvariable=prop_dist).grid(column=2, row=2, sticky=(W, E))
    ttk.Label(mainframe, textvariable=time_bb).grid(column=2, row=3, sticky=(W, E))
    ttk.Label(mainframe, textvariable=lum_dist).grid(column=2, row=4, sticky=(W, E))
    ttk.Button(mainframe, text = "Calculate", command=calculate_dist_time).grid(column=2, row=5, sticky=W)

    ttk.Label(mainframe, text = "Redshift ").grid(column=1, row=1, sticky=E)
    ttk.Label(mainframe, text = "Proper distance to redshift ").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text = "Mpc").grid(column=3, row=2, sticky=W)
    ttk.Label(mainframe, text = "Time after the Big Bang ").grid(column=1, row=3, sticky=E)
    ttk.Label(mainframe, text = "Gyr").grid(column=3, row=3, sticky=W)
    ttk.Label(mainframe, text = "Luminosity distance to redshift ").grid(column=1, row=4, sticky=E)
    ttk.Label(mainframe, text = "Mpc").grid(column=3, row=4, sticky=W)

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    redshift_entry.focus()
    root.bind('<Return>', calculate_dist_time)

    root.mainloop()

    sys.exit(0)