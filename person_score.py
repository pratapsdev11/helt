def analyze_health_classification(weight, height, age, gender):
    # Calculate BMI
    height_in_m = height / 100  # Convert height from cm to meters
    bmi = weight / (height_in_m ** 2)

    # Calculate BMR using the Mifflin-St Jeor Equation
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Classify based on BMI
    if bmi < 18.5:
        bmi_classification = "Underweight"
    elif 18.5 <= bmi < 24.9:
        bmi_classification = "Normal weight"
    elif 25 <= bmi < 29.9:
        bmi_classification = "Overweight"
    else:
        bmi_classification = "Obesity"

    # BMR interpretation based on general activity levels and age (ranges for moderate activity)
    if gender == 'male':
        normal_bmr_range = (1500, 2500)
    else:
        normal_bmr_range = (1200, 2200)

    if bmr < normal_bmr_range[0]:
        bmr_classification = "Low BMR (low energy expenditure)"
    elif normal_bmr_range[0] <= bmr <= normal_bmr_range[1]:
        bmr_classification = "Normal BMR"
    else:
        bmr_classification = "High BMR (high energy expenditure)"

    # Final health classification logic
    if bmi_classification == "Normal weight" and bmr_classification == "Normal BMR":
        classification = "Good"
    elif bmi_classification == "Overweight" or bmr_classification in ["Low BMR", "High BMR"]:
        classification = "Normal"
    else:
        classification = "Poor"

    return classification, bmi_classification, bmr_classification

# Example user
# user = { 
#     'weight': 110,  # kg
#     'height': 177,  # cm
#     'age': 22,  # years
#     'gender': 'male'
# }

# # Analyze health classification
# health_classification, bmi_classification, bmr_classification = analyze_health_classification(user['weight'], user['height'], user['age'], user['gender'])

# print(f"Health Classification: {health_classification}")
# print(f"BMI Classification: {bmi_classification}")
# print(f"BMR Classification: {bmr_classification}")
