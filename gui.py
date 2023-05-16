from tkinter import *
from typing import Optional, Tuple, Union
import customtkinter
import pokedata
from PIL import Image
import requests
from io import BytesIO
import os
import urllib3.util.connection
import math

urllib3.util.connection.HAS_IPV6 = False



customtkinter.set_appearance_mode("light")
colorThemesPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "colorThemes")
customtkinter.set_default_color_theme(os.path.join(colorThemesPath, "customStyle.json"))
imagePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")


class root(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("485x350")
        self.title("Pokédex")
        
        self.smallFont = customtkinter.CTkFont(family="Helvetica", size=14)
        self.bigFont = customtkinter.CTkFont(family="Helvetica", size=15, weight="bold")
        self.iconbitmap(default=os.path.join(imagePath, "icon.ico"))
        
        self.grid_columnconfigure(0, weight=1)

        
        self.searchFrame = customtkinter.CTkFrame(self, corner_radius=0)
        self.searchFrame.grid(row=0, column=0, sticky="nsew")
        self.searchFrame.grid_rowconfigure(4, weight=1)
        
        self.entry = customtkinter.CTkEntry(self.searchFrame, placeholder_text="Pokémon name", width=200)
        self.entry.grid(row=0, column=0, padx=20, pady=10)
        self.entry.bind('<Key-Return>', self.fetchPokemon)

        
        self.mglassImage = customtkinter.CTkImage(Image.open(os.path.join(imagePath, "mglassLight.png")), size=(16, 16))

        self.button = customtkinter.CTkButton(self.searchFrame, image=self.mglassImage, text="", width=20, corner_radius=14)
        self.button.grid(row=0, column=1, padx=0, pady=0)
        self.button.bind("<Button-1>", self.fetchPokemon)

        self.artSwitchVar = customtkinter.StringVar(value="sprite")
        self.artSwitch = customtkinter.CTkSwitch(self.searchFrame, variable=self.artSwitchVar, onvalue="artwork", offvalue="sprite", command=self.artSwitchEvent, text="Use artwork", progress_color="#AD262E", button_color="#9E2028", button_hover_color="#831C22", fg_color="#FF6F6A", text_color="white", font=self.smallFont)
        self.artSwitch.grid(row=0, column=2, padx=20, pady=0)

        self.infoFrame = customtkinter.CTkFrame(self, fg_color="transparent") #defining it for later

        self.toplevel_window = None

        self.isShowingPokemon = False

        self.after(200, lambda: self.entry.focus()) #focus on entry widget


    def updateData(self, newData):
        self.isShowingPokemon = True
        #Image and name
        self.buildImage(newData["spriteUrl"], newData["artworkUrl"])
        self.name.configure(text=("#" + str(newData["dexNumber"]) + "  " + newData["name"]))
        #Types
        self.buildTypes(newData["dualType"], newData["firstType"], newData["secondType"])
        self.infoFrameC2 = customtkinter.CTkFrame(self.infoFrame, fg_color="transparent")
        self.infoFrameC2.grid(row=0, column=1, sticky="wn", pady=0)

        dexEntry = str(newData["dexEntry"]).replace('\n', " ").replace('\x0c', " ")
        
        self.textEntry = customtkinter.CTkTextbox(self.infoFrameC2, width=240, height=98, font=self.smallFont, fg_color="#DB3E39", text_color="#FFFFFF", scrollbar_button_color="#FD7878", scrollbar_button_hover_color="#ED5B5B", wrap="word")
        self.textEntry.insert("0.0", dexEntry)
        self.textEntry.grid(row=0, column=0, padx=0, pady=15, sticky="wne")

        

        self.statFrame = customtkinter.CTkFrame(self.infoFrameC2, fg_color="transparent")
        self.statFrame.grid(row=1, column=0, sticky="wn", pady=0)

        self.statNameFrame = customtkinter.CTkFrame(self.statFrame, fg_color="transparent")
        self.statNameFrame.grid(row=0, column=0, sticky="wn", pady=0)

        self.statLevelFrame = customtkinter.CTkFrame(self.statFrame, fg_color="transparent")
        self.statLevelFrame.grid(row=0, column=1, sticky="wn", pady=0)
        
        #HP
        self.statHP = customtkinter.CTkLabel(self.statNameFrame, text="HP", font=self.smallFont)
        self.statHP.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.statHPImg = customtkinter.CTkLabel(self.statLevelFrame, text="", image= self.getStatBarImage(newData["HP"]))
        self.statHPImg.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="w")

        #Atk
        self.statAtk = customtkinter.CTkLabel(self.statNameFrame, text="Atk", font=self.smallFont)
        self.statAtk.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        self.statAtkImg = customtkinter.CTkLabel(self.statLevelFrame, text="", image= self.getStatBarImage(newData["Attack"]))
        self.statAtkImg.grid(row=1, column=1, padx=(10, 0), pady=0, sticky="w")

        #Def
        self.statDef = customtkinter.CTkLabel(self.statNameFrame, text="Def", font=self.smallFont)
        self.statDef.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        self.statDefImg = customtkinter.CTkLabel(self.statLevelFrame, text="", image= self.getStatBarImage(newData["Defence"]))
        self.statDefImg.grid(row=2, column=1, padx=(10, 0), pady=0, sticky="w")
        
        #SpAtk
        self.statSpAtk = customtkinter.CTkLabel(self.statNameFrame, text="SpAtk", font=self.smallFont)
        self.statSpAtk.grid(row=3, column=0, padx=0, pady=0, sticky="w")
        self.statSpAtkImg = customtkinter.CTkLabel(self.statLevelFrame, text="", image= self.getStatBarImage(newData["SpecialAttack"]))
        self.statSpAtkImg.grid(row=3, column=1, padx=(10, 0), pady=0, sticky="w")

        #SpDef
        self.statSpDef = customtkinter.CTkLabel(self.statNameFrame, text="SpDef", font=self.smallFont)
        self.statSpDef.grid(row=4, column=0, padx=0, pady=0, sticky="w")
        self.statSpDefImg = customtkinter.CTkLabel(self.statLevelFrame, text="", image= self.getStatBarImage(newData["SpecialDefense"]))
        self.statSpDefImg.grid(row=4, column=1, padx=(10, 0), pady=0, sticky="w")

        #Spd
        self.statSpd = customtkinter.CTkLabel(self.statNameFrame, text="Spd", font=self.smallFont)
        self.statSpd.grid(row=5, column=0, padx=0, pady=0, sticky="w")
        self.statSpdImg = customtkinter.CTkLabel(self.statLevelFrame, text="", image= self.getStatBarImage(newData["Speed"]))
        self.statSpdImg.grid(row=5, column=1, padx=(10, 0), pady=0, sticky="w")

        
    def fetchPokemon(self, event):
        if self.entry.get() != "":
            try:
                self.data = pokedata.fetchPokemon(self.entry.get())
                self.updateData(self.data)
            except Exception as e:
                self.openAlertWindow(e)
    
    def buildImage(self, spriteUrl, artworkUrl):
        
        self.infoFrame.destroy()#destroy previous info frame to create a new one

        self.infoFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.infoFrame.grid(row=1, column=0, sticky="w")
        self.infoFrame.grid_rowconfigure(1, weight=1)

        self.infoFrameC1 = customtkinter.CTkFrame(self.infoFrame, fg_color="transparent")
        self.infoFrameC1.grid(row=0, column=0, sticky="wn")
        self.infoFrameC1.grid_rowconfigure(1, weight=1)

        if self.artSwitchVar.get() == "sprite":
            pokemonImageResponse = requests.get(spriteUrl, timeout=5)
            pokemonImage = Image.open(BytesIO(pokemonImageResponse.content)).convert('RGBA').resize((192,192), Image.Resampling.NEAREST) #I use NEAREST here to not get blurry pixels
        else:
            pokemonImageResponse = requests.get(artworkUrl, timeout=5)
            pokemonImage = Image.open(BytesIO(pokemonImageResponse.content)).convert('RGBA').resize((192,192))


        
        shadowImage = Image.open(os.path.join(imagePath, "shadow.png")).convert('RGBA').resize((158, 77), Image.Resampling.NEAREST)

        #Expanding shadow image to be the same size as the pokemon image for alpha compositing
        transparentImage = Image.new('RGBA', (192, 192), (0, 0, 0, 0))
        transparentImage.paste(shadowImage, (19,114))

        #Joining both images
        pokemonImage = Image.alpha_composite(transparentImage, pokemonImage)
        
        image = customtkinter.CTkImage(light_image=pokemonImage, dark_image=pokemonImage, size=(192, 192))


        self.name = customtkinter.CTkLabel(self.infoFrameC1, text="  Pokemon name", image=image, compound="top", font= self.bigFont)
        self.name.grid(row=0, column=0, padx=20, pady=0)
    
    def buildTypes(self, dualType, firstType, secondType):
        
        type1path = os.path.join(imagePath, "types\\type" + str(firstType).capitalize() + ".png")
        type2path = os.path.join(imagePath, "types\\type" + str(secondType).capitalize() + ".png")

        self.typeFrame = customtkinter.CTkFrame(self.infoFrameC1, fg_color="transparent")
        self.typeFrame.grid(row=1, column=0)
        self.typeFrame.grid_rowconfigure(1, weight=1)


        self.type1 = customtkinter.CTkImage(Image.open(type1path), size=(77,34))
        self.labeltest = customtkinter.CTkLabel(self.typeFrame, text="", image= self.type1)
        self.labeltest.grid(row=0, column=0, padx=5, pady=5)

        if dualType:
            self.type2 = customtkinter.CTkImage(Image.open(type2path), size=(77,34))
            self.labeltest = customtkinter.CTkLabel(self.typeFrame, text="", image= self.type2)
            self.labeltest.grid(row=0, column=1, padx=5, pady=5)

    def openAlertWindow(self, message):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AlertWindow(message) 
        else:
            self.toplevel_window.focus()
    
    def artSwitchEvent(self):
        if self.isShowingPokemon:
            self.updateData(self.data)

    def calculateStatLevel(self, baseStat):
        baseStat = (baseStat * 10)/260
        baseStat = math.ceil(baseStat)
        return baseStat

    def getStatBarImage(self, baseStat):
        statLevel = self.calculateStatLevel(baseStat)
        statBarPath = os.path.join(imagePath, "stat bars\\statbar-" + str(statLevel) + ".png")
        return customtkinter.CTkImage(Image.open(statBarPath), size=(188,21))



    

class AlertWindow(customtkinter.CTkToplevel):
    def __init__(self, message):
        super().__init__()
        self.grab_set()
        self.geometry("370x130")
        self.title("Error")
        self.iconbitmap(default=os.path.join(imagePath, "icon.ico"))

        self.grid_columnconfigure(0, weight=1)
        self.messageText = customtkinter.CTkLabel(self, text=message)
        self.messageText.grid(row=0, column=0, padx=20, pady=20)

        self.okButton = customtkinter.CTkButton(self, text="Ok", fg_color="#DB3E39", hover_color="#AD262E", command=self.closeAlert)
        self.okButton.grid(row=1, column=0, padx=20, pady=0)
    
    def closeAlert(self):
        self.destroy()

    


app = root()
app.mainloop()
