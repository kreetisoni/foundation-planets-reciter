import tkinter as tk
import win32com.client
import random
import pygame
from tkinter import Scale
import requests
from bs4 import BeautifulSoup
import re
import threading
import os
import json
import io
import asyncio
from tkinter import scrolledtext

CACHE_FILE = "planets.json"

def fetch_planets():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            planets = json.load(f)
        return planets

    url = 'https://foundation-fanon.fandom.com/wiki/List_of_planets'
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        planet_names = []

        content_div = soup.find('div', class_='mw-parser-output')
        for li in content_div.find_all('li'):
            text = li.get_text(" ", strip=True)
            if text and re.match(r'^[A-Za-z0-9\s\-]+$', text):
                if any(skip in text.lower() for skip in ['category', 'privacy', 'about', 'help']):
                    continue
                planet_names.append(text)

        planet_names = sorted(set(planet_names), reverse=True)

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(planet_names, f, ensure_ascii=False, indent=2)

        return planet_names
    except requests.exceptions.RequestException:
        print("⚠️ Could not fetch planets online. Using offline cache if available.")
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

planet_names = fetch_planets()
if not planet_names:
    planet_names = ["No planets available"]  


speaker = win32com.client.Dispatch("SAPI.SpVoice")
pygame.mixer.init()

url = "https://github.com/kreetisoni/foundation-planets-reciter/raw/refs/heads/main/nebula.ogg"
response = requests.get(url)
mp3_data = io.BytesIO(response.content)

pygame.mixer.music.load(mp3_data)
pygame.mixer.music.play(-1)

HOST = "127.0.0.1"
PORT = 8888

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
        self.list_frame = tk.Frame(root, bg="black")
        self.list_frame.place(x=20, y=150, width=100, height=400)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.planet_listbox = tk.Listbox(
            self.list_frame, bg="black", fg="cyan",
            font=("Helvetica", 12), yscrollcommand=self.scrollbar.set
        )
        self.planet_listbox.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.planet_listbox.yview)

        for planet in self.planets:
            self.planet_listbox.insert("end", planet)

        self.page_title = self.canvas.create_text(
            400, 100,
            text="Seldon’s Stellar Codex \n   (In reverse order :))",
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
        def __init__(self, root, planets):
        # ... your existing UI setup ...

        # 📌 Chat Section
        self.chat_box = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=40, height=15, bg="black", fg="white"
        )
        self.chat_box.place(x=300, y=350)

        self.chat_entry = tk.Entry(root, width=30, bg="black", fg="cyan")
        self.chat_entry.place(x=300, y=560)

        self.send_btn = tk.Button(
            root, text="Send", command=self.send_message,
            bg="cyan", fg="black"
        )
        self.send_btn.place(x=550, y=555)

        # Start background networking thread
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_network, daemon=True).start()

    def start_network(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run_client())

    async def run_client(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
        while True:
            data = await self.reader.readline()
            if not data:
                break
            message = data.decode().strip()
            self.display_message(message)

    def send_message(self):
        msg = self.chat_entry.get().strip()
        if msg:
            self.writer.write((msg + "\n").encode())
            asyncio.run_coroutine_threadsafe(self.writer.drain(), self.loop)
            self.chat_entry.delete(0, tk.END)

    def display_message(self, msg):
        self.chat_box.insert(tk.END, msg + "\n")
        self.chat_box.see(tk.END)

    def animate_stars(self):
        for star, size in self.stars:
            self.canvas.move(star, 0, size * 0.2)
            x1, y1, x2, y2 = self.canvas.coords(star)
            if y1 > 600:
                new_x = random.randint(0, 800)
                self.canvas.coords(star, new_x, 0, new_x+size, size)
        self.root.after(50, self.animate_stars)

    def fade_in_text(self, planet, step=0):
        if step > 15:
            return
        color = f"#00{step*10:02x}{step*10:02x}"
        self.canvas.itemconfig(self.label, text=planet, fill=color)
        self.root.after(50, lambda: self.fade_in_text(planet, step+1))

    def show_planet(self):
        if not self.running or self.index >= len(self.planets):
            self.running = False
            return

        planet = self.planets[self.index]
        self.fade_in_text(planet)
        self.planet_listbox.selection_clear(0, "end")
        self.planet_listbox.selection_set(self.index)
        self.planet_listbox.see(self.index)  


        
        threading.Thread(target=lambda: speaker.Speak(planet), daemon=True).start()

        self.index += 1
        self.root.after(2500, self.show_planet)

    def start(self):
        if not self.running:
            self.running = True
            self.index = 0
            self.show_planet()

    def stop(self):
        self.running = False
        #to stop TTS asap
        speaker.Speak("")  

def on_close():
    pygame.mixer.music.stop()
    pygame.quit()
    root.destroy()

icon_url = "https://github.com/kreetisoni/foundation-planets-reciter/raw/refs/heads/main/icon.ico"
icon_path = "icon_temp.ico"

# Download icon if not already present
if not os.path.exists(icon_path):
    response = requests.get(icon_url)
    with open(icon_path, "wb") as f:
        f.write(response.content)

root = tk.Tk()
root.iconbitmap(icon_path)  # set the icon
app = PlanetRecitor(root, planet_names)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
