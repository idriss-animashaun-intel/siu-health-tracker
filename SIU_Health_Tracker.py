import os
import urllib.request
import zipfile
import shutil
import time
from subprocess import Popen
from subprocess import call

siu_tracker_master_directory = os.getcwd()
siu_tracker_directory = siu_tracker_master_directory+"\siu-health-tracker-updates"
siu_tracker_file = siu_tracker_directory+"\\main.exe"
siu_tracker_old_directory = siu_tracker_master_directory+"\\old_revisions"
siu_tracker_old_file = siu_tracker_old_directory+"\\main.exe"

proxy_handler = urllib.request.ProxyHandler({'https': 'http://proxy-dmz.intel.com:912'})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)

def installation():
    print("*** Downloading new version ***")
    urllib.request.urlretrieve("https://github.com/idriss-animashaun-intel/siu-health-tracker/archive/refs/heads/updates.zip", siu_tracker_master_directory+"\\siu_tracker_new.zip")
    print("*** Extracting new version ***")
    zip_ref = zipfile.ZipFile(siu_tracker_master_directory+"\siu_tracker_new.zip", 'r')
    zip_ref.extractall(siu_tracker_master_directory)
    zip_ref.close()
    os.remove(siu_tracker_master_directory+"\siu_tracker_new.zip")
    time.sleep(5)
    
def upgrade():    
    print("*** Removing old files ***")
    shutil.rmtree(siu_tracker_directory)
    time.sleep(10)
    installation()

def main(autoinstall=0):
    ### Is siu_tracker already installed? If yes get file size to compare for upgrade
    if os.path.isfile(siu_tracker_file):
        local_file_size = int(os.path.getsize(siu_tracker_file))
        print(local_file_size)
        ### Check if update needed:
        f = urllib.request.urlopen("https://github.com/idriss-animashaun-intel/siu-health-tracker/raw/updates/main.exe") # points to the exe file for size
        i = f.info()
        web_file_size = int(i["Content-Length"])
        print(web_file_size)
        if local_file_size != web_file_size:# upgrade available
            if autoinstall:
                print("*** New upgrade available! Upgrading now *** ")
                upgrade()
            else:
                updt = input("*** New upgrade available! enter <y> to upgrade now, other key to skip upgrade *** ")
                if updt == "y": # proceed to upgrade
                    upgrade()
    ### For the transfer between GitHub and GitLab
    elif os.path.isfile(siu_tracker_old_file):
        installation()
    ### siu_tracker wasn't installed, so we download and install it here                
    else:
        if autoinstall:
            print("*** Installing SIUHealthTracker for the first time ***")
            installation()
        else:
            install = input("Welcome to siu_tracker! If you enter <y> siu_tracker will be downloaded in the same folder where this file is.\nAfter the installation, this same file you are running now (\"siu_tracker.exe\") will the one to use to open siu_tracker :)\nEnter any other key to skip the download\n -->")
            if install == "y":
                installation()
    print('Ready')
    ### We open the real application:
    try:
        Popen(siu_tracker_file)
        print("*** Opening SIU Health Tracker ***")
        if not autoinstall:
            time.sleep(20)
    except:
        print('Failed to open application, Please open manually in subfolder')
        pass

def main_with_autoinstall():
    main(autoinstall=1)

if __name__ == "__main__":
    main()
