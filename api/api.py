import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MultipleLocator
from tabulate import tabulate
from flask import Flask, jsonify, send_file

#load dataset
df = pd.read_csv("dataset/datasetcleaned.csv", encoding="latin1")

#----------------------------------------------------------------
app = Flask(__name__)
#----------------------------------------------------------------
@app.route('/')
def mainpage():
    try:
        with open('files/index.txt', 'r', encoding='utf-8') as file:
            texto = file.read()  
        return f'<pre>{texto}</pre>'
    except FileNotFoundError:
        return jsonify({'error': 'The file index.txt was not found.'})
    except Exception as e:
        return jsonify({'error': str(e)})

def load_data(archivo, region=None):
    try:
        df_cleaned = pd.read_csv(archivo, encoding='latin1')
        if region:
            df_filtered = df_cleaned[df_cleaned['Region'] == region]
        else:
            df_filtered = df_cleaned
        datos = df_filtered.to_dict(orient='records')
        return jsonify(datos)
    except FileNotFoundError:
        return jsonify({'error': f'El archivo {archivo} no se encontró.'})
    except Exception as e:
        return jsonify({'error': str(e)})

#----------------------------------------------------------------
@app.route('/DATASET')
def get_data():
    return load_data('dataset/datasetcleaned.csv')

@app.route('/DATASET/CA')
def get_data_CA():
    return load_data('dataset/datasetcleaned.csv', region='CA')

@app.route('/DATASET/TX')
def get_data_TX():
    return load_data('dataset/datasetcleaned.csv', region='TX')

@app.route('/DATASET/PA')
def get_data_PA():
    return load_data('dataset/datasetcleaned.csv', region='PA')
#----------------------------------------------------------------
@app.route('/question1', methods=['GET'])
def handed_analysis():
    handed_counts = df['Handed'].value_counts()
    handed_counts_df = handed_counts.to_frame().reset_index()
    handed_counts_df.columns = ['Laterality', 'Quantity']

    plt.figure(figsize=(8, 6))
    ax = handed_counts.plot(kind='bar', color=['blue', 'orange', 'green'])
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')
    plt.title('Number of students by type of laterality:')
    plt.xlabel('Laterality')
    plt.ylabel('Number of students')
    plt.xticks(rotation=0)

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/png')

@app.route('/question1.2', methods=['GET'])
def handed_analysis_byregion():
    foot_length_by_region = df.groupby(['Region', 'Longer_foot']).size().unstack(fill_value=0)
    plt.figure(figsize=(10, 6))
    ax = foot_length_by_region.plot(kind='bar', stacked=True)
    plt.title('Number of students by type of foot length and region:')
    plt.xlabel('Region')
    plt.ylabel('Number of students')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Foot Length')
    plt.tight_layout()
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        ax.annotate(f'{height}', (x + width / 2, y + height / 2), ha='center', va='center')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/png') 

# ----------------------------------------------------------------
@app.route('/question2', methods=['GET'])
def question2_1():
    foot_length_counts = df['Longer_foot'].value_counts().reset_index()# Count how many students have the longest each foot.
    foot_length_counts.rename(columns={'Longer_foot': 'Foot', 'count': 'Count'}, inplace=True)
    plt.figure(figsize=(8, 6))
    ax = foot_length_counts.plot(kind='bar', x='Foot', y='Count', color=['orange', 'blue', 'green']) # Plot the results
    for p in ax.patches: # Add the values in each bar
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')
    plt.title('Number of students by type of foot length:')
    plt.xlabel('Foot Length')
    plt.ylabel('Number of students')
    plt.xticks(rotation=0)
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/png') 

@app.route('/question2.2', methods=['GET'])
def question2_2():
    foot_length_by_region = df.groupby(['Region', 'Longer_foot']).size().unstack(fill_value=0) # Group by region and count the unique foot length values within each group.
    plt.figure(figsize=(10, 6))
    ax = foot_length_by_region.plot(kind='bar', stacked=True) # Plot the distribution of foot length by region.

    plt.title('Number of students by type of foot length and region:')
    plt.xlabel('Region')
    plt.ylabel('Number of students')
    plt.xticks(rotation=0, ha='right')
    plt.legend(title='Foot Length')
    plt.tight_layout()

    for p in ax.patches:
            width = p.get_width()
            height = p.get_height()
            x, y = p.get_xy()
            ax.annotate(f'{height}', (x + width / 2, y + height / 2), ha='center', va='center')
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return send_file(img_buffer, mimetype='image/png') 

