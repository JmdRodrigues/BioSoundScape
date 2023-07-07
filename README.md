# BioSoundScape

Welcome to the journey where the signals of your body wil create Ssssoooouuuund.

You can use an interface that we developed if you have a BiosignalsPlux device.
In case you have one, you can make use of a biosingal to generate sound.
we have predefined experiments for specific types of signals.

In order to use it, you should have Python installed.
Currently, we only support Python < 3.11.
You should also download the plux_api file that corresponds to your python version.
You can find it here:
https://github.com/pluxbiosignals/python-samples/tree/master/PLUX-API-Python3

Add the file at "tools/" and change the plux.pyd file.

Afterwards, please install the necessary packages. For this, run:
pip install -r requirements.txt 

Then, you should be able to run the interface at sandbox/new_gui2.
For this, run the command:
python sandbox/new_gui2/main.py

It should open the app. You can the  edit the mac adress 
to find your plux device. It should then start recording the data
once you Launch button.
