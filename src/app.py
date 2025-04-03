import customtkinter as ctk
import os
import sys
import time
import subprocess
import platform
import signal
from threading import Thread
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

OS = platform.system()

def get_package_manager():
    if os.path.exists("/usr/bin/apt"):  # Debian, Ubuntu, Mint, Kali
        return "apt", "sudo apt update -y && sudo apt install -y"
    elif os.path.exists("/usr/bin/pacman"):  # Arch, Manjaro
        return "pacman", "sudo pacman -Sy --noconfirm"
    elif os.path.exists("/usr/bin/dnf"):  # Fedora
        return "dnf", "sudo dnf install -y"
    elif os.path.exists("/usr/bin/zypper"):  # OpenSUSE
        return "zypper", "sudo zypper install -y"
    elif os.path.exists("/usr/bin/yum"):  # RHEL, CentOS
        return "yum", "sudo yum install -y"
    else:
        console.print("[bold red]❌ Unknown package manager. Installation impossible.[/bold red]")
        sys.exit(1)

PACKAGE_MANAGER, INSTALL_CMD = get_package_manager()

def run_command(command, error_message):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        console.print(f"[red]❌ Error:[/red] {error_message}")
        console.print(f"[red]❌ Command output:[/red] {result.stderr}") 
        return False
    return True

def set_proxy(enabled):
    if OS == "Linux":
        desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()

        if "gnome" in desktop_env:  # GNOME
            if enabled:
                console.print("[cyan]🌐 Enabling proxy through Tor (127.0.0.1:9050) in GNOME...[/cyan]")
                os.system("gsettings set org.gnome.system.proxy mode 'manual'")
                os.system("gsettings set org.gnome.system.proxy.socks host '127.0.0.1'")
                os.system("gsettings set org.gnome.system.proxy.socks port 9050")
            else:
                console.print("[cyan]🚫 Disabling proxy in GNOME...[/cyan]")
                os.system("gsettings set org.gnome.system.proxy mode 'none'")

        elif "kde" in desktop_env:  # KDE
            if enabled:
                console.print("[cyan]🌐 Enabling proxy in KDE...[/cyan]")
                os.system("kwriteconfig5 --file kioslaverc --group 'Proxy Settings' --key ProxyType 2")
                os.system("kwriteconfig5 --file kioslaverc --group 'Proxy Settings' --key SocksProxy 127.0.0.1:9050")
            else:
                console.print("[cyan]🚫 Disabling proxy in KDE...[/cyan]")
                os.system("kwriteconfig5 --file kioslaverc --group 'Proxy Settings' --key ProxyType 0")

        elif "awesome" in desktop_env:  # Awesome WM
            console.print("[yellow]⚠ Proxy configuration for Awesome WM is not automated. Please configure manually.[/yellow]")

        elif "budgie" in desktop_env:  # Budgie
            console.print("[yellow]⚠ Proxy configuration for Budgie is not automated. Please configure manually.[/yellow]")

        elif "cinnamon" in desktop_env:  # Cinnamon
            if enabled:
                console.print("[cyan]🌐 Enabling proxy in Cinnamon...[/cyan]")
                os.system("gsettings set org.cinnamon.settings-daemon.plugins.proxy mode 'manual'")
                os.system("gsettings set org.cinnamon.settings-daemon.plugins.proxy.socks host '127.0.0.1'")
                os.system("gsettings set org.cinnamon.settings-daemon.plugins.proxy.socks port 9050")
            else:
                console.print("[cyan]🚫 Disabling proxy in Cinnamon...[/cyan]")
                os.system("gsettings set org.cinnamon.settings-daemon.plugins.proxy mode 'none'")

        elif "deepin" in desktop_env:  # Deepin
            console.print("[yellow]⚠ Proxy configuration for Deepin is not automated. Please configure manually.[/yellow]")

        elif "enlightenment" in desktop_env:  # Enlightenment
            console.print("[yellow]⚠ Proxy configuration for Enlightenment is not automated. Please configure manually.[/yellow]")

        elif "i3" in desktop_env:  # i3wm
            console.print("[yellow]⚠ Proxy configuration for i3wm is not automated. Please configure manually.[/yellow]")

        elif "icewm" in desktop_env:  # IceWM
            console.print("[yellow]⚠ Proxy configuration for IceWM is not automated. Please configure manually.[/yellow]")

        else:
            console.print("[yellow]⚠ Unknown or unsupported desktop environment, proxy not changed.[/yellow]")

    elif OS == "Windows":  # Windows (coming soon)
        if enabled:
            console.print("[cyan]🌐 Enabling proxy in Windows...[/cyan]")
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d "socks=127.0.0.1:9050" /f')
        else:
            console.print("[cyan]🚫 Disabling proxy in Windows...[/cyan]")
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f')

