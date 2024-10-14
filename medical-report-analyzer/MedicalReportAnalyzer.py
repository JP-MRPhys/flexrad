import openai
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from unstructured.partition.pdf import partition_pdf


class PreProcessing:
      def __init__(self, api_key):
          self.api_key=api_key
      
      def read_pdf_text_and_tables_from_file(self, filename):

          elements = partition_pdf(filename, infer_table_structure=True, strategy="fast")
          tables = [el for el in elements if el.category == "Table"]
          for table in tables:
                #print(table.text)

            texts = [el for el in elements if el.category == "Text"]

          for text in texts:
                #print(text.text)

           return table, text


class MedicalReportAnalyzer:

    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.preprocessing=PreProcessing()

    def extract_keywords(self, text):
        
        prompt = f"""
        You are an expert medical professional tasked with extracting important keywords from medical reports.
        Given the following medical report, identify and list the most significant keywords.
        Focus on medical terms, diagnoses, treatments, symptoms, and medications.
        Provide the keywords as a Python list of strings.

        Medical Report:
        {text}

        Keywords:
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts keywords from medical reports."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5,
            )

            keywords_str = response.choices[0].message['content'].strip()
            # Convert the string representation of a list to an actual list
            keywords = eval(keywords_str)
            return keywords
        
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return []

    def analyze_report(self, text):
        prompt = f"""
        You are an expert medical professional tasked with analyzing medical reports.
        Given the following medical report, provide a brief summary and highlight key findings.
        Focus on diagnoses, treatments, and any notable medical observations.

        Medical Report:
        {text}

        Analysis:
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes medical reports."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                n=1,
                stop=None,
                temperature=0.5,
            )

            analysis = response.choices[0].message['content'].strip()
            return analysis
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return "Analysis could not be performed due to an error."