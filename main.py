import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from ttkthemes import ThemedTk

def analyze_text():
    # Get input text from the text widget
    text = text_widget.get("1.0", tk.END)

    # Check if the input text is not empty
    if not text.strip():
        messagebox.showwarning("Warning", "Please enter some text for analysis.")
        return

    # Remove punctuation and convert to lowercase
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())

    # Character count
    char_count = len(cleaned_text)

    # Word count
    words = cleaned_text.split()
    word_count = len(words)

    # Average word length
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0

    # Word frequency
    word_freq = Counter(words)
    top_words = word_freq.most_common(top_n)

    # Display results in a modal window
    result_window = tk.Toplevel(root)
    result_window.title("Analysis Results")
    result_window.geometry("1000x550")

    # Create and pack the result label
    result_label = ttk.Label(result_window, text="", justify=tk.LEFT, font=("Helvetica", 12))
    result_label.pack(padx=10, pady=10, anchor="w")

    # Set the result text
    result_text = f"Character Count: {char_count}\t\t"
    result_text += f"Word Count: {word_count}\t\t"
    result_text += f"Average Word Length: {avg_word_length:.2f}\n\n"
    result_text += "Top Words:\n"
    for word, frequency in top_words:
        result_text += f"{word}: {frequency}\n"

    # Update the result label
    result_label.config(text=result_text)

    # Plotting bar chart for top words in the result window
    plot_top_words(top_words, result_window)

def plot_top_words(top_words, parent):
    # Create the frame for the plot
    plot_frame = ttk.Frame(parent)
    plot_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Plotting bar chart
    fig, ax = plt.subplots()
    ax.bar(*zip(*top_words))
    ax.set_title(f"Top {top_n} Words")
    ax.set_xlabel("Words")
    ax.set_ylabel("Frequency")

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    # Create the themed main window
    root = ThemedTk(theme="arc")  # You can choose other themes such as "clearlooks", "radiance", etc.
    root.title("Text Analyzer")

    # Create and pack the text input widget
    text_widget = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD, font=("Helvetica", 12))
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create and pack the analyze button with style
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12))
    analyze_button = ttk.Button(root, text="Analyze", command=analyze_text, style="TButton")
    analyze_button.pack(pady=10)

    # Set the top N value for word frequency analysis
    top_n = 10

    # Run the Tkinter main loop
    root.mainloop()
