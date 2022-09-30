from bertopic import BERTopic
import pandas as pd
import numpy as np

def runBERTopic(tweets_file='en_BW_tweets.csv',save_path='./'):
    """ Runs BERTopic code and saves (1) the model, (2) the probabilities, and (3) a file used to label the topics.

    Args:
        tweets_file (str, optional): CSV file containing tweets. Defaults to 'en_BW_tweets.csv'.
        save_path (str, optional): Path to save to. Defaults to './'.
    """
    # load tweets
    en_BW = pd.read_csv(tweets_file)
    docs = list(en_BW.full_text)
    # run BERTopic
    topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
    topics, probs = topic_model.fit_transform(docs)
    # save model
    topic_model.save(save_path+"BW_BertTopic.model")
    # save probs
    np.save(save_path+'probs',probs)
    # prepare and save csv file for labeling
    ts=topic_model.get_topics()
    d=pd.DataFrame([[k,v] for (k,v) in ts.items()],columns=['Topic ID','Topic Word Scores'])
    d.to_csv(save_path+'ToLabelTopics.csv',index=False)

def predictBerTopic(model_file, docs):
    """ Loads a BERTopic model and predicts the top topic and topic-distribution for documents

    Args:
        model_file ([str]): model file
        docs (List[str]): list of documents

    Returns:
        [type]: [description]
    """    
    topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
    topic_model=topic_model.load(model_file)
    topics, probs = topic_model.transform(docs)

    return topics, probs

def GetTopicDict(file='Manual_Topic_Label_Done.csv'):
    df = pd.read_csv(file)
    d = dict(zip(df['Topic ID'],df['Generic Label']))
    return d
