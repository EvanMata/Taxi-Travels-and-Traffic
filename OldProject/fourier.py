import numpy as np
import matplotlib.pyplot as plt

def gen_data(period, size):
    #Generates data where there are very discrete peaks.
    #This matches the pattern's we're expecting.
    print("Size: {0},  Input Period: {1},  Size/Period: {2}" \
      .format(size, period, float(size)/period))
    x = []
    for i in range(size):
        if i % period == 0:
            x.append(10)
        else:
            x.append(0)
    return x

def fft_info(in_lst):
    #Get our period and coeefficient information.
    modes = np.fft.rfft(in_lst)
    freqs = np.fft.rfftfreq(len(in_lst))
    freqs = list(freqs)
    freqs.remove(0)
    freqs = np.array(freqs)
    freqs = freqs
    modes = modes.real
    periods = 1.0/freqs
    info = zip(modes, periods)
    return info

def clean_fft(info, period, size):
    #Clear our data - we want only real periods,
    #We also only want periods that correspond to full days.
    #Finally, we only care about relatively large info.
    d = {}
    for item in info:
        coef = item[0].real
        coef = period * coef / size
        period = round(item[1])
        if period not in d:
            d[period] = coef
        else:
            d[period] += coef

    for key, value in d.items():
        d[key] = round(value, 2)
        if d[key] > 0.5:
            if size / key > 1:
                print("Period: {0}  Coef: {1}".format(key, value))

def graph_it(data):
    #Graph a set of data.
    xs = range(len(data))
    plt.plot(xs[0:100], data[0:100])
    plt.show()

def sin_per(period):
    #Generate the y values for the sin of a given period.
    xs = np.linspace(0, 100, 10001)
    ys = np.sin(2*np.pi*xs/period)
    #plt.plot(xs, ys)
    #plt.show()
    return ys

def first_test(coefs, periods):
    #Make sure we can actually sum sin's correctly.
    xs = np.linspace(0, 100, 10001)
    total_coefs = [0.0]*10001 #B.c. 10001 xs.
    total_coefs = np.array(total_coefs)
    for i in range(len(coefs)):
        period = periods[i]
        amplitude = coefs[i]
        ys = sin_per(period)
        ys = ys*amplitude
        total_coefs += ys
    plt.plot(xs, total_coefs)
    plt.show()            

def test_it(info, period, size):
    #Make sure our fourier analysis does well replicate our input data.
    periods = []
    amplitudes = []
    for i in range(len(info)):
        per = 2*info[i][0] #Normalize things
        amp = info[i][1]*1.0/size #Normalize things
        periods.append(per)
        amplitudes.append(amp)
    first_test(amplitudes, periods)
            
period = 10
#size = 2*3*4*5*6*7*8
size = 365
a = gen_data(period, size)
b = fft_info(a)
#print(b)
c = clean_fft(b, period, size)

e = test_it(b, period, size)





        