# ----------------------------------------------------------------
@app.route('/question3', methods=['GET'])
def question3():
    # Find the most common birth month for each region
    most_common_birth_month_by_region = df.groupby('Region')['Birth_month'].apply(lambda x: x.value_counts().idxmax()).reset_index(name='Most_common_month')
    # Filter the original DataFrame to include only students born in the most common month for each region
    filtered_df = df.merge(most_common_birth_month_by_region, on='Region')
    filtered_df = filtered_df[filtered_df['Birth_month'] == filtered_df['Most_common_month']]
    # Count the number of students born in the most common month for each region
    students_by_common_month_and_region = filtered_df.groupby(['Region', 'Most_common_month']).size().reset_index(name='Total')
    # Plotting
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=students_by_common_month_and_region, x='Region', y='Total', hue='Most_common_month')
    plt.title('Number of students born in the most common month by region')
    plt.xlabel('Region')
    plt.ylabel('Number of students')
    plt.xticks(rotation=0, ha='right')
    plt.legend(title='Most common month', bbox_to_anchor=(1, 1))
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png') 

# ----------------------------------------------------------------
@app.route('/question4', methods=['GET'])
def question4():
    # Find the most common favorite station for each region
    most_common_station_by_region = df.groupby('Region')['Favorite_Season'].apply(lambda x: x.value_counts().idxmax()).reset_index(name='Most_Favorite_Season')
    # Merge the most_common_station_by_region DataFrame with the original DataFrame on the 'Region' column
    filtered_df = df.merge(most_common_station_by_region, on='Region')
    filtered_df = filtered_df[filtered_df['Favorite_Season'] == filtered_df['Most_Favorite_Season']]
    # Count the total number of students with the most common favorite station for each region
    students_by_common_month_and_region = filtered_df.groupby(['Region', 'Most_Favorite_Season']).size().reset_index(name='Total')
    # Plotting
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=students_by_common_month_and_region, x='Region', y='Total', hue='Most_Favorite_Season', palette='Set1')
    plt.title('Number of students born in the most common month by region')
    plt.xlabel('Region')
    plt.ylabel('Number of students')
    plt.xticks(rotation=0, ha='right')
    plt.legend(title='Most common month', bbox_to_anchor=(1, 1))
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png') 

# ----------------------------------------------------------------
@app.route('/question5', methods=['GET'])
def question5():
    # Find the most common favorite station for each region
    most_common_drink_by_region = df.groupby('Region')['Beverage'].apply(lambda x: x.value_counts().idxmax()).reset_index(name='Most_common_beverage')
    # Merge the most_common_station_by_region DataFrame with the original DataFrame on the 'Region' column
    filtered_df = df.merge(most_common_drink_by_region, on='Region')
    filtered_df = filtered_df[filtered_df['Most_common_beverage'] == filtered_df['Most_common_beverage']]
    # Count the total number of students with the most common favorite station for each region
    students_by_most_common_drink_by_region = filtered_df.groupby(['Region', 'Most_common_beverage']).size().reset_index(name='Total')
    # Plotting
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=students_by_most_common_drink_by_region, x='Region', y='Total', hue='Most_common_beverage')
    plt.title('Number of students born in the most common month by region')
    plt.xlabel('Region')
    plt.ylabel('Number of students')
    plt.xticks(rotation=0, ha='right')
    plt.legend(title='Most common month', bbox_to_anchor=(1, 1))
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png') 

# ----------------------------------------------------------------
@app.route('/question6', methods=['GET'])
def question6():
    plt.figure(figsize=(10, 6))
    counts, edges, _ = plt.hist(df['Paid_Work_Hours'], bins=50, color='green', edgecolor='black')
    for count, edge in zip(counts, edges):
        plt.text(edge + (edges[1] - edges[0]) / 2, count, str(int(count)), ha='center', va='bottom', fontsize=9)
    plt.title('Distribution of Paid Work Hours')
    plt.xlabel('Paid Work Hours')
    plt.ylabel('Frequency')
    plt.grid(True)
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png') 

