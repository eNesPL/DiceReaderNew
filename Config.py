from configparser import ConfigParser
from Logic import Ui_Logic
config = ConfigParser()
config.read('config.ini')



def save():
    for i in Ui_Logic.CamRadioButtons:
        if(i.isChecked()):
            print(i.text)