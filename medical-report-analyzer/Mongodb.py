from pymongo import MongoClient
from datetime import datetime
import openai



#TODO add anonmization and deployment and data based replication
#TODO create based of all illusration for keywords detected

class Mongodb:
    def __init__(self, connection_string='mongodb://localhost:27017/', db_name='medical_reports'):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.reports_collection = self.db['reports']

    def store_report(self, report_text, keywords):
        report_data = {
            'text': report_text,
            'keywords': keywords,
            'created_at': datetime.utcnow()
        }
        result = self.reports_collection.insert_one(report_data)
        return str(result.inserted_id)

    def get_report(self, report_id):
        report = self.reports_collection.find_one({'_id': ObjectId(report_id)})
        if report:
            report['_id'] = str(report['_id'])
            report['created_at'] = report['created_at'].isoformat()
        return report

    def close_connection(self):
        self.client.close()