# ----------------------------------------------------------------
@app.route('/question6.A-F', methods=['GET'])
def question6_n():
    # 1. Percentage of students working maximum 13 hours per week with pay
    percentage_less_than_13 = len(df[df['Paid_Work_Hours'] <= 13]) / len(df) * 100
    # 2. Percentage of students working minimum 3 hours per week with pay
    percentage_greater_than_3 = len(df[df['Paid_Work_Hours'] >= 3]) / len(df) * 100
    # 3. Minimum value of paid work hours corresponding to the 20th percentile
    percentile_20 = np.percentile(df['Paid_Work_Hours'], 20)
    # 4. Maximum value of paid work hours corresponding to the 80th percentile
    percentile_80 = np.percentile(df['Paid_Work_Hours'], 80)
    # 5. Interval where the mode lies (range of the bin with the highest frequency)
    # Using the previously constructed histogram to find the bin with the highest frequency
    hist, bins = np.histogram(df['Paid_Work_Hours'], bins=20)
    mode_bin_index = np.argmax(hist)
    mode_interval = (bins[mode_bin_index], bins[mode_bin_index + 1])
    # 6. Maximum value of paid work hours corresponding to the 50th percentile (median)
    median = np.percentile(df['Paid_Work_Hours'], 50)
    # 7. Mean and standard deviation of paid work hours
    mean_paid_work_hours = df['Paid_Work_Hours'].mean()
    std_dev_paid_work_hours = df['Paid_Work_Hours'].std()
    # 8. Type of skewness (positive, negative, or symmetric)
    skewness = df['Paid_Work_Hours'].skew()
    if skewness > 0:
        skew_type = 'Positive (left-skewed)'
    elif skewness < 0:
        skew_type = 'Negative (right-skewed)'
    else:
        skew_type = 'Symmetric'
    # Store results in a dictionary
    results = {
        "1": {"question": "Percentage of students working maximum 13 hours per week with pay", "percentage_less_than_13": percentage_less_than_13},
        "2": {"question": "Percentage of students working minimum 3 hours per week with pay", "percentage_greater_than_3": percentage_greater_than_3},
        "3": {"question": "Minimum value of paid work hours corresponding to the 20th percentile", "percentile_20": percentile_20},
        "4": {"question": "Maximum value of paid work hours corresponding to the 80th percentile", "percentile_80": percentile_80},
        "5": {"question": "Interval where the mode lies (range of the bin with the highest frequency)", "mode_interval": mode_interval},
        "6": {"question": "Maximum value of paid work hours corresponding to the 50th percentile (median)", "median": median},
        "7": {"question": "Mean and standard deviation of paid work hours", "mean_paid_work_hours": mean_paid_work_hours, "std_dev_paid_work_hours": std_dev_paid_work_hours},
        "8": {"question": "Type of skewness (positive, negative, or symmetric)", "skew_type": skew_type}
    }
    # Convert dictionary to JSON format
    return jsonify(results)

# ----------------------------------------------------------------
@app.route('/question7', methods=['GET'])
def question7():
    # Plot the Ogive
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah)
    frcumul = df_wah_sorted.reset_index().index + 1
    fig, ax = plt.subplots(figsize=(10,7))
    ax.set_facecolor('lightgrey')
    ax.plot(df_wah_sorted[wah].apply(lambda x: None if x > 90 else x), frcumul, marker=".", linestyle="-", color="#B60000", markersize=5, linewidth=1)
    ax.set_title('Ogive of Time spent by students to help with household chores')
    ax.set_xlabel("Work at home hours per week")
    ax.set_ylabel("Students")
    ax.grid(True, linestyle="-", color="#E3E3E3", linewidth=2.4)
    ax.autoscale()
    ax.set_xlim(-0.5, 90.5)  # Adjusted x-axis limit
    ax.set_ylim(0)
    ax.xaxis.set_minor_locator(MultipleLocator(5))

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question7.A', methods=['GET'])
def question7_A():
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah) #we create the narray of the Work_At_Home_Hours column and sort it in ascending order
    frcumul = df_wah_sorted.reset_index().index + 1 #create the narray of the Work_At_Home_Hours cummulative frequencep15 = df.Work_At_Home_Hours[df_wah_sorted[wah] >= 15].count()  # Número de estudiantes con horas de trabajo desde casa mayores o iguales a 15
    p100 = df_wah_sorted.Work_At_Home_Hours.count()  # Total number of students
    p15 = df.Work_At_Home_Hours[df_wah_sorted[wah] >= 15].count()  # Number of students with work-from-home hours greater than or equal to 15

    p = p15 / p100
    fig, ax = plt.subplots(figsize=(10,7))
    ax.set_facecolor('lightgrey')
    ax.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul, marker=".", linestyle="-", color="#B60000", markersize=5, linewidth=1)
    ax.set_xlabel("Work at home hours per week")
    ax.set_ylabel("Students")
    ax.grid(True, linestyle="-", color="#E3E3E3", linewidth=2.4)
    ax.autoscale()
    ax.set_xlim(-0.5,80.4)
    ax.set_ylim(0)
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.axvline(x=15, label="15_hours per week")
    ax.axhline(y=p100-p15)
    ax.scatter(x=15,y=p100-p15, label=f"percentil = {100 - p*100:.0f}")
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul / frcumul.max(), linestyle="", color="blue")
    ax2.set_ylabel("Relative Cumulative Frequency students")
    fig.set_facecolor('#FFCA68')
    fig.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question7.B', methods=['GET'])
