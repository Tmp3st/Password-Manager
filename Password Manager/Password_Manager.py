from cryptography.fernet import Fernet

class PasswordManager:
    
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
   
    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read() 
    
    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)
    
    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode())

    def add_password(self, site, password):
        self.password_dict[site] = password 

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password( self, site):
        return self.password_dict[site]

 
def main():
    password = {
        "Gmail": "thisisatest",
        "Instagram": "instapass",
        "Netflix": "netpass"
    }
    
    pm = PasswordManager()        
    
    print("""Hello! What would you like to do?
    (1) Create a new master key
    (2) Load an existing master key
    (3) Create a new password file
    (5) Add a new password
    (6) Show existing passwords
    (e) Exit
    """)
    
    done = False

    while not done:

        choice = input("Please enter a choice. ")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("Enter path: ")
            pm.load_password_file(path)
        elif choice == "5":
            site = input("Enter the site: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)
        elif choice == "6":
            site = input("Which site would you like the password for? ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "e":
            done = True
            print("Goodbye.")
        else:
            print("Invalid choice.")



if __name__ == "__main__":
    main()




