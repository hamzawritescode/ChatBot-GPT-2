import json
import os
from transformers import pipeline, AutoTokenizer

CHAT_HISTORY_FILE = "chat_history.json"

model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
text_generator = pipeline(
    'text-generation',
    model=model_name,
    tokenizer=tokenizer,
    pad_token_id=tokenizer.eos_token_id
)

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_chat_history(chat_data):
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump(chat_data, file, indent=4)

def initiate_new_chat_session(chat_data):
    chat_id = input("Enter a name for this new chat session: ")
    chat_data[chat_id] = []
    print(f"Starting new chat session: {chat_id}")
    return chat_id

def resume_existing_chat_session(chat_data):
    if not chat_data:
        print("No saved chat sessions found. Starting a new one.")
        return initiate_new_chat_session(chat_data)
    
    else:
        print("Available chat sessions:")
        for chat_id in chat_data:
            print(f"- {chat_id}")
        
        chat_id_to_resume = input("Enter the name of the chat to continue (or type 'new' to start a new session): ")
        
        if chat_id_to_resume.lower() == 'new':
            return initiate_new_chat_session(chat_data)
        
        elif chat_id_to_resume in chat_data:
            print(f"Resuming chat session: {chat_id_to_resume}")
            return chat_id_to_resume
        
        else:
            print("Chat session not found.")
            return None

def conduct_chat(chat_data, active_chat_id):
    if not active_chat_id:
        print("No active chat session.")
        return

    current_conversation = chat_data[active_chat_id]
    for i, message_entry in enumerate(current_conversation):
        speaker, text = message_entry.split(": ", 1)
        print(f"{speaker}: {text}")
        
        if i < len(current_conversation) - 1:
            print()

    while True:
        user_message = input("You: ")
        print()

        if user_message.lower() == 'exit':
            break

        prompt_template_prefix = f"You: {user_message}\n\nBot:"
        
        available_tokens_for_history = 1024 - tokenizer.encode(prompt_template_prefix, return_tensors='pt').size(1) - 50 
        
        history_for_prompt = []
        accumulated_token_count = 0
        
        for entry in reversed(current_conversation):
            entry_token_count = tokenizer.encode(entry, return_tensors='pt').size(1)
            
            if accumulated_token_count + entry_token_count < available_tokens_for_history:
                history_for_prompt.insert(0, entry)
                accumulated_token_count += entry_token_count
            
            else:
                break
        
        full_prompt = ""
        for entry in history_for_prompt:
            full_prompt += f"{entry}\n\n"
        full_prompt += f"You: {user_message}\n\nBot:"

        try:
            generated_output = text_generator(
                full_prompt,
                max_new_tokens=70,
                num_return_sequences=1,
                do_sample=True,
                top_k=50,
                top_p=0.95
            )
            
            bot_response = generated_output[0]['generated_text'].split("Bot:")[-1].strip()
            print(f"Bot: {bot_response}")
            print()
            
            chat_data[active_chat_id].append(f"You: {user_message}")
            chat_data[active_chat_id].append(f"Bot: {bot_response}")

        except Exception as error:
            print(f"Bot: I'm sorry, I had trouble generating a response. ({error})")
            print()
            chat_data[active_chat_id].append(f"You: {user_message}")
            chat_data[active_chat_id].append(f"Bot: I'm sorry, I had trouble generating a response.")

if __name__ == "__main__":
    all_chats = load_chat_history()
    current_session_id = None

    while True:
        print("\nChoose an action: new, continue, exit")
        user_choice = input("Your choice: ").lower()

        if user_choice == 'new':
            current_session_id = initiate_new_chat_session(all_chats)
        
            if current_session_id:
                conduct_chat(all_chats, current_session_id)
                save_chat_history(all_chats)
                current_session_id = None 
        
        elif user_choice == 'continue':
            current_session_id = resume_existing_chat_session(all_chats)
        
            if current_session_id:
                conduct_chat(all_chats, current_session_id)
                save_chat_history(all_chats)
                current_session_id = None
        
        elif user_choice == 'exit':
            print("Exiting the chat application.")
            break
        
        else:
            print("That's not a valid option. Please type 'new', 'continue', or 'exit'.")