def question7_B():
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah) #we create the narray of the Work_At_Home_Hours column and sort it in ascending order
    frcumul = df_wah_sorted.reset_index().index + 1 #create the narray of the Work_At_Home_Hours cummulative frequencep15 = df.Work_At_Home_Hours[df_wah_sorted[wah] >= 15].count()  # Número de estudiantes con horas de trabajo desde casa mayores o iguales a 15

    students_max_5_hours = df_wah_sorted[df_wah_sorted[wah] <= 5]
    percentage_max_5_hours = (len(students_max_5_hours) / len(df_wah_sorted)) * 100
    position_line = frcumul.max() * (percentage_max_5_hours / 100)
    fig, ax = plt.subplots(figsize=(10,7))
    ax.set_facecolor('lightgrey')
    ax.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul, marker=".", linestyle="-", color="#B60000", markersize=5, linewidth=1)
    ax.set_xlabel("Work at home hours per week")
    ax.set_ylabel("Students")
    ax.grid(True, linestyle="-", color="#E3E3E3", linewidth=2.4)
    ax.autoscale()
    ax.set_xlim(-0.5,80.4)
    ax.set_ylim(0)
    ax.axhline(y=position_line, color='green', linestyle='--', label='Max 5 hours')
    ax.text(0.7, 0.7, f"{percentage_max_5_hours:.2f}% of students dedicate 5 hours maximum,", transform=ax.transAxes, ha='right', va='top', fontsize=12, color='black')
    ax.xaxis.set_minor_locator(MultipleLocator(5))

    ax2 = ax.twinx()
    ax2.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul / frcumul.max(), linestyle="", color="blue")
    ax2.set_ylabel("Relative Cumulative Frequency students")
    fig.set_facecolor('#FFCA68')
    fig.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question7.C', methods=['GET'])
def question7_C():
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah) #we create the narray of the Work_At_Home_Hours column and sort it in ascending order
    frcumul = df_wah_sorted.reset_index().index + 1 #create the narray of the Work_At_Home_Hours cummulative frequencep15 = df.Work_At_Home_Hours[df_wah_sorted[wah] >= 15].count()  # Número de estudiantes con horas de trabajo desde casa mayores o iguales a 15

    df_wah_sorted_na = df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x)
    df_wah_sorted_na = df_wah_sorted_na.dropna()
    percentile_15 = np.percentile(df_wah_sorted_na, 15)
    percentile_15_students = np.percentile(frcumul, 15)
    fig, ax = plt.subplots(figsize=(10,7))
    ax.set_facecolor('lightgrey')
    ax.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul, marker=".", linestyle="-", color="#B60000", markersize=5, linewidth=1, label="")
    ax.set_xlabel("Work at home hours per week")
    ax.set_ylabel("Students")
    ax.grid(True, linestyle="-", color="#E3E3E3", linewidth=2.4)
    ax.autoscale()
    ax.set_xlim(-0.5,80.4)
    ax.set_ylim(0)
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.axvline(x=percentile_15, color='green', linestyle='--', label='15th Percentile')
    ax.axhline(y=percentile_15_students, color='green', linestyle='--')
    ax.scatter(x=percentile_15, y=percentile_15_students, color='green', s=50,marker="o",alpha=True, label=f"Hours_worked = {percentile_15}")
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul / frcumul.max(), linestyle="", color="blue")
    ax2.set_ylabel("Relative Cumulative Frequency students")
    ax2.yaxis.set_minor_locator(MultipleLocator(0.1))
    fig.set_facecolor('#FFCA68')
    fig.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question7.D', methods=['GET'])
def question7_D():
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah) #we create the narray of the Work_At_Home_Hours column and sort it in ascending order
    frcumul = df_wah_sorted.reset_index().index + 1 #create the narray of the Work_At_Home_Hours cummulative frequencep15 = df.Work_At_Home_Hours[df_wah_sorted[wah] >= 15].count()  # Número de estudiantes con horas de trabajo desde casa mayores o iguales a 15

    students_max_5_hours = df_wah_sorted[df_wah_sorted[wah] >= 5]
    percentage_max_5_hours = (len(students_max_5_hours) / len(df_wah_sorted)) * 100
    position_line = frcumul.max() * (percentage_max_5_hours / 100)
    fig, ax = plt.subplots(figsize=(10,7))
    ax.set_facecolor('lightgrey')
    ax.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul, marker=".", linestyle="-", color="#B60000", markersize=5, linewidth=1)
    ax.set_xlabel("Work at home hours per week")
    ax.set_ylabel("Students")
    ax.grid(True, linestyle="-", color="#E3E3E3", linewidth=2.4)
    ax.autoscale()
    ax.set_xlim(-0.5,80.4)
    ax.set_ylim(0)
    ax.axhline(y=position_line, color='green', linestyle='--', label='min 5 hours')
    ax.text(0.7, 0.7, f"{percentage_max_5_hours:.2f}% of students dedicate at least 5 hours", transform=ax.transAxes, ha='right', va='top', fontsize=12, color='black')
    ax.xaxis.set_minor_locator(MultipleLocator(5))

    ax2 = ax.twinx()
    ax2.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul / frcumul.max(), linestyle="", color="blue")
    ax2.set_ylabel("Relative Cumulative Frequency students")
    fig.set_facecolor('#FFCA68')
    fig.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question7.E', methods=['GET'])
