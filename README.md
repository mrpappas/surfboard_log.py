# surfboard_log.py
========
Signal strength logging for Arris/Motorola [Surfboard 6141](http://surfboard.com/products/sb6141/) modem.  

## Overview:  
Script I wrote to scrape the pertinent data from my modem's web portal.  The modem does keep logs but I was interested in keeping data on the actual signal strength and SNR.  The surfboard 6141 is a pretty widely used modem so I'm sharing in hopes someone else can find use / improve it.  
###### The script compiles and logs:
* Downstream Signal
* Upstream Signal  
* SNR (Signal to Noise Ratio)  
* Error Correction Rate  


## Sample output:  
    --------------------------------------------
    --------------------------------------------
    -- Data logged: 2016-Dec-10 09:52:41 --
    --------------------------------------------
    --------------------------------------------
    --  Downstream Signal  --
    Channel 9 : Downstream Signal 0 DBmV -- in spec
    Channel 10 : Downstream Signal 0 DBmV -- in spec
    Channel 11 : Downstream Signal 0 DBmV -- in spec
    Channel 12 : Downstream Signal 0 DBmV -- in spec
    Channel 13 : Downstream Signal 0 DBmV -- in spec
    Channel 14 : Downstream Signal 0 DBmV -- in spec
    Channel 15 : Downstream Signal 0 DBmV -- in spec
    Channel 16 : Downstream Signal 0 DBmV -- in spec
    --------------------------------------------
    --  Upstream Signal  --
    Channel 68 : Upstream Signal 47 DBmV -- in spec
    Channel 65 : Upstream Signal 45 DBmV -- in spec
    Channel 66 : Upstream Signal 46 DBmV -- in spec
    Channel 67 : Upstream Signal 47 DBmV -- in spec
    --------------------------------------------
    --  Signal to Noise Ratio  --
    Channel 9 : Signal to Noise Ratio 38 DBmV -- in spec
    Channel 10 : Signal to Noise Ratio 38 DBmV -- in spec
    Channel 11 : Signal to Noise Ratio 38 DBmV -- in spec
    Channel 12 : Signal to Noise Ratio 37 DBmV -- in spec
    Channel 13 : Signal to Noise Ratio 38 DBmV -- in spec
    Channel 14 : Signal to Noise Ratio 38 DBmV -- in spec
    Channel 15 : Signal to Noise Ratio 38 DBmV -- in spec
    Channel 16 : Signal to Noise Ratio 38 DBmV -- in spec
    --------------------------------------------
    -- Error Correction --
    99.9999955587121 % Unerrored Codewords
    --------------------------------------------
----
## Setup  
##### Dependencies:  
`python3`  
`BeautifulSoup`  

##### Config:  
Modem.log is created automatically and is by default stored in the same directory.  
Set IP variable to your modem's IP, the default on my model was http://192.168.100.1/cmSignalData.htm  
If you need to change the IP ensure you include the suffix `/cmSignalData.htm`  
The page you are aiming for looks like this:  

![Alt text](https://s30.postimg.org/76e7gd5kh/4034_signal.png "Your page should look like this")

Signal thresholds are measured in **dB** (decibels) or **dBmV** (decibel millivolts) are adjusted throughout their _high or _low variables, example:  

    downstream_high = 10  
    downstream_low = -10  

The default values are fairly standard but your provider may have different tolerances.  

## Usage:  
I set it as a cron job and have it run every 20 minutes.  
0,30 * * * * python3 ~/surfboard_log.py

## Support:  
Drop me a line @ mrbenpappas@gmail.com  
Or drop by [my site](http://mrbenpappas.com)

## License:  
**The MIT License (MIT)**
