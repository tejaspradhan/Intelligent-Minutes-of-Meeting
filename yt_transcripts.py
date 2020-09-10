from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize


def get_transcripts(video_url):
    # Parsing the URL to find the VIDEO ID
    url_data = urlparse(video_url)
    query = url_data.query
    video_id = query[2:]

    # Getting the transcripts
    YouTubeTranscriptApi.get_transcript(video_id)

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en'])
    trans_list = transcript.fetch()
    text = ''

    for d in trans_list:
        text+=d['text']+'. '
    return text

    # Writing transcripts to the file 
    '''
    f = open('transcripts.txt','w+')
    f.write(text)
    print('Your video transcripts have been downloaded in the file transcripts.txt')
    f.close()
    '''
def create_wft(text):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    wft = dict()
    words = word_tokenize(text)
    for word in words:
        word = ps.stem(word)
        if word in stop_words:
            continue
        if word in wft:
            wft[word] += 1
        else:
            wft[word] = 1

    return wft
    
def score(sentences, wft):
    s_val = dict()
    for sent in sentences:
        word_count = len(word_tokenize(sent))
    
        for word_val in wft:
            if word_val in sent.lower():
                if sent[:10] in s_val:
                    s_val[sent[:10]] += wft[word_val]
                else:
                    s_val[sent[:10]] = wft[word_val]
        s_val[sent[:10]] = s_val[sent[:10]]// word_count
    
    return s_val

def find_average_score(s_val):
    sum = 0
    for entry in s_val:
        sum += s_val[entry]

    # Average value of a sentence from original text
    average = int(sum/ len(s_val))

    return average

def summarize(sentences,s_val,threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in s_val and s_val[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1
    return summary

def generate_summary(text):
    
    table = create_wft(text)   # ... creating the word freuency table
    sentences = sent_tokenize(text)
    sentence_scores = score(sentences,table)
    threshold = find_average_score(sentence_scores)
    summary = summarize(sentences,sentence_scores,threshold)
    return summary
#...Driver code...

print("Enter url...")
video_url = input()   # We can also hard code the url 
#copy url from the url bar. Don't use the copy video url option

text = get_transcripts(video_url)
summary = generate_summary(text)
print(summary)