def question7_E():
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah) #we create the narray of the Work_At_Home_Hours column and sort it in ascending order
    frcumul = df_wah_sorted.reset_index().index + 1 #create the narray of the Work_At_Home_Hours cummulative frequencep15 = df.Work_At_Home_Hours[df_wah_sorted[wah] >= 15].count()  # Número de estudiantes con horas de trabajo desde casa mayores o iguales a 15
    
    fig, ax = plt.subplots(figsize=(10,7))
    ax.set_facecolor('lightgrey')
    ax.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul, marker=".", linestyle="-", color="#B60000", markersize=5, linewidth=1)
    ax.set_xlabel("Work at home hours per week")
    ax.set_ylabel("Students")
    ax.grid(True, linestyle="-", color="#E3E3E3", linewidth=2.4)
    ax.autoscale()
    ax.set_xlim(-0.5,80.4)
    ax.set_ylim(0)
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    closest_index = np.abs(frcumul / frcumul.max() - 0.35).argmin()
    min_hours = df_wah_sorted[wah].iloc[closest_index]
    ax.text(0.7, 0.7, f"35% of estudents works at home min: {min_hours} hours" , transform=ax.transAxes, ha='right', va='top', fontsize=12, color='black')

    ax2 = ax.twinx()
    ax2.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul / frcumul.max(), linestyle="", color="blue")
    ax2.set_ylabel("Relative Cumulative Frequency students")
    fig.set_facecolor('#FFCA68')
    percentile = 35
    ax2.axhline(percentile / 100, color='red', linestyle='--', label=f'{percentile}th Percentile')
    ax2.legend()
    fig.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question7.F', methods=['GET'])
def question7_F():
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah) #we create the narray of the Work_At_Home_Hours column and sort it in ascending order
    frcumul = df_wah_sorted.reset_index().index + 1 #create the narray of the Work_At_Home_Hours cummulative frequencep15 = df.Work_At_Home_Hours[df_wah_sorted[wah] >= 15].count()  # Número de estudiantes con horas de trabajo desde casa mayores o iguales a 15
    df_wah_sorted_na = df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x)
    df_wah_sorted_na = df_wah_sorted_na.dropna()
    
    fig, ax = plt.subplots(figsize=(10,7))
    ax.set_facecolor('lightgrey')
    ax.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul, marker=".", linestyle="-", color="#B60000", markersize=5, linewidth=1)
    ax.set_xlabel("Work at home hours per week")
    ax.set_ylabel("Students")
    ax.grid(True, linestyle="-", color="#E3E3E3", linewidth=2.4)
    ax.autoscale()
    ax.set_xlim(-0.5,80.4)
    ax.set_ylim(0)
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    percentile_50 = np.percentile(df_wah_sorted_na, 50)
    ax.scatter(x="", y=100, color='black', s=100, marker="<", alpha=True, label="Mode")
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x), frcumul / frcumul.max(), linestyle="", color="blue")
    ax2.set_ylabel("Relative Cumulative Frequency students")
    fig.set_facecolor('#FFCA68')
    fig.tight_layout()
    percentile = 50
    ax.text(0.7, 0.7, f"the Mode is 2.0 hours per week", transform=ax.transAxes, ha='right', va='top', fontsize=12, color='black')
    ax2.axhline(9.5 / 100, color='red', linestyle='--', label=f'Mode')
    ax2.legend()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')
    
@app.route('/question7.G', methods=['GET'])
def question7_G():
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah) #we create the narray of the Work_At_Home_Hours column and sort it in ascending order
    df_wah_sorted_na = df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x)
    df_wah_sorted_na = df_wah_sorted_na.dropna()
    std_deviation = df_wah_sorted_na.std()
    mean_hours = df_wah_sorted_na.mean()
    # Construct the JSON response
    results_json = {
        "1": {
            "Statistic": "Standard Deviation",
            "Value": f"{std_deviation:.1f}"
        },
        "2": {
            "Statistic": "Average Hours",
            "Value": f"{mean_hours:.1f}"
        }
    }
    # Return the JSON response
    return results_json

@app.route('/question7.H', methods=['GET'])
def question7_H():
    # Calculate skewness
    skewness = df['Work_At_Home_Hours'].skew()
    # Determine skewness type
    if skewness > 0:
        skew_type = 'Positive (left-skewed)'
    elif skewness < 0:
        skew_type = 'Negative (right-skewed)'
    else:
        skew_type = 'Symmetric'
    # Construct the JSON response
    results_json = {
        "A": {
            "Skewness type": skew_type,
            "Skewness value": f"{skewness:.2f}"
        }
    }
    # Return the JSON response
    return results_json
    
