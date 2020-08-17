# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 19:07:49 2020

@author: shrir
"""


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer

def create_frequency_table(text_string) -> dict:
    
    """
    input:  a paragraph as text_string
    process: tokenize text into words, stem words, remove stopwords
    output: a bag of word dictionary {word: frequency}
    
    Note: customized weight of word could be applied
    """

    stopWords = set(stopwords.words("english"))
    
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1 
        else:
            freqTable[word] = 1

    return freqTable

def score_sentences(sentences, freqTable) -> dict:
    
    """
    input:  list of sentences and word frequency table
    process: compute score for each sentence = total word value / word count
    output: a sentence soore dictionary {sentence: score}
    
    """   
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

    return sentenceValue


def find_average_score(sentenceValue) -> int:
    """
    input:  sentence score dictionary
    process: compute average sentence score = total sentence score / sentence number
    output: avreage sentence score as threshold
    
    Note: the computation ov average score can be customized / weighted
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average

def generate_summary(sentences, sentenceValue, threshold) -> str:
    
    """
    input:  list of sentences, sentence value dictionary
    
    output: sentence whose score > threshold as the summary
    
    """
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


def summarize_text_wf(text) -> str:
     
    """
    input:  a paragraph of text
    
    output: summary of text according to word frequency algorithm
    
    """
    freq_table = create_frequency_table(text)
    sent = sent_tokenize(text)
    sent_value = score_sentences(sent,freq_table)
    threshold = find_average_score(sent_value)
    
    return generate_summary(sent,sent_value,threshold)

text = "There are times when the night sky glows with bands of colour. The bands may begin as cloud shapes and then spread into a great arc across the entire sky. They may fall in folds like a curtain drawn across the heavens. The lights usually grow brighter, then suddenly dim. During this time the sky glows with pale yellow, pink, green, violet, blue, and red. These lights are called the Aurora Borealis. Some people call them the Northern Lights. Scientists have been watching them for hundreds of years. They are not quite sure what causes them. In ancient times people were afraid of the Lights. They imagined that they saw fiery dragons in the sky. Some even concluded that the heavens were on fire."
a=summarize_text_wf(text)
print(a)