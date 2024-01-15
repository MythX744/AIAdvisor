from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from model import db, AIRecords
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64

app = Flask(__name__)

# import our excel file
file_path = 'AI-Advisor.xlsx'

# our dataframe
df = pd.read_excel(file_path)
df = df.iloc[:, 6:]
new_columns = ["Gender", "Age", "Status", "Usage", "Field", "Tasks", "Price", "Expectation", "Manner of usage",
               "Preference", "Ratings", "Impact"]
df.columns = new_columns

# Clean the data
# Expection
df['separated-Expectation'] = df['Expectation'].str.split(';')
# Explode choices into separate rows
data_exploded = df.explode('separated-Expectation')
# Handle missing values
data_exploded.dropna(subset=['separated-Expectation'], inplace=True)
choices_counts = data_exploded['separated-Expectation'].value_counts()

# Field
df['separated-Field'] = df['Field'].str.split(';')
# Explode choices into separate rows
data_exploded2 = df.explode('separated-Field')
# Handle missing values
data_exploded2.dropna(subset=['separated-Field'], inplace=True)
choices_counts2 = data_exploded2['separated-Field'].value_counts()

# Tasks
df['separated-Tasks'] = df['Tasks'].str.split(';')
# Explode choices into separate rows
data_exploded3 = df.explode('separated-Tasks')
# Handle missing values
data_exploded3.dropna(subset=['separated-Tasks'], inplace=True)
choices_counts3 = data_exploded3['separated-Tasks'].value_counts()


def convert(plt):
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url


def generate_chart1():
    df['Price'] = pd.Categorical(df['Price'], ['0$ (Free)', '1$ - 10$', '11$ - 50$', '51$ - 200$', '+ 200$'])
    sns.countplot(x='Price', hue='Status', data=df)
    plt.title('Relation between status and Price')
    title = 'Chart 1: Relation between status and Price'
    plot_url = convert(plt)
    analysis = ['''The count plot illustrates budget distribution across status categories. Each bar
represents a category, with height indicating occurrence count. Bar color
distinguishes status categories within each budget group, revealing how allocations
vary.''',
                '''We can identify that the status “Student” dominates in every budget category, and
tend to allocate a lower budget to AI tools comparing to other category, it decreases
whenever the budget increases. So we can say that student tend not to spend too
much on AI tools due to their status of being a student.''',
                ''' Retired/Unemployed" evenly
distributes across initial categories, reflecting lower AI tool spending, possibly due to
financial constraints, different spending priorities or limited interest or need.
Employed individuals spend relatively little money on AI tools, and not many of them
can allocate a budget in AI tools, influenced by workplace provisions and access to
advanced tools, reducing the need for personal investment.''']

    return plot_url, analysis, title


def generate_chart2():
    df['Price'] = pd.Categorical(df['Price'], ['0$ (Free)', '1$ - 10$', '11$ - 50$', '51$ - 200$', '+ 200$'])
    title = 'Chart 2: Distribution of Price based on the Gender'
    # Seperate hist for each gender
    male_price = df[df['Gender'] == 'Male']['Price']
    female_price = df[df['Gender'] == 'Female']['Price']
    plt.figure(figsize=(12, 6))
    # Hist for male price
    plt.subplot(1, 2, 1)
    sns.histplot(male_price, bins=10, kde=True, color='blue')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Price for Males')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    # Hist for female price
    plt.subplot(1, 2, 2)
    sns.histplot(female_price, bins=10, kde=True, color='red')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Price for Females')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plot_url = convert(plt)
    analysis = ['''Both graphs depict a right-skewed, unimodal distribution of prices
based on gender. It is evident that females tend to utilize free AI tools
more frequently than males and exhibit a slightly higher expenditure.
This trend may be attributed to variations in job roles and industries,
income disparities favoring females, and the perceived necessity for AI
tools. It is crucial to recognize that these explanations are
generalizations, and a multitude of environmental and personal factors
can affect an individual's decision-making process.
''']
    return plot_url, analysis, title


