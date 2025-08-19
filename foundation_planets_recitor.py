import tkinter as tk
import win32com.client
import random
import pygame
from tkinter import Scale, HORIZONTAL

#1
planets = [
    "61 Cygni", "Alpha", "Anacreon", "Askone", "Asperta", "Aurora",
    "Baronn", "Bonde", "Cil", "Cinna", "Comporellon", "Daribow",
    "Derowd", "Earth", "Eos", "Erytho", "Euterpe", "Florina",
    "Fomalhaut", "Gaia", "Gamma Andromeda", "Getorin", "Glyptal IV",
    "Haven", "Helicon", "Hesperos", "Horleggor", "Ifni", "Iss",
    "Jennisek", "Kalgan", "Konom", "Korell", "Libair", "Lingane",
    "Livia", "Loris", "Lyonesse", "Lystena", "Mandress", "Melpomenia",
    "Mnemon", "Mores", "Neotrantor", "Nephelos", "Nexon", "Nishaya",
    "Ophiuchus", "Orsha II", "Pallas", "Pleiades", "Radole", "Rhampora",
    "Rhodia", "Rhea", "Rigel", "Rossem", "Salinn", "Santanni", "Sarip",
    "Sark", "Sayshell", "Sirius", "Siwenna", "Smitheus", "Smushyk",
    "Smyrno", "Solaria", "Synnax", "Tazenda", "Terel", "Terminus",
    "Trantor", "Tyrann", "Vega", "Vincetori", "Voreg", "Wanda",
    "Wencory", "Zoranel"
]

planets.sort(reverse=True)


speaker = win32com.client.Dispatch("SAPI.SpVoice")


pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\kreet\Downloads\deep-grounding-earth-bowl-vibrations-388623.mp3")
pygame.mixer.music.play(-1)  
#2
class PlanetRecitor:
    def __init__(self, root, planets):
        self.root = root
        self.planets = planets
        self.index = 0
        self.running = False

        self.root.title("Foundation Planets Recitor 🌌")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

       
        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        
        self.page_title = self.canvas.create_text(
            400, 100,  # x, y position
            text="Seldon’s Stellar Codex \n   (In reverse order :))",  # your epic page title
            fill="magenta",
            font=("Helvetica", 36, "bold")
        )

        
        self.stars = []
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.randint(1, 3)
            star = self.canvas.create_oval(x, y, x+size, y+size, fill="white", outline="")
            self.stars.append((star, size))
        self.animate_stars()

        
        self.label = self.canvas.create_text(
            400, 280, text="", fill="cyan", font=("Helvetica", 44, "bold")
        )

        
        self.start_btn = tk.Button(
            root, text="▶ Start Recital", command=self.start,
            font=("Arial", 14, "bold"),
            fg="black", bg="cyan", activebackground="#00b3b3",
            relief="flat", padx=10, pady=5
        )
        self.start_btn.place(x=220, y=530)

        
        self.stop_btn = tk.Button(
            root, text="⏹ Stop", command=self.stop,
            font=("Arial", 14, "bold"),
            fg="black", bg="red", activebackground="#b30000",
            relief="flat", padx=10, pady=5
        )
        self.stop_btn.place(x=420, y=530)

        
        self.volume_slider = Scale(
            root, from_=0, to=100, orient='vertical',  
            command=self.set_volume, label="    ",
            length=250, bg="black", fg="cyan"
        )
        self.volume_slider.set(50)  
        self.volume_slider.place(x=700, y=150) 
        self.volume_label = tk.Label(
            root,
            text="M\nu\ns\ni\nc\n\nV\no\nl\nu\nm\ne",
            bg="black",
            fg="cyan",
            font=("Helvetica", 10, "bold")
)
        self.volume_label.place(x=745, y=180) 

   
    def set_volume(self, val):
        volume = int(val) / 100
        pygame.mixer.music.set_volume(volume)

    def animate_stars(self):
        for star, size in self.stars:
            self.canvas.move(star, 0, size * 0.2)
            x1, y1, x2, y2 = self.canvas.coords(star)
            if y1 > 600:
                new_x = random.randint(0, 800)
                self.canvas.coords(star, new_x, 0, new_x+size, size)
        self.root.after(50, self.animate_stars)

    def fade_in_text(self, planet, step=30):
        if step > 255:
            return
        color = f"#{0:02x}{step:02x}{step:02x}"
        self.canvas.itemconfig(self.label, text=planet, fill=color)
        self.root.after(50, lambda: self.fade_in_text(planet, step+15))
    
    def show_planet(self):
        if not self.running or self.index >= len(self.planets):
            self.running = False
            return

        planet = self.planets[self.index]
        self.fade_in_text(planet)

        
        speaker.Speak(planet, 1)

        self.index += 1
        self.root.after(2500, self.show_planet)

    def start(self):
        if not self.running:
            self.running = True
            self.index = 0
            self.show_planet()

    def stop(self):
        self.running = False
        speaker.Speak("", 2)


def on_close():
    pygame.mixer.music.stop()
    pygame.quit()
    root.destroy()


root = tk.Tk()
app = PlanetRecitor(root, planets)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

