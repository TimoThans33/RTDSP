##Lab 4: FIR Filter Design
The goal of this lab was to design a real time Finite Impulse Response (FIR) filter. We have done this by retrieving 
the filter coefficients from Matlab and implementing this using the C6713 DSK system in C.
The implementation of the filter in real time requires the design of a buffer. The most obvious
design of this is the delay operator but as it turned out this is not the most quickest and 
efficient design. Therefore we have also designed two versions of circular buffers and
evaluated their results in terms of clock cycles.
###repo structure
    ├── ProjectFiles 
               └── intio.c         # Actual C file
    ├── RemoteSystemsTempFiles
    └── Readme.md 