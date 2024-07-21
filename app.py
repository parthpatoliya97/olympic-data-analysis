import streamlit as st
import pandas as pd
import preprocessor
import plotly.express as px
import helper
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")    

df=preprocessor.preprocess(df,region_df)

st.sidebar.header("Olmpics Analysis")   
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu=st.sidebar.radio(
    "Select an  Option",
    ("Medal Tally","Overall Analysis","Country-wise Analysis","Athelete wise Analysis")
)
# st.dataframe(df)

if user_menu=="Medal Tally":
    # st.header("Medal Tally")
    years,country=helper.country_year_list(df)
    
    selected_year=st.sidebar.selectbox("Select year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=="Overall" and selected_country=="Overall":
        st.title("Overall Tally")
    if selected_year!="Overall" and selected_country=="Overall":
        st.title("Medal Tally in " +str(selected_year)+ " Olympics")
    if selected_year=="Overall" and selected_country!="Overall":
        st.title(selected_country+ " Overall perfomance")
    if selected_year!="Overall" and selected_country!="Overall":
        st.title(selected_country+" perfomance in " +str(selected_year)+ " Olympic")
    
    st.table(medal_tally)
    
if user_menu=="Overall Analysis":
    edition=df["Year"].unique().shape[0]-1
    cities=df["City"].unique().shape[0]
    sports=df["Sport"].unique().shape[0]
    events=df["Event"].unique().shape[0]
    athletes=df["Name"].unique().shape[0]
    nations=df["region"].unique().shape[0]
    
    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Edition")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
        
        
         
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    
    
    nations_over_time=helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x="Edition",y="No Of Countries" )
    st.title("Participating Nations Over The Years :")
    st.plotly_chart(fig)
    
    Eventsover_time=helper.Events_over_time(df)
    fig = px.line(Eventsover_time, x="Edition",y="Events" )
    st.title("Events Over The Years :")
    st.plotly_chart(fig)
    
    Athlets_over_time=helper.Athlets_over_time(df)
    fig = px.line(Athlets_over_time, x="Edition",y="Athlets" )
    st.title("Athlets Over The Years :")
    st.plotly_chart(fig)
    
    
    st.title("No of Evnets Over time(Every Sport):")
    
    x=df.drop_duplicates(subset=["Year","Sport","Event"])
    fig=plt.figure(figsize=(20,20))
    sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype("int"),annot=True)
    st.pyplot(fig)
    
    
    st.title("Most Sucessful Athletes")
    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "overall")
    selected_sport=st.sidebar.selectbox("Select a Sport",options=sport_list)
    x=helper.most_succesful(df,selected_sport)
    st.table(x)


if user_menu=="Country-wise Analysis":
    country_list=df["region"].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox("Select a Country",options=country_list)
    
    country_df=helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year",y="Medal" )
    st.title(selected_country +" Medal Tally Over The Years :")
    st.plotly_chart(fig)
    
    st.title(selected_country +" Excels in the Following Sport  :")
    pt=helper.country_event_heatmap(df,selected_country)
    fig=plt.figure(figsize=(20,20))
    sns.heatmap(pt,annot=True)
    st.pyplot(fig)
    
    st.title("Top 10 Athletes of " +selected_country)
    top10_df=helper.most_succesful_country_wise(df,selected_country)
    st.table(top10_df)
    
if user_menu=="Athelete wise Analysis":
    athlete_df=df.drop_duplicates(subset=["Name","region"])
    
    x1=athlete_df["Age"].dropna()
    x2=athlete_df[athlete_df["Medal"]=="Gold"]["Age"].dropna()
    x3=athlete_df[athlete_df["Medal"]=="Silver"]["Age"].dropna()
    x4=athlete_df[athlete_df["Medal"]=="Bronze"]["Age"].dropna()
    
    fig=ff.create_distplot([x1,x2,x3,x4],["Overall Age","Gold Medalist","Silver Medalist","Bronze Medalist"],show_hist=False,show_rug=False)
    
    fig.update_layout(width=1000,height=600,autosize=False)
    st.title("Distribution Of Age")
    st.plotly_chart(fig)
    
    
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
     
    x=[]
    name=[]
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df["Sport"]==sport]
        x.append(temp_df[temp_df["Medal"]=="Gold"]["Age"].dropna())
        name.append(sport)  
        
    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(width=1000,height=600,autosize=False)
    st.title("Distribution Of Age wrt Sport(Gold Medalist)")
    st.plotly_chart(fig)
    
    st.title("Height Vs Weight")
    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "overall")
    selected_sport =st.selectbox("Select a Sport",sport_list)
    temp_df=helper.weight_V_height(df,selected_sport)
    
    fig=plt.figure(figsize=(8,8))
    sns.scatterplot(temp_df,x="Weight",y="Height",hue="Medal",style="Sex",s=60)
    
    st.plotly_chart(fig)
    
    st.title("Men Vs Women Participation Over the Years")
    final_df=helper.men_v_women(df)
    fig=px.line(final_df,x="Year",y=["Male","Female"])
    fig.update_layout(width=1000,height=600,autosize=False)
    st.plotly_chart(fig)
    
    
    
     