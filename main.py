from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import string
import requests
import matplotlib.pyplot as plt

def download_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word.lower(), 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return list(shuffled.items())

def reduce_function(reduced_value):
    key, values = reduced_value
    return key, sum(values)

def map_reduce(text, search_words=None):
    text = remove_punctuation(text)
    words = text.split()

    if search_words:
        words = [word for word in words if word.lower() in search_words]

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_counts, top_n=10):
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    if not sorted_words:
        return

    words, counts = zip(*sorted_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words[::-1], counts[::-1], color='skyblue')
    plt.xlabel("Частота використання")
    plt.ylabel("Слова")
    plt.title(f"Топ {top_n} найчастіше вживаних слів (MapReduce)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    url = "https://gutenberg.net.au/ebooks/e00029.txt"
    
    print("Завантаження тексту...")
    text = download_text(url)
    
    print("Виконання MapReduce...")
    word_freq = map_reduce(text)
    
    print("Візуалізація результатів...")
    visualize_top_words(word_freq, top_n=10)