from configparser import ConfigParser
config = ConfigParser()


class Config():
    Music = 0
    Effects = 0
    Camera = ""
    RemoteCamera = ""


global ui

def getui(d):
    global ui
    ui = d

def GenerateConfig():
    config.add_section("Sound")
    config.add_section("Camera")
    config.set("Sound",'Music',str(100))
    config.set("Sound",'Effects',str(100))
    config.set("Camera","CameraID",str(""))
    config.set("Camera","RemoteCamera",str(""))


def SaveConfig():
    from Logic import Ui_Logic
    global ui
    for i in Ui_Logic.CamRadioButtons:
        if(i.isChecked()):
            config.set("Camera","CameraID",i.text().replace(" ","_"))
            if(i.text() == "Remote Camera"):
                config.set("Camera","RemoteCamera",ui.GetCameraAddress())
    with open('config.ini','w') as configfile:
        config.write(configfile)

def LoadConfig():

    Config.Music = config.get("Sound","Music")
    Config.Effects = config.get("Sound","Effects")
    Config.Camera = config.get("Camera","CameraID")
    Config.RemoteCamera = config.get("Camera","RemoteCamera")


if(len(config.read('config.ini'))==0):
    GenerateConfig()
else:
    LoadConfig()



