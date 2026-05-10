import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
import time

console = Console()

def generate_summary(text, ratio=0.3):
    try:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        
        word_freq = {}
        for word in doc:
            if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
                word_freq[word.text.lower()] = word_freq.get(word.text.lower(), 0) + 1
        
        if not word_freq:
            return "I couldn't find enough meaningful words to summarize that!"

        max_val = max(word_freq.values())
        for word in word_freq:
            word_freq[word] /= max_val
            
        sent_scores = {}
        for sent in doc.sents:
            for word in sent:
                if word.text.lower() in word_freq:
                    sent_scores[sent] = sent_scores.get(sent, 0) + word_freq[word.text.lower()]
        
        num_sentences = max(1, int(len(list(doc.sents)) * ratio))
        summary = nlargest(num_sentences, sent_scores, key=sent_scores.get)
        
        return " ".join([s.text.strip() for s in summary])
    except Exception as e:
        return f"Oops! Something went wrong: {e}"

def start_app():
    console.print(Panel("[bold cyan]Welcome to your AI Reading Assistant![/bold cyan]\nI'll help you turn long articles into quick summaries.", title="NLP Tool"))
    
    while True:
        console.print("\n[yellow]Paste your article below (Press Enter twice to finish):[/yellow]")
        
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        
        user_text = " ".join(lines)
        
        if not user_text.strip():
            console.print("[red]No text provided. Goodbye![/red]")
            break


        for _ in track(range(10), description="[green]Reading and analyzing..."):
            time.sleep(0.05)

        summary_result = generate_summary(user_text)

        console.print("\n[bold green]Here is your Concise Summary:[/bold green]")
        console.print(Panel(summary_result, border_style="bright_blue"))
        
        choice = console.input("\n[bold white]Would you like to summarize something else? (y/n): [/bold white]")
        if choice.lower() != 'y':
            console.print("[italic]Happy reading! Closing the tool...[/italic]")
            break

if __name__ == "__main__":
    start_app()
