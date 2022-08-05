#!/usr/bin/python3

import subprocess
import sys
import getopt
from time import sleep

class fastboot:

    def __init__(self):
        self.device_id = ''
        self.file_name = ''
        self.fb_status = 0

        try:
            opts, arg = getopt.getopt(sys.argv[1:], "f:d:mh")
        
        except getopt.GetoptError as err:
            print("Error:")
            print(err)
            print("")
            quit(0)
        
        for op, val in opts:
            if op == "-d":
                self.device_id = val

            if op == "-f":
                self.file_name = val
            
            if op == "-m":
                self.fb_status = 1

            if op == "-h":
                self.print_help_info()
                quit(0)    

    def main(self):
        if self.fb_status == 1:
            self.main_fb()
            return

        self.get_dev_id_by_adb()
        if len(self.device_id_list_adb) == 0:
            print("No device serach!")
            quit(0)

        if len(self.device_id) == 0:
            self.device_id = self.device_id_list_adb[0]
        else:
            ret = self.check_dev_id_by_adb()
            if ret == False:
                print("No device serach by adb!")
                quit(0)     

        self.reboot_in_bootloader();
        self.main_fb()
                    
    def main_fb(self):
        if self.fb_status == 1:
            self.get_dev_id_by_fb()
            
            if len(self.device_id) == 0:
                self.device_id = self.device_id_list_fb[0]
            else:
                ret = self.check_dev_id_by_fb()
                if ret == False:
                    print("No device serach by fastboot!")
                    quit(0)
        
        self.fb_img()
        
    def get_dev_id_by_adb(self):
        self.__cmd_ret = subprocess.run(["adb", "devices"], check=True, stdout=subprocess.PIPE)

        self.__cmd_ret_output = self.__cmd_ret.stdout

        byte_to_str = str(self.__cmd_ret_output)

        original_list = byte_to_str.split('\\n')

        device_list = original_list[1:-2]

        self.device_id_list_adb = []

        for i in device_list:
            list_temp = i.split("\\t")
            self.device_id_list_adb.append(list_temp[0])

    def get_dev_id_by_fb(self):
        self.__cmd_ret = subprocess.run(["fastboot", "devices"], check=True, stdout=subprocess.PIPE)

        self.__cmd_ret_output = self.__cmd_ret.stdout

        byte_to_str = str(self.__cmd_ret_output)

        original_list = byte_to_str.split("\'")

        device_str = original_list[1]

        device_list = device_str.split("\\n")[0:-1]

        self.device_id_list_fb = []

        for i in device_list:
            list_temp = i.split("\\t")
            self.device_id_list_fb.append(list_temp[0])  

    def check_dev_id_by_fb(self) -> bool:
        for i in self.device_id_list_fb:
            if i == self.device_id:
                return True

        return False

    def check_dev_id_by_adb(self) -> bool: 
        for i in self.device_id_list_adb:
            if i == self.device_id:
                return True

        return False

    def reboot_in_bootloader(self):
        self.__cmd_ret = subprocess.run(["adb", "reboot", "bootloader"], check=True, stdout=subprocess.PIPE)

        print("wait a minutes，reboot bootloader......")

        while True:
            self.get_dev_id_by_fb();
            ret = self.check_dev_id_by_fb();
            if ret == True:
                break
        
        print("reboot bootloader done......")
        
        sleep(3)

    def fb_img(self):
        img = self.file_name + ".img"
        path = "./out/target/product/lahaina/" + img

        print("wait a minutes, fastboot " + img)

        self.__cmd_ret = subprocess.run(["fastboot", "flash", self.file_name, path], check=True, stdout=subprocess.PIPE)

        print("fastboot done,restart device........")
        
        sleep(5)

        self.reboot_device()

    def reboot_device(self):
        self.__cmd_ret = subprocess.run(["fastboot", 'reboot'], check=True, stdout=subprocess.PIPE)

    def print_help_info(self):
        print("usage: fastboot [OPTION...] COMMAND...")
        print("options:")
        print("  -d    device id, default: 'adb devices' first id")
        print("  -f    filename (boot, vendor_boot....)")
        print("  -m    device mode is bootloader now")
        print("  -h    help infomation")


if __name__ == '__main__':

    fb = fastboot()
    
    fb.main()
    

