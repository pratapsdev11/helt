import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from nutrition_extractor import extract_nutrition_info, parse_nutrition_table
from nana_real import classify_nutrition_data
from person_score import analyze_health_classification
from XYZ2 import classify_food_for_person, classify_person_and_food  # Importing the functions from XYZ2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        weight = request.form.get('weight')
        height = request.form.get('height')
        age = request.form.get('age')
        gender = request.form.get('gender')

        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            # Secure the filename and save it
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Step 1: Extract nutrition info from the image
            extracted_text = extract_nutrition_info(file_path)

            # Step 2: Classify food healthiness
            nutrition_data = parse_nutrition_table(extracted_text)
            food_classification = classify_nutrition_data(nutrition_data)

            # Step 3: Analyze the person's health classification
            health_classification, bmi_classification, bmr_classification = analyze_health_classification(
                weight=float(weight), 
                height=float(height), 
                age=int(age), 
                gender=gender
            )

            # Step 4: Classify the food for the person
            person_and_food = classify_person_and_food(float(weight), float(height), int(age), gender, nutrition_data)

            # Step 5: Combine health and food analysis results
            result = f"""
            Person's Health: {health_classification} (BMI: {bmi_classification}, BMR: {bmr_classification})
            Food Healthiness: {food_classification}
            Food Suitability: {person_and_food}
            """

            # Render the result on a new page
            return render_template('result.html', result=result)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
