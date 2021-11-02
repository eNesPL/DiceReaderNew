import os
from configparser import ConfigParser

configparser = ConfigParser()


class Config():
    Music = 0
    Effects = 0
    Camera = ""
    RemoteCamera = ""
    ConfirmRoll = False

    def ToJson(self):
        Json = '{"Music":"' + str(self.Music) + '","Effects":"' + str(self.Effects) + '"}'
        return Json


config = Config()


def configGetUi(d):
    global ui
    ui = d


def GenerateConfig():
    configparser.add_section("Camera")
    configparser.add_section("Game")
    configparser.set("Camera", "cameraid", str(""))
    configparser.set("Camera", "remotecamera", str(""))
    configparser.set("Game", 'confirmroll', str(0))
    with open('config.ini', 'w') as configfile:
        configparser.write(configfile)


def SaveConfig():
    configparser.read('config.ini')
    for i in ui.CamRadioButtons:
        if (i.isChecked()):
            configparser.set("Camera", "cameraid", i.text().replace(" ", "_"))
    configparser.set("Camera", "remotecamera", ui.GetCameraAddress())
    configparser.set("Game", "confirmroll", str(ui.ConfirmRollsCheckBox.checkState()))
    with open('config.ini', 'w') as configfile:
        configparser.write(configfile)
    ui.ChangeIndex(3)


def LoadConfig():
    if (CheckConfig()):
        GenerateConfig()
    configparser.read('config.ini')
    config.Camera = configparser.get("Camera", "cameraid")
    config.RemoteCamera = configparser.get("Camera", "remotecamera")
    config.ConfirmRoll = configparser.get("Game", "confirmroll")
    ui.LoadConfig(config)


def CheckConfig():
    """ Check if file is empty by confirming if its size is 0 bytes"""
    if (os.path.exists("config.ini")):
        print("FILE IS HERE")
        if (os.stat("config.ini").st_size == 0):
            print("FILE IS EMPTY")
            return True
        return False
    return True
