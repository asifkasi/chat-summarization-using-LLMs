# %%
# !pip isntall openai

# {
#     "openai_api" : "https://platform.openai.com/api-keys"
#     "google gemini api" : "https://aistudio.google.com/app/apikey"
# }

# %%

import openai

table = """
Term	Category	Amount
Annatto Powder	Cheese (e.g., cheddar, processed cheese)	0.5-2%
Annatto Powder	Snack Foods (e.g., chips, crackers, popcorn)	0.1-1%
Annatto Powder	Beverages (e.g., soft drinks, fruit juices)	0.05-0.5%
Annatto Powder	Processed Meats (e.g., sausages, hot dogs, deli meats)	0.1-0.5%
Annatto Powder	Prepared Foods (e.g., sauces, soups, dressings)	0.1-0.5%
Annatto Powder	Bakery Products (e.g., cakes, pastries)	0.1-0.5%
Annatto Powder	Sweets and Confectionery (e.g., candy, ice cream, jellies)	0.1-0.5%
Cumin	Seasoning Mixes (e.g., taco seasoning, curry blends)	10-20%
Cumin	Soups and Sauces	0.1-0.5%
Cumin	Snack Foods (e.g., chips, nuts, crackers)	0.2-0.5%
Cumin	Meat Products (e.g., sausages, marinades)	0.1-0.3%
Cumin	Rice and Grain-Based Dishes	0.1-0.3%
Cumin	Bakery Products (e.g., savory breads, crackers)	0.05-0.2%
Cumin	Beverages (e.g., cumin-flavored buttermilk, spiced drinks)	0.01-0.1%
Cumin	Condiments (e.g., chutneys, dips, spreads)	0.2-0.5%

"""
OPENAI_API_KEY = "access key"
# os.getenv("OPENAI_API_KEY")

# client = openai(api_key=OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY  # Set API key for OpenAI

# Try OpenAI completion
def chatty(input_text,table):
    response = openai.ChatCompletion.create(
    model="gpt-4-0125-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Convert the following text into a table with columns 'Term', 'Category', and 'Amount':\n{input_text}\n\nTable: {table}"}
    ],
    temperature=0.0,
    max_tokens=1000,
    n=1
    )

    table_output = response.choices[0].message['content']
    return table_output


# %%
# Define the input text
input_text = """
Steviol glycosides are the sweet compounds extracted from the leaves of the stevia plant (Stevia rebaudiana). They are used as natural, zero-calorie sweeteners in a variety of commercial food products. Due to their high sweetness intensity (200–400 times sweeter than sucrose), only small amounts are needed to achieve the desired level of sweetness.Typical Usage Levels of Steviol Glycosides in Commercial Food Products:
1.	Beverages (e.g., soft drinks, juices, flavored water):
o	Amount: 0.01–0.05% of the product weight.
o	Purpose: Replaces sugar to provide sweetness without calories.
2.	Dairy Products (e.g., yogurt, flavored milk, ice cream):
o	Amount: 0.02–0.06% of the product weight.
o	Purpose: Sweetens without adding sugar, often combined with bulking agents like erythritol to replicate texture.
3.	Baked Goods (e.g., cakes, cookies, muffins):
o	Amount: 0.01–0.04% of the product weight.
o	Purpose: Provides sweetness, often used with sugar alcohols or fibers to compensate for sugar's role in structure and texture.
4.	Confectionery (e.g., candies, gum, chocolate):
o	Amount: 0.02–0.05% of the product weight.
o	Purpose: Sweetens low-sugar or sugar-free products, sometimes combined with other sweeteners for taste balance.
5.	Sauces and Dressings:
o	Amount: 0.01–0.03% of the product weight.
o	Purpose: Adds sweetness to low-calorie or sugar-free sauces like ketchup, barbecue sauce, and salad dressings.
6.	Snacks (e.g., bars, granola, crisps):
o	Amount: 0.01–0.05% of the product weight.
o	Purpose: Reduces sugar content while maintaining sweetness in healthy or low-calorie snack products.
7.	Processed Foods (e.g., jams, jellies, canned fruit):
o	Amount: 0.02–0.05% of the product weight.
o	Purpose: Provides sweetness in reduced-sugar or sugar-free versions.
Key Considerations for Usage:
•	Sweetness Potency: Steviol glycosides are extremely sweet; precise blending is required to avoid over-sweetness or bitter aftertaste.
•	Blends with Other Sweeteners: Often used in combination with sugar alcohols (e.g., erythritol) or other high-intensity sweeteners to improve flavor and reduce bitterness.
•	Regulatory Limits: Maximum allowable usage levels may vary by region and food type. Manufacturers must comply with local food safety regulations.
Regulatory and Safety Considerations:
•	GRAS Status: Steviol glycosides are generally recognized as safe (GRAS) by the FDA and approved for use in many countries.
•	Labeling: On ingredient lists, they may appear as "steviol glycosides," "stevia extract," or "Rebaudioside A" (depending on the specific compound used).
Shelf Life and Storage:
•	Shelf Life: Typically 2–3 years when stored properly.
•	Storage Conditions: Keep in a cool, dry place in an airtight container to prevent moisture absorption and degradation.
Summary:
The typical amount of steviol glycosides used in commercial food products ranges from 0.01% to 0.06% of the product weight, depending on the sweetness required and the application. They are widely used in beverages, dairy, baked goods, confectionery, sauces, and snacks to replace sugar and create lower-calorie options. Manufacturers must carefully balance usage to ensure optimal sweetness while minimizing potential aftertaste.

"""

table_output = chatty(input_text,table)
print(table_output)


# %% [markdown]
# # Gemini

# %%
import os
import pandas as pd
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import time
from dotenv import load_dotenv
# import io
from io import StringIO


# Retrieve the API key from environment variables
GEMINI_API_KEY = "access key"
# os.getenv("GOOGLE_API_KEY")
# Configure the Generative AI API with the provided key
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-pro')  # Load the model.

prompt = f"Convert the following text into a table with columns 'Term', 'Category', and 'Amount':\n{input_text} output must similar to given below table\n\nTable: {table}"
response = model.generate_content(prompt)  # Generate content.
# if response and response.parts:
#     return response.text  # Return the response text if available.

markdown_table = str(response.text)
# Use io.StringIO to treat the string as a file
# Use StringIO to read the Markdown formatted string into a DataFrame
df = pd.read_csv(StringIO(markdown_table), sep="|", engine='python', skiprows=1, skipinitialspace=True)

# Drop any columns with NaN values due to parsing issues
df = df.dropna(axis=1, how='all')

# Drop the empty row that might be created due to trailing separators
df = df.iloc[1:].reset_index(drop=True)

# Clean up the column names
df.columns = ['Term', 'Category', 'Amount']

# Print the DataFrame
df

# %%



