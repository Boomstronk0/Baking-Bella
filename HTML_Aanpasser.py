#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Voor didactisch gebruik aangepast door Robbe Wulgaert, Sint-Lievenscollege Gent.
Niet verspreiden zonder naamsvermelding
robbewulgaert.be
"""

import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

# Probeer BeautifulSoup te importeren, en installeer het indien nodig.
try:
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

def update_html():
    """
    Haalt de invoer van de gebruiker op, opent de index.html,
    wijzigt de <title>, <h1> en <h2> tags en slaat de wijzigingen op.
    """
    # Verkrijg de invoer van de gebruiker uit de GUI-velden
    title_text = title_entry.get().strip()
    h1_text = h1_entry.get().strip()
    h2_texts = [line.strip() for line in h2_text.get("1.0", tk.END).splitlines() if line.strip()]

    # Controleer of index.html bestaat in de huidige map
    if not os.path.exists("index.html"):
        messagebox.showerror("Fout", "index.html bestand niet gevonden in de huidige map.")
        return

    # Open en parse het HTML-bestand met BeautifulSoup
    with open("index.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Wijzig de inhoud van het <title> element
    if soup.title:
        soup.title.string = title_text

    # Wijzig alle <h1> elementen met de nieuwe H1 tekst
    h1_tags = soup.find_all("h1")
    for tag in h1_tags:
        tag.string = h1_text

    # Wijzig de <h2> elementen: elke regel van de invoer vervangt één <h2>
    h2_tags = soup.find_all("h2")
    for i, tag in enumerate(h2_tags):
        if i < len(h2_texts):
            tag.string = h2_texts[i]

    # Sla het aangepaste HTML-bestand op
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    messagebox.showinfo("Succes", "index.html succesvol bijgewerkt!")

# Zet het Tkinter-venster op
root = tk.Tk()
root.title("HTML Updater Tool")

# Invoerveld voor de nieuwe titel
tk.Label(root, text="Nieuwe Titel:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=0, column=1, padx=5, pady=5)

# Invoerveld voor de nieuwe H1 tekst
tk.Label(root, text="Nieuwe H1 Tekst:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
h1_entry = tk.Entry(root, width=50)
h1_entry.grid(row=1, column=1, padx=5, pady=5)

# Tekstvak voor de nieuwe H2 teksten (één per regel)
tk.Label(root, text="Nieuwe H2 Teksten (één per regel):").grid(row=2, column=0, padx=5, pady=5, sticky="ne")
h2_text = tk.Text(root, width=50, height=10)
h2_text.grid(row=2, column=1, padx=5, pady=5)

# Knop om de HTML bij te werken
update_button = tk.Button(root, text="Update HTML", command=update_html)
update_button.grid(row=3, column=0, columnspan=2, pady=10)

# Start de Tkinter hoofdloop
root.mainloop()
