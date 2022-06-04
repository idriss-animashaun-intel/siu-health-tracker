import os
import urllib.request
import zipfile
import shutil
import time


siu_tracker_master_directory = os.getcwd()
siu_tracker_file = siu_tracker_master_directory+"\\SIU Health Tracker.exe"
Old_siu_tracker_directory = siu_tracker_master_directory+"\\siu_tracker_exe-master"

proxy_handler = urllib.request.ProxyHandler({'https': 'http://proxy-dmz.intel.com:912'})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)


def installation():
    urllib.request.urlretrieve("https://github.com/idriss-animashaun-intel/siu-health-tracker/archive/refs/heads/master.zip", siu_tracker_master_directory+"\\siu_tracker_luancher_new.zip")
    print("*** Updating Launcher Please Wait ***")
    zip_ref = zipfile.ZipFile(siu_tracker_master_directory+"\siu_tracker_luancher_new.zip", 'r')
    zip_ref.extractall(siu_tracker_master_directory)
    zip_ref.close()
    os.remove(siu_tracker_master_directory+"\siu_tracker_luancher_new.zip")

    src_dir = siu_tracker_master_directory + "\\siu-health-tracker-master"
    dest_dir = siu_tracker_master_directory
    fn = os.path.join(src_dir, "SIU Health Tracker.exe")
    shutil.copy(fn, dest_dir)

    shutil.rmtree(siu_tracker_master_directory+"\\siu-health-tracker-master")

    time.sleep(5)
    
def upgrade():
    print("*** Updating Launcher Please Wait ***")    
    print("*** Removing old files ***")
    time.sleep(20)
    os.remove(siu_tracker_file)
    time.sleep(10)
    installation()


### Is siu_tracker already installed? If yes get file size to compare for upgrade
if os.path.isfile(siu_tracker_file):
    local_file_size = int(os.path.getsize(siu_tracker_file))
    # print(local_file_size)

    url = 'https://github.com/idriss-animashaun-intel/siu-health-tracker/raw/master/SIU%20Health%20Tracker.exe'
    f = urllib.request.urlopen(url)

    i = f.info()
    web_file_size = int(i["Content-Length"])
    # print(web_file_size)

    if local_file_size != web_file_size:# upgrade available
        upgrade()

### siu_tracker wasn't installed, so we download and install it here                
else:
    installation()

if os.path.isdir(Old_siu_tracker_directory):
        print('removing siu_tracker_exe-master')
        time.sleep(5)
        shutil.rmtree(Old_siu_tracker_directory)

print('Launcher up to date')