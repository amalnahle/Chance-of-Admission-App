import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly
from plotly.offline import iplot
import streamlit as st

plotly.offline.init_notebook_mode(connected= True)

#google drive url
url = 'https://drive.google.com/file/d/1yU8vVr3MFXegrWdnJzwYt75jxH0JauBK/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
data = pd.read_csv(path)


#app title
st.title('Chance of Admission into Graduate Studies')

#load data
@st.cache
def load_data(nrows):
    data = pd.read_csv(path, nrows=nrows)
    return data

#Let the reader know the data is loading
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(100)
# Notify the reader that the data was successfully loaded.
data_load_state.text("You're set!")

#inspect/toggle data
if st.checkbox('Show a sample of the data'):
    st.subheader('Raw Data')
    st.write(data)
   

#widget left
option = st.selectbox(
    'What can this data be used for?',
     ("Predictive Modeling", "Classification Modeling"))

'You selected:', option 

if option=="Predictive Modeling":
    expander0 = st.beta_expander("Predictive Model")
    expander0.write("""A predictive model can be generated where the chance
                    of admission of a new student will be forecasted
                    according to the criteria he possesses.""")
                    
if option=="Classification Modeling":
    expander1 = st.beta_expander("Classification Model")
    expander1.write("""A classification model can be generated that
                   will forecast whether or not the new student will be admitted
                    according to the criteria he possesses. Note: the chance variable needs
                    to be transformed into a binary variable.""")                   

#column names
list1= list(data.columns)
print(list1)


st.subheader('Info about variables')
st.write('(Press below)', size=5)

#widget, info about GRE and TOEFL variable
left_column, right_column = st.beta_columns(2)
pressed = left_column.button('GRE, TOEFL')
if pressed:
    right_column.write("""Student's GRE and TOEFL test scores\n
                       GRE Range: 260-340, TOEFL Range: 0-120""")
                       
#widget, info about SOP and LOR variable
left_column, right_column = st.beta_columns(2)
pressed = left_column.button('SOP, LOR')
if pressed:
    right_column.write("""Student's Statement of Purpose and Letter of Recommendation strengths\n
                       Range: 1-5 (5: highest strength) """)

#widget, info about Uni Rating 
left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Uni Rating')
if pressed:
    right_column.write("""Rating of the uni the student is applying to\n
                       Range: 1-5 (5: best rating)""")
                       
#widget, info about CGPA 
left_column, right_column = st.beta_columns(2)
pressed = left_column.button('CGPA')
if pressed:
    right_column.write("""Student's Cumulative GPA in undergrad studies\n
                       Range: 0-10""")  
                       
#widget, info about Research
left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Research')
if pressed:
    right_column.write("""Student's possession of research experience\n
                       1: has research experience, 0: doesn't have research experience""")  

#widget, info about Chance 
left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Chance')
if pressed:
    right_column.write("""Student's chance of admission into uni\n
                       Range: 0-1""")
                       
st.subheader('Data Exploration')                     
#bivariate relationships
fig = px.scatter_matrix(data, dimensions=["GRE ", "TOEFL ", "SOP", "LOR ", "CGPA"], color="Chance ", title="Bivariate Relationships")
st.write(fig)   


#explanation
expander = st.beta_expander("Insight")
expander.write("""There is a positive correlation between GRE and TOEFL. 
               The same association is observed between the GRE and 
               CGPA, and TOEFL and CGPA. Recommendation 
               letters are expected to be better for students with high CGPA.""")

#scatterplot, box plot, violin plot
fig1 =px.scatter(data, x="CGPA", y="Chance ",
           size="Research", color="LOR ", title="Relationship between Chance of Admission and CGPA", marginal_y="violin",
           marginal_x="box")
st.write(fig1)


#explanation
expanderr = st.beta_expander("Insight")
expanderr.write("""There is a positive association between CGPA and
               Chance of Admission: the higher the CGPA is, the higher 
               the student’s chance of admission.""")
               
#barplot
fig2b = px.bar(data, x="Uni Rating", y="Chance ", color="Research", barmode="group", title= "Chance of admission vs University rating")
st.write(fig2b)

#explanation
expander1 = st.beta_expander("Insight")
expander1.write("""Most students who apply for top rated universities (rated 4-5)
                have research experience.""")

#side-by-side boxplots
fig3 = px.box(data, x="Uni Rating", y="Chance ", color="Research", notched=True, title="Boxplots of University Rating and Chance")
st.write(fig3)

#explanation
expander2 = st.beta_expander("Insight")
expander2.write("""The higher the university rating, 
                the higher the student's chance of admission.""")

#barplot
research = go.Histogram(x=data["Uni Rating"],
                  y=(data[data["Research"]==1]),
                  name='Research Experience',
                  marker=dict(color='#ffcdd2'))

no_research = go.Histogram(x=data["Uni Rating"],
                  y=(data[data["Research"]==0]),
                  name='No Research Experience',
                  marker=dict(color='#A2D5F2'))


data1 = [research, no_research]

layout = go.Layout(title="Students with & without research experience",
                xaxis=dict(title='Uni Rating'), yaxis=dict(title='Count'))

fig4 = go.Figure(data=data1, layout=layout)

plotly.offline.iplot(fig4, filename='jupyter-styled_bar')



#add dropdown
fig4.update_layout( 
    updatemenus=[ 
        dict( 
            type="buttons", 
            direction="left", 
            buttons=list([ 
                dict(label="Both", 
                     method="update", 
                     args=[{"visible": [True, True]}, 
                           {"title": "Students with & without research experience"}]), 
                dict(label="Research", 
                     method="update", 
                     args=[{"visible": [True, False]}, 
                           {"title": "Students with research experience", 
                            }]), 
                dict(label="No Research", 
                     method="update", 
                     args=[{"visible": [False, True]}, 
                           {"title": "Students without research experience", 
                            }]), 
            ]), 
        ) 
    ]) 
  
 
st.write(fig4)


#explanation
expander3 = st.beta_expander("Insight")
expander3.write("""The highest proportion of students
                apply to universities with a rating of 3.""")
                
#animated scatterplot
fig5 =px.scatter(data, x="CGPA", y="Chance ",
           title="Relationship between chance of admission, CGPA, and Uni rating", animation_frame="Uni Rating")
st.write(fig5)

#explanation
expander3 = st.beta_expander("Insight")
expander3.write("""Students who apply for high-rated universities (rated 5) have higher
                CGPAs than those who apply for lower-rated ones (rated 1-2), with a higher
                chance of admission.""")