from pydantic import BaseModel


class BaseRecipe(BaseModel):
    name: str
    cook_time: int


class RecipeIn(BaseRecipe):
    ingredients: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Chocolate Cake",
                "ingredients": "Flour, Sugar, Cocoa, Eggs, Butter, Baking Powder",
                "cook_time": 45,
                "description": "Mix all ingredients, bake in a stove "
                "for 30 mins at 200 degrees",
            }
        }


class RecipeOut(BaseRecipe):
    id: int

    class Config:
        orm_mode = True


class RecipeDetail(RecipeOut):
    ingredients: str
    description: str


class RecipeList(RecipeOut):
    views_count: int
