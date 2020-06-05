# rpi_home_lights
A server on raspberry pi that can run commands for neopixel light strips.

### How to run (currently only in dev mode):

Unfortuantly you will need 3 separate terminals to run the complete application. Then from the `./rpi_home_lights` location do the following:

 1) Start the physical lights: `sudo python3 -m server.run_lights`

 2) Next in a separate terminal start the lights socket server: `sudo python3 -m server.app`

 3) Finally in the 3rd terminal start the client with: `cd client/ && npm run start`