# ----------------------------------------------------------------
@app.route('/question8-men', methods=['GET'])
def question8_men():
    df_filtered = df[(df['Importance_reducing_pollution'] >= 0) & (df['Importance_reducing_pollution'] <= 1000)]
    df_male = df_filtered[df_filtered["Gender"] == 'Male']
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Gender', y='Importance_reducing_pollution', data=df_male, hue='Region')
    plt.title('Opinion on the importance of reducing pollution by gender and state (Men)')
    plt.xlabel('Gender')
    plt.ylabel('Importance of reducing pollution')
    plt.xticks(rotation=0)
    plt.legend(title='Region', loc='upper right', fontsize='small')
    plt.ylim(-10, 1100)
    plt.yticks(range(0, 1001, 100))
    
    for i in range(100, 1100, 100):
        plt.axhline(y=i, color='gray', linestyle='--', linewidth=0.5)
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question8-women', methods=['GET'])
def question8_women():
    df_filtered = df[(df['Importance_reducing_pollution'] >= 0) & (df['Importance_reducing_pollution'] <= 1000)]
    df_female = df_filtered[df_filtered["Gender"] == 'Female']
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Gender', y='Importance_reducing_pollution', data=df_female, hue='Region')
    plt.title('Opinion on the importance of reducing pollution by gender and state (Women)')
    plt.xlabel('Gender')
    plt.ylabel('Importance of reducing pollution')
    plt.xticks(rotation=0)
    plt.legend(title='Region', loc='upper right', fontsize='small')
    plt.ylim(-10, 1100)
    plt.yticks(range(0, 1001, 100))
    for i in range(100, 1100, 100):
        plt.axhline(y=i, color='gray', linestyle='--', linewidth=0.5)
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question8.A-G', methods=['GET'])
def question8_n():
    # Filter the DataFrame
    df_filtered = df[(df['Importance_reducing_pollution'] >= 0) & (df['Importance_reducing_pollution'] <= 1000)]
    # df_genders
    df_female = df_filtered[df_filtered["Gender"] == 'Female']
    df_male = df_filtered[df_filtered["Gender"] == 'Male']
    # Calculate the average of the responses by gender
    mean_by_gender = df_filtered.groupby('Gender')['Importance_reducing_pollution'].mean().round(2)
    max_mean_gender = mean_by_gender.idxmax()
    max_mean_value_gender = mean_by_gender.max()
    # Calculate the average of the responses by region
    mean_by_region = df_filtered.groupby('Region')['Importance_reducing_pollution'].mean().round(2)
    max_mean_region = mean_by_region.idxmax()
    max_mean_value_region = mean_by_region.max()
    # Calculate the average of the responses by region and gender
    mean_by_region_gender_female = df_female.groupby('Region')['Importance_reducing_pollution'].mean().round(2)
    max_mean_region_female = mean_by_region_gender_female.idxmax()
    max_mean_value_female = mean_by_region_gender_female.max()
    mean_by_region_gender_male = df_male.groupby('Region')['Importance_reducing_pollution'].mean().round(2)
    max_mean_region_male = mean_by_region_gender_male.idxmax()
    max_mean_value_male = mean_by_region_gender_male.max()
    # Calculate the standard deviation of the responses by gender
    std_by_gender = df_filtered.groupby('Gender')['Importance_reducing_pollution'].std().round(2)
    min_std_gender = std_by_gender.idxmin()
    min_std_value_gender = std_by_gender.min()
    # Calculate the standard deviation of the responses by region
    std_by_region = df_filtered.groupby('Region')['Importance_reducing_pollution'].std().round(2)
    min_std_region = std_by_region.idxmin()
    min_std_value_region = std_by_region.min()
    # Calculate the skewness of the responses by gender
    skew_by_gender = df_filtered.groupby('Gender')['Importance_reducing_pollution'].skew().round(2)
    max_skew_gender = skew_by_gender.idxmax()
    max_skew_value_gender = skew_by_gender.max()
    # Calculate the skewness of the responses by region
    skew_by_region = df_filtered.groupby('Region')['Importance_reducing_pollution'].skew().round(2)
    max_skew_region = skew_by_region.idxmax()
    max_skew_value_region = skew_by_region.max()
    # Calculate the skewness of the responses by region and gender
    skew_by_region_gender_female = df_female.groupby('Region')['Importance_reducing_pollution'].skew().round(2)
    min_skew_region_female = skew_by_region_gender_female.idxmin()
    min_skew_value_female = skew_by_region_gender_female.min()
    skew_by_region_gender_male = df_male.groupby('Region')['Importance_reducing_pollution'].skew().round(2)
    min_skew_region_male = skew_by_region_gender_male.idxmin()
    min_skew_value_male = skew_by_region_gender_male.min()
    # Construct the JSON response
    results_json = {
        "A": {
            "Gender": max_mean_gender,
            "Average": max_mean_value_gender
        },
        "B": {
            "Region": max_mean_region,
            "Average": max_mean_value_region
        },
        "C": {
            "Gender": max_mean_region_female,
            "Average": max_mean_value_female
        },
        "D": {
            "Gender": max_mean_region_male,
            "Average": max_mean_value_male
        },
        "E": {
            "Gender": min_std_gender,
            "Standard Deviation": min_std_value_gender
        },
        "F": {
            "Region": min_std_region,
            "Standard Deviation": min_std_value_region
        },
        "G": {
            "Gender": max_skew_gender,
            "Skewness": max_skew_value_gender
        },
        "H": {
            "Region": max_skew_region,
            "Skewness": max_skew_value_region
        },
        "I": {
            "Gender": min_skew_region_female,
            "Skewness": min_skew_value_female
        },
        "J": {
            "Gender": min_skew_region_male,
            "Skewness": min_skew_value_male
        }
    }
    # return the JSON response
    return(results_json)
