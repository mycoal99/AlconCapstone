# AlconCapstone NGENUITY 3D Vision System

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

[contributors-shield]: https://img.shields.io/badge/contributors-green?style=for-the-badge&logo=appveyor
[contributors-url]: https://github.com/mycoal99/AlconCapstone/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mycoal99/AlconCapstone?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/mycoal99/AlconCapstone?style=for-the-badge
[stars-url]: https://github.com/mycoal99/AlconCapstone/stargazers
[issues-shield]: https://img.shields.io/github/issues/mycoal99/AlconCapstone?style=for-the-badge
[issues-url]: https://github.com/mycoal99/AlconCapstone/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/mycoal99/AlconCapstone/blob/main/LICENSE

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#overview">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
      <ul>
        <li><a href="#motivation-and-background">Motivation and Background</a></li>
      </ul>
      <ul>
        <li><a href="#existing-solutions">Existing Solutions</a></li>
      </ul>
    </li>
    <li>
      <a href="#core-components"> Core Components</a>
        <ul>
          <li><a href="#facial-detection">Facial Detection</a></li>  
        </ul>
        <ul>
          <li><a href="#eye-detection">Eye Detection</a></li>  
        </ul>
        <ul>
          <li><a href="#simulation-environment">Built With</a></li>  
        </ul>
    </li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

## Overview

### Motivation and Background

<p> 
Streamlining eye surgery through automation means that doctors will be able to bring improved vision to more patients and restore one of the most important human senses. With the prediction that the world’s population will increase by about one-third and along with it, the demand for cataract surgery, optometrists will struggle to keep up with the demand. At the relatively low rate at which optometrists are trained, the demand will outpace the current solution. Automation of the NGENUITY 3D Visualization system will drastically cut down the amount of time medical professionals will need to spend on preparing the patient for surgery and in turn allow optometrists to help more patients.
</p>

### Existing Solutions

<p>
The increase in cataract surgery demand is already causing great concern in the medical community and there are solutions currently being used to alleviate the problem. Beyond changes in administrative workflow, using lasers to make incisions increases consistency and accuracy while decreasing the amount of time to make the incisions, however even with advances in the actual surgical operation technology,systems using lasers will still benefit from decreasing the actual setup time through automation.
</p>

## Built With

<img src="https://raw.githubusercontent.com/mycoal99/AlconCapstone/main/tech_used.png"></img>

## Core Components
<img src="https://github.com/mycoal99/AlconCapstone/blob/main/architecture.png" height="500" width="750"></img>

### Facial Detection

<p>
The facial detection will be used to both uniquely identify the patient and determine where precisely they are in the room so that the robot can prepare for surgery. The facial detection algorithm will be run on each frame of the video four times, once at each right angle of the frame, to detect the patient at any orientation. Additionally, for each frame, the algorithm will compare the current detected face, with any previously recorded faces to determine if it is the same face. If the eye coordinates and the orientation of the current face is similar to a previous face, the algorithm will update that face, rather than saving the current face as a new face. The patient will be determined as the face that has the highest probability of being a face, and has been in the most frames of the video. The coordinates of the patient’s eyes, and the orientation of their face will be saved and sent to the robot controller, so that the robot can be moved above the correct eye of the patient, and rotated to the desired orientation.
</p>

### Eye Detection

<p>
The eye detection algorithm will use iris and pupil detection to detect the patient's eye. The eye detection algorithm uses the eye coordinates returned from the facial detection algorithm to move the robot camera into the relative area of the patient's eye then uses image processing techniques to perform iris and pupil detection. Once the iris and pupil are detected the eye detection interacts with the robot to make use of the existing focus and zoom functions on the camera to clarify the feed of the eye.
</p>

### Simulation Environment

<p>
The simulation environment will act as an abstraction of the actual environment that the software will be used in. The simulation will include basic controls including: pan left and right to mimic changing x/y-coordinates and a zoom to mimic z-coordinates. The controls will be called by the facial detection algorithm to center and focus the camera onto the patient. The controls are implemented using HTTP requests to the local IP address of the camera. Each time controls need to be accessed, a token is granted to the process looking to access the controls; the token is then used indefinitely until desired controls have been called. The token is then released.
</p>

## Acknowledgements

<p>
We would like to thank our mentors from Alcon - True Vision for their amazing dedication in supporting us through an extremely challenging but amazing learning experience!
</p>
