'''Functions for starting and closing Miralix'''

import os
import subprocess
import time

import uiautomation as auto


def open_miralix():
    subprocess.Popen("C:\Program Files\Miralix\Miralix OfficeClient\Miralix OfficeClient.exe")


def login(username: str, password: str) -> auto.WindowControl:
    window = auto.WindowControl(Name = "Miralix Desktop", searchDepth=1)
    bruger_text = window.EditControl(AutomationId = "Email")
    password_text = window.EditControl(AutomationId = "Password")

    bruger_text.GetValuePattern().SetValue(username)
    password_text.GetValuePattern().SetValue(password)
    auto.ButtonControl(AutomationId = "LoginButton").GetInvokePattern().Invoke()
    return window


def dismiss_phone_check(window: auto.WindowControl):
    if not window.ListControl(ClassName = "ListBox").Exists(10, 1):
        print("Phone selection never finished")
    window.ButtonControl().GetInvokePattern().Invoke()
    time.sleep(10)  # Wait for popup to disappear


def close_miralix():
    os.system('taskkill /F /IM "Miralix OfficeClient.exe" /T')
