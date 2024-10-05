import time
import zhinst.core

import os, sys 
from sys import exit

import numpy as np 
import matplotlib.pyplot as plt 
from scipy.ndimage import gaussian_filter1d
import matplotlib as mpl 

import uhfli_setup 


file = ""





def smooth_sweep(f, new_f, amplitude) -> np.array:
    amplitude = np.interp(new_f, f, amplitude)
    return gaussian_filter1d(amplitude, 30)




def calculate_global_minimum(freq, amplitude) -> float:
    minimumIndex = np.abs(amplitude - np.min(amplitude)).argmin()
    return freq[minimumIndex]





def main():
    global file 

    # set important parameters 
    NUMBER_OF_POINTS = 120
    START = 2_168_000 # Hz
    STOP = 2_180_000 # Hz
    number_of_data_history = 80
    daq, scope, daq_module, sweeper, awg = uhfli_setup.set_uhfli_tabs_and_settings(START, STOP, NUMBER_OF_POINTS)

    
    anti_resonance_history_list = np.array([])
    time_array = np.array([])


    
    

    GENERAL_START_TIME = time.time()
    localtime = time.localtime(GENERAL_START_TIME)
    date_time = f"{localtime.tm_year}{localtime.tm_mon}{localtime.tm_mday}_{localtime.tm_hour}_{localtime.tm_min}_{localtime.tm_sec}"

    file = open(f"data\\real-time-code-exports\\Real-time-UHFLI-data-{date_time}.txt", "w")
    file.write("Time(s);Anti-res-freq(MHz)\n")

    reference_is_set = False
    sweep_counter = 0
    
    while True:

        sweep_counter += 1
        print(f"Performing sweep #{sweep_counter}...", end="\r")


        sweeper.execute()
        start = time.time()
        while not sweeper.finished():  # Wait until the sweep is complete, with timeout of 30s.
            progress = sweeper.progress()

            if (time.time() - start) > 30:
                # If for some reason the sweep is blocking, force the end of the measurement.
                print("\nSweep still not finished, forcing finish...")
                sweeper.finish()

        data = sweeper.read(True)

        sample = data['/dev2566/demods/0/sample'][0][0]
        f = sample["frequency"]/1e6 # in MHz
        r = sample["r"]*1e3 # in mV

        new_f = np.linspace(f[0], f[-1], f.size*10)
        smooth_r = smooth_sweep(f, new_f, r) # gaussian filtered 
        anti_res = calculate_global_minimum(new_f, smooth_r) # antires frequency in MHz

        time_array = np.append(time_array, time.time() - GENERAL_START_TIME)
        anti_resonance_history_list = np.append(anti_resonance_history_list, anti_res)
        if sweep_counter >= 2:
            anti_resonance_history_list[-1] = np.mean(anti_resonance_history_list[-2:])


        if len(time_array) > number_of_data_history:
            time_array = time_array[-1*number_of_data_history:]
            anti_resonance_history_list = anti_resonance_history_list[-1*number_of_data_history:]

        file.write(f"{time_array[-1]:.3f};{anti_resonance_history_list[-1]:.6f}\n")


        if sweep_counter == 1: # create plots

            reference = anti_res

            fig, ax = plt.subplots()
            line, = ax.plot(new_f,smooth_r, lw=2, color="black")
            line_raw, = ax.plot(f,r, lw=2, color="orange")
            ax.set_title("Pulse-echo Sweep")
            ax.set_xlabel("Frequency (MHz)"); ax.set_ylabel("Amplitude (mV)")
            ax.set_xlim([START/1e6, STOP/1e6])
            ax.set_ylim([np.min(smooth_r), np.max(smooth_r)])

            fig2, ax2 = plt.subplots()
            line2, = ax2.plot(time_array, reference - anti_resonance_history_list, lw=2, color="blue",\
                marker="o", markersize=5)
            ax2.set_title("Anti-resonance Frequency")
            ax2.set_xlabel("Time (s)"); ax2.set_ylabel("Frequency (MHz)")
            ax2.grid()
            first_sweep = False
            plt.show(block=False)

        else: # update plots
            line.set_ydata(smooth_r)
            line_raw.set_ydata(r)

            if (not reference_is_set) and (sweep_counter >= 10):
                reference_is_set = True
                reference = np.mean(anti_resonance_history_list[:10])


            line2.set_xdata(time_array)
            line2.set_ydata(reference - anti_resonance_history_list)
            ax2.set_xlim([np.min(time_array), np.max(time_array)*1.01])
            ax2.set_ylim([-0.001, 0.004])

            fig.canvas.draw()
            fig2.canvas.draw()

            fig.canvas.flush_events()
            fig2.canvas.flush_events()


        



if __name__ == '__main__':
    os.system("cls") if "win" in sys.platform else os.system("clear")

    if not os.path.exists(".\\data"):
        os.mkdir(".\\data")

    if not os.path.exists(".\\data\\real-time-code-exports"):
        os.mkdir(".\\data\\real-time-code-exports")



    plt.style.use('fast')
    mpl.rcParams["font.size"] = 14
    mpl.rcParams["font.family"] = "Arial"
    mpl.rcParams["axes.labelweight"] = "bold"

    try: 
        main()
    except KeyboardInterrupt:
        file.close()
        print("Exiting the program...")




