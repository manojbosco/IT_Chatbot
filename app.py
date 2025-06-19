from flask import Flask, render_template, request, redirect, url_for,session

app = Flask(__name__)

app.secret_key = 'supersecretkey123'



# Sample QA database (very basic)
qa_pairs = {
    "how to reset my password": "To reset your password, go to Settings > Account > Reset Password. Follow the instructions to create a new password.",
    "wifi not working": "Try restarting your router and checking the network adapter. If the issue continues, contact IT support.",
    "system is slow": "Close unused programs, clear temporary files, and restart your computer. You can also check for malware.",
    "printer not working": "Ensure the printer is turned on, properly connected, and has paper and ink. Try restarting it or reinstalling drivers.",
    "blue screen error on startup": "This is often a sign of a hardware or driver issue. Try booting in Safe Mode and updating your drivers.",
    "email not syncing in outlook": "Check your internet connection and Outlook server settings. Try restarting Outlook or re-adding your account.",
    "cannot connect to vpn": "Verify your VPN credentials, internet connection, and firewall settings. Restart the VPN client.",
    "keyboard not responding": "Check if the keyboard is connected properly. Try using another port or restarting the computer.",
    "how to update antivirus software": "Open your antivirus application and look for an 'Update' button or setting. Click it to get the latest version.",
    "what to do when screen freezes": "Try pressing Ctrl + Alt + Del and open Task Manager to end unresponsive tasks. If that doesn't work, restart your PC.",
    "how to connect to wifi": "Go to Network Settings, choose your WiFi network from the list, and enter the password to connect.",
    "my mouse is not working": "Check if it’s plugged in or needs new batteries. Try it on another port or computer.",
    "computer not turning on": "Ensure the power cable is connected and the outlet is working. Try holding the power button for 10 seconds."
}
qa_pairs.update({
    "hello": "Hello! 😊 How can I assist you today?",
    "hi": "Hi there! 👋 What can I help you with?",
    "hey": "Hey! Need help with something?",
    "good morning": "Good morning! ☀️ How can I support you today?",
    "good afternoon": "Good afternoon! 🌞 What issue are you facing?",
    "good evening": "Good evening! 🌙 How can I help?",
    "what's up": "All good here! Let me know how I can help you.",
    "how are you": "I'm just a bot, but I'm functioning perfectly! 😄 What can I help you with today?"
})

