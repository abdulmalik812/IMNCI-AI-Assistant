import google.generativeai as genai
import json
import os

# Load your Gemini API key from environment variables
GEMINI_API_KEY = "AIzaSyAnPRyLwM35ymHmCktds1gqAV0k1DOxFTE"  # Replace with your API key
genai.configure(api_key=GEMINI_API_KEY)

# Load IMNCI rules from a JSON file
def load_imnci_rules():
    with open("utils/imnci_rules.json", "r") as f:
        return json.load(f)

# Function to classify symptoms using predefined IMNCI rules
def classify_with_rules(symptoms_text):
    imnci_rules = load_imnci_rules()
    
    symptoms = symptoms_text.lower().split(", ")  # Convert to list
    
    classification = "Mild"  # Default classification
    for symptom in symptoms:
        if symptom in imnci_rules["severe"]:
            classification = "Severe"
            break  # Stop if a severe condition is found
        elif symptom in imnci_rules["moderate"]:
            classification = "Moderate"

    return classification

# Function to classify symptoms using Google Gemini AI
def classify_with_gemini(symptoms_text):
    prompt = f"""
    You are an AI assistant for nurses following WHO's IMNCI guidelines.
    Analyze the following newborn symptoms:
    "{symptoms_text}"
    
    Classify based on IMNCI rules:
    - SEVERE (Red)
    - MODERATE (Yellow)
    - MILD (Green)

    Then provide a structured IMNCI treatment plan, including:
    - Classification
    - Treatment Steps
    - If urgent referral is needed
    - Medication and dosage
    - Follow-up recommendations

    Format the output as a structured medical chart.
    """

    # Generate response using Gemini
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text  # Extracts text output

# Main function to classify symptoms
def classify_symptoms(symptoms_text):
    basic_classification = classify_with_rules(symptoms_text)

    if basic_classification == "Severe":
        return f"⚠️ **Severe Case!** Immediate referral needed.\n\n{classify_with_gemini(symptoms_text)}"
    else:
        return f"🟡 **{basic_classification} Case**\n\n{classify_with_gemini(symptoms_text)}"
