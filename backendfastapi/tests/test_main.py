import pytest
from fastapi.testclient import TestClient
from api.main import app

# Create a TestClient instance
client = TestClient(app)

# Sample valid input data
valid_input = {
    "Exercise": "Yes",
    "Heart_Disease": "No",
    "Sex": "Male",
    "BMI": 25.0,
    "Smoking_History": "No",
    "Alcohol_Consumption": 1.5,
    "Fruit_Consumption": 3.0,
    "Green_Vegetables_Consumption": 2.5,
    "FriedPotato_Consumption": 0.5
}

# Sample invalid input data
invalid_input = {
    "Exercise": "Maybe",
    "Heart_Disease": "No",
    "Sex": "Male",
    "BMI": 25.0,
    "Smoking_History": "No",
    "Alcohol_Consumption": 1.5,
    "Fruit_Consumption": 3.0,
    "Green_Vegetables_Consumption": 2.5,
    "FriedPotato_Consumption": 0.5
}

def test_predict_valid_input():
    response = client.post("/predict", json=valid_input)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "result" in response.json()
    assert "createdAt" in response.json()

def test_predict_invalid_input():
    response = client.post("/predict", json=invalid_input)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid input value: 'Maybe'"

def test_predict_missing_field():
    incomplete_input = valid_input.copy()
    del incomplete_input["Exercise"]
    response = client.post("/predict", json=incomplete_input)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "Exercise"]
    assert response.json()["detail"][0]["msg"] == "field required"

