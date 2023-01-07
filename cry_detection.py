import numpy as np
import pyaudio as pa
import struct   # convert data to integers
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import time

def butter_bandpass(lowcut, highcut, fs, order):
    return butter(order, [lowcut, highcut], fs=fs, btype="band")

def band_pass_filter(data, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    filtered_data = lfilter(b, a, data)
    return filtered_data


CHUNK = 1024 * 2    # number of samples plot in a second
FORMAT = pa.paInt16
CHANNEL = 1
fs = 44100  # sample rate: Hz
# fs = 20000

# open a live stream
p = pa.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNEL, rate=fs, input=True, output= True, frames_per_buffer=CHUNK)


# Debug: print data and plot data
# print(audioData)

fig, (raw, freq) = plt.subplots(2)  # 2 rows of plots, subplot returns a Figure and the axes of subplots --- (raw, freq) can be stored in one 'arg' which is a list -> arg[0] = raw, arg[1] = freq

fig.suptitle('Audio Data & Audio Frequency')

raw_x = np.arange(0, 2 * CHUNK, 2)  # raw audio data x-axis range: 0 to 2 * CHUNK, interval is 2 -> 2048 points [0, 2 * CHUNK)
freq_x = np.linspace(0, fs, CHUNK)  # freq data x-axis: start: 0, end: fs, number of samples: CHUNK -> 2048 points [0, fs]

raw_line, = raw.plot(raw_x, np.random.rand(CHUNK), 'r')     # raw.plot return a list of Line2D objects representing plotted data, "raw_line," can unpack the list and store the element, type of 'raw_line' is Line2D
freq_line, = freq.semilogx(freq_x, np.random.rand(CHUNK))   # make a plot with log scaling on the x-axis

# print (len(freq_x))

# set axes view limits
raw.set_ylim(-20000, 20000)
raw.set_xlim(0, CHUNK)

freq.set_ylim(0, 10)
freq.set_xlim(10, fs/2)


fig.show()

# plt.show()
global cry_curr_time, cry_next_time
cry_next_time = time.time()

global loud_curr_time, loud_next_time
loud_next_time = time.time()

try:
    while True:
        # get audio data
        audioData = stream.read(CHUNK)

        # convert hexadecimal to integer
        audioData = struct.unpack(str(CHUNK) + 'h', audioData)  # size: chunk, type: hexadecimal

        raw_line.set_ydata(audioData)   # set y-axis of audio data

        filtered_data = band_pass_filter(audioData, 280, 2000, fs, order=5)     # band pass filter the audio data
        audioData_freq = np.abs(np.fft.fft(filtered_data)) * 2 / (200 * CHUNK)  # compute frequency and scale the output
        freq_line.set_ydata(audioData_freq)     # set y-axis of freq data


        # infants crying frequency range: 300 - 600 Hz
        # if crying frequency with strong enough intensity is detected: do actions
        if(audioData_freq.max() > 1.2):
            index, = np.where(audioData_freq == audioData_freq.max())   # array: indices of max_freq elements

            # according to y-coordinate index find the point's x-coordinate (frequency)
            frequency = []
            for i in range(len(index)):
                frequency.append(freq_x[index[i]])

            # if frequency is higher than 20kHz (max human can hear)
            for f in frequency:
                if f > 20000:
                    frequency.remove(f)

            # intensive sound frequency: cry or loud sound
            if len(frequency) >= 1:
                cry_curr_time = time.time()
                loud_curr_time = time.time()

                if frequency[0] > 280 and frequency[0] < 620 and cry_curr_time >= cry_next_time:    # frequency within range of 280-620: cry
                    cry_curr_time = time.time()
                    cry_next_time = cry_curr_time + 3   # limit the detetction time

                    print("cry detected.")

                    # send 'take photo' command:
                    with open('cry.txt', 'w') as cry_file:
                        cry_file.write('True')
                        cry_file.close()



                elif audioData_freq.max() > 4 and loud_curr_time >= loud_next_time:
                    loud_curr_time = time.time()
                    loud_next_time = loud_curr_time + 2   # limit the detetction time

                    print("loud sound detected.")

                    # send 'take photo' command:
                    with open('loud_sound.txt', 'w') as loud_file:
                        loud_file.write('True')
                        loud_file.close()


        # update existing fig
        fig.canvas.draw()   # update a figure that has been changed, will redraw the current figure
        fig.canvas.flush_events()

except KeyboardInterrupt:
    p.terminate()
    quit()