import requests
from nana_real import classify_nutrition_data  # Assumed to classify the nutritional data for food
from person_score import analyze_health_classification  # Assumed to analyze the person's health data

# Hugging Face API key and endpoint
API_KEY = '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'
LLM_API_ENDPOINT = "https://api-inference.huggingface.co/models/roberta-large-mnli"

# Function to classify the overall food recommendation based on person and food classifications
def classify_food_for_person(person_score, food_label):
    # Create a detailed prompt to pass to the LLM API for final classification
    prompt = f"""
    A person has the following health profile:
    - BMI Classification: {person_score['bmi_classification']}
    - BMR Classification: {person_score['bmr_classification']}
    - Overall Health Classification: {person_score['classification']}

    The food being analyzed has been classified as: {food_label}.

    Based on this information, categorize the food for this person as one of the following:
    1. Great
    2. Good
    3. Okay
    4. No
    5. Hell no
    """
    
    # Send the prompt to the Hugging Face model for final classification
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "inputs": prompt,
        "options": {
            "use_cache": False
        }
    }

    response = requests.post(LLM_API_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        # Find the label with the maximum score
        max_score_label = max(result[0], key=lambda x: x['score'])['label']
        return max_score_label
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Main function to combine person and food scores
def classify_person_and_food(weight, height, age, gender, nutrition_data):
    # Analyze the health profile of the person
    person_classification, bmi_classification, bmr_classification = analyze_health_classification(weight, height, age, gender)
    
    person_score = {
        "classification": person_classification,
        "bmi_classification": bmi_classification,
        "bmr_classification": bmr_classification
    }
    
    # Classify the nutritional data of the food
    food_label = classify_nutrition_data(nutrition_data)

    if food_label:
        # Get the final classification based on person and food profiles
        final_classification = classify_food_for_person(person_score, food_label)
        
        if final_classification:
            return final_classification
        else:
            return "Error in final classification."
    else:
        return "Error in food classification."

# Example usage
if __name__ == "__main__":
    # Example person and nutrition data
    weight = 70  # kg
    height = 175  # cm
    age = 30  # years
    gender = 'male'
    
    # Example nutrition data
    nutrition_data = {
        "calories": 400,
        "protein": 30.0,
        "carbs": 50.0,
        "sugars": 5.0,
        "fat": 15.0,
        "saturated_fat": 5.0,
        "trans_fat": 0.0,
        "sodium": 500
    }

    # Get the final classification for the food
    result = classify_person_and_food(weight, height, age, gender, nutrition_data)

    # Output the result
    if result:
        print(f"Final Food Classification: {result}")
