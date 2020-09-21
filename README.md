# ds_lab_6

Assignment:
Create server and client scripts to transfer files using one of the approaches described above. Client script should accept name of file and server address+port as arguments. 
Format:
$ python3 your_script.py file domain-name|ip-address port-number
Example usage:
$ python3 send_file.py meme.png your_vps.ru 8800
$ python3 send_file.py video.mp4 18.33.12.49 9332
In addition, client script should calculate and print to console the current progress of transferring in percents. Server should run on AWS (use other VPS if you already have) and save the file with the same name as it was on the client machine. 
