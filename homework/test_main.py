from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_recipes_list():
    response = client.get("/recipes/")
    assert response.status_code == 200


def test_get_recipe_details():
    response = client.get("/recipes/1")
    assert response.status_code == 200


def test_add_recipe():
    recipie = {
        "name": "Chocolate Cake",
        "ingredients": "Flour, Sugar, Cocoa, Eggs, Butter, Baking Powder",
        "cook_time": 45,
        "description": "Mix all ingredients, bake in a stove "
        "for 30 mins at 200 degrees",
    }
    response = client.post("/recipes/", json=recipie)
    assert response.status_code == 200
