import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st 
import cohere 
from cohere import ClassifyExample

co = cohere.Client('api_key')

df = pd.read_csv('/Users/kelvinfoo/Desktop/Side Projects/Parliament NLP/Combined Data 14th.csv')
df['speaker'] = df['speaker'].replace({
    'Mr Pritam': 'Mr Pritam Singh',
    'Ms Joan Pereira –': 'Ms Joan Pereira',
    'Ms He Ting Ru –': 'Ms He Ting Ru'
})


# Filter out unwanted speakers
unwanted_speakers = [
    'Mr Speaker', 'Mr Deputy Speaker', '[Mr Speaker in the Chair]', 'Deputy Speaker',
    'Mdm Deputy Speaker', 'The Chairman', 'The Chairman:', 'The President'
]
df = df[~df['speaker'].isin(unwanted_speakers)]


unique_speakers = df['speaker'].unique()

def filter_session_by_speaker(selected_speaker): 
    return df[df['speaker'] == selected_speaker]

st.header("Analysis of Singapore Parliament Debates")
st.subheader('Sessions that members of parliament spoke at')
selected_speaker = st.selectbox('Select the member of parliament', unique_speakers)
filtered_by_speaker = filter_session_by_speaker(selected_speaker)
filtered_by_speaker = filtered_by_speaker.drop_duplicates(subset = ['session_title'])
number_of_speeches = filtered_by_speaker.shape[0]

if not filtered_by_speaker.empty: 
    st.write(f"Sessions that {selected_speaker} has spoken at")
    st.dataframe(filtered_by_speaker[['session_title', 'parliament_sitting_date']])
    st.write(f"Number of sessions that {selected_speaker} has spoken at: {number_of_speeches}")

else: 
    st.write(f"No speeches found for {selected_speaker}.")

st.text('Top 10 members of Parliament by number of sessions that he has spoken at')
speaker_session_count = df.drop_duplicates(subset=['speaker', 'session_title']).groupby('speaker').size().sort_values(ascending = False).head(10)
fig,ax = plt.subplots()
speaker_session_count.plot(kind = 'bar', ax = ax)
ax.set_xlabel('Speaker')
ax.set_ylabel('Number of Sessions')
st.pyplot(fig)

unique_session = df['session_title'].unique()

st.subheader('Members of parliament who spoke at each session')
selected_session = st.selectbox('Select the session', unique_session)

sentiment_df = df[df['session_title'] == selected_session]
sentiment_df = sentiment_df.groupby(['speaker'])['text'].apply(' '.join).reset_index()