qa_pairs.update({
    "laptop overheating": "Ensure your laptop is on a hard surface, clean the vents with compressed air, and avoid using it on beds or couches.",
    "how to install a printer driver": "Go to the printer manufacturer's website, download the latest driver for your model, and follow the installation instructions.",
    "monitor display issues": "Check the cable connections, ensure the monitor is powered on, and adjust display settings in your OS.",
    "getting too many pop-ups": "Run a malware scan using antivirus software and use a browser with pop-up blocking enabled.",
    "how to clean up disk space": "Use built-in tools like Disk Cleanup or delete temporary files and unused applications manually.",
    "my usb port is not working": "Try another port, restart your PC, or update the USB drivers from Device Manager.",
    "how to open task manager": "Press Ctrl + Shift + Esc or right-click the taskbar and select 'Task Manager'.",
    "slow internet connection": "Restart your modem/router, close background apps, and check for signal interference.",
    "outlook keeps crashing": "Try restarting Outlook in Safe Mode, disabling add-ins, or repairing the installation.",
    "how to recover deleted files": "Check the Recycle Bin first. Use recovery software if the files are permanently deleted.",
    "sound not working on my pc": "Check if your speakers are connected, ensure sound is not muted, and update audio drivers.",
    "microphone not detected": "Make sure it's plugged in, enabled in sound settings, and the correct input device is selected.",
    "webcam not working in zoom": "Check if Zoom has permission to use the camera and that no other app is using it simultaneously.",
    "how to change my windows password": "Press Ctrl + Alt + Del and select 'Change Password'. Follow the on-screen steps.",
    "i forgot my email password": "Go to your email provider’s login page and click 'Forgot password' to start the recovery process.",
    "battery draining too fast": "Lower screen brightness, close unused apps, and disable Bluetooth/Wi-Fi when not needed.",
    "software not opening": "Try running it as administrator, reinstalling, or checking for compatibility issues.",
    "my desktop icons disappeared": "Right-click the desktop > View > Show desktop icons. Also check if you’re in tablet mode.",
    "how to turn off startup apps": "Open Task Manager > Startup tab, right-click an app, and select 'Disable'.",
    "unable to install software": "Check if you have admin rights, enough disk space, and try running the installer as admin.",
    "system updates stuck": "Restart your system and check for updates again. You can also run the Windows Update troubleshooter.",
    "touchpad not working on laptop": "Make sure it’s enabled in settings, check the function key (Fn + touchpad icon), or update drivers.",
    "screen flickering issue": "Update display drivers, lower the refresh rate, or disable incompatible software.",
    "how to take a screenshot": "Press PrtScn to capture the screen or use Windows + Shift + S for snipping tool.",
    "my files are missing": "Check the Recycle Bin, recent files, and use file recovery tools if needed.",
    "how to connect to a projector": "Use HDMI/VGA cable, then press Windows + P to switch to projector mode.",
    "pc shuts down automatically": "Could be overheating or hardware issue. Check fan, run a virus scan, or test the battery.",
    "how to access shared folders": "Go to File Explorer, type the shared path (e.g., \\\\ComputerName\\SharedFolder), and press Enter.",
    "error code 403 - what does it mean?": "It means 'Forbidden' – the server is refusing to fulfill your request, often due to permissions.",
    "blocked from accessing a website": "Try another browser or device, check firewall settings, or use a VPN if necessary.",
    "my device is not recognized": "Check the device connection, restart your computer, or reinstall the device driver.",
    "how to run disk cleanup": "Type 'Disk Cleanup' in the start menu, select a drive, and follow the prompts.",
    "excel keeps crashing": "Try starting in Safe Mode, disabling add-ins, or repairing Office.",
    "word file is corrupted": "Open Word > File > Open > select the file > click the arrow on Open button > Open and Repair.",
    "how to remove a virus": "Run a full system scan with antivirus software and delete any threats found.",
    "how to use remote desktop": "Enable Remote Desktop in settings, get the IP address, and connect using the Remote Desktop app.",
    "printer showing offline": "Check if it's powered on, connected to the network, and set as default printer.",
    "outlook password prompt keeps popping up": "Check your saved credentials, update the password, or remove and re-add your account."
})
qa_pairs.update({
    "how to enable dark mode": "Go to Settings > Personalization > Colors and choose Dark mode.",
    "my files won’t open": "Check if the correct application is installed. Try restarting or updating it.",
    "how to empty recycle bin": "Right-click the Recycle Bin icon and select 'Empty Recycle Bin'.",
    "laptop making strange noises": "It could be the fan or hard drive. Save your work and get it checked.",
    "fan is too loud": "Clean the vents and ensure the laptop is on a hard, flat surface for airflow.",
    "how to change default browser": "Go to Settings > Apps > Default Apps > Web browser and choose your preferred one.",
    "browser is too slow": "Clear cache, disable extensions, and restart your browser.",
    "how to clear browser cache": "Go to your browser settings > Privacy > Clear browsing data.",
    "i clicked on a suspicious email": "Don’t click any links. Run a full antivirus scan and inform IT.",
    "how to schedule a scan": "In Windows Security, go to Virus & threat protection > Scan options > Microsoft Defender Offline scan.",
    "can’t open pdf files": "Install Adobe Reader or use a browser to open PDF files.",
    "how to zip and unzip files": "Right-click the file/folder > Send to > Compressed (zipped) folder or Extract All.",
    "how to find ip address": "Open Command Prompt and type `ipconfig` then press Enter.",
    "wifi keeps disconnecting": "Check router distance, reset the network, or update drivers.",
    "bluetooth not working": "Make sure it's turned on. Update drivers and restart your device.",
    "can’t login to the system": "Double-check your credentials or reset your password if needed.",
    "laptop screen is black": "Try a hard reboot or connecting to an external monitor.",
    "how to back up files": "Use File History or copy files to an external drive or cloud service.",
    "usb device not recognized": "Try a different port. If it still fails, update USB drivers.",
    "pc won't boot after update": "Boot into Safe Mode and uninstall recent updates.",
    "how to access bios settings": "Restart and press F2, F10, DEL, or ESC during startup (depends on brand).",
    "not receiving emails": "Check spam folder, storage limit, or server settings.",
    "how to block a sender in outlook": "Right-click the email > Junk > Block Sender.",
    "shared drive not accessible": "Ensure you're connected to the network and have permission.",
    "unable to print in color": "Check printer settings and replace low/empty color cartridges.",
    "how to check ram usage": "Open Task Manager > Performance tab > Memory.",
    "why is my disk at 100%": "Too many background processes. Disable startup apps, run disk cleanup.",
    "laptop camera is blurry": "Clean the lens and adjust video settings in the app.",
    "my cursor is stuck": "Try restarting or using an external mouse.",
    "how to change screen resolution": "Right-click desktop > Display settings > Display resolution.",
    "network drive disconnected": "Reconnect from File Explorer or map it again with credentials.",
    "how to run antivirus scan": "Open your antivirus software and click 'Scan Now' or use Windows Security.",
    "can't open microsoft teams": "Reinstall Teams or clear its cache folder and restart.",
    "teams microphone not working": "Check Teams settings and system audio settings. Make sure mic access is allowed.",
    "files won't download": "Check your internet and ensure browser download permissions are enabled.",
    "no internet access": "Restart router, check WiFi settings or try network troubleshooter.",
    "how to check system specs": "Right-click This PC > Properties or use the System Information tool.",
    "how to share my screen": "In Teams or Zoom, click the 'Share Screen' icon during a call.",
    "slow file transfer": "Use USB 3.0 ports and avoid background processes.",
    "how to install zoom": "Go to zoom.us, download the client, and follow the setup instructions.",
    "can’t access company portal": "Check VPN, login credentials, and firewall settings.",
    "how to connect second monitor": "Right-click desktop > Display settings > Detect and Extend displays.",
    "how to scan using printer": "Use printer’s software or Windows Fax & Scan utility.",
    "how to connect to a network printer": "Settings > Devices > Printers & scanners > Add a printer.",
    "error while opening excel": "Repair Office via Control Panel > Programs > Office > Change > Repair.",
    "laptop won’t wake up from sleep": "Check power settings and update graphics drivers.",
    "flickering laptop screen": "Check display cable, update drivers, or try adjusting refresh rate.",
    "pc won’t shut down": "Force shutdown by holding the power button. Check for background apps next time.",
    "disk read error occurred": "Check cables, run disk check (chkdsk), or use recovery tools.",
    "how to use command prompt": "Search 'cmd' in Start Menu. Use it to run commands like `ping`, `ipconfig`, etc."
})