def generate_chart3():
    df['Usage'] = pd.Categorical(df['Usage'], ['None', 'Light', 'Moderate', 'High'])
    title = 'Chart 3: Distribution of Usage based on the Status'
    # Seperate hist for each gender
    student_usage = df[df['Status'] == 'Student']['Usage']
    unemployed_usage = df[df['Status'] == 'Retired/Unemployed']['Usage']
    employee_usage = df[df['Status'] == 'Employee']['Usage']
    plt.figure(figsize=(12, 6))
    # Hist for Usage for Students
    plt.subplot(2, 2, 1)
    sns.histplot(student_usage, bins=10, kde=True, color='blue')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Usage for Students')
    plt.xlabel('Usage')
    plt.ylabel('Frequency')
    # Hist for Usage for Unemployed
    plt.subplot(2, 2, 2)
    sns.histplot(unemployed_usage, bins=10, kde=True, color='red')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Usage for Unemployed')
    plt.xlabel('Usage')
    plt.ylabel('Frequency')
    # Hist for Usage for Employee
    plt.subplot(2, 2, 3)
    sns.histplot(employee_usage, bins=10, kde=True, color='green')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Usage for Employee')
    plt.xlabel('Usage')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plot_url = convert(plt)
    analysis = ['''Here we have three separate histograms for the usage distribution of AI tools based on
different status categories (Student, Retired/Unemployed and Employee).
Therefore, for the first graph, we have a bimodal distribution, which its peak stands on the
light and moderate usage of AI tools and the line provides a smooth estimate of the
distribution. For a light usage it suggests that students may use AI tools occasionally or for
specific tasks rather than as a regular and intensive part of their activities. In addition, for
moderate usage implies that certain students are more actively incorporating AI tools into
their activities, possibly for a broader range of tasks or with a somewhat regular frequency.
The second graph show a concave line of the distribution of usage for retired/unemployed.
For this status category, have an equal frequency of the light, moderate and high usage of AI
tools. The usage patterns of AI tools among retired/unemployed individuals reflect a
spectrum, with financial, motivational, and educational factors playing pivotal roles in
shaping their engagement with AI technologies
The third graph, we can observe a unimodal distribution with a little skewness to the right.
Moderate usage of AI tools among employees may signify a strategic and purposeful
integration of artificial intelligence into their workflow. It suggests that organizations are not
merely experimenting with AI but are adopting it in a measured and calculated manner.
''']
    return plot_url, analysis, title


def generate_chart4():
    gender_counts = df['Gender'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140)
    title = 'Chart 4: Distribution of Gender'
    plt.title('Distribution of Gender')
    plot_url = convert(plt)
    analysis = ['''The pie chart titled "Chart 4: Distribution of Gender" illustrates the gender distribution of a certain population or dataset. 
    The chart is divided into two segments, representing male and female categories: ''',
                '''The larger segment, representing females, constitutes 56.1% of the total. This indicates that in the population or dataset being analyzed, there are more females than males.
The smaller segment, representing males, accounts for 43.9% of the total.
The chart shows a relatively balanced distribution of genders, though females are represented slightly more than males.''',
                '''This suggests that AI tools may be more frequently adopted or preferred by females in the context from which the data was collected. 
The conclusion drawn from this data could indicate potential gender-based preferences or differences in the utilization of AI technologies. 
Understanding these disparities is crucial for developers and companies in the AI field to ensure that AI tools are inclusive and cater to the needs and preferences 
of a diverse user base. Additionally, it may prompt further investigation into the factors influencing these gender dynamics in AI tool usage.
''']
    return plot_url, analysis, title


def generate_chart5():
    df['Usage'] = pd.Categorical(df['Usage'], ['None', 'Light', 'Moderate', 'High'])
    sns.barplot(x='Usage', y='Preference', data=df)
    title = 'Chart 5: Relation between frequency of use and performance preference'
    plt.title('Relation between frequency of use and performance preference')
    plot_url = convert(plt)
    analysis = ['''Upon analyzing the depicted relationship between the frequency of
usage and the preferred performance rate of AI tools—specifically, their
processing speed—we observe a subtle uptick in the preferred
performance rate as the usage frequency increases. This phenomenon is
attributed to avid users who prioritize faster tools to minimize time
consumption and efficiently accomplish a greater number of tasks.
In contrast, individuals who either don't utilize these tools or use them
sparingly may not place as much emphasis on the performance factor,
considering it less crucial to their usage patterns.
''']
    return plot_url, analysis, title


