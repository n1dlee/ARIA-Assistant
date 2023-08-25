from PIL import Image, ImageTk

def main():
    root = tk.Tk()
    root.title("Voice Assistant")
    root.geometry("600x480")

    # Load the background image
    background_image = Image.open("background.jpg")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a label to display the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def start_voice_assistant_thread():
        threading.Thread(target=start_voice_assistant).start()

    button = tk.Button(root, text="Start Voice Assistant", command=start_voice_assistant_thread)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
