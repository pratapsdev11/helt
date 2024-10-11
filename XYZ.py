import requests
from nana_real import classify_nutrition_data
from person_score import analyze_health_classification

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
    
    # Send the prompt to the LLM for final classification
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
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Main function to combine person and food scores
def classify_person_and_food(weight, height, age, gender, nutrition_data):
    # Get person classification
    person_classification, bmi_classification, bmr_classification = analyze_health_classification(weight, height, age, gender)
    
    person_score = {
        "classification": person_classification,
        "bmi_classification": bmi_classification,
        "bmr_classification": bmr_classification
    }
    
    # Get food classification
    food_label = classify_nutrition_data(nutrition_data)

    if food_label:
        # Classify the food for this person's profile
        final_classification = classify_food_for_person(person_score, food_label)
        
        # Return final result
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

    # Get the final classification
    result = classify_person_and_food(weight, height, age, gender, nutrition_data)

    # Output the result
    if result:
        print(f"Final Food Classification: {result}")
