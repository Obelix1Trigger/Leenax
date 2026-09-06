from core.chat import Chat

leenax = Chat()

print("🤖 Leenax is online")
print("Type exit to stop")

while True:
    user = input("You: ")

    if user.lower() == "exit":
        print("Leenax: Goodbye")
        break

    response = leenax.respond(user)

    print("Leenax:", response)