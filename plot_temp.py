import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from astropy.time import Time
import tqdm


times = []
temps = []
with open("temp_log.txt", "r") as fil:
    for line in tqdm.tqdm(fil.readlines()):
        t, temp = line.split(",")
        temp = temp.strip('\n')
        try:
            times.append(Time(t, format='iso').plot_date)
        except:
            continue
        temps.append(float(temp))
times = np.array(times)
temps = np.array(temps)
hot = temps > 80
print("Temperature is above 80C {:.1f}% of the time".format(
    np.sum(hot)/len(temps)*100))


fig = plt.figure(figsize=(10, 6))
ax = fig.gca()
ax.plot_date(times, temps,"o", tz=None,
             xdate=True, ydate=False, drawstyle="steps-post")
ax.set_title("CPU Temperature Over Time")
ax.set_xlabel("Date")
ax.set_ylabel(u"Temperature (\N{DEGREE SIGN}C)")
ax.axhline(80)
fig.savefig("temps.png")

fig2 = plt.figure(figsize=(10, 6))
ax2 = fig2.gca()
ax2.hist(temps, 50, alpha=0.7, rwidth=0.9)
ax2.set(xlabel=u"Temperature (\N{DEGREE SIGN}C)", ylabel="Frequency",
        title="Temperature Histogram")
ax2.axvline(80)
fig2.savefig("temp_hist.png")
