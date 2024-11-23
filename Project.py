import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class Securitecode:
    def __init__(self, master):
        self.master = master
        self.cover_image = None
        self.result_image = None
        self.secret_text = ""
        self.master.geometry("1070x600")
        self.master.config(bg="#c7a3c1") 
        self.create_widgets()

    def create_widgets(self):
        self.Original = tk.Frame(self.master, bd=2, relief=tk.GROOVE, bg="#8c6987")
        self.Original.grid(row=0, column=0, padx=10, pady=10)
        self.originallabel = tk.Label(self.Original, text="Input Image", font=("Arial", 16), bg="#8c6987")
        self.originallabel.pack(pady=5)
        self.originalCanvas = tk.Canvas(self.Original, width=400, height=300, bg="#eaeaea")
        self.originalCanvas.pack(padx=5, pady=5)
        self.loadImageB= tk.Button(self.Original, text="load input Image", command=self.LoadImage, bg="#d6c3d3", fg="#240f20", font=("Times New Roman", 12))
        self.loadImageB.pack(pady=5)
        self.SecretFrame = tk.Frame(self.master, bd=6, relief=tk.GROOVE, bg="#8c6987")
        self.SecretFrame.grid(row=0, column=1, padx=10, pady=10) 
        self.loadB = tk.Button(self.SecretFrame, text="Load Secret Text File", command=self.load_secret_text_file, bg="#d6c3d3", fg="#240f20", font=("Arial", 12))
        self.loadB.pack(pady=5)   
        self.controlF = tk.Frame(self.master, bg="#f7f9fc")
        self.controlF.grid(row=1, column=0, columnspan=10, padx=10, pady=10)
        self.lsb_option = tk.IntVar(value=1) 
        self.lsb_option = tk.IntVar(value=1)
        self.lsb_option_label = tk.Label(self.controlF, text="LSBs :", bg="#f7f9fc", font=("Arial", 12))
        self.lsb_option_label.pack(side=tk.LEFT)
        lsb_options = [1, 2, 3]  
        self.option_Menu = tk.OptionMenu(self.controlF, self.lsb_option, *lsb_options)
        self.option_Menu.config(bg="#f2f2f2", font=("Arial", 12)) 
        self.option_Menu.pack(side=tk.LEFT)
        for i in range(1, 4):
            rb = tk.Radiobutton(self.controlF, text=f"{i} LSBs", variable=self.lsb_option, value=i, bg="#f7f9fc",font=("Times New Roman", 15))
        self.restore_button = tk.Button(self.controlF, text="Restore", command=self.Restore, bg="#69255e", fg="white", font=("Times New Roman", 15))
        self.restore_button.pack(side=tk.LEFT, fill=tk.X, padx=3, pady=2)
        self.saveB = tk.Button(self.controlF, text="Save", command=self.Save, bg="#69255e", fg="white", font=("Times New Roman", 15))
        self.saveB.pack(side=tk.LEFT, fill=tk.X, padx=3, pady=2)
        self.hideB = tk.Button(self.controlF, text="Hide", command=self.Hide, bg="#69255e", fg="white", font=("Times New Roman", 15))
        self.hideB.pack(side=tk.LEFT, fill=tk.X, padx=3, pady=2)
        self.clearB = tk.Button(self.controlF, text="Clear", command=self.clear, bg="#69255e", fg="white", font=("Times New Roman", 15))
        self.clearB.pack(side=tk.LEFT, fill=tk.X, padx=3, pady=2)
        self.result_frame = tk.Frame(self.master, bd=2, relief=tk.GROOVE, bg="#8c6987")
        self.result_frame.grid(row=0, column=2, padx=10, pady=10)
        self.Rlabel = tk.Label(self.result_frame, text="Image With Securite text", font=("Times New Roman", 16), bg="#8c6987")
        self.Rlabel.pack(pady=5)
        self.canvasR = tk.Canvas(self.result_frame, width=400, height=300, bg="#eaeaea")
        self.canvasR.pack(padx=5, pady=5)

    

    def load_secret_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.secret_text = file.read()
            messagebox.showinfo("Loaded", "done")

    def show_image(self, canvas, image):
        image.thumbnail((700, 300)) 
        self.photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(200, 150, image=self.photo_image)
        canvas.image = self.photo_image  
    def LoadImage(self):
        file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if file_path:
            self.cover_image = Image.open(file_path)
            self.show_image(self.originalCanvas, self.cover_image)
    def Hide(self):
        if self.cover_image is None:
            messagebox.showwarning("Warning", "Please : cover image first!")
            return

        if not self.secret_text:
            messagebox.showwarning("Warning", "Please : secret text from a file!")
            return

        lsb_count = self.lsb_option.get()
        pixel_changes = self.embed_text(self.cover_image, self.secret_text, lsb_count)
        self.show_image(self.canvasR, self.result_image)
        
        
        messagebox.showinfo("Pixel Change : ", f"Number of pixels changed: {pixel_changes}")

    def embed_text(self, image, secret, lsb_count):
        img_data = list(image.getdata())
        secret_bin = ''.join(format(ord(char), '08b') for char in secret) + '00000000'  
        secret_len = len(secret_bin)

        new_data = []
        data_index = 0
        changed_pixels = 0  

        for pixel in img_data:
            if data_index < secret_len:
                r, g, b = pixel
           
                r = (r & ~(1 << lsb_count) + 1) & 255
                g = (g & ~(1 << lsb_count) + 1) & 255
                b = (b & ~(1 << lsb_count) + 1) & 255

                
                if data_index < secret_len:
                    if (r & 1) != (int(secret_bin[data_index]) << (lsb_count - 1)):
                        changed_pixels += 1
                    r |= (int(secret_bin[data_index]) << (lsb_count - 1))
                    data_index += 1
                if data_index < secret_len:
                    if (g & 1) != (int(secret_bin[data_index]) << (lsb_count - 1)):
                        changed_pixels += 1
                    g |= (int(secret_bin[data_index]) << (lsb_count - 1))
                    data_index += 1
                if data_index < secret_len:
                    if (b & 1) != (int(secret_bin[data_index]) << (lsb_count - 1)):
                        changed_pixels += 1
                    b |= (int(secret_bin[data_index]) << (lsb_count - 1))
                    data_index += 1

                new_data.append((r, g, b))
            else:
                new_data.append(pixel)

        result_image = Image.new(image.mode, image.size)
        result_image.putdata(new_data)
        self.result_image = result_image  
        return changed_pixels  

    def Restore(self):
   
       if self.result_image is None and self.cover_image is None:
        messagebox.showwarning("Warning", "please: cover image first!")
        return

       lsb_count = self.lsb_option.get()
       if self.result_image is not None:
        hidden_text = self.extract_text(self.result_image, lsb_count)
       else:
        hidden_text = self.extract_text(self.cover_image, lsb_count)
       if hidden_text:  
        messagebox.showinfo("Extracted Text", f"Text: {hidden_text}")
       else:
        messagebox.showinfo("Extracted Text", "No text found")




    def extract_text(self, image, lsb_count):
        img_data = list(image.getdata())
        secret_bin = ""

        for pixel in img_data:
            r, g, b = pixel
            secret_bin += str((r >> (lsb_count - 1)) & 1)
            secret_bin += str((g >> (lsb_count - 1)) & 1)
            secret_bin += str((b >> (lsb_count - 1)) & 1)

        
        secret_chars = [chr(int(secret_bin[i:i + 8], 2)) for i in range(0, len(secret_bin), 8)]
        secret = ''.join(secret_chars).rstrip('\x00')  
        return secret

    def Save(self):
        if self.result_image is None:
            messagebox.showwarning("Warning", "No Save")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
        if filepath:
            self.result_image.save(filepath)
            messagebox.showinfo("Saved", "Saved successfully.")

    def clear(self):
        self.cover_image = None
        self.result_image = None
        self.secret_text = ""
        self.originalCanvas.delete("all")
        self.canvasR.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = Securitecode(root)
    root.mainloop()
