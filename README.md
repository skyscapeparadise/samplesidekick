
<img width="1072" alt="Screenshot 2024-01-29 at 8 29 32 PM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/17ddec24-6fcc-4c51-b689-a29f1378f938">

# samplesidekick

A beautiful graphical sample-renaming tool for developing sample-based virtual instruments for use in digital audio workstations.

This project serves as a proof-of-concept for creating development tools with graphical interfaces made of GPU-accelerated video elements using the cross-platform Qt 6 API (among others). It takes a directory of sequentially numbered samples as an input, copies the samples into an output folder, and gives them a name containing their appropriate key, octave, velocity, round robin, and signal track.

# Requirements

Releases will include all necessary packages but if you're working with the source code itself, you will need the following additional Python packages:

○ PySide6

○ opencv-python

samplesidekick was developed with Python 3.10.7 so your milage may vary using it with other versions.

# Instructions
samplesidekick can be used with any digital audio workstation, but the standard workflow is intended for Logic Pro:

1. Split all of your tracks into individual samples. Arrange the samples so that the quietest/smallest velocity layer is first and the loudest/biggest velocity layer is last. Use Cmd/Cntl-A to select all of your clips.

<img width="1750" alt="Screenshot 2024-01-29 at 8 50 19 PM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/9da81c10-b8fa-4e49-b73a-4a98c9bff5f9">

2. Rename the first clip in the top left to the number "1". Logic will rename all the subsequent clips in ascending numerical order, iterating over the tracks. Your milage may vary with other DAWs.

<img width="1624" alt="Screenshot 2024-03-05 at 2 16 05 PM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/1ac707b6-54e4-430a-9399-ea56f1444811">

3. Right-click one of the clips (with them all selected still) and export the regions as audio files to a directory to feed to samplesidekick.

<img width="284" alt="Screenshot 2024-03-01 at 12 20 07 AM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/6320af69-bfc3-40f8-b9ff-2cd420c0efd2">

4. Use that directory as the "sample directory" inside of samplesidekick. Choose the settings that best represent your samples.

<img width="1072" alt="Screenshot 2024-03-07 at 1 30 59 AM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/241f268d-1e59-4562-9fdf-8cde97c808d4">





# License
samplesidekick is licensed under the GPLv3 license.
