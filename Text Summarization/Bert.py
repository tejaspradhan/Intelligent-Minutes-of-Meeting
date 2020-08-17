from nltk.tokenize import sent_tokenize
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np

def bertSent_embeding(sentences):
    ## Add sentence head and tail as BERT requested
    marked_sent = ["[CLS] " +item + " [SEP]" for item in sentences]
    
    ## USE Bert tokenizization 
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokenized_sent = [tokenizer.tokenize(item) for item in marked_sent]
    
    ## index to BERT vocabulary
    indexed_tokens = [tokenizer.convert_tokens_to_ids(item) for item in tokenized_sent]
    tokens_tensor = [torch.tensor([item]) for item in indexed_tokens]
    
    ## add segment id as BERT requested
    segments_ids = [[1] * len(item) for ind,item in enumerate(tokenized_sent)]
    segments_tensors = [torch.tensor([item]) for item in segments_ids]
    
    ## load BERT base model and set to evaluation mode
    bert_model = BertModel.from_pretrained('bert-base-uncased')
    bert_model.eval()
    
    ## Output 12 layers of latent vector
    assert len(tokens_tensor) == len(segments_tensors)
    encoded_layers_list = []
    for i in range(len(tokens_tensor)):
        with torch.no_grad():
            encoded_layers, _ = bert_model(tokens_tensor[i], segments_tensors[i])
        encoded_layers_list.append(encoded_layers)
    
    ## Use only the last layer vetcor, other choice available
    token_vecs_list = [layers[11][0] for layers in encoded_layers_list]
    
    ## Pooling word vector to sentence vector, use mean pooling, other choice available
    sentence_embedding_list = [torch.mean(vec, dim=0).numpy() for vec in token_vecs_list]
    
    
    
    return sentence_embedding_list

def kmeans_sumIndex(sentence_embedding_list):
    n_clusters = np.ceil(len(sentence_embedding_list)**0.5)
    kmeans = KMeans(n_clusters=int(n_clusters))
    kmeans = kmeans.fit(sentence_embedding_list)
    
    sum_index,_ = pairwise_distances_argmin_min(kmeans.cluster_centers_, sentence_embedding_list,metric='euclidean')
    
    sum_index = sorted(sum_index)
    
    return sum_index


def bertSummarize(text):
    sentences = sent_tokenize(text)
    
    sentence_embedding_list = bertSent_embeding(sentences)
    sum_index = kmeans_sumIndex(sentence_embedding_list)
    
    summary = ' '.join([sentences[ind] for ind in sum_index])
    
    return summary

text = "There are times when the night sky glows with bands of colour. The bands may begin as cloud shapes and then spread into a great arc across the entire sky. They may fall in folds like a curtain drawn across the heavens. The lights usually grow brighter, then suddenly dim. During this time the sky glows with pale yellow, pink, green, violet, blue, and red. These lights are called the Aurora Borealis. Some people call them the Northern Lights. Scientists have been watching them for hundreds of years. They are not quite sure what causes them. In ancient times people were afraid of the Lights. They imagined that they saw fiery dragons in the sky. Some even concluded that the heavens were on fire."
print(bertSummarize(text))
