class FacebookSystem:
    users = {}

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.posts = []

    def register(self):
        FacebookSystem.users[self.email] = self

    def login(self, email, password):
        if email in FacebookSystem.users and FacebookSystem.users[email].password == password:
            return True
        else:
            return False

    def create_post(self, post):
        self.posts.append(post)
        print(f"{self.name} has posted: {post}")

    def view_posts(self):
        for post in self.posts:
            print(post)

class Facebook:
    def __init__(self):
        pass

    def menu(self):
        print("1. Register")
        print("2. Login")
        print("3. Create Post")
        print("4. View Posts")
        print("5. Exit")

    def run(self):
        while True:
            self.menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                user = FacebookSystem(name, email, password)
                user.register()

            elif choice == "2":
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                if user.login(email, password):
                    print("Login successful")
                else:
                    print("Invalid email or password")

            elif choice == "3":
                if user:
                    post = input("Enter your post: ")
                    user.create_post(post)
                else:
                    print("Please login first")

            elif choice == "4":
                if user:
                    user.view_posts()
                else:
                    print("Please login first")

            elif choice == "5":
                break

            else:
                print("Invalid choice")

if __name__ == "__main__":
    fb = Facebook()
    fb.run()