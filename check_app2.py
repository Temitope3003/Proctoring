
import tkinter as tk
from tkinter import messagebox
import psutil
import os

# Set of application names to ignore regardless of case
IGNORED_APPS = {"chrome.exe", "zoom.exe", "vlc.exe", "edge.exe", "microsoft edge.exe", 
                "wps.exe", "firefox.exe", "mozilla firefox.exe", "microsoft.exe", "word.exe", 
                "acroRd32.exe", "Spotify.exe", "Discord.exe", "Slack.exe", "Zoom.exe",
                "Skype.exe", "TeamViewer.exe", "Steam.exe", "Origin.exe", "Code.exe",
                "Dropbox.exe", "chrome.exe", "firefox.exe", "Photoshop.exe", "Word.exe",
                "Excel.exe", "PowerPoint.exe", "GIMP.exe", "vlc.exe", "Adobe Premiere Pro.exe",
                "iTunes.exe", "WinRAR.exe", "Illustrator.exe", "AfterFX.exe", "InDesign.exe",
                "Lightroom.exe", "audacity.exe", "obs64.exe", "filezilla.exe", "notepad++.exe",
                "ZoomIt.exe", "putty.exe", "blender.exe", "acad.exe", "maya.exe", "3dsmax.exe",
                "sublime_text.exe", "eclipse.exe", "idea.exe", "studio.exe", "devenv.exe",
                "paintdotnet.exe", "GitHubDesktop.exe", "HandBrake.exe", "soffice.exe", "Evernote.exe",
                "Teams.exe", "zoommtg.exe", "OneDrive.exe", "googledrivesync.exe", "slack.exe",
                "WhatsApp.exe", "Telegram.exe", "Signal.exe", "brave.exe", "tor.exe", "thunderbird.exe",
                "Acrobat.exe", "msedge.exe", "opera.exe",
                "VSCodePortable.exe", "AdobeFlashPlayer.exe", "TeamViewerQS.exe", "SkypeHost.exe", "slackhook.exe",
                "DropboxUpdate.exe", "DiscordPTB.exe", "SpotifyLauncher.exe", "zoom_installer.exe", "firefox.exe",
                "SteamTmp.exe", "BlenderPlayer.exe", "MayaBatch.exe", "3dsmaxcmd.exe", "Sublime Merge.exe", 
                "eclipsec.exe", "idea64.exe", "studio64.exe", "devenv.com", "git-bash.exe", 
                "notepad++.cmd", "ZoomIt64.exe", "puttytel.exe", "Google Chrome Canary.exe", "opera_developer.exe", 
                "WhatsAppSetup.exe", "TelegramDesktop.exe", "Signal-Desktop.exe", "tor-browser_en-US.exe", "thunderbird.exe",
                "minecraft.exe", "fortniteclient-win64-shipping.exe", "league of legends.exe", "valorant.exe",
                "csrss.exe", "dota2.exe", "steam.exe", "epicgameslauncher.exe", "gta5.exe", "pubg.exe",
                "witcher3.exe", "csgo.exe", "overwatch.exe", "warframe.exe", "rdr2.exe", "apex_legends.exe",
                "fifa22.exe", "rocketleague.exe", "valorant.exe", "fallguys_client.exe", "cyberpunk2077.exe",
                "battlefieldv.exe", "destiny2.exe", "far cry.exe", "reddeadredemption2.exe", "cyberpunk2077.exe",
                "doom.exe", "callofduty.exe", "ark.exe", "rainbowsix.exe", "msedge.exe"
                 "pes.exe", "pes2022.exe", "pes2021.exe", "pes2020.exe", "pes2019.exe", "pes2018.exe", "pes2017.exe"
}

# Set of process prefixes to ignore regardless of case
IGNORED_PROCESS_PREFIXES = {"system", "registry", "process","MemCompression","CodeSetup","csrss"}

# Function to check if a process should be ignored
def should_ignore_process(proc):
    # Check if the process name starts with any of the ignored prefixes, irrespective of case
    if proc.name().lower().startswith(tuple(prefix.lower() for prefix in IGNORED_PROCESS_PREFIXES)):
        return True
    # Check if the process name ends with ".exe" and not in the list of allowed apps
    if proc.name().lower().endswith(".exe") and proc.name().lower() not in IGNORED_APPS:
        return True
    return False

# Function to get a list of running user processes
def get_user_processes():
    user_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if not should_ignore_process(proc):
                user_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return user_processes

# Function to display message if user-installed applications are running
def display_message(user_processes):
    apps_to_close = []
    for proc in user_processes:
        try:
            apps_to_close.append(proc.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if apps_to_close:
        app_list = "\n".join(apps_to_close)
        messagebox.showinfo("Close Running Applications",
                            f"Please close the following applications before proceeding with the test:\n\n{app_list}")
        return True
    else:
        return False

# Main function to check and display message
def check_and_display():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    user_processes = get_user_processes()
    if display_message(user_processes):
        root.mainloop()

check_and_display()
