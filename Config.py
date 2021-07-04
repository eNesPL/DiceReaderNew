import os
from configparser import ConfigParser

import falcon

config = ConfigParser()


class Config():
    Music = 0
    Effects = 0
    Camera = ""
    RemoteCamera = ""
    ConfirmRoll = False

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = Config().ToJson()

    def ToJson(self):
        Json = '{"Music":"'+str(self.Music)+'","Effects":"'+str(self.Effects)+'"}'
        return Json


global ui

def getui(d):
    global ui
    ui = d

def GenerateConfig():
    config.add_section("Sound")
    config.add_section("Camera")
    config.add_section("Game")
    config.set("Sound",'music',str(100))
    config.set("Sound",'effects',str(100))
    config.set("Camera","cameraid",str(""))
    config.set("Camera","remotecamera",str(""))
    config.set("Game", 'confirmroll', str(0))
    with open('config.ini','w') as configfile:
        config.write(configfile)

def SaveConfig():
    config.read('config.ini')
    global ui
    for i in ui.CamRadioButtons:
        if(i.isChecked()):
            config.set("Camera","cameraid",i.text().replace(" ","_"))
    config.set("Camera","remotecamera",ui.GetCameraAddress())
    (Music,Effect) = ui.GetSliderValues()
    config.set("Sound","music",str(Music))
    config.set("Sound","effects",str(Effect))
    config.set("Game","confirmroll",str(ui.ConfirmRollsCheckBox.checkState()))
    with open('config.ini','w') as configfile:
        config.write(configfile)

def LoadConfig():
    if(CheckConfig()):
        GenerateConfig()
    config.read('config.ini')
    Config.Music = config.get("Sound","music")
    Config.Effects = config.get("Sound","effects")
    Config.Camera = config.get("Camera","cameraid")
    Config.RemoteCamera = config.get("Camera","remotecamera")
    Config.ConfirmRoll = config.get("Game","confirmroll")
    global ui
    ui.LoadConfig(Config)


def CheckConfig():
    """ Check if file is empty by confirming if its size is 0 bytes"""
    if(os.path.exists("config.ini")):
        print("FILE IS HERE")
        if(os.stat("config.ini").st_size == 0):
            print("FILE IS EMPTY")
            return True
        return False
    return True