def install_tor():
    console.print("[green]📥 Installing Tor...[/green]")
    if not run_command(f"{INSTALL_CMD} tor torsocks", "Failed to install Tor"):
        return

    console.print("[green]🚀 Starting Tor service...[/green]")
    if not run_command("sudo systemctl start tor", "Failed to start Tor service"):
        return
    if not run_command("sudo systemctl enable tor", "Failed to enable Tor service auto-start"):
        return

    console.print("[bold green]✅ Tor is installed and running on 127.0.0.1:9050[/bold green]")
    set_proxy(False)

def change_ip():
    console.print("[blue]♻ Restarting Tor to change IP...[/blue]")
    if not run_command("sudo systemctl restart tor", "Failed to restart Tor"):
        return

    with Progress(SpinnerColumn(), TextColumn("[bold cyan]{task.description}[/bold cyan]")) as progress:
        task = progress.add_task("🔄 Changing IP...", total=5)
        for _ in range(5):
            time.sleep(0.5)
            progress.update(task, advance=1)
    
    console.print("[bold green]✅ IP changed![/bold green]")

def exit_program():
    console.print("\n[red]🛑 Stopping Tor...[/red]")
    run_command("sudo systemctl stop tor", "Failed to stop Tor")
    set_proxy(False)
    console.print("[bold red]👋 Tor is stopped. Exiting the program.[/bold red]")
    sys.exit(0)

def signal_handler(sig, frame):
    exit_program()

def toggle_connection():
    global connected

    if connected:
        status_label.configure(text="Disconnected", text_color="red")
        connect_button.configure(text="Connect")
        set_proxy(False)
        connected = False
    else:
        status_label.configure(text="Connected", text_color="green")
        connect_button.configure(text="Disconnect")
        set_proxy(True)
        connected = True

def animate_loading():
    
    loading_texts = ["IP changing .", "IP changing ..", "IP changing ..."]
    for i in range(15):  
        status_label.configure(text=loading_texts[i % len(loading_texts)], text_color="orange")
        time.sleep(0.33)

def gui_change_ip():

    
    loading_thread = Thread(target=animate_loading)
    loading_thread.start()

   
    app.after(5000, lambda: status_label.configure(text="Connected", text_color="green"))

def main():
    signal.signal(signal.SIGINT, signal_handler)

 
    install_tor()

   
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    global app, status_label, connect_button, connected  
    connected = False

    app = ctk.CTk()
    app.geometry("300x400")
    app.title("Tor VPN")
    app.resizable(False, False)

    
    title_label = ctk.CTkLabel(app, text="Tor VPN", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

 
    status_label = ctk.CTkLabel(app, text="Disconnected", font=("Arial", 16), text_color="red")
    status_label.pack(pady=10)


    connect_button = ctk.CTkButton(app, text="Connect", command=toggle_connection, width=150, height=40, corner_radius=20)
    connect_button.pack(pady=10)

   
    change_ip_button = ctk.CTkButton(app, text="Change IP", command=gui_change_ip, width=150, height=40, corner_radius=20)
    change_ip_button.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()
