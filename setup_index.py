from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['assessment_db']
employees = db['employees']

# Create index on employee_id
employees.create_index("employee_id", unique=True)

print("Index created successfully!")
