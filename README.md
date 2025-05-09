# ChatBot-GPT-2

This Python script is basically a little command-line chat buddy. You can use it to:

Kick off new conversations: Just give your chat a name, and you're good to go.
Jump back into old chats: If you've chatted before, you can pick up right where you left off.
Actually talk to a bot: It uses some clever tech from Hugging Face (specifically a model like GPT-2) to come up with responses.
It remembers what you said: Your chats get saved in a little file (chat_history.json), so you don't lose your conversation history when you close it.
It tries to keep things manageable: If a chat gets super long, the script is smart enough to only feed the most recent bits to the language model so it doesn't get overwhelmed.
In a nutshell, it's a straightforward way to have an ongoing, interactive chat with an AI, all from your terminal.

What you'll need to get this running (Requirements)
To get this chat script working, here's the rundown:

Python Version
You'll want to have Python 3.6 or something newer installed. This is mainly because the script uses some handy features (like f-strings for text) that came in with that version, and the transformers library usually plays best with Python 3.6 and up.
A Few Extra Tools (Modules/Libraries)
You'll need to grab a couple of Python libraries if you don't have them already. The good news is you can usually install them with a simple command: pip install transformers torch.

json: This one's a built-in part of Python, so no need to install it. It's just used for stashing your chat history in that chat_history.json file.
os: Another standard Python tool. This script uses it to check if your chat history file already exists. Again, nothing to install here.
transformers: This is the key ingredient from Hugging Face. It’s what lets the script tap into those pre-trained language models (like GPT-2) and understand your text.
torch: The transformers library often leans on PyTorch behind the scenes to do its magic, especially for models like GPT-2. So, having PyTorch installed is important for the transformers part to work correctly.
(Heads up: The script also mentions random and re, but they don't seem to be used right now. You could probably remove those lines if you wanted.)

The Chat Log File
chat_history.json: Don't worry about creating this file yourself. The script will make it automatically in the same folder where you run the script. This is where all your conversations will be saved.
Getting the AI Brain (Model Access)
An Internet Connection (at least for the first time): When you first run the script, it'll need to go online to download the language model (GPT-2, by default) and its dictionary (tokenizer) if you haven't used them before. Once they're downloaded and saved on your computer, you won't necessarily need to be online every time you run it.