def generate_chart6():
    df['Manner of usage'] = pd.Categorical(df['Manner of usage'], ['Both', 'Professional', 'Personal'])
    title = 'Chart 6: Distribution of Usage based on the Age'
    # Seperate hist for each gender
    u18_usage = df[df['Age'] == 'Under 18']['Manner of usage']
    cat_18_24 = df[df['Age'] == '18-24']['Manner of usage']
    cat_25_44 = df[df['Age'] == '25-44']['Manner of usage']
    cat_45_64 = df[df['Age'] == '45-64']['Manner of usage']
    cat_65 = df[df['Age'] == '65 and older']['Manner of usage']

    plt.figure(figsize=(12, 6))

    # Hist for Usage for Students
    plt.subplot(3, 3, 1)
    sns.histplot(u18_usage, bins=10, kde=True, color='blue')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Usage for under 18')
    plt.xlabel('Usage')
    plt.ylabel('Frequency')

    # Hist for Usage for Unemployed
    plt.subplot(3, 3, 2)
    sns.histplot(cat_18_24, bins=10, kde=True, color='red')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Usage for 18-25')
    plt.xlabel('Usage')
    plt.ylabel('Frequency')

    # Hist for Usage for Employee
    plt.subplot(3, 3, 3)
    sns.histplot(cat_25_44, bins=10, kde=True, color='green')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Usage for 25-44')
    plt.xlabel('Usage')
    plt.ylabel('Frequency')

    # Hist for Usage for Employee
    plt.subplot(3, 3, 4)
    sns.histplot(cat_45_64, bins=10, kde=True, color='pink')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Usage for 45-64')
    plt.xlabel('Usage')
    plt.ylabel('Frequency')

    # Hist for Usage for Employee
    plt.subplot(3, 3, 5)
    sns.histplot(cat_65, bins=10, kde=True, color='yellow')  # kde : to have the line that shows the distribution
    plt.title('Distribution of Usage for 65 and older')
    plt.xlabel('Usage')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plot_url = convert(plt)
    analysis = [
        "Under 18: ",
        '''For users below 18, there is a notable absence of AI tool usage for professional purposes.
This can be attributed to their limited exposure to the professional work environment.
At this age, individuals are generally not confronted with substantial job-related tasks,
making them more inclined to utilize AI tools for a combination of personal and
professional needs or solely for personal benefits.''',
        "18-25: ",
        '''Within this age bracket, the data illustrates a prevalent trend of using AI tools for both
personal and professional purposes, with a higher preference for the former. As
individuals transition from 18 years and above, exposure to a work-focused environment
becomes more prominent. Consequently, there is an increasing number of users
considering or opting for AI tools in professional settings compared to personal use''',
        "25-44:",
        '''Similar to the previous age group, users aged between 25 and 44 exhibit a
comparable pattern, although the margin between those exclusively using AI tools
professionally and those using them solely for personal purposes is narrower. This
could be attributed to individuals in this age range seeking a balance between workrelated tools and those enhancing their quality of life or opting for less work-intensive
paths.''',
        "45-64: ",
        '''The usage trend in this age group closely mirrors that of individuals between 25 and
44. Similar lifestyles and priorities contribute to a parallel distribution of AI tool usage
preferences. The slight variation may be associated with certain individuals in the 45-
64 age range desiring tools for lifestyle improvements or opting for less work-centric
paths.
''',
        "65 and above: ",
        '''Users in this age category predominantly express a preference for personal
usage of AI tools.
This inclination can be straightforwardly explained by the likelihood that
many individuals in this group are retirees, emphasizing a shift towards
personal needs and interests rather than professional requirements.
'''
    ]

    return plot_url, analysis, title


