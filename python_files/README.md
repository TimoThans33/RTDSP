## Project
This directory includes the python files used the design and test the signal detection algorithm.
Our design process existed of three steps in the same order as shown order.
* cross_correlation.py          # only cross correlation is used to detect the signal
* cross_correlation_fft.py      # does a cross correlation in the frequency domain
* cross_correlation_noise_sub.py # uses an estimate noise spectral subtractor to improve results
## repo structure
    .
    ├── .npy                    
    ├── SoundSamples            
    ├── src                     
           ├── cross_correlation.py                 # signal detection with just the cross correlation
           ├── cross_correlation_fft.py             # signal detection with cross correlation in the frequency domain
           └── cross_correlation_noise_sub.py       # making use of estimation noise spectrum subtraction
    └── README.md
 ```
python --V  python3.6
```
