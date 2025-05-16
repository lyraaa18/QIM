import os
import json
import datetime

HISTORY_FILE = "invoice_history.json"

def add_to_history(invoice_number, recipient, total_amount, file_path):
    history = load_history()
    
    new_entry = {
        "invoice_number": invoice_number,
        "recipient": recipient,
        "total_amount": total_amount,
        "file_path": file_path,
        "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    history.append(new_entry)
    
    save_history(history)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    else:
        return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def get_history():
    history = load_history()
    
    history.sort(key=lambda x: x.get("date_created", ""), reverse=True)
    
    return history

def open_invoice(file_path):
    if os.path.exists(file_path):
        try:
            import platform
            system = platform.system()
            
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":
                import subprocess
                subprocess.call(["open", file_path])
            else: 
                import subprocess
                subprocess.call(["xdg-open", file_path])
            
            return True
        except:
            return False
    else:
        return False