def generate_chart7():
    title = 'Chart 7: Relation between status and type of use of AI tools'
    sns.countplot(x='Status', hue='Manner of usage', data=df)
    plt.title('Relation between status and type of use of AI tools')
    plot_url = convert(plt)
    analysis = ['''When analyzing this plot alongside the one depicting usage distribution
across age groups, it becomes evident that students are likely predominant in
the under-18 and 18 to 25 age categories, as evidenced by the prevalent
choice of both usage types within these groups.
Similarly, for employees, the plot reveals consistent shifts in usage patterns,
notably with a higher percentage of professional-only users compared to the
overall user base. This suggests a probable representation of individuals aged
25 to 44 and 45 to 64.''',
                '''Examining the statistics for retired or unemployed individuals, a logical trend
emerges with personal usage surpassing professional use. This aligns with the
needs of these individuals, particularly those aged 65 and above.
Nevertheless, there are instances of individuals in these categories opting for
both usage types or exclusively professional use, likely indicating unemployed
or early retired adults within the previously mentioned age groups.

''']
    return plot_url, analysis, title


def generate_chart8():
    fields = df['Field'].str.get_dummies(sep=';').sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    fields.plot(kind='barh')
    plt.title('Fields where AI Tools are Deemed Useful')
    plt.xlabel('Count')
    plt.ylabel('Field')
    plot_url = convert(plt)
    analysis = ['''
    Chart 8 depicts how AI tools are viewed to be useful across various content types. "Text" related tasks, such as writing blog posts, 
    articles, product descriptions, and social media posts, are where AI tools are seen as most useful, with a count significantly higher 
    than other categories. This shows a substantial reliance on AI for textual content generation and management, which is a cornerstone of 
    online communication and marketing. The tasks listed below are "Code" related, demonstrating the usefulness of AI in software development and web design. 
    "Creative text formats" and "Visual content" also have significant counts, showing, if to a lesser extent, AI's role in artistic and multimedia undertakings. 
    The least perceived utility is in "Audio content" and "Study," suggesting these areas may currently have less AI integration or awareness about AI's capabilities 
    among the respondents.''',
                '''
    The graphic depicts a trend in which AI is most likely to impact areas with a high textual component, maybe due to the maturity of AI in natural language 
    processing, which can efficiently support these jobs. The significant figure for "Code" shows an acknowledgement of AI's rising significance in automating 
    and assisting complex problem-solving processes in technical sectors. However, the lower value perception in "Audio content" and "Study" could indicate either 
    a current lack of sophisticated AI tools in these sectors or a lesser importance placed on these tasks by the surveyed group. The research suggests that there 
    is a need for increasing awareness or development of AI applications in educational support and audio processing to match the value found in text and coding applications.
    ''']
    title = '''Chart 8: Fields where AI Tools are deemed useful'''
    return plot_url, analysis, title


def generate_chart9():
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Status', y='Ratings', data=df)
    plt.title('Willingness to Share Data by Status')
    plt.xlabel('Status')
    plt.ylabel('Willingness to Share Data')
    plt.xticks(rotation=45)
    plot_url = convert(plt)
    analysis = ['''
Willingness to Share Data by Status : ''',
                '''Status Variation: Different statuses (like student, employed, retired) show varying levels of willingness to share data.
Comparative Analysis: Comparing the medians across different statuses can reveal which groups are more open to sharing their data.
Consistency and Spread: The consistency within each status group and the spread of responses (indicated by the height of the boxes and the whiskers) provide insights into how homogeneous the opinions are within each status group.
Outliers: Observing any outliers can indicate exceptions or unique cases in specific statuses.''',
                '''Variation by Status: Different statuses (student, employed, retired, etc.) exhibit different levels of willingness to share data. This suggests that one's professional or social status influences their perspective on data sharing.
Comparison of Groups: Certain statuses might show a higher median, indicating a greater openness to sharing data. For instance, if students have a higher median than retired individuals, it could suggest that those in academia or early in their careers are more comfortable with data sharing.
Outliers: The presence of outliers in certain groups might indicate exceptions or specific sub-groups within those categories that have distinctly different views on data sharing.
    ''']
    title = '''Chart 9: Relation between Status and Willingness to Share Data'''
    return plot_url, analysis, title


