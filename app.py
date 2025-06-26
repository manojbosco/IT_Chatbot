from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

# -------------------------- QA FLOW --------------------------
qa_flow = {
    "How to reset my password?": {
        "Ask": "What type of device are you using?",
        "Options": ["Windows", "Mac", "Android", "iOS"],
        "Windows": {
            "Ask": "Which version of Windows are you using?",
            "Options": ["8", "10", "11"],
            "8": {
                "Ask": "What would you like to do?",
                "Options": ["How to reset login password?", "Forgot password?"],
                "How to reset login password?": "Go to Control Panel > User Accounts > Manage another account > Change the password.",
                "Forgot password?": "Use a password reset disk or boot into Safe Mode and use an admin account to reset it."
            },
            "10": {
                "Ask": "What would you like to do?",
                "Options": ["How to reset login password?", "Forgot password?"],
                "How to reset login password?": "Go to Settings > Accounts > Sign-in options > Password.",
                "Forgot password?": "Click 'Reset password' on the login screen and follow the instructions."
            },
            "11": {
                "Ask": "What would you like to do?",
                "Options": ["How to reset login password?", "Forgot password?"],
                "How to reset login password?": "Go to Settings > Accounts > Sign-in options > Password.",
                "Forgot password?": "Use the 'Reset password' option on the login screen or reset using a Microsoft account recovery."
            }
        },
        "Mac": {
            "Ask": "Which macOS version are you using?",
            "Options": ["Monterey", "Ventura", "Sonoma"],
            "Monterey": {
                "Ask": "What would you like to do?",
                "Options": ["Reset Mac password", "Forgot password options"],
                "Reset Mac password": "Restart and hold Command + R. Open Terminal from Utilities, then type `resetpassword` to reset.",
                "Forgot password options": "Use your Apple ID on the login screen to reset the password."
            },
            "Ventura": {
                "Ask": "What would you like to do?",
                "Options": ["Reset Mac password", "Forgot password options"],
                "Reset Mac password": "Restart and hold Command + R to enter recovery. Use Terminal and type `resetpassword`.",
                "Forgot password options": "Click the question mark or 'Forgot password' on login, then use Apple ID or FileVault recovery key."
            },
            "Sonoma": {
                "Ask": "What would you like to do?",
                "Options": ["Reset Mac password", "Forgot password options"],
                "Reset Mac password": "Boot into recovery (Command + R), go to Terminal, and type `resetpassword` to launch the reset tool.",
                "Forgot password options": "Choose 'Forgot password' at login and follow instructions using your Apple ID."
            }
        },
        "Android": {
            "Ask": "What is your phone brand?",
            "Options": ["Samsung", "Xiaomi", "OnePlus", "Other"],
            "Samsung": {
                "Ask": "What would you like to do?",
                "Options": ["Reset Android password", "Forgot pattern lock"],
                "Reset Android password": "Use Samsung's Find My Mobile (findmymobile.samsung.com) to unlock or reset password remotely.",
                "Forgot pattern lock": "Boot into Recovery Mode (Power + Volume Up + Bixby), then factory reset if needed."
            },
            "Xiaomi": {
                "Ask": "What would you like to do?",
                "Options": ["Reset Android password", "Forgot pattern lock"],
                "Reset Android password": "Use Xiaomi Cloud (i.mi.com) to locate and reset device if Find Device is enabled.",
                "Forgot pattern lock": "Use Recovery Mode (Power + Volume Up), then wipe data. Or use Mi PC Suite."
            },
            "OnePlus": {
                "Ask": "What would you like to do?",
                "Options": ["Reset Android password", "Forgot pattern lock"],
                "Reset Android password": "Go to Google's Find My Device to erase and reset your phone.",
                "Forgot pattern lock": "Enter Recovery Mode (Power + Volume Down) and perform a factory reset."
            },
            "Other": {
                "Ask": "What would you like to do?",
                "Options": ["Reset Android password", "Forgot pattern lock"],
                "Reset Android password": "Use Google Find My Device (google.com/android/find) to erase and reset the phone.",
                "Forgot pattern lock": "Use Recovery Mode: hold Power + Volume keys, then select factory reset (note: data will be lost)."
            }
        },
        "iOS": {
            "Ask": "Which iPhone model are you using?",
            "Options": ["Face ID", "Home Button", "Older"],
            "Face ID": {
                "Ask": "What would you like to do?",
                "Options": ["Reset iPhone password", "Reset Apple ID password"],
                "Reset iPhone password": "Put the device into recovery mode by pressing Volume Up, then Volume Down, then hold Side Button until you see the recovery screen. Connect to iTunes or Finder to restore.",
                "Reset Apple ID password": "Visit appleid.apple.com > Click 'Forgot Apple ID or password?' > Follow the instructions."
            },
            "Home Button": {
                "Ask": "What would you like to do?",
                "Options": ["Reset iPhone password", "Reset Apple ID password"],
                "Reset iPhone password": "Put the device into recovery mode: press and hold Home + Power button until recovery mode appears. Connect to iTunes or Finder to restore.",
                "Reset Apple ID password": "Go to appleid.apple.com > Select 'Forgot Apple ID or password' > Follow the on-screen steps."
            },
            "Older": {
                "Ask": "What would you like to do?",
                "Options": ["Reset iPhone password", "Reset Apple ID password"],
                "Reset iPhone password": "Use iTunes (if available) or Recovery Mode: hold Home + Power button until you see the iTunes logo. Restore the device.",
                "Reset Apple ID password": "Visit appleid.apple.com and click 'Forgot password' to reset."
            }
        }
    },
"WiFi not working": {
    "Ask": "Is your device connected to the WiFi network?",
    "Options": ["Yes", "No"],
    "Yes": {
        "Ask": "Can you access any websites?",
        "Options": ["Yes", "No"],
        "Yes": {
            "Answer": "Try restarting your router or forget and reconnect to the WiFi network."
        },
        "No": {
            "Answer": "Check if your internet service is active or contact your ISP."
        }
    },
    "No": {
        "Ask": "Is the WiFi option turned on?",
        "Options": ["Yes", "No"],
        "Yes": {
            "Answer": "Try reconnecting to the network or updating your network drivers."
        },
        "No": {
            "Answer": "Turn on WiFi from your device’s settings."
        }
    }
},

"System is slow": {
    "Ask": "What operating system are you using?",
    "Options": ["Windows", "macOS"],
    "Windows": {
        "Ask": "Have you recently installed any new software?",
        "Options": ["Yes", "No"],
        "Yes": {
            "Answer": "Try uninstalling the software or checking for background processes in Task Manager."
        },
        "No": {
            "Answer": "Try disk cleanup and disable startup programs."
        }
    },
    "macOS": {
        "Ask": "Do you have enough disk space?",
        "Options": ["Yes", "No"],
        "Yes": {
            "Answer": "Try resetting the SMC or checking Activity Monitor for heavy apps."
        },
        "No": {
            "Answer": "Free up space on your disk and restart the system."
        }
    }
},

"Printer not working": {
    "Ask": "Is your printer connected properly?",
    "Options": ["Yes", "No"],
    "Yes": {
        "Ask": "What issue are you facing?",
        "Options": ["Paper jam", "Driver issue", "Not printing"],
        "Paper jam": {
            "Answer": "Turn off the printer and clear any jammed paper inside carefully."
        },
        "Driver issue": {
            "Answer": "Reinstall or update the printer driver from the manufacturer’s website."
        },
        "Not printing": {
            "Answer": "Check if the printer is set as default and has enough ink or toner."
        }
    },
    "No": {
        "Answer": "Check the cable connections or reconnect the printer via Bluetooth or WiFi."
    }
},


    "How to troubleshoot my computer system?": {
        "Ask": "What operating system are you using?",
        "Options": ["Windows", "macOS", "Linux", "Other"],
        "Windows": {
            "Ask": "What happens when you press the power button?",
            "Options": ["It turns on normally", "Nothing happens"],
            "It turns on normally": {
                "Ask": "Do you see any lights or hear any startup sounds?",
                "Options": ["Yes, I see lights and hear sounds", "No lights or sounds"],
                "Yes, I see lights and hear sounds": {
                    "Ask": "Is the monitor showing any display?",
                    "Options": ["Yes, I can see something", "No, nothing appears"],
                    "Yes, I can see something": {
                        "Ask": "What do you see on the screen?",
                        "Options": ["Manufacturer's logo appears", "No logo, just blank screen"],
                        "Manufacturer's logo appears": {
                            "Ask": "Does the system continue to load the operating system?",
                            "Options": ["Yes, it boots up", "No, it doesn't go beyond the logo"],
                            "Yes, it boots up": {
                                "Ask": "Can you reach the login screen and log in successfully?",
                                "Options": ["Yes, I can log in", "No, login fails or freezes"],
                                "Yes, I can log in": {
                                    "Ask": "Is your internet connection working?",
                                    "Options": ["Yes, the internet works", "No, the internet is not working"],
                                    "Yes, the internet works": {
                                        "Ask": "Are you facing problems with specific applications?",
                                        "Options": ["Yes, a particular app is problematic", "No, apps are working fine"],
                                        "Yes, a particular app is problematic": {
                                            "Ask": "Which application is causing issues?",
                                            "Options": ["Browser", "Office Suite", "Games", "Other"],
                                            "Browser": {
                                                "Ask": "What browser issue are you experiencing?",
                                                "Options": ["Slow performance", "Crashes", "Won't load pages"],
                                                "Slow performance": {
                                                    "Ask": "Have you cleared cache and cookies recently?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Try disabling extensions or resetting browser settings."
                                                    },
                                                    "No": {
                                                        "Answer": "Clear browser cache and cookies first."
                                                    }
                                                },
                                                "Crashes": {
                                                    "Ask": "Does it crash immediately or after some use?",
                                                    "Options": ["Immediately", "After some use"],
                                                    "Immediately": {
                                                        "Answer": "Try reinstalling the browser."
                                                    },
                                                    "After some use": {
                                                        "Answer": "Check for memory leaks in Task Manager."
                                                    }
                                                },
                                                "Won't load pages": {
                                                    "Ask": "Can you ping websites from Command Prompt?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Reset browser network settings."
                                                    },
                                                    "No": {
                                                        "Answer": "Check your DNS settings."
                                                    }
                                                }
                                            },
                                            "Office Suite": {
                                                "Ask": "What Office application is problematic?",
                                                "Options": ["Word", "Excel", "PowerPoint", "Outlook"],
                                                "Word": {
                                                    "Ask": "Does it crash when opening files?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Try repairing Office installation."
                                                    },
                                                    "No": {
                                                        "Answer": "Check for conflicting add-ins."
                                                    }
                                                },
                                                "Excel": {
                                                    "Ask": "Are formulas calculating correctly?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Check for macro conflicts."
                                                    },
                                                    "No": {
                                                        "Answer": "Verify calculation settings."
                                                    }
                                                },
                                                "PowerPoint": {
                                                    "Ask": "Do animations play correctly?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Check graphics driver."
                                                    },
                                                    "No": {
                                                        "Answer": "Try converting to basic transitions."
                                                    }
                                                },
                                                "Outlook": {
                                                    "Ask": "Are emails syncing properly?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Check rules and filters."
                                                    },
                                                    "No": {
                                                        "Answer": "Rebuild Outlook profile."
                                                    }
                                                }
                                            },
                                            "Games": {
                                                "Ask": "What game issue are you experiencing?",
                                                "Options": ["Won't launch", "Low FPS", "Graphics glitches"],
                                                "Won't launch": {
                                                    "Ask": "Do you get any error message?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Search for the specific error code online."
                                                    },
                                                    "No": {
                                                        "Answer": "Verify game files integrity."
                                                    }
                                                },
                                                "Low FPS": {
                                                    "Ask": "Have you updated graphics drivers?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Lower in-game graphics settings."
                                                    },
                                                    "No": {
                                                        "Answer": "Update graphics drivers first."
                                                    }
                                                },
                                                "Graphics glitches": {
                                                    "Ask": "Does this happen in other games?",
                                                    "Options": ["Yes", "No"],
                                                    "Yes": {
                                                        "Answer": "Check GPU temperature and stability."
                                                    },
                                                    "No": {
                                                        "Answer": "Reinstall the game's graphics drivers."
                                                    }
                                                }
                                            },
                                            "Other": {
                                                "Ask": "What specific issue are you facing?",
                                                "Options": ["Crashes", "Slow performance", "Feature not working"],
                                                "Crashes": {
                                                    "Answer": "Check application logs for error details."
                                                },
                                                "Slow performance": {
                                                    "Answer": "Monitor resource usage in Task Manager."
                                                },
                                                "Feature not working": {
                                                    "Answer": "Check application documentation for requirements."
                                                }
                                            }
                                        },
                                        "No, apps are working fine": {
                                            "Ask": "Is your system running slower than usual?",
                                            "Options": ["Yes, it feels slow", "No, it works smoothly"],
                                            "Yes, it feels slow": {
                                                "Ask": "Have you checked Task Manager for high resource usage?",
                                                "Options": ["Yes", "No"],
                                                "Yes": {
                                                    "Answer": "Consider upgrading hardware if consistently high."
                                                },
                                                "No": {
                                                    "Answer": "Check Task Manager first to identify bottlenecks."
                                                }
                                            },
                                            "No, it works smoothly": {
                                                "Answer": "Your system appears to be functioning properly."
                                            }
                                        }
                                    },
                                    "No, the internet is not working": {
                                        "Ask": "Have you tried basic troubleshooting?",
                                        "Options": ["Yes", "No"],
                                        "Yes": {
                                            "Answer": "Contact your ISP for further assistance."
                                        },
                                        "No": {
                                            "Answer": "Restart router and check physical connections first."
                                        }
                                    }
                                },
                                "No, login fails or freezes": {
                                    "Ask": "Does this happen in Safe Mode?",
                                    "Options": ["Yes", "No"],
                                    "Yes": {
                                        "Answer": "Perform system restore or clean install."
                                    },
                                    "No": {
                                        "Answer": "Disable startup programs and services."
                                    }
                                }
                            },
                            "No, it doesn't go beyond the logo": {
                                "Ask": "Can you access BIOS/UEFI settings?",
                                "Options": ["Yes", "No"],
                                "Yes": {
                                    "Answer": "Check boot order and hardware diagnostics."
                                },
                                "No": {
                                    "Answer": "Reset CMOS or check motherboard."
                                }
                            }
                        },
                        "No logo, just blank screen": {
                            "Ask": "Does your monitor show any signs of life?",
                            "Options": ["Yes", "No"],
                            "Yes": {
                                "Answer": "Check GPU and display connections."
                            },
                            "No": {
                                "Answer": "Test with another monitor if possible."
                            }
                        }
                    },
                    "No, nothing appears": {
                        "Ask": "Is your monitor powered on?",
                        "Options": ["Yes", "No"],
                        "Yes": {
                            "Answer": "Check video cable connections."
                        },
                        "No": {
                            "Answer": "Ensure monitor is plugged in and powered."
                        }
                    }
                },
                "No lights or sounds": {
                    "Ask": "Is the power cable properly connected?",
                    "Options": ["Yes", "No"],
                    "Yes": {
                        "Answer": "Test with another power outlet."
                    },
                    "No": {
                        "Answer": "Securely connect power cable first."
                    }
                }
            },
            "Nothing happens": {
                "Ask": "Is the power supply switched on?",
                "Options": ["Yes", "No"],
                "Yes": {
                    "Answer": "Check internal power connections."
                },
                "No": {
                    "Answer": "Turn on power supply first."
                }
            }
        },
        "macOS": {
            "Ask": "What happens when you press the power button?",
            "Options": ["It turns on normally", "Nothing happens"],
            "It turns on normally": {
                "Ask": "Do you see any lights or hear the startup chime?",
                "Options": ["Yes", "No"],
                "Yes": {
                    "Ask": "What do you see on the screen?",
                    "Options": ["Apple logo", "Blank screen", "Question mark folder"],
                    "Apple logo": {
                        "Ask": "Does it complete the boot process?",
                        "Options": ["Yes", "No"],
                        "Yes": {
                            "Answer": "Proceed with normal troubleshooting."
                        },
                        "No": {
                            "Answer": "Boot in Safe Mode (hold Shift)."
                        }
                    },
                    "Blank screen": {
                        "Answer": "Reset NVRAM (Command+Option+P+R)."
                    },
                    "Question mark folder": {
                        "Answer": "Recovery Mode (Command+R) to reinstall macOS."
                    }
                },
                "No": {
                    "Answer": "Check power adapter and battery."
                }
            },
            "Nothing happens": {
                "Answer": "Try SMC reset (specific key combo for your model)."
            }
        },
        "Linux": {
            "Ask": "What happens when you boot?",
            "Options": ["Boots normally", "Kernel panic", "Black screen"],
            "Boots normally": {
                "Answer": "Check system logs for errors."
            },
            "Kernel panic": {
                "Answer": "Boot previous kernel version."
            },
            "Black screen": {
                "Answer": "Try text mode (Ctrl+Alt+F1)."
            }
        },
        "Other": {
            "Ask": "What symptoms are you experiencing?",
            "Options": ["Won't power on", "Boots but crashes", "Performance issues"],
            "Won't power on": {
                "Answer": "Check power supply and connections."
            },
            "Boots but crashes": {
                "Answer": "Check system logs for errors."
            },
            "Performance issues": {
                "Answer": "Monitor resource usage."
            }
        }
    }
}