def get_bot_response(user_input):
    print("User asked:", user_input)

    user_input_lower = user_input.strip().lower()

    # Try partial keyword match
    for question, answer in qa_pairs.items():
        if question in user_input_lower:
            return answer

    # If no match found, log it
    print("Unknown question detected. Logging...")
    with open("unknown_questions.txt", "a") as file:
        file.write(user_input + "\n")
    return "I'm not sure how to answer that yet. Let me get back to you!"



chat_history = []

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/clear', methods=['POST'])
def clear_chat():
    session.pop('chat_history', None)
    return redirect(url_for('home'))  # Make sure 'index' is your main route name



@app.route("/chat", methods=["GET", "POST"])
def chat():
    welcome_messages = [
        "👋 Hello! How can I help you today?",
        "Hi there! I'm your Helpdesk Assistant.",
        "Welcome! Ask me any IT-related question.",
        "Hey! Need any tech support?",
        "Hello! I'm here to help with your issues."
    ]
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "clear":
            session.pop('chat_history', None)
            return redirect(url_for("chat"))

        if action == "send":
            user_message = request.form["message"]
            session['chat_history'].append({"sender": "You", "text": user_message})

            response = get_bot_response(user_message)

            session['chat_history'].append({"sender": "Bot", "text": response})
            session.modified = True
            return redirect(url_for("chat"))



    return render_template("chat.html", chat_history=session.get('chat_history', []))

if __name__ == "__main__":
    app.run(debug=True)