# ----------------------------------------------------------------
@app.route('/question9', methods=['GET'])
def question9_1():
    # Build histograms by gender and sleep hours
    df_9 = df[["Gender", "Sleep_Hours_Non_Schoolnight"]][(df['Sleep_Hours_Non_Schoolnight'] >= 1) & (df['Sleep_Hours_Non_Schoolnight'] <= 15)]
    # Create a bar chart
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x='Sleep_Hours_Non_Schoolnight', hue='Gender', data=df_9)
    # Adjust labels and legends
    plt.title('Distribution of sleep hours by gender')
    plt.xlabel('Sleeping hours per night')
    plt.ylabel('Number of people')
    plt.legend(title='Gender')
    plt.ylim(0, 100) # Adjust the y-axis limits according to your need
    plt.yticks(range(0, 110, 10))  
    # Add horizontal lines in intervals of 100 on the y-axis
    for i in range(10, 110, 10):
        plt.axhline(y=i, color='gray', linestyle='--', linewidth=0.5)
    # Add rounded values on top of each bar
    for p in ax.patches:
        ax.annotate(f'{int(round(p.get_height()))}', (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=8)
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png') 

@app.route('/question9.A-E', methods=['GET'])
def question9_n():
    df_9 = df[["Gender", "Sleep_Hours_Non_Schoolnight"]][(df['Sleep_Hours_Non_Schoolnight'] >= 1) & (df['Sleep_Hours_Non_Schoolnight'] <= 15)]
    # Filter the rows where the gender is female
    percentage_women = (df_9["Gender"] == "Female").mean() * 100
    # hours of sleep
    mean_students = df_9["Sleep_Hours_Non_Schoolnight"].mean()
    # Calculate the mean of the answers by gender
    mean_by_sleep_gender = df_9.groupby('Gender')['Sleep_Hours_Non_Schoolnight'].mean().round(2)
    # Get the gender with the highest mean
    max_mean_gender = mean_by_sleep_gender.idxmax()
    max_mean_value = mean_by_sleep_gender.max()
    # Calculate the standard deviation of responses by gender
    std_by_sleep_gender = df_9.groupby('Gender')['Sleep_Hours_Non_Schoolnight'].std().round(2)
    # Get the gender with the lowest std
    min_std_gender = std_by_sleep_gender.idxmin()
    min_std_value = std_by_sleep_gender.min()
    # Calculate the skewness of responses by gender
    skew_by_sleep_gender = df_9.groupby('Gender')['Sleep_Hours_Non_Schoolnight'].skew().round(2)
    # Get the gender with the least skewness
    min_skew_gender = skew_by_sleep_gender.idxmin()
    min_skew_value = skew_by_sleep_gender.min()
    # Construct the JSON response
    results_json = {
        "Percentage_Women": round(percentage_women, 2),
        "Average_Sleep_Hours": round(mean_students, 2),
        "Max_Mean_Gender": max_mean_gender,
        "Max_Mean_Value": max_mean_value,
        "Min_Std_Gender": min_std_gender,
        "Min_Std_Value": min_std_value,
        "Min_Skew_Gender": min_skew_gender,
        "Min_Skew_Value": min_skew_value
    }
    # Print the JSON response
    return jsonify(results_json)

@app.route('/question9.F', methods=['GET'])
def question9_f():
    df_9 = df[["Gender", "Sleep_Hours_Non_Schoolnight"]][(df['Sleep_Hours_Non_Schoolnight'] >= 1) & (df['Sleep_Hours_Non_Schoolnight'] <= 15)]
    # Filter the data by gender
    df9_female = df_9[df_9["Gender"] == "Female"]
    df9_male = df_9[df_9["Gender"] == "Male"]
    # Set the size of the graphic
    plt.figure(figsize=(10, 6))
    # Plot histogram for males
    sns.histplot(data=df9_male, x='Sleep_Hours_Non_Schoolnight', color='blue', kde=True, label='Male')
    # Plot histogram for females
    sns.histplot(data=df9_female, x='Sleep_Hours_Non_Schoolnight', color='orange', kde=True, label='Female')
    # Add title and labels
    plt.title('Histogram of Sleep Times by Gender')
    plt.xlabel('Sleeping hours per night')
    plt.ylabel('Frequency')
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')
    
@app.route('/question9.F.1', methods=['GET'])
def question9_f_1():
    df_9 = df[["Gender", "Sleep_Hours_Non_Schoolnight"]][(df['Sleep_Hours_Non_Schoolnight'] >= 1) & (df['Sleep_Hours_Non_Schoolnight'] <= 15)]
    # Calculate the kurtosis for each gender
    kurtosis_by_gender = df_9.groupby('Gender')['Sleep_Hours_Non_Schoolnight'].apply(lambda x: x.kurtosis()).round(2)
    # Get the gender with the highest and lowest kurtosis
    max_kurtosis_gender = kurtosis_by_gender.idxmax()
    min_kurtosis_gender = kurtosis_by_gender.idxmin()
    # Construct the JSON response
    kurtosis_json = {
        "Max_Kurtosis_Gender": max_kurtosis_gender,
        "Max_Kurtosis_Value": kurtosis_by_gender[max_kurtosis_gender],
        "Min_Kurtosis_Gender": min_kurtosis_gender,
        "Min_Kurtosis_Value": kurtosis_by_gender[min_kurtosis_gender]
    }
    # Print the JSON response
    return jsonify(kurtosis_json)

# ----------------------------------------------------------------
@app.route('/question10', methods=['GET'])
def question10():
    wah = "Work_At_Home_Hours"
    df_wah_sorted = df.sort_values(by=wah)
    df_wah_sorted_na = df_wah_sorted[wah].apply(lambda x: None if x >= 90 else x)
    df_wah_sorted_na = df_wah_sorted_na.dropna()
    p15 = df_wah_sorted.Work_At_Home_Hours[df_wah_sorted[wah] >= 15].count()  
    p100 = df_wah_sorted.Work_At_Home_Hours.count()  
    p = p15 / p100
    
    crosstab_table = pd.crosstab(df['Gender'], df['Favorite_School_Subject'], margins=True, margins_name="Total")
    crosstab_table = crosstab_table.iloc[:-1, :-1]
    
    plt.figure(figsize=(12, 8))  # Ajustar el tamaño de la figura
    ax = sns.countplot(data=df, x='Favorite_School_Subject', hue='Gender')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    plt.title('Distribution of favorite school subject by gender')
    plt.xlabel('Favorite School Subject')
    plt.ylabel('Number of persons')
    plt.legend(title='Gender')
    
    plt.annotate(f'{int(round(p * 100))}%', (0, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', ha='center', fontsize=8)
    
    plt.tight_layout(pad=3.0)  # Ajustar el espacio entre subgráficos
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return send_file(img_buffer, mimetype='image/png')

@app.route('/question10.A-H', methods=['GET'])
def question10_H():
    # Calculate crosstab table
    crosstab_table = pd.crosstab(df['Gender'], df['Favorite_School_Subject'])
    
    # Calculate total number of students
    total_students = crosstab_table.sum().sum()
    
    # Calculate statistics
    students_history_men = crosstab_table.loc[df['Gender'].unique()[0], df['Favorite_School_Subject'].unique()[0]]
    percentage_men = crosstab_table.loc['Male'].sum() / total_students * 100
    percentage_music = crosstab_table[df['Favorite_School_Subject'].unique()[10]].sum() / total_students * 100
    percentage_women_other_activities = crosstab_table.loc['Female', df['Favorite_School_Subject'].unique()[6]] / crosstab_table.loc['Female'].sum() * 100
    percentage_men_sciences = crosstab_table.loc['Male', df['Favorite_School_Subject'].unique()[1]] / crosstab_table[df['Favorite_School_Subject'].unique()[1]].sum() * 100
    percentage_women_or_music = (crosstab_table.loc['Female'].sum() + crosstab_table[df['Favorite_School_Subject'].unique()[10]].sum() - crosstab_table.loc['Female', df['Favorite_School_Subject'].unique()[10]]) / total_students * 100
    percentage_women_music_sciences = (crosstab_table.loc['Female', df['Favorite_School_Subject'].unique()[6]] + crosstab_table.loc['Female', df['Favorite_School_Subject'].unique()[1]]) / crosstab_table.loc['Female'].sum() * 100
    
    # Construct JSON response
    results_json = {
        "A": "Male {} students like history.".format(students_history_men),
        "B": "{:.2f}% of the students are male.".format(percentage_men),
        "C": "{:.2f}% of students prefer music.".format(percentage_music),
        "D": "The {:.2f}% of women prefer other activities.".format(percentage_women_other_activities),
        "E": "The {:.2f}% of students who prefer Science are male.".format(percentage_men_sciences),
        "F": "The {:.2f}% are women and prefer other activities.".format(percentage_women_other_activities),
        "G": "The {:.2f}% are female or prefer music.".format(percentage_women_or_music),
        "H": "{:.2f}% of women like music or the Sciences.".format(percentage_women_music_sciences)
    }

    # Return JSON response
    return results_json

# ----------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
