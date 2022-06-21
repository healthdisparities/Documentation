# Create a Jupyter notebook in Biowulf

#### Created by: Whitney Teagle

#### Contents
1. [Create a Jupyter notebook](#section1)  
    1.a. [Biowulf](#section1)

<a id='section1'></a>

## 1. Create a Jupyter notebook

### 1.a. Biowulf
Goal: use Jupyter Lab on Biowulf.

#### Step 1. Allocate an interactive session in Biowulf

1. Connect to NIH VPN
2. Open PuTTY and connect to Biowulf
3. Login with username and password
4. Allocate an interactive session using the following code:
```
sinteractive --gres=lscratch:5 --mem=200g --tunnel
```
While this is loading, move on to step 2.

Note: The eventual output of this command will say what port to use. For example, the output ```ssh -L 42549:localhost:42549 username@biowulf.nih.gov``` indicates that the port number is 42549. Keep this information in your brain for later.

#### Step 2. Open new PuTTY window

1. Leaving the PuTTY window from Step 1 running, open a new PuTTY session.
2. Load Biowulf (but don't "Open" right away!)
3. In the menu on the left side of the PuTTY window, go to the "Tunnels" settings in the "SSH" tab. There, you will see a textbox labeled **Source port** and a textbox labeled **Destination**. Input the following information, replacing the port number with the number generated from your first PuTTY session:
	- Source port: ```42549```
	- Destination: ```localhost:42549```
4. Click "Add".
5. Click "Open", then login using your username and password. Next, proceed to Step 3.

#### Step 3. Initiate Jupyter notebook

1. In the first PuTTY window (the one created during Step 1), start a Jupyter instance using the following code:
```
module load jupyter
```
2. Use the following code to initiate a Jupyter notebook:
```
jupyter notebook --ip localhost --port $PORT1 --no-browser
```
Note: if you get the error ```jupyter-notebook: error: argument --port: expected one argument```, you may be trying to do this step in the wrong PuTTY window. Go back to the original PuTTY window (the first one you made, from Step 1 of these instructions) and try running the code in Step 3 of these instructions there.

3. Copy the link given in the output.
4. Paste the link into the search bar in your internet browser and push enter to start your Jupyter notebook session. 

When you are done with Jupyter, save your changes in the browser and close both PuTTY windows.

**More information:**

Jupyter on Biowulf https://hpc.nih.gov/apps/jupyter.html  
SSH Tunneling on Biowulf https://hpc.nih.gov/docs/tunneling/ 