def generate_chart10():
    choices_countsIndex = choices_counts.index[1:]
    choices_countsValue = choices_counts.values[1:]
    plt.bar(choices_countsIndex, choices_countsValue)
    plt.title('Distribution of Choices')
    plt.ylabel('Frequency')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plot_url = convert(plt)
    analysis = ['''
    The bar chart, titled "Chart 10: Distribution of the expectation of AI tools," 
    illustrates participants' expectations regarding AI tool capabilities. "Intelligent Tutoring Systems" ranks as the most anticipated application, 
    slightly surpassing "Assessment and Evaluation" in frequency. "Personalisation" follows closely, indicating a moderately high expectation, 
    while "Profiling and Prediction" is the least expected AI tool feature''',
                '''
    we can interpret that there is a clear preference among participants for AI tools that support educational functions, such as "Intelligent Tutoring Systems" 
    and "Assessment and Evaluation," which have the highest frequencies. The relatively lower expectation for "Personalisation" suggests that while there is interest in 
    AI that tailors experiences or content, it is not as prioritized as the educational applications. The least expectation for "Profiling and Prediction" could indicate 
    a lesser interest or possible concerns about AI tools that delve into user profiling and behavior prediction, possibly due to privacy considerations. 
    Overall, the chart demonstrates a trend towards favoring AI applications that enhance learning and performance over those that require extensive personal data analysis.
    ''']
    title = '''Chart 10: Distribution of the expectation of AI tools'''
    return plot_url, analysis, title



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airecords.db'
db.init_app(app)

