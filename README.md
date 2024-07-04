# Analysis-of-Singapore-Parliament-Debates
A Streamlit app that allows you to see which member of parliament spoke at each session and the sentiment of their speech.

### Data Collection 
Only parliament sessions conducted from 2020-2021 were considered. 

### App Features 
- See which sessions a member of parliament has spoken at.
- See which member of parliament spoke at a particular session and the sentiment of their speech.
- Summarise the speeches made by members of parliaments at a specific session.

### Model 
- Cohere large language model was used for embedding, sentiment analysis and summary of speeches.
- Few-shot classification was used to ensure better performance for sentiment analysis.

### Future Works 
- Fine-tuning using a larger dataset is needed instead of few-shot classification to ensure better performance of sentiment analysis.
