import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import pandas as pd
import warnings
import os
import sys

warnings.filterwarnings('ignore')

class TextAnalyser:
    
    sentences = []
    words = []
    raw_text = ""
    complex_words = 0
    
    def __init__(self, url, url_id):
        results = requests.get(url)
        
        try:
            soup = BeautifulSoup(results.content, 'html5lib')
            data = soup.find('div', class_ = 'td-post-content tagdiv-type')
            
            if data == None:
                data = soup.find('div', class_ = 'tdb-block-inner td-fix-index')
            
            title = soup.find('h1', class_ = 'entry-title')
            
            if title == None:
                title = soup.find('h1', class_ = 'tdb-title-text')

            title = title.text
            
            extracted_data = title.strip()

            for elem in data:
                extracted_data += f"{elem.text.strip()}"

            self.raw_text = extracted_data.replace("\n", "").strip()
            
            self.sentences = self.raw_text.split(".")
            self.words = self.raw_text.replace(".", "").split(" ")
            
            if not os.path.isdir("Data"):
                os.mkdir("Data")
            
            with open(f"Data/{url_id}.txt", "w") as f:
                f.write(self.raw_text)
                
        except(Exception) as e:
            print(e)
            
    def calculate_complex_words_percentage(self):

        tk = nltk.SyllableTokenizer()
        complex_word_count = 0
        
        for word in self.words:
            syllable_count = len(tk.tokenize(word))
            if(syllable_count > 2):
                complex_word_count += 1

        self.complex_words = complex_word_count
        return complex_word_count/len(self.words)
    
    def calculate_avg_sentence_length(self):
        
        return (len(self.words)/len(self.sentences))
    
    def calculate_fog_index(self):
        
        avg_sentence_length = len(self.words)/len(self.sentences)
        if not self.complex_words:
            self.calculate_complex_words_percentage()
        return 0.4 * (avg_sentence_length + self.complex_words)
    
    def calculate_cleaned_word_count(self):
        
        stop_words = set(stopwords.words('english'))
        word_tokens = nltk.word_tokenize(self.raw_text)
        punctuation_marks = ['.', ',', '?', '!', ':', ';', '-', '_', '{', '}', '[', ']', '\'', '\"']
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words and w not in punctuation_marks]
        return len(filtered_sentence)
    
    def calculate_personal_pronouns(self):
        
        pronouns = ['i', 'we', 'my', 'ours', 'us']
        personal_pronoun_count = 0
        
        for word in self.words:
            if(word == 'US'):
                continue
            if pronouns.count(word.lower()) != 0:
                personal_pronoun_count += 1
        
        return personal_pronoun_count
    
    def calculate_avg_word_length(self):
        
        total_characters = 0
        
        for word in self.words:
            total_characters += len(word)
        
        return total_characters/len(self.words)
    
    def __count_syllables(self, word):
        word = word.lower()
        vowels = "aeiou"
        num_vowels = 0
        
        # Handle exception: words ending with "es" or "ed"
        if word.endswith("es") or word.endswith("ed"):
            return 0
        
        for letter in word:
            if letter in vowels:
                num_vowels += 1
        
        for i in range(len(word) - 1):
            if word[i] in vowels and word[i + 1] in vowels:
                num_vowels -= 1

        if word.endswith("e") and num_vowels > 1:
            num_vowels -= 1
        
        return num_vowels

    def calculate_syllables_per_word(self):
        
        syllable_count = 0

        for word in self.words:
            syllables = self.__count_syllables(word)
            syllable_count += syllables
        
        return syllable_count/len(self.words)

    def __read_txt_files(self, filePath):
        
        words = []
        with open(filePath, 'r') as f:
            words = f.read().split("\n")
            
        return words
    
    def sentimental_analysis(self):
        
        stopWords = []
        filePaths = ['StopWords_Auditor.txt', 'StopWords_Currencies.txt', 'StopWords_DatesandNumbers.txt', 'StopWords_Generic.txt', 'StopWords_GenericLong.txt', 'StopWords_Geographic.txt', 'StopWords_Names.txt']
        
        for filePath in filePaths:
            stopWords.extend(self.__read_txt_files(f"StopWords/{filePath}"))
            
        words = []
        
        for word in self.words:
            if(word not in stopWords):
                words.append(word)
                
        cleaned_text = " ".join(words)
        
        positive_words = self.__read_txt_files("MasterDictionary/positive-words.txt")
        negative_words = self.__read_txt_files("MasterDictionary/negative-words.txt")
        
        tokenize_words = nltk.word_tokenize(cleaned_text)
        positive_count = 0
        negative_count = 0
        
        for word in tokenize_words:
            if word in positive_words:
                positive_count += 1
            elif word in negative_words:
                negative_count += 1
                
        polarity_score = (positive_count - negative_count)/((positive_count + negative_count) + 0.000001)
        subjectivity_score = (positive_count + negative_count)/(len(tokenize_words) + 0.000001)
        
        return [positive_count, negative_count, polarity_score, subjectivity_score]
    
    
    
def perform_text_analysis(url, url_id):
    
    analyser = TextAnalyser(url, url_id)
    
    sentimental_analysis_scores = analyser.sentimental_analysis()
    avg_sentence_length = analyser.calculate_avg_sentence_length()
    percentage_of_complex_words = analyser.calculate_complex_words_percentage()
    fog_index = analyser.calculate_fog_index()
    avg_number_of_words_per_sentence = avg_sentence_length
    complex_words_count = analyser.complex_words
    word_count = analyser.calculate_cleaned_word_count()
    syllable_per_word = analyser.calculate_syllables_per_word()
    personal_pronouns = analyser.calculate_personal_pronouns()
    avg_word_length = analyser.calculate_avg_word_length()
    
    del analyser
    
    return [sentimental_analysis_scores[0], sentimental_analysis_scores[1], sentimental_analysis_scores[2], sentimental_analysis_scores[3], avg_sentence_length, percentage_of_complex_words, fog_index, avg_number_of_words_per_sentence, complex_words_count, word_count, syllable_per_word, personal_pronouns, avg_word_length]
    
if(__name__ == "__main__"):

    input_sheet = pd.read_excel('Input.xlsx')
    main = pd.DataFrame([], columns=['POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'])
    # main.loc[len(main.index)] = ['Rehan', 20]
    cnt = 0
    error_cnt = 0
    
    for i in range(len(input_sheet)):
        url = input_sheet.loc[i, "URL"]
        url_id = input_sheet.loc[i, "URL_ID"]
        try:
            output = perform_text_analysis(url, url_id)
            main.loc[len(main.index)] = output
            cnt += 1
            # print(url_id + " extract and processing completed")
            sys.stdout.write(f"     {cnt} extracted and processed \r")
            sys.stdout.flush()
        except(Exception) as e:
            print(e)
            error_cnt += 1
            print(f"Error at {url_id}\nerror cnt {error_cnt}")
        
    result = pd.concat([input_sheet, main], axis=1, join='inner')
    result.to_excel("output.xlsx")
    print(f"Error count : {error_cnt}");