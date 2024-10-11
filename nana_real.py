import requests

# Hugging Face API key
API_KEY = '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'

# Hugging Face model endpoint for classification
BART_ENDPOINT = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

# Function to classify using BART
def classify_nutrition(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    candidate_labels = ["super healthy", "healthy", "unhealthy", "toxic"]
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "candidate_labels": candidate_labels
        },
        "options": {
            "use_cache": False
        }
    }

    response = requests.post(BART_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to generate nutrition summary based on WHO guidelines
def generate_nutrition_summary(nutrition_data):
    summary_parts = []

    # Analyze nutritional values according to WHO Dietary Guidelines
    # Calories
    if nutrition_data['calories'] > 500:
        summary_parts.append("high calories")
    elif nutrition_data['calories'] < 250:
        summary_parts.append("low calories")
    else:
        summary_parts.append("moderate calories")

    # Protein
    if nutrition_data['protein'] < 10:
        summary_parts.append("very low protein")
    elif nutrition_data['protein'] < 20:
        summary_parts.append("low protein")
    elif nutrition_data['protein'] > 50:
        summary_parts.append("high protein")
    else:
        summary_parts.append("adequate protein")

    # Carbohydrates
    if nutrition_data['carbs'] > 130:
        summary_parts.append("high carbs")
    elif nutrition_data['carbs'] < 50:
        summary_parts.append("low carbs")
    else:
        summary_parts.append("moderate carbs")

    # Sugars
    if nutrition_data['sugars'] > 10:
        summary_parts.append("high sugars")
    elif nutrition_data['sugars'] < 5:
        summary_parts.append("low sugars")
    else:
        summary_parts.append("moderate sugars")

    # Total Fat
    if nutrition_data['fat'] > 35:
        summary_parts.append("high total fat")
    elif nutrition_data['fat'] < 15:
        summary_parts.append("low total fat")
    else:
        summary_parts.append("moderate total fat")

    # Saturated Fat
    if nutrition_data['saturated_fat'] > 10:
        summary_parts.append("high saturated fat")
    elif nutrition_data['saturated_fat'] < 5:
        summary_parts.append("low saturated fat")
    else:
        summary_parts.append("moderate saturated fat")

    # Trans Fat
    if nutrition_data['trans_fat'] > 0:
        summary_parts.append("contains trans fat")

    # Sodium
    if nutrition_data['sodium'] > 2000:
        summary_parts.append("high sodium")
    elif nutrition_data['sodium'] < 1200:
        summary_parts.append("low sodium")
    else:
        summary_parts.append("moderate sodium")

    # Combine summary parts into a statement
    summary = f"The food for a 100g serving has: {', '.join(summary_parts)}." if summary_parts else "The food has a balanced nutritional profile."
    
    return summary

# Main function to classify nutrition data
def classify_nutrition_data(nutrition_data):
    # Generate nutrition summary
    nutrition_summary = generate_nutrition_summary(nutrition_data)

    # Create a prompt for BART using the generated summary
    input_prompt = f"""
    Classify the nutritional content based on the following analysis:
    Nutrition Summary: {nutrition_summary}
    """

    # Classify using BART
    classification_result = classify_nutrition(input_prompt)

    # Return the label with the maximum score
    if classification_result:
        # Extracting the label with the maximum score
        if 'scores' in classification_result and 'labels' in classification_result:
            max_score_index = classification_result['scores'].index(max(classification_result['scores']))
            max_label = classification_result['labels'][max_score_index]
            
            return max_label
        else:
            print("Classification result format is unexpected.")
            return None
    else:
        print("Failed to classify the nutrition data.")
        return None

# Example usage as a module
if __name__ == "__main__":
    # Nutrition data to evaluate
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

    # Classify the nutrition data
    result = classify_nutrition_data(nutrition_data)

    # Output the result
    if result:
        print(f"Classification: {result}")
