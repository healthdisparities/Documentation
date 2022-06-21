# How to download UK Biobank data

#### Created by: Whitney Teagle

#### Contents
1. [Download data from UKB](#section2)  

<a id='section2'></a>

## 2. Download data from UKB

Note: This data takes up at least 130G memory, so you should request 200G memory for the nodes when requesting an sinteractive session in Biowulf.  

Likewise, prepare to save the data in a directory that has enough disc space available (at least 55G).  

*****  


#### 1. Navigate to UK Biobank data download page
- To download UKB data from https://www.ukbiobank.ac.uk/, click the menu button on the top right of the screen. From there, click “Researcher log in” and follow the instructions to log in using your UKB credentials.  
- In the menu on the left side of the screen, click on “Projects”. Then, click the “View/Update” button. This will navigate you to a page with your application details, with the Application ID at the top of the page.  
- Click on “Data”, located at the top of the page. Then click on the button under “Data refresh or download” (Go to Showcase to refresh or download data).  

Here you will see six files:
![image](https://user-images.githubusercontent.com/60749131/135088344-88bd3f6d-d828-4c28-94f1-6d94221d79e9.png)

#### 2. Download programs for data processing
- For each file located under “6 File Handlers”, 
	- Click the link for your Operating System of choice (for example, we used linux).  
![image](https://user-images.githubusercontent.com/60749131/135088738-e2daac45-67fd-4261-9183-10bda3b956b5.png)
	- Copy the "wget" code. In the example above, the code is ```wget -nd biobank.ndph.ox.ac.uk/ukb/util/ukbconv```.  
	- In the server/directory you want to download the data to in your PuTTY/terminal window, paste and run the code.  
	- Once it is done, run ```chmod 755 [file name]```, replacing [file name] with the name of the file you are downloading. In this example, the file name is “ukbconv” so you would type ```chmod 755 ukbconv```.
	- Run ```ls -l``` to confirm that the file is now executable (aka turned into green text in your terminal).

- Next, click on “1 Miscellaneous Utility”: 
![image](https://user-images.githubusercontent.com/60749131/135089673-c050dec3-0e81-43a7-96f8-f8e7a0ec42dc.png) 
- Click on the “all” link under Operating System and download the encoding.ukb file:
![image](https://user-images.githubusercontent.com/60749131/135090588-8e556adc-95ed-43b2-a6cf-b2b42a589b38.png)

#### 3. Download UKB datasets
- Finally, click on the “3 Datasets” tab and follow the instructions on screen to download the data.

#### 4. Process UKB datasets
- After you have downloaded each of the files, follow the instructions located at https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.3.pdf, beginning with section 2.4.

#### Notes and checks:
Note: if the programs are not in your path (downloaded into a “bin” directory), you will have to execute them from your directory. To do so, add “./” before each command through sections 2.6.3 in order to execute the line from the current directory. For example, when decrypting the encrypted file “ukb12345.enc” (replacing 12345 with your application number) in step 2.4, type ```./ukbmd5 ukb12345.enc```

The MD5 checksum for our data should be xxxxxxxxxxxxxxxxxxxxxxxxxxxx18ce  
(refer to email for the first 28 digits)

Note, when finished expect these sizes for the data:

```console
[teaglewl@biowulf raw_data]$ ls -lh  
 total 58G  
 -rw-r--r--. 1 teaglewl teaglewl  44M Jul 25 07:11 encoding.ukb  
 -rw-r--r--. 1 teaglewl teaglewl  20K Sep 23 15:40 fields.ukb  
 -rwxr-xr-x. 1 teaglewl teaglewl 356K Jul 25 07:11 gfetch  
 -rw-r-----. 1 teaglewl teaglewl 3.4G Sep 22 12:21 my_ukb_data.rda  
 -rw-r--r--. 1 teaglewl teaglewl 376M Sep 23 11:12 ukb12345.csv  
 -rw-r--r--. 1 teaglewl teaglewl 4.9G Mar 13  2021 ukb12345.enc  
 -rw-r-----. 1 teaglewl teaglewl  16G Sep 22 07:38 ukb12345.enc_ukb  
 -rw-r-----. 1 teaglewl teaglewl  11M Sep 23 17:50 ukb12345.html  
 -rw-r--r--. 1 teaglewl teaglewl  354 Sep 23 17:50 ukb12345.log  
 -rw-r-----. 1 teaglewl teaglewl 511K Sep 24 09:41 ukb12345.r  
 -rw-r--r--. 1 teaglewl teaglewl  34G Sep 23 14:43 ukb12345.tab  
 -rwxr-xr-x. 1 teaglewl teaglewl 2.0M Mar 14  2018 ukbconv  
 -rwxr-xr-x. 1 teaglewl teaglewl 335K Jul 25 07:11 ukbfetch  
 -rwxr-xr-x. 1 teaglewl teaglewl 327K Jul 25 07:11 ukblink  
 -rwxr-xr-x. 1 teaglewl teaglewl 1.8M Mar 14  2018 ukbmd5  
 -rwxr-xr-x. 1 teaglewl teaglewl 1.5M Mar 14  2018 ukbunpack
 ```
Steps to confirm data is complete forthcoming.
