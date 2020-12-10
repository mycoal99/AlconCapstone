'stream.py' is a very simple controller script for the Reolink E1 pan-tilt-zoom line of cameras controlled over local wifi.

There are currently two methods of controlling the camera. The first method is using cURL which sends a request using the local terminal. The second method is using Python's Request library by directly sending a control request.

Authentication is currently done in a naive way by sending credentials directly to the website in plain text. 

Camera controls using the user keyboard will probably be implemented by using interrupts.