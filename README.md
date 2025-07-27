# CODERECET

## Project Repository
*Commit and save your changes here*

### Team Name :TechieDo
### Team Members :Nihal M and Ashik M
### Project Description
HealthSync, is a smart AI-powered shopping cart designed to guide individuals in making healthier food choices based on their personal health conditions. Through this innovation, we strive to make everyday decisions simpler, safer, and more supportive for everyone.
## Technical Details

### Technologies/Components Used
* Raspberry Pi 4, 

* Pi cam model3, 

* Arduino uno, 

* Load cell,

* HX711 Amplifier

## For Software:
We made an app for collecting health data of user using Flutter

And then we use python for both Hardware and a simple user interface in our cart so in there we use so many libraries like

cv2 (OpenCV) – for image processing and resizing

numpy – for array manipulation and preprocessing input for the model

tflite_runtime.interpreter – for running the TensorFlow Lite model on Raspberry Pi

requests – for sending HTTP requests (used to get health recommendations)

PIL.Image, ImageTk (from Pillow) – for handling and displaying images in the GUI

serial (pyserial) – for communication between Arduino and Raspberry Pi

picamera2 – for accessing the Pi Camera (specific to libcamera on Raspberry Pi OS)

tkinter and tkinter.ttk – for building the GUI

and we use Arduino for getting data from the load cell and sending the dats to Raspberry pi so for that we use arduino ide and a library for the amplifier HX711.h

## For Hardware:

* Raspberry Pi 4, 

* Pi cam model3, 

* Arduino uno, 

* Load cell,

* HX711 Amplifier

[List specifications]

## Implementation

## For Software:

### Installation
[commands]

### Run
[commands]

### Project Documentation

### Screenshots (Add at least 3)

<img width="1017" height="562" alt="Screenshot 2025-07-27 025412" src="https://github.com/user-attachments/assets/d6d75be9-f1a5-42a1-a634-476158e0c6e4" />

<img width="3113" height="1000" alt="Untitled design (7)" src="https://github.com/user-attachments/assets/1fdb35fa-4bb0-4479-95d5-792c2895e4df" />


### Diagrams
[ Start ]

   ↓
   
[ User enters health data in mobile app ]

  ↓
   
[ App generates QR code ]
  
   ↓
   
[ QR code is scanned by cart camera ]

   ↓
   
[ Health profile is loaded into system ]

   ↓
   
[ User places food item in front of Pi Camera ]

   ↓
   
[ AI model identifies the food item ]

   ↓
   
[ Arduino reads weight using load cell ]

   ↓
   
[ Raspberry Pi calculates price (weight × rate) ]

   ↓
   
[ System checks food against health profile ]

   ↓
   
[ Real-time health recommendation is displayed ]

   ↓
   
[ User decides → Add to cart or skip ]

   ↓
   
[ Item added to virtual cart (with name, weight, price) ]

   ↓
   
[ Repeat for other items ]

   ↓
   
[ At end: Bill is generated ]

   ↓


[ End ]

## For Hardware:

### Schematic & Circuit

<img width="6000" height="3375" alt="Untitled design (5)" src="https://github.com/user-attachments/assets/7b7ca290-e597-4624-ac32-09a001d0b5b1" />


### Build Photos
Components(![Uploading IMG20250727063053.jpg…])
Raspberry Pi 4 
Pi cam model3
Arduino uno
Load cell
HX711 Amplifier

![IMG20250727063019](https://github.com/user-attachments/assets/c3574440-81f3-4a97-8555-86361dbd4390)


We started with trying out just with camera and raspberry pi and making a python code to understand or recognize each and every items we show so we firstly trained a model which was not perfect just for testing and it worked perfectly then we added more features to it like added and user interface which is also in python first we tried html but it was not thet good sowe built frontend also in python so we added like basic things like recognizing them,then we where move on to like the section where weight checking we built a small circuit using arduino and load cell so that we can check every product weight we need to buy .so actually we can directly connect this load cell to raspberry pi but we where a little bit scared of unexpected short circuit or something killing the pi so we just connected load cell to arduino and then to pi so that if there is short circuit or something in the circuit part it will only affected to arduino so after that wwe integrated this weighing system to the ui like showing price of the product according to the weight and prices are stored in a json file also the last generated bill is also connected by using json files and at these time we where also involved in building the app for generating qrcodes so yaa that's the building process

 ![VID20250727063218 (1) (1)](https://github.com/user-attachments/assets/ab476653-41f8-4f75-8b21-208567c97c18)

 
After all this works it works just as we expected like we have a software where user can input there health data 
then the software generates qr code which we can scan using the camera we have in the raspberry pi 
raspberry pi gets the data from the qr code then move on to the object recognation setup using tensorflowlite so it recognizes the object and gets the weight reading from arduino and shows the price the product we just weighed in the User interface and then user can add or not add the product to cart if the user is ok they can add it symply by clicking a button and whenever user weighs the product or object symulteniously it shows the suggetion as it good or bad for your disease in the UI .after adding all the needed things to cart we can symply press the print bill button which shows the bill of the products you added to cart .

### Project Demo

### Video
https://drive.google.com/file/d/1e2F2ogqojToN24Hm8SQZY-vU54sRm0Bo/view?usp=sharing

In the video we are showing how the things work like first we need to take the software and type our health conserns in it it will generate a qr code accordingly then we need to scan it in the picam so that pi will get our details ,then we just put the things we needed like carrot and in the UI we can see its good or bad for our health condition so then we added it our cart then we clicked print bill then the billshow up .

## Additional Demos
[Add any extra demo materials/links]

## Team Contributions
[Name 1]: [Specific contributions]
[Name 2]: [Specific contributions]
[Name 3]: [Specific contributions]
