import os
import re  # Importing the re module for regular expressions
import easyocr  # Import EasyOCR

def extract_nutrition_info(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found at: {image_path}")
    
    reader = easyocr.Reader(['en'])  # You can set the language here
    result = reader.readtext(image_path)

    # Combine the results into a single string
    extracted_text = "\n".join([text[1] for text in result])
    return extracted_text

def parse_nutrition_table(text):
    # Initialize dictionary for nutrition info
    nutrition_info = {
        "calories": 0,
        "fat": 0,
        "saturated_fat": 0,
        "trans_fat": 0,
        "carbs": 0,
        "sugars": 0,
        "protein": 0,
        "sodium": 0
    }

    calorie_match = re.search(r'energy\s*kcal\s*(\d+)', text, re.IGNORECASE)
    protein_match = re.search(r'protein\s*g\s*(\d+\.?\d*)', text, re.IGNORECASE)
    carbs_match = re.search(r'total\s*carbohydrate\s*g\s*(\d+\.?\d*)', text, re.IGNORECASE)
    sugars_match = re.search(r'sugars\s*g\s*(\d+\.?\d*)', text, re.IGNORECASE)
    fat_match = re.search(r'total\s*fat\s*g\s*(\d+\.?\d*)', text, re.IGNORECASE)
    saturated_fat_match = re.search(r'saturated\s*fat\s*g\s*(\d+\.?\d*)', text, re.IGNORECASE)
    trans_fat_match = re.search(r'trans\s*fat\s*g\s*(\d+\.?\d*)', text, re.IGNORECASE)
    sodium_match = re.search(r'sodium\s*mg\s*(\d+)', text, re.IGNORECASE)    

    # Fill the nutrition info dictionary with the extracted values
    if calorie_match:
        nutrition_info["calories"] = int(calorie_match.group(1))
    if protein_match:
        nutrition_info["protein"] = float(protein_match.group(1))
    if carbs_match:
        nutrition_info["carbs"] = float(carbs_match.group(1))
    if sugars_match:
        nutrition_info["sugars"] = float(sugars_match.group(1))
    if fat_match:
        nutrition_info["fat"] = float(fat_match.group(1))
    if saturated_fat_match:
        nutrition_info["saturated_fat"] = float(saturated_fat_match.group(1))
    if trans_fat_match:
        nutrition_info["trans_fat"] = float(trans_fat_match.group(1))
    if sodium_match:
        nutrition_info["sodium"] = int(sodium_match.group(1))

    return nutrition_info