# Set up the application context
with app.app_context():
    # Create the tables
    db.create_all()
    # Insert the first 5 AIs
    ai1 = AIRecords(name='CopyAI', description='Text generation tool', field='Text', expectation='Profiling and Prediction', performance_rate=7, personaldata='Low', price='free', task='Text-related tasks')
    ai2 = AIRecords(name='ChatGPT 3.5', description='Language model', field='Text, Code', expectation='Profiling and Prediction, Assessment and Evaluation, Personalization, Intelligent Tutoring Systems', performance_rate=8, personaldata='Low', price='free, 200+', task='Text and code-related tasks')
    ai3 = AIRecords(name='Hivemind', description='Text analysis tool', field='Text', expectation='Profiling and Prediction', performance_rate=6, personaldata='Low', price='200+', task='Text-related tasks')
    ai4 = AIRecords(name='WordAI', description='Text rewriting tool', field='Text', expectation='Profiling and Prediction', performance_rate=6, personaldata='Low', price='11-50', task='Text-related tasks')
    ai5 = AIRecords(name='Quillbot', description='Paraphrasing tool', field='Text', expectation='Profiling and Prediction', performance_rate=6, personaldata='Low', price='11-50', task='Text-related tasks')

    # Add and commit the records
    db.session.add_all([ai1, ai2, ai3, ai4, ai5])
    db.session.commit()

    # Insert the next 5 AIs
    ai6 = AIRecords(name='Jasper', description='AI-powered personal assistant', field='Text', expectation='Profiling and Prediction', performance_rate=7, personaldata='Low', price='51-200', task='Household chores and cleaning')
    ai7 = AIRecords(name='OpenAI Codex', description='AI for code generation', field='Code', expectation='Profiling and Prediction', performance_rate=8, personaldata='Low', price='11-50', task='Code-related tasks')
    ai8 = AIRecords(name='Copilot', description='AI-powered code completion', field='Code', expectation='Profiling and Prediction', performance_rate=8, personaldata='Low', price='11-50', task='Code-related tasks')
    ai9 = AIRecords(name='DALL-E 2', description='AI for visual content creation', field='Visual Content', expectation='Profiling and Prediction', performance_rate=8, personaldata='Low', price='11-50', task='Visual content creation')
    ai10 = AIRecords(name='Leonardo AI', description='AI for visual content creation', field='Visual Content', expectation='Profiling and Prediction', performance_rate=7, personaldata='Low', price='11-50', task='Visual content creation')

    # Add and commit the records
    db.session.add_all([ai6, ai7, ai8, ai9, ai10])
    db.session.commit()

    # Insert the next 5 AIs
    ai11 = AIRecords(name='Synthesia', description='AI for visual content creation', field='Visual Content', expectation='Profiling and Prediction', performance_rate=7, personaldata='Low', price='11-50, 51-200', task='Visual content creation')
    ai12 = AIRecords(name='Runway', description='AI for visual content creation', field='Visual Content', expectation='Profiling and Prediction', performance_rate=7, personaldata='Low', price='11-50, 51-200', task='Visual content creation')
    ai13 = AIRecords(name='Luma', description='AI for visual content creation', field='Visual Content', expectation='Profiling and Prediction', performance_rate=7, personaldata='Low', price='51-200', task='Visual content creation')
    ai14 = AIRecords(name='AudioSonic', description='AI for audio content creation', field='Audio Content', expectation='Profiling and Prediction', performance_rate=7, personaldata='Low', price='11-50, 51-200', task='Audio content creation')
    ai15 = AIRecords(name='Speechify', description='AI for audio content creation', field='Audio Content', expectation='Profiling and Prediction', performance_rate=7, personaldata='Low', price='200+', task='Audio content creation')

    # Add and commit the records
    db.session.add_all([ai11, ai12, ai13, ai14, ai15])
    db.session.commit()

    # Insert the next 5 AIs
    ai16 = AIRecords(name='Fitbit', description='Health and fitness tracking device', field=None, expectation='Health and fitness', performance_rate=9, personaldata='A Lot', price='free', task='Health and fitness tracking')
    ai17 = AIRecords(name='MyFitnessPal', description='Health and fitness tracking app', field=None, expectation='Health and fitness', performance_rate=8, personaldata='A Lot', price='11-50', task='Health and fitness tracking')
    ai18 = AIRecords(name='Nest', description='Smart home automation system', field=None, expectation='Smart home automation', performance_rate=9, personaldata='A Lot', price='free', task='Smart home automation')
    ai19 = AIRecords(name='SmartThings', description='Smart home automation platform', field=None, expectation='Smart home automation', performance_rate=8, personaldata='A Lot', price='free', task='Smart home automation')
    ai20 = AIRecords(name='Adaptive Learning Systems', description='AI for educational purposes', field=None, expectation='Educational purposes', performance_rate=7, personaldata='A Lot', price='200+', task='Educational purposes')

    # Add and commit the records
    db.session.add_all([ai16, ai17, ai18, ai19, ai20])
    db.session.commit()


    # Insert the next 5 AIs
    ai21 = AIRecords(name='Apple Siri', description='Apple\'s virtual assistant', field=None, expectation='Personal assistant tasks', performance_rate=8, personaldata='A Lot', price='free', task='Personal assistant tasks')
    ai22 = AIRecords(name='Google Assistant', description='Google\'s virtual assistant', field=None, expectation='Personal assistant tasks', performance_rate=8, personaldata='A Lot', price='free', task='Personal assistant tasks')
    ai23 = AIRecords(name='Amazon Alexa', description='Amazon\'s virtual assistant', field=None, expectation='Personal assistant tasks', performance_rate=8, personaldata='A Lot', price='free', task='Personal assistant tasks')
    ai24 = AIRecords(name='Microsoft Cortana', description='Microsoft\'s virtual assistant', field=None, expectation='Personal assistant tasks', performance_rate=8, personaldata='A Lot', price='free', task='Personal assistant tasks')
    ai25 = AIRecords(name='Facebook Portal', description='Smart display with video calling', field=None, expectation='Socializing and maintaining relationships', performance_rate=8, personaldata='A Lot', price='free', task='Socializing and maintaining relationships')

    # Add and commit the records
    db.session.add_all([ai21, ai22, ai23, ai24, ai25])
    db.session.commit()

    # Insert the next 5 AIs
    ai26 = AIRecords(name='Google Search', description='Search engine by Google', field=None, expectation='Information retrieval and search', performance_rate=9, personaldata='A Lot', price='free', task='Information retrieval and search')
    ai27 = AIRecords(name='Amazon Echo', description='Smart speaker by Amazon', field=None, expectation='Smart home automation', performance_rate=8, personaldata='A Lot', price='free', task='Smart home automation')
    ai28 = AIRecords(name='Google Maps', description='Mapping and navigation service by Google', field=None, expectation='Commuting or travel assistance', performance_rate=9, personaldata='A Lot', price='free', task='Commuting or travel assistance')
    ai29 = AIRecords(name='Grammarly', description='Writing assistance tool', field=None, expectation='Profiling and Prediction', performance_rate=8, personaldata='A Lot', price='free, 11-50', task='Text-related tasks')

    # Add and commit the records
    db.session.add_all([ai26, ai27, ai28, ai29])
    db.session.commit()

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/chart1', methods=['GET'])
def chart1():
    plot_url, analysis, title = generate_chart1()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart2', methods=['GET'])
