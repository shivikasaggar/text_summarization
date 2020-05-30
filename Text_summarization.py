# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:41:43 2020

@author: Shivika Sagar
"""

import nltk
nltk.download()
#importing all the relevant packages
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize


#declaring the text that needs to be summarised
#took this text from wikipedia
text_str = '''
In 1982, Trump was listed on the initial Forbes list of wealthy individuals as having a share of his family's estimated $200 million net worth. 
His financial losses in the 1980s caused him to be dropped from the list between 1990 and 1995.In its 2020 billionaires ranking, Forbes estimated Trump's net worth at $2.1 billion(1,001st in the world, 275th in the U.S.)making him one of the richest politicians in American history and the first billionaire American president.
During the three years since Trump announced his presidential run in 2015, Forbes estimated his net worth declined 31% and his ranking fell 138 spots.
When he filed mandatory financial disclosure forms with the Federal Elections Commission (FEC) in July 2015, Trump claimed a net worth of about $10 billion;
however FEC figures cannot corroborate this estimate because they only show each of his largest buildings as being worth over $50 million, yielding total assets worth more than $1.4 billion and debt over $265 million.
Trump said in a 2007 deposition, "My net worth fluctuates, and it goes up and down with markets and with attitudes and with feelings, even my own feelings.
Journalist Jonathan Greenberg reported in April 2018 that Trump, using the pseudonym "John Barron" and claiming to be a Trump Organization official, called him in 1984 to falsely assert that he owned "in excess of ninety percent" of the Trump family's business, in an effort to secure a higher ranking on the Forbes 400 list of wealthy Americans.
Greenberg also wrote that Forbes had vastly overestimated Trump's wealth and wrongly included him on the Forbes 400 rankings of 1982, 1983, and 1984.
Trump has often said he began his career with "a small loan of one million dollars" from his father, and that he had to pay it back with interest.
In October 2018, The New York Times reported that Trump "was a millionaire by age 8", borrowed at least $60 million from his father, largely failed to reimburse him, and had received $413 million (adjusted for inflation) from his father's business empire over his lifetime.
According to the report, Trump and his family committed tax fraud, which a lawyer for Trump denied. The tax department of New York says it is "vigorously pursuing all appropriate avenues of investigation" into it.
Analyses by The Economist and The Washington Post have concluded that Trump's investments underperformed the stock market.
Forbes estimated in October 2018 that the value of Trump's personal brand licensing business had declined by 88% since 2015, to $3 million.
Trump's tax returns from 1985 to 1994 show net losses totaling $1.17 billion over the ten-year period, in contrast to his claims about his financial health and business abilities.
The New York Times reported that "year after year, Mr. Trump appears to have lost more money than nearly any other individual American taxpayer", and Trump's "core business losses in 1990 and 1991 – more than $250 million each year – were more than double those of the nearest taxpayers in the I.R.S. information for those years".
In 1995 his reported losses were $915.7 million.
'''
    
#function for making a frequency table of the words in the text by eleminating the stopwords
def frequency_table_creation(text_string) -> dict:
    
    #this is to find the stopwords from english.txt directory
    stop_words = set(stopwords.words("english"))
    #print(stopWords)
    
   #to find syllable of the given string
    w = word_tokenize(text_string)
   # print(words)
    
    ps = PorterStemmer()
   #for stemming
   

    frequencyTable = dict()
    for word in w:
        word = ps.stem(word)
        if word in stop_words:
            continue
        if word in frequencyTable:
            frequencyTable[word] += 1
        else:
            frequencyTable[word] = 1

    return frequencyTable

#function to score each sentence using the frequency table from the above function.
def score_of_sentences(sentences, frequencyTable) -> dict:
   

    sentence_value = dict()

    for sentence in sentences:
        #wor_tokenize returns words in a sentence
        word_count_in_sentence = (len(word_tokenize(sentence)))
        
        word_count_in_sentence_except_stopwords = 0
        for wordValue in frequencyTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stopwords += 1
                if sentence[:10] in sentence_value:
                    sentence_value[sentence[:10]] += frequencyTable[wordValue]
                else:
                    sentence_value[sentence[:10]] = frequencyTable[wordValue]

        if sentence[:10] in sentence_value:
            sentence_value[sentence[:10]] = sentence_value[sentence[:10]] / word_count_in_sentence_except_stopwords

         #dividing every sentence value by the number of words in the sentence so as to maintain balance irrespective of the sentence length.
     

    return sentence_value


#function to calculate the average score of the sentence value,using it as a threshold later.
def average_score(sentence_value) -> int:
   
    sum_of_vals = 0
    for entry in sentence_value:
        sum_of_vals += sentence_value[entry]
        
        #finding average by dividing by the total length
    average_of_sentence = (sum_of_vals / len(sentence_value))

    return average_of_sentence

#function to give the summary as output
#if the sentence value of any sentence is greter than the calculated threshold value,then adding it to the summary.
def generating_summary(sentences, sentence_value, threshold_val):
    sentence_count = 0
    summary_of_text = ''

    for sentence in sentences:
        if sentence[:10] in sentence_value and sentence_value[sentence[:10]] >= (threshold_val):
            summary_of_text += " " + sentence
            sentence_count += 1

    return summary_of_text


#combining all funtions into one function as summarrization
def summarization_func(text):
    # STEP:1 create the frequency table
    freq_table = frequency_table_creation(text)
    print(freq_table ,end=' ')

    # STEP:2 Tokenizing to make array of sentences.
    sentences = sent_tokenize(text)
    print(sentences ,end=' ')
    
    # STEP:3 score the sentences according to frequency
    sentence_scores = score_of_sentences(sentences, freq_table)
    print(sentence_scores ,end=' ')

    # STEP:4 finding the threshold value for summarization
    threshold_val =average_score(sentence_scores)
    print(threshold_val ,end=' ')

    # STEP:5 finally,generating the summary
    #we have made the threshold value 1*3 times.
    text_summary = generating_summary(sentences, sentence_scores, 1.3 * threshold_val)
    print(text_summary)

    return text_summary

if __name__ == '__main__':
    f =frequency_table_creation(text_str)
    s=sent_tokenize(text_str)
    score= score_of_sentences(s,f)
    t=average_score(score)
    result=generating_summary(s, score, 1.3 * t)
    print(result)