This tool was originally created in order to display any image on a OLED screen that I [fit inside my keyboard](https://www.thingiverse.com/thing:4811993) and connected to a microcontroller running micropython.

You can call the script as follows: `python3 ./image_to_oled_micropython.py image.jpg`

The tool then generates the main.py file that can be flashed on the microcontroller e.g. like this `ampy --port /dev/ttyUSB0 put main.py /main.py`
    
For instructions on how to get micropython running on your ESP, see [this](https://pythonforundergradengineers.com/upload-py-files-to-esp8266-running-micropython.html)
