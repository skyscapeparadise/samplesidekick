
<img width="1072" alt="Screenshot 2024-01-29 at 8 29 32 PM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/17ddec24-6fcc-4c51-b689-a29f1378f938">

# samplesidekick

A beautiful graphical sample-renaming tool for developing sample-based virtual instruments for use in digital audio workstations.

This project serves as a proof-of-concept for creating development tools with graphical interfaces made of GPU-accelerated video elements using the cross-platform Qt 6 API (among others). It takes a directory of sequentially numbered samples as an input, copies the samples into an output folder, and gives them a name containing their appropriate key, octave, velocity, round robin, and signal track.

NOTE: AS OF JANUARY 29, 2024, THIS SOFTWARE IS STILL INCOMPLETE AND DOES NOT FUNCTION PROPERLY. PLEASE REFRAIN FROM USING IT TO RENAME YOUR SAMPLES UNTIL A RELEASE IS COMPLETE.

# Instructions
samplesidekick can be used with any digital audio workstation, but I'll use the workflow with Logic Pro as an example:

1. Split all of your tracks into individual samples however you like. Use Cmd/Cntl-A to select all of your clips.

<img width="1750" alt="Screenshot 2024-01-29 at 8 50 19 PM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/9da81c10-b8fa-4e49-b73a-4a98c9bff5f9">

2. Rename the first clip in the top left to the number "1". Logic will rename all the subsequent clips in ascending numerical order, iterating over the tracks.

<img width="1750" alt="Screenshot 2024-01-29 at 8 50 52 PM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/395133f5-d002-4321-8ef8-a82d069bec11">

3. Right-click one of the clips (with them all selected still) and export the regions as audio files to a directory to feed to samplesidekick.

<img width="506" alt="Screenshot 2024-01-29 at 8 51 17 PM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/828ffc0d-fc05-49f9-9939-3d167ac831ac">

4. Use that directory as the "sample directory" inside of samplesidekick. Choose the settings that best represent your samples.


<img width="1072" alt="Screenshot 2024-02-25 at 6 35 43 PM" src="https://github.com/skyscapeparadise/samplesidekick/assets/132173748/fba3861c-70ff-469e-b3ce-72581d35a376">



# License
samplesidekick is licensed under the GPLv3 license.
