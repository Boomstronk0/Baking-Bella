import os
import sys
import webbrowser
import subprocess
from sys import platform

# Probeer tkinter te importeren; als dit niet lukt, gebruik dan de CMD-interface
try:
    import tkinter as tk
    from tkinter import messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

# Dit project is van Robbe Wulgaert, auteur van 'AI in de Klas'.
# Meer informatie op www.robbewulgaert.be

def get_download_path():
    """Geeft het standaard downloadpad terug voor het huidige besturingssysteem."""
    if platform == 'win32':
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    elif platform == 'darwin':  # macOS
        return os.path.join(os.environ['HOME'], 'Downloads')
    else:
        return os.path.join(os.environ['HOME'], 'Downloads')

def find_sketch_js(download_path):
    """Zoekt naar het bestand sketch.js binnen de mappenstructuur."""
    # Voeg debugging statements toe
    print(f"Begint met zoeken naar sketch.js in {download_path}")
    for root, dirs, files in os.walk(download_path):
        print(f"Doorzoekt map: {root}")
        if "sketch.js" in files:
            print(f"sketch.js gevonden in: {root}")
            return os.path.join(root, "sketch.js")
    print("sketch.js niet gevonden in de standaard Downloads-map. Probeer specifieke submap.")
    
    # Probeer in specifieke submap te zoeken
    specific_path = os.path.join(download_path, "4- HTML-bestanden", "sketch.js")
    if os.path.exists(specific_path):
        print(f"sketch.js gevonden op specifieke locatie: {specific_path}")
        return specific_path
    else:
        print(f"sketch.js niet gevonden op specifieke locatie: {specific_path}")
    
    return None

def find_chrome_path():
    """Zoekt het pad naar Google Chrome op verschillende besturingssystemen."""
    if platform == 'win32':
        mogelijke_paden = [
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
            'C:/Program Files/Google/Chrome/Application/chrome.exe'
        ]
    elif platform == 'darwin':  # macOS
        mogelijke_paden = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
    elif platform.startswith('linux'):  # Linux
        mogelijke_paden = ['/usr/bin/google-chrome', '/usr/bin/chromium-browser']
    else:
        mogelijke_paden = []

    for pad in mogelijke_paden:
        if os.path.exists(pad):
            #return f'"{pad}" %s --incognito'
            return f'"{pad}" %s'
    return None

def start_server_and_open_browser():
    """Start de HTTP-server en opent de webapplicatie in de browser."""
    try:
        # Ga naar de directory waar sketch.js zich bevindt
        download_path = get_download_path()
        sketch_js_path = find_sketch_js(download_path)
        if not sketch_js_path:
            print("Fout: sketch.js niet gevonden.")
            return None
        target_directory = os.path.dirname(sketch_js_path)
        
        if not os.path.exists(target_directory):
            print(f"Fout: Directory niet gevonden: {target_directory}")
            return None

        print(f"Veranderen van directory naar: {target_directory}")  # Debugging output
        os.chdir(target_directory)

        # Start de HTTP-server
        print("Starten van de HTTP-server op poort 8000...")  # Debugging output
        server = subprocess.Popen([sys.executable, '-m', 'http.server'])

        # Open de browser
        url = "http://localhost:8000"
        chrome_path = find_chrome_path()
        
        if chrome_path:
            print(f"Opening URL in Google Chrome: {url}")  # Debugging output
            webbrowser.get(chrome_path).open_new(url)
        else:
            print("Google Chrome niet gevonden. De standaardbrowser wordt geopend.")
            print(f"Opening URL: {url}")  # Debugging output
            webbrowser.open_new(url)

        return server  # Return de server om later te kunnen afsluiten
    except Exception as e:
        print(f"Het starten van de HTTP-server is mislukt: {e}")
        return None

def main():
    # Geen behoefte meer aan pyserial of COM-poort selectie
    # Start de server en open de browser direct

    # Als GUI beschikbaar is, gebruik deze
    if GUI_AVAILABLE:
        try:
            # Maak de GUI
            root = tk.Tk()
            root.title("AI Model Starter")
            root.geometry("400x200")
            root.resizable(False, False)

            # Titel
            title_label = tk.Label(root, text="AI Model Starter", font=("Helvetica", 16))
            title_label.pack(pady=10)

            # Instructies
            instructions = tk.Label(root, text="Klik op de knop om de AI applicatie te starten.", font=("Helvetica", 12))
            instructions.pack(pady=5)

            # Startknop
            def start_button_clicked():
                # Start de server en open de browser
                server = start_server_and_open_browser()
                if not server:
                    messagebox.showerror("Fout", "Kon de HTTP-server niet starten.")
                    return

                # Sluit de GUI
                root.destroy()

                # Wacht tot de gebruiker het proces afsluit
                try:
                    server.wait()
                except KeyboardInterrupt:
                    server.terminate()

            start_button = tk.Button(root, text="Start AI Model", command=start_button_clicked)
            start_button.pack(pady=20)

            # Informatie over het project
            info_label = tk.Label(root, text="Dit project is van Robbe Wulgaert, auteur van 'AI in de Klas'.\nMeer informatie op www.robbewulgaert.be", font=("Helvetica", 9), fg="blue", cursor="hand2")
            info_label.pack(side="bottom", pady=10)
            info_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.robbewulgaert.be"))

            root.mainloop()
        except Exception as e:
            print(f"Er is een fout opgetreden in de GUI: {e}")
            fallback_cmd_interface()
    else:
        # Als GUI niet beschikbaar is, gebruik de CMD-interface
        fallback_cmd_interface()

def fallback_cmd_interface():
    """Fallback naar command-line interface als GUI niet beschikbaar is."""
    try:
        print("GUI niet beschikbaar. We schakelen over naar de command-line interface.")

        input("Druk op Enter om de AI applicatie te starten...")

        # Start de server en open de browser
        server = start_server_and_open_browser()
        if not server:
            print("Kon de HTTP-server niet starten.")
            return

        # Wacht tot de gebruiker het proces afsluit
        try:
            server.wait()
        except KeyboardInterrupt:
            server.terminate()
    except Exception as e:
        print(f"Er is een onverwachte fout opgetreden: {e}")
    finally:
        input("Druk op Enter om te sluiten...")

if __name__ == "__main__":
    main()
