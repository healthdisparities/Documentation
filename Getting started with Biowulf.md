## PuTTY

1. [Download PuTTY software.](https://www.putty.org/) PuTTY is a free SSH and telnet client for Windows.  

## Connect to Biowulf

##### If this is your first time connecting to Biowulf
1. Open the PuTTY application. You won't have any settings saved yet; however, you can save your Biowulf settings now to make it easier for next time.  
2. In the "Host Name (or IP address)" box, type ```<your NIH username>@biowulf.nih.gov```  
3. In the "Port" box, type ```22```  
4. "Connection type" should be set to SSH  
5. In the "Saved Sessions" box, type "Biowulf"  
6. Click "Save", located under the *Load* and above the *Delete* buttons. This will make it easier for next time.  
7. Now press "Open", located on the bottom-right of the PuTTY window. A new window should appear asking for <your username>@biowulf.nih.gov's password.  
8. Enter your password. You should see ```[<your NIH username>@biowulf ~]$``` at the bottom of the window if you successfully logged in. This means you are in the login node of Biowulf. Otherwise, it will ask for your password again.  

##### If you have already saved the Biowulf connection settings
1. Open the PuTTY application  
2. Click on "Biowulf" located in the big white box under *Load, save or delete a stored session*  
3. Click on the "Load" button, located above the *Save* and *Delete* buttons  
4. Press "Open", located on the bottom-right of the PuTTY window. A new window shold appear asking for your password  
5. Enter your password  

## Create an interactive session

1. You can't do much in the login node, so the first thing to do when you log in to Biowulf is to create an interactive session. The basic version of this is to type ```sinteractive``` and press enter. Other settings can be added for [more specific use cases](https://hpc.nih.gov/docs/userguide.html). This step should take a few minutes to connect.  
2. When your nodes have been allocated, you should see ```[<your NIH username>@cn#### ~]$``` at the bottom of the window.  

For more information on creating interactive sessions, go to <https://hpc.nih.gov/docs/userguide.html> or watch  <https://www.youtube.com/watch?v=HuWf5-SIIMk&ab_channel=NIH_HPC>.  

For creating a Jupyter notebook in Biowulf, see the first step in <https://github.com/healthdisparities/Documentation/blob/main/How%20to%20extract%20data%20from%20the%20UK%20Biobank.md>.
