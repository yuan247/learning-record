import re
from collections import Counter
import numpy as np  
import matplotlib.pyplot as plt
def calculate_hanzi_entropy(text):
    # 保留文本中的汉字字符
    hanzi_only = ''.join(re.findall(r'[\u4e00-\u9fff]+', text))
    
    freq = {}
    for char in hanzi_only:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    
    total_chars = len(hanzi_only)
    entropy = 0.0
    for count in freq.values():
        p = count / total_chars
        entropy -= p * np.log2(p)
    
    return entropy, hanzi_only

def process_text_file_incrementally(file_path, increment_size=1024*1024):
    entropy_values = []
    total_chars_list = []
    unique_chars_list = []
    top_chars_list = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = ''
        while True:
            chunk = file.read(increment_size)  
            if not chunk:
                break
            
            data += chunk
            # 计算仅包含汉字的信息熵
            entropy, hanzi_data = calculate_hanzi_entropy(data)     
            
            total_chars = len(hanzi_data)
            unique_chars = len(set(hanzi_data))
            char_freq = Counter(hanzi_data)
            top_10_chars = char_freq.most_common(10)

            entropy_values.append(entropy)
            total_chars_list.append(total_chars)
            unique_chars_list.append(unique_chars)
            top_chars_list.append(top_10_chars)
            
            print(f"Total processed: {total_chars} 汉字, Entropy: {entropy}")
            print(f"Unique characters: {unique_chars}")
            print(f"Top 10 characters: {top_10_chars}")
    

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(entropy_values)), entropy_values, marker='o')
    plt.xlabel('Increment Steps')
    plt.ylabel('Entropy')
    plt.title('Entropy Change with Increasing Data Size (Hanzi Only)')
    plt.grid(True)
    plt.savefig('hanzi_entropy_curve_qingyunian.png')
    plt.close()

file_path = './庆余年/庆余年.txt'
process_text_file_incrementally(file_path)