examples = [ClassifyExample(text = ": Mr Speaker, employers are responsible to pay for their migrant worker’s medical expenses incurred in Singapore. Injured workers must be certified medically fit to fly, before being repatriated. Therefore, this prevents workers with serious injuries from being repatriated before they are treated. Employers are also prohibited from repatriating migrant workers whose presence in Singapore is required to process their work injury or salary claims. MOM took action against two errant employers for illegal repatriation of migrant workers in the past five years. MOM holds employers liable to pay for their migrant worker’s medical expenses incurred in Singapore. Under our laws, employers must buy medical insurance for migrant workers, which provides coverage of $15,000 and typically covers 95% of hospital bills arising from non-work injury. Most employers also buy work injury insurance coverage of at least $45,000 per accident, which will also cover 95% of work injury bills. Employers may claim the medical expenses from these insurance plans. For medical emergency cases, the hospitals will proceed even without LOGs. Workers are not denied such treatment regardless of their employer’s ability to pay. For non-emergency cases, hospitals may ask for LOG before treatment, to be assured that the employer knows and is able to pay. MOM is reviewing medical insurance coverage to help employers better manage large unexpected medical expenses and give both employers and workers greater peace of mind. Between 2016 and 2020, there were 63 substantiated cases of employers not paying medical bills of their migrant workers. For the vast majority of these cases, the employers paid up shortly after administrative actions were taken by MOM. The remaining employers who failed to pay were prosecuted under the Employment of Foreign Manpower Act. MOM educates new migrant workers about their employment rights and protections under Singapore law. And this is done via the Settling-In-Programme, or SIP. The SIP is conducted in the workers’ native languages to aid understanding. It covers workers’ entitlements to insurance coverage, healthcare access and work injury compensation. MOM has also produced a guide for migrant workers, in their native languages, on how to seek medical help and provided contact information of MOM and NGOs. Workers may also use the 24/7 telemedicine service in the FWMOMCare mobile application to consult doctors. At any time, workers may contact MOM about any employment issues through the reporting service on MOM website. Workers are also informed to alert ICA officers at immigration checkpoints if their employer attempts to repatriate them when they have a pending work injury or salary claim. : The hotline is just one channel. I do not have the numbers with me so I cannot comment on what the rates are at this point. The Member can always file a Parliamentary Question (PQ). What I can say is this, beyond the hotline, workers can always call the hotline but there is also the FWMOMCare app, in which they can do more than just report. They can also get telemedicine consultation service from doctors. At the same time, they can walk into any hospital and make a report, or work through any of the NGOs that are available. I know of many NGOs today who are very active on the ground. The Migrant Workers' Centre (MWC), for example, has migrant worker ambassadors too, among their peers, about 5,000 of them, who can also take feedback. If they stay in a dormitory, they can also report to the dorm operators and we will take those on board. Today, we have the Forward Assurance and Support Team or FAST teams which are very active on the on ground within the dorms; so they can report to any of our officers to inform them of some of the challenges. So, there are two things: one, you can reach out but the nearest is the FWMOMCare app and through which the workers can also receive telemedicine service. So, beyond just reporting, the workers can also receive telemedicine assistance. Both ways, to some extent, compared to a few years ago before these developments, I think today, we got a lot more coverage than before. As I mentioned, we are also reviewing the medical insurance coverage for the workers too. : I thank the Member for his query. In fact, the requests come under the hospitals because they would like to be assured that the employers can pay. In fact, for me personally, I do not think that this is needed. However, the hospitals have a very different view. This is something we will continue to work through with the hospitals, to assure them. My sense, as I shared earlier, 95% of cases are covered by both the medical insurance as well as work injury compensation insurance. What the hospitals have committed to is that for serious injury cases, they would take them in, even without the LOGs. For that, there will be no delay in treatment. However, these are things that we have to work through because I know hospitals too are concerned. They have to ascertain first that it is a work injury – that is one part to it. So, whether it is work injury or injury caused by something else. And secondly, the employers should be notified as well when their worker gets injured. Therefore, there is a process in place. But let us work through to see how we can make it more seamless for the workers. : Okay, thank you, Deputy Speaker. On this aspect, we are reviewing it. I do not have a deadline that I can commit at this point. But rest assured it will be soon. I would let Dr Tan See Leng take over for further comments.", 
                            label = 'neutral'), 
            ClassifyExample(text = ': May I ask the Minister of State, how does MOM balance the interests of employers who may be falsely accused by the foreign domestic worker? I have received feedback that there are occasions when a foreign domestic worker may not want to work with a particular family, because they have to look after the elderly or the house is too big, so they lodge a complaint to their Embassy. At the end of the day, no further action was taken against the employee and the foreign domestic then gets a free transfer out. Meanwhile, the employer is stuck because he is not allowed to hire another foreign domestic worker. He is also stuck in the sense that he has this so-called report made against him. So, how do we balance the interests of the foreign domestic worker versus an innocent employer who may be desperately looking to get another worker?', 
                            label = 'negative'), 
            ClassifyExample(text = ': We have been releasing information on the progress of our vaccination programme over the past few weeks, including the number of people vaccinated, through a variety of channels, including the MOH website.', 
                            label = 'neutral'), 
            ClassifyExample(text = ': I thank the Minister for his Statement. I think we certainly welcome the new framework. I have spoken on this on a number of occasions and I welcome the updates. Just one clarification I seek from the Minister. In the last two years, one of the questions that was raised is, quite a number of cases relate to those who have a position of trust with the victim. Just to rattle off some recent cases: teacher molests seven boys, former Secondary school teacher abuses 15-year-old students, Secondary school teacher molests boy in school lab, Primary school teacher molests 12-year-old boy and so on. You also have, recently: male nurse allegedly molests male patient, Statutory Board director outrages modesty of female subordinate, doctor at Mt E accused of molest against a female patient. Many of these are in a position of trust. Would the Ministry consider further enhancing the sentencing framework and increase the penalties for those who not only cause hurt or sexually abuse the victim, but start out from a position of trust, so that we ensure that such crimes where the victim already feels a sense of comfort in the presence of the person, does not fall prey to such offences.', 
                            label = 'negative'), 
            ClassifyExample(text = ': The Urban Redevelopment Authority (URA) and the Housing & Development Board (HDB) work closely together to plan the supply and development of land for housing in Singapore. These plans ensure a good mix of public and private housing, including executive condominiums (ECs), and a wide range of supporting amenities to serve the needs of the residents. In planning for the supply of land for ECs, the Government takes into consideration many factors, such as existing unsold stock, take-up rate of new EC units, and prevailing economic and housing market conditions, which can fluctuate from year to year. The Government will continue to monitor the EC market closely and adjust the supply of ECs in future Government Land Sales (GLS) Programmes as necessary.', 
                            label = 'positive'), 
            ClassifyExample(text = ': Home ownership is the cornerstone of our public housing programme, and the Government is committed to providing Singaporeans with affordable homes. To ensure affordability, HDB provides generous housing subsidies, especially to first-timer buyers. Eligibility conditions are put in place to ensure that these housing subsidies are targeted at those who need them the most. One such condition is the income ceiling. The income ceiling had been raised from $10,000 to $12,000 in August 2015 and from $12,000 to $14,000 in September 2019. At the current income ceiling of $14,000, about 8 in 10 citizen households qualify for subsidised public housing. Those who do not meet the eligibility conditions for subsidised public housing have the option of buying a resale flat on the open market without subsidy. Such households may be eligible for the Proximity Housing Grant, which does not have an income ceiling. HDB will continue to monitor the housing market closely to ensure that housing policies remain relevant and responsive to the needs of the population.', 
                            label = 'positive')

    
]

def classify_text(inputs, examples): 
    response = co.classify(
        model = 'embed-english-v2.0', 
        inputs = inputs, 
        examples = examples
    )

    classifications = response.classifications
    return classifications

def sentiment_classification(df, examples): 
    combined_text = df['text'].tolist()
    classifications = classify_text(combined_text, examples)
    df['sentiment'] = [classification.prediction for classification in classifications]
    return df

classified_df = sentiment_classification(sentiment_df, examples)

st.dataframe(classified_df[['speaker', 'sentiment']], width = 1000)

def summarize_text(df):
    summaries = []
    for index, row in df.iterrows():
        text = row['text']
        if 'asked' not in text.lower():
            response = co.summarize(
                text=text,
                model='command-light',
                length='medium',  
                format='bullets',  
                temperature=0.1,
            )
            summaries.append((row['speaker'], response.summary)) 
    return summaries

summaries = summarize_text(sentiment_df)

for index, row in sentiment_df.iterrows(): 
    speaker = row['speaker']
    text = row['text']
    if 'asked' in text.lower(): 
        st.write(f"Speaker: {speaker}")
        st.write(f"Question: {text}")

for speaker, summary in summaries:
    st.write(f"Speaker: {speaker}")
    st.write(f"{summary}")