# --------------------- BOT RESPONSE LOGIC ---------------------
def get_bot_response(user_input):
    user_input_clean = user_input.strip()
    user_input_lower = user_input_clean.lower()

    matched_key = next((key for key in qa_flow if key.lower() == user_input_lower), None)

    # ✅ Log unknown root-level inputs immediately
    if matched_key is None and not session.get("path"):
        with open("unknown_questions.txt", "a") as f:
            f.write(user_input + "\n")

    if matched_key:
        session['path'] = [matched_key]
        current = qa_flow[matched_key]
        ask = current.get("Ask")
        options = current.get("Options", [])
        return ask, options

    if "path" not in session or not isinstance(session.get("path", []), list):
        session['path'] = []

    path = session['path']
    current = qa_flow
    for step in path:
        current = current.get(step, {})

    if user_input_clean in current:
        path.append(user_input_clean)
        session['path'] = path
        next_node = current[user_input_clean]

        if isinstance(next_node, dict):
            # ✅ If final answer node is reached
            if "Answer" in next_node:
                session.pop('path', None)
                return next_node["Answer"], []

            ask = next_node.get("Ask")
            options = next_node.get("Options", [])
            if ask:
                return ask, options

            return "\n".join(f"- {k}" for k in next_node if k != "Ask"), []

        else:
            session.pop('path', None)
            return next_node, []
    else:
        # Save unknown input even during flow
        with open("unknown_questions.txt", "a") as f:
            f.write(f"{' > '.join(path)} > {user_input}\n")

        return "Sorry, I couldn’t understand that. Please contact tech support for assistance.", []

    # Fallback logging (in case something goes wrong)
    with open("unknown_questions.txt", "a") as f:
        f.write(user_input + "\n")

    return "Sorry, I couldn't understand that. Please try rephrasing.", []

# ------------------------ ROUTES ------------------------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/thankyou", methods=["POST"])
def thankyou():
    session.pop("chat_history", None)
    return "", 204  # Just a successful empty response

@app.route('/clear', methods=['POST'])
def clear_chat():
    session.pop('chat_history', None)
    session.pop('path', None)
    return redirect(url_for('home'))



@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        # Only clear chat if the user is manually visiting the page or opening a new tab
        if not request.referrer or not request.referrer.endswith("/chat"):
            session.pop('chat_history', None)
            session.pop('path', None)

    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "clear":
            session.pop('chat_history', None)
            session.pop('path', None)
            return redirect(url_for("chat"))

        if action == "send":
            user_message = request.form["message"]
            session['chat_history'].append({"sender": "You", "text": user_message})

            response, options = get_bot_response(user_message)
            new_bot_msg = {"sender": "Bot", "text": response}
            if options:
                new_bot_msg["options"] = options

            # remove old options
            for msg in session['chat_history']:
                if msg["sender"] == "Bot":
                    msg.pop("options", None)

            session['chat_history'].append(new_bot_msg)
            session.modified = True
            return redirect(url_for("chat"))

    return render_template("chat.html", chat_history=session.get('chat_history', []))


# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    app.run(debug=True)
