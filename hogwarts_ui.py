import tkinter as tk
from tkinter import messagebox, simpledialog
from hogwarts_core import Hogwarts, Wizard

hogwarts = Hogwarts()
hogwarts.load_data("hogwarts_data.json")  # Auto-load

def enroll():
    name = name_entry.get()
    house = house_entry.get()
    try:
        iD = int(id_entry.get())
    except:
        messagebox.showerror("Error", "ID must be a number.")
        return

    for group in (hogwarts.wizards, hogwarts.graduated, hogwarts.expelled):
        if iD in group:
            messagebox.showwarning("Duplicate ID", f"Wizard with ID {iD} already exists.")
            return

    hogwarts.wizards[iD] = Wizard(name, house, iD)
    hogwarts.save_data("hogwarts_data.json")
    messagebox.showinfo("Enrolled", f"{name} enrolled to {house} with ID {iD}.")
    clear_entries()

def graduate():
    iD = get_id()
    if iD is None: return
    if iD in hogwarts.wizards:
        wizard = hogwarts.wizards.pop(iD)
        hogwarts.graduated[iD] = wizard
        hogwarts.save_data("hogwarts_data.json")
        messagebox.showinfo("Graduated", f"{wizard.name} has graduated.")
    else:
        messagebox.showwarning("Not Found", "Wizard not found in active list.")

def expel():
    iD = get_id()
    if iD is None: return
    if iD in hogwarts.wizards:
        wizard = hogwarts.wizards.pop(iD)
        hogwarts.expelled[iD] = wizard
        hogwarts.save_data("hogwarts_data.json")
        messagebox.showinfo("Expelled", f"{wizard.name} has been expelled.")
    else:
        messagebox.showwarning("Not Found", "Wizard not found in active list.")

def update():
    iD = get_id()
    if iD is None or iD not in hogwarts.wizards:
        messagebox.showwarning("Not Found", "Wizard not found.")
        return
    wizard = hogwarts.wizards[iD]
    new_name = simpledialog.askstring("Update", "Enter new name (Leave blank to keep unchanged):")
    new_house = simpledialog.askstring("Update", "Enter new house (Leave blank to keep unchanged):")
    if new_name:
        wizard.name = new_name
    if new_house:
        wizard.house = new_house
    hogwarts.save_data("hogwarts_data.json")
    messagebox.showinfo("Updated", f"Wizard {iD} updated.")

def search_by_id():
    iD = get_id()
    if iD is None: return
    for group in (hogwarts.wizards, hogwarts.graduated, hogwarts.expelled):
        if iD in group:
            display_text(f"{group[iD]}")
            return
    display_text("Wizard not found.")

def search_by_name():
    name = simpledialog.askstring("Search", "Enter wizard's name:")
    if not name:
        return
    result = [str(w) for w in hogwarts.wizards.values() if w.name.lower() == name.lower()]
    display_text("\n".join(result) if result else "No match found.")

def search_by_house():
    house = simpledialog.askstring("Search", "Enter house name:")
    if not house:
        return
    result = [str(w) for w in hogwarts.wizards.values() if w.house.lower() == house.lower()]
    display_text("\n".join(result) if result else "No match found.")

def list_wizards(group_name):
    group = getattr(hogwarts, group_name)
    display_text("\n".join(str(w) for w in group.values()) or "No wizards found.")

def delete():
    iD = get_id()
    if iD is None: return
    for group in (hogwarts.wizards, hogwarts.graduated, hogwarts.expelled):
        if iD in group:
            name = group[iD].name
            del group[iD]
            hogwarts.save_data("hogwarts_data.json")
            messagebox.showinfo("Deleted", f"Wizard {name} deleted.")
            return
    messagebox.showwarning("Not Found", "Wizard not found.")

def save():
    hogwarts.save_data("hogwarts_data.json")
    messagebox.showinfo("Saved", "Data saved successfully.")

def load():
    hogwarts.load_data("hogwarts_data.json")
    messagebox.showinfo("Loaded", "Data loaded successfully.")

def show_all():
    full = []
    for title, group in [("Active", hogwarts.wizards), ("Graduated", hogwarts.graduated), ("Expelled", hogwarts.expelled)]:
        full.append(f"{title} Wizards:")
        full.extend(str(w) for w in group.values())
        full.append("\n")
    display_text("\n".join(full))

def get_status():
    iD = get_id()
    if iD is None: return
    for label, group in [("Active", hogwarts.wizards), ("Graduated", hogwarts.graduated), ("Expelled", hogwarts.expelled)]:
        if iD in group:
            messagebox.showinfo("Status", f"{group[iD].name} is {label}.")
            return
    messagebox.showwarning("Not Found", "Wizard not found.")

def change_status():
    iD = get_id()
    if iD is None: return
    group_map = {"Active": hogwarts.wizards, "Graduated": hogwarts.graduated, "Expelled": hogwarts.expelled}
    current_group = None
    for group in group_map.values():
        if iD in group:
            wizard = group[iD]
            current_group = group
            break
    else:
        messagebox.showwarning("Not Found", "Wizard not found.")
        return

    status = simpledialog.askstring("Change Status", "Enter new status (Active / Graduated / Expelled):")
    if not status or status.title() not in group_map:
        return messagebox.showerror("Invalid", "Invalid status input.")
    new_group = group_map[status.title()]
    if wizard:
        del current_group[iD]
        new_group[iD] = wizard
        hogwarts.save_data("hogwarts_data.json")
        messagebox.showinfo("Changed", f"{wizard.name}'s status changed to {status.title()}.")

def clear_entries():
    name_entry.delete(0, tk.END)
    house_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)

def get_id():
    try:
        return int(id_entry.get())
    except:
        messagebox.showerror("Error", "Enter a valid ID.")
        return None

def display_text(content):
    display.delete("1.0", tk.END)
    display.insert(tk.END, content)

# --- GUI ---
root = tk.Tk()
root.title("Hogwarts Wizard Management")
root.geometry("750x600")

# Labels and entries
tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="House").grid(row=1, column=0)
tk.Label(root, text="ID").grid(row=2, column=0)

name_entry = tk.Entry(root)
house_entry = tk.Entry(root)
id_entry = tk.Entry(root)

name_entry.grid(row=0, column=1, padx=5, pady=5)
house_entry.grid(row=1, column=1, padx=5, pady=5)
id_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons (2 per row)
btns = [
    ("Enroll", enroll), ("Expel", expel),
    ("Graduate", graduate), ("Update", update),
    ("Search by ID", search_by_id), ("Search by Name", search_by_name),
    ("Search by House", search_by_house), ("List Active", lambda: list_wizards("wizards")),
    ("List Graduated", lambda: list_wizards("graduated")), ("List Expelled", lambda: list_wizards("expelled")),
    ("Delete", delete), ("Save", save),
    ("Load", load), ("Show All", show_all),
    ("Get Status", get_status), ("Change Status", change_status)
]

for i, (label, cmd) in enumerate(btns):
    tk.Button(root, text=label, width=18, command=cmd).grid(row=4 + i // 2, column=i % 2, padx=10, pady=5)

# Display area
display = tk.Text(root, height=12, width=85)
display.grid(row=14, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()