def chart2():
    plot_url, analysis, title = generate_chart2()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart3', methods=['GET'])
def chart3():
    plot_url, analysis, title = generate_chart3()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart4', methods=['GET'])
def chart4():
    plot_url, analysis, title = generate_chart4()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart5', methods=['GET'])
def chart5():
    plot_url, analysis, title = generate_chart5()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart6', methods=['GET'])
def chart6():
    plot_url, analysis, title = generate_chart6()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart7', methods=['GET'])
def chart7():
    plot_url, analysis, title = generate_chart7()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart8', methods=['GET'])
def chart8():
    plot_url, analysis, title = generate_chart8()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart9', methods=['GET'])
def chart9():
    plot_url, analysis, title = generate_chart9()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/chart10', methods=['GET'])
def chart10():
    plot_url, analysis, title = generate_chart10()
    return render_template('index.html', plot_url=plot_url, analysis=analysis, title=title)


@app.route('/bonus', methods=['GET'])
def bonus():
    return render_template('welcome.html')


# Mehdi's part:
app.config['user_data'] = []
app.config['advisor_data'] = []


@app.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        status = request.form['status']
        app.config['user_data'].append({'gender': gender, 'age': age, 'status': status})

        return redirect(url_for('page2'))

    return render_template('page1.html')


@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        usage = request.form['usage']
        field = request.form.getlist('field')
        tasks = request.form.getlist('tasks')
        app.config['user_data'].append({'usage': usage, 'field': field, 'tasks': tasks})
        app.config['advisor_data'].append({'field': field, 'tasks': tasks})

        return redirect(url_for('page3'))

    return render_template('page2.html')


@app.route('/page3', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        spending = request.form['spending']
        expectations = request.form.getlist('expectations')
        usage_manner = request.form['usage_manner']
        app.config['user_data'].append(
            {'spending': spending, 'expectations': expectations, 'usage_manner': usage_manner})
        app.config['advisor_data'].append({'spending': spending, 'expectations': expectations})

        return redirect(url_for('page4'))

    return render_template('page3.html')


@app.route('/page4', methods=['GET', 'POST'])
def page4():
    if request.method == 'POST':
        rating = request.form['rating']
        rating_star = request.form['rating1']
        impact = request.form['impact']
        app.config['user_data'].append({'rating': rating, 'rating_star': rating_star, 'impact': impact})
        app.config['advisor_data'].append({'rating': rating, 'rating_star': rating_star})

        return redirect('/BonusResult')

    return render_template('page4.html')


all_user_data = app.config['user_data']
all_advisor_data = app.config['advisor_data']
print("all user data: " + str(all_user_data))
print("all advisor data: " + str(all_advisor_data))


@app.route('/BonusResult', methods=['GET'])
def result():
    all_data = app.config['user_data']
    print(all_data)
    return render_template('result.html', all_data=all_data)


@app.route('/get_cleaned_data', methods=['GET'])
def get_cleaned_data():
    choices_counts_df = pd.DataFrame({
        "axis": choices_counts.index,
        "value": choices_counts.values
    })

    choices_counts2_df = pd.DataFrame({
        "axis": choices_counts2.index,
        "value": choices_counts2.values
    })

    choices_counts3_df = pd.DataFrame({
        "axis": choices_counts3.index,
        "value": choices_counts3.values
    })

    cleaned_dfs = [choices_counts_df, choices_counts2_df, choices_counts3_df]
    cleaned_data = []

    for df in cleaned_dfs:
        df2 = df.dropna(subset=['axis']).replace('', pd.NA).dropna(subset=['axis'])
        # Convert DataFrame to a list of dictionaries
        data = df2.to_dict(orient='records')

        # Convert axis and value to a structure without quotes
        data = [{key: str(val) for key, val in entry.items()} for entry in data]

        cleaned_data.append(data)

    # Wrap the cleaned_data list in another list to match the structure you need
    cleaned_data = [cleaned_data]

    print(cleaned_data)
    return jsonify(cleaned_data=cleaned_data)


if __name__ == '__main__':
    app.run(debug=True)
