#Welcome to Hogwats
import json
class Wizard:
    def __init__(self, name, house, iD):
        self.name = name
        self.house = house
        self.iD = iD
    def __str__(self):
        return f"ID: {self.iD}, Name: {self.name}, House: {self.house}"
    def __repr__(self):
        return self._str_()
    def to_dict(self):
        return {"name": self.name, "house": self.house, "iD": self.iD}
    @staticmethod
    def from_dict(data):
        return Wizard(data['name'], data['house'], data['iD'])
 
class Hogwarts:
    def __init__(self):
        self.wizards = {}        
        self.graduated = {}
        self.expelled = {}
    # To add new students in Hogwarts
    def enroll_wizards(self):
        name = input("Enter the name of the student: ").strip()
        house = input("Enter the house of the student: ").strip()
        try:
            iD = int(input("Enter the ID of the student: "))
        except ValueError:
            print("Invalid ID. Please enter a number!")
            return
        for category, record in [("active", self.wizards), ("graduated", self.graduated), ("expelled", self.expelled)]:
            if iD in record:
                existing = record[iD]
                print(f"ID already exists for {existing.name} in {existing.house} ({category}). Try again.")  
                return
        wizard = Wizard(name, house, iD)
        self.wizards[wizard.iD] = wizard
        print(f"{wizard.name}, Welcome to Hogwarts! Have a wonderful journey!")
    # Deleting students
    def delete_wizard(self):
        try:
            iD = int(input("Enter ID to delete: "))
        except ValueError:
            print("Invalid ID.")
            return
        for status_dict in [self.wizards, self.graduated, self.expelled]:
            if iD in status_dict:
                removed = status_dict.pop(iD)
                print(f"Deleted wizard: {removed.name}")
                return
        print("Wizard not found.")
    # Expelling students
    def expel_wizard(self):
        try:
            iD = int(input("Enter the ID of the student to expel: "))
        except ValueError:
            print("Invalid ID. Please enter a number!")
            return
        if iD in self.wizards:  
            expel_wizard = self.wizards.pop(iD)
            print(f"{expel_wizard.name}, has been expelled from Hogwarts for violating the school's rules. Let this be a warning to others.")
            self.expelled[iD] = expel_wizard
        else:
            print("Student with that ID was not found")
    # Marking students as graduate   
    def graduate_wizard(self):
        try:
            iD = int(input("Enter the ID of the student: "))
        except ValueError:
            print("Invalid ID. Please enter a number!")
            return
        if iD in self.wizards:
            wizard = self.wizards.pop(iD)  
            self.graduated[iD] = wizard    
            print(f"{wizard.name} has successfully graduated from Hogwarts. Congratulations on a successful journey!")
        else:
            print("Wizard with this ID not found.")
    # Updating details of students
    def update_wizard(self):
        try:
            iD = int(input("Enter the student's ID to update: "))
            if iD in self.wizards:
                wizard = self.wizards[iD]
                print(f"Current Details: Name: {wizard.name}, House: {wizard.house}, ID: {wizard.iD}")                
                new_name = input("Enter the updated name (or press Enter to keep the same): ").strip()  
                new_house = input("Enter the updated house (or press Enter to keep the same): ").strip()  
                if new_name:
                    wizard.name = new_name
                if new_house:
                    wizard.house = new_house
                print(f"Updated Details: Name: {wizard.name}, house: {wizard.house},  iD: {wizard.iD}")
            else:
                print("Student's ID not found")
        except ValueError:
            print("Invalid input! Please enter a valid numeric ID.")
    # Search wizards by ID
    def wizard_by_iD(self):
        try:
            iD = int(input("Enter the ID: "))
            if iD in self.wizards:
                wizard = self.wizards[iD]
                print(f"Wizard Found: Name: {wizard.name}, House: {wizard.house}, ID: {wizard.iD}")
            else:
                print("No wizard found with that ID.")
        except ValueError:
            print("Invalid ID. Please enter a number.")
    # Search wizards by Name
    def search_by_name(self):
        name = input("Enter the name: ").strip()
        found_wizards = [wizard for wizard in self.wizards.values() if wizard.name.lower() == name.lower()]  
        if found_wizards:
            for wizard in found_wizards:
                print(f"Name: {wizard.name}")       
        else:
            print("No wizard found with that name.")
    # Search wizards by house
    def search_by_house(self):
        house = input("Enter the name of the house: ").strip()
        found_wizards = [wizard for wizard in self.wizards.values() if wizard.house.lower() == house.lower()] 
        if found_wizards:
            print(f"Wizards in {house.title()}: ")
            for wizard in found_wizards:
                print(wizard)       
        else:
            print("No wizard found with that house.")        
    # List of all the students that are active
    def list_active(self):
        if not self.wizards:
            print("No active students at the moment.")
            return
        print("List of Active Students: ")
        for wizard in self.wizards.values():
            print(wizard)
        print(f"Total: {len(self.wizards)} students.\n")
    # List of all the students those who have graduated
    def list_graduated(self):
        if not self.graduated:
            print("No students have graduated at the moment.")
            return
        print("List of Graduated Students: ")
        for graduated in self.graduated.values():
            print(graduated)
        print(f"Total: {len(self.graduated)} students.\n")
    # List of all the expelled students
    def list_expelled(self):
        if not self.expelled:
            print("No students have been expelled at the moment.")
            return
        print("List of Expelled Students: ")
        for expelled in self.expelled.values():
            print(expelled)
        print(f"Total: {len(self.expelled)} students.\n")        
    # Save data
    def save_data(self, filename):
        data = {
            "active": [wizard.to_dict() for wizard in self.wizards.values()],
            "graduated": [wizard.to_dict() for wizard in self.graduated.values()],
            "expelled": [wizard.to_dict() for wizard in self.expelled.values()]
        }
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Data successfully saved to {filename}.")
        except Exception as e:
            print(f"Error saving data: {e}")
    # Load data
    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            self.wizards.clear()
            self.graduated.clear()
            self.expelled.clear()
            self.wizards = {w['iD']: Wizard.from_dict(w) for w in data.get("active", [])}
            self.graduated = {w['iD']: Wizard.from_dict(w) for w in data.get("graduated", [])}
            self.expelled = {w['iD']: Wizard.from_dict(w) for w in data.get("expelled", [])}
            print(f"Data successfully loaded from {filename}.")
        except FileNotFoundError:
            print(f"No such file: {filename}")
        except json.JSONDecodeError:
            print(f"File {filename} is not a valid JSON file.")
        except Exception as e:
            print(f"Error loading data: {e}")
    # Get all wizards
    def get_all_wizards(self):
        print("All Wizards at Hogwarts (Grouped by Status):\n")
        print("Active:")
        for w in self.wizards.values():
            print(w)
        print("\nGraduated:")
        for w in self.graduated.values():
            print(w)
        print("\nExpelled:")
        for w in self.expelled.values():
            print(w)
    # Get status
    def get_status(self):
        try:
            iD = int(input("Enter the wizard ID: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        for status, record in [('Active', self.wizards), ('Graduated',  self.graduated), ('Expelled', self.expelled)]:
            if iD in record:
                wizard = record[iD]
                print(f"{wizard.name} is currently {status}.")
                return
        print("No wizard found with that ID.")
    # Change wizard status
    def change_status(self):
        try:
            iD = int(input("Enter the ID: "))
        except ValueError:
            print("Invalid input. ID must be a number.")
            return
        if iD in self.wizards:
            current_status = 'active'
        elif iD in self.graduated:
            current_status = 'graduated'
        elif iD in self.expelled:
            current_status = 'expelled'
        else:
            print("ID not found in any record. Please enroll the wizard first.")
            return
        print(f"Current status: {current_status.capitalize()}")
        print("Choose new status: ")
        try:
            choice = int(input("1. Active\n2. Graduated\n3. Expelled: "))
        except ValueError:
            print("Invalid choice. Must be 1, 2, or 3.")
            return
        target_status_map = {1: 'active', 2: 'graduated', 3: 'expelled'}
        new_status = target_status_map.get(choice)
        if new_status == current_status:
            print("Wizard is already in that status.")
            return
        if current_status == 'active':
            wizard = self.wizards.pop(iD)
        elif current_status == 'graduated':
            wizard = self.graduated.pop(iD)
        else:
            wizard = self.expelled.pop(iD)
        if new_status == 'active':
            self.wizards[iD] = wizard
        elif new_status == 'graduated':
            self.graduated[iD] = wizard
        else:
            self.expelled[iD] = wizard
        print(f"{wizard.name}'s status changed to {new_status}.")        
# Main Menu Loop for Hogwarts Wizard Management System
# hogwarts = Hogwarts()
# menu = """
# --- Welcome to Hogwarts Wizard Management System ---
# 1. Enroll Wizard
# 2. Expel Wizard
# 3. Graduate Wizard
# 4. Update Wizard Details
# 5. Search Wizard by ID
# 6. Search Wizard by Name
# 7. Search Wizard by House
# 8. List Active Wizards
# 9. List Graduated Wizards
# 10. List Expelled Wizards
# 11. Delete Wizard
# 12. Save Data to File
# 13. Load Data from File
# 14. Show All Wizards
# 15. Get Wizard Status
# 16. Change Wizard Status
# 17. Exit
# """
# while True:
#     print(menu)
#     try:
#         choice = int(input("Enter your choice (1 to 17): "))
#     except ValueError:
#         print("Invalid input. Please enter a number between 1 and 17.\n")
#         continue
#     if choice == 1:
#         hogwarts.enroll_wizards()
#     elif choice == 2:
#         hogwarts.expel_wizard()
#     elif choice == 3:
#         hogwarts.graduate_wizard()
#     elif choice == 4:
#         hogwarts.update_wizard()
#     elif choice == 5:
#         hogwarts.wizard_by_iD()
#     elif choice == 6:
#         hogwarts.search_by_name()
#     elif choice == 7:
#         hogwarts.search_by_house()
#     elif choice == 8:
#         hogwarts.list_active()
#     elif choice == 9:
#         hogwarts.list_graduated()
#     elif choice == 10:
#         hogwarts.list_expelled()
#     elif choice == 11:
#         hogwarts.delete_wizard()
#     elif choice == 12:
#         file = input("Enter filename to save (e.g., data.json): ")
#         hogwarts.save_data(file)
#     elif choice == 13:
#         file = input("Enter filename to load (e.g., data.json): ")
#         hogwarts.load_data(file)
#     elif choice == 14:
#         hogwarts.get_all_wizards()
#     elif choice == 15:
#         hogwarts.get_status()
#     elif choice == 16:
#         hogwarts.change_status()
#     elif choice == 17:
#         print("Thank you for using the Hogwarts Wizard Management System!")
#         break
#     else:
#         print("Invalid choice. Please select from the menu.\n")