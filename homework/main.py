from typing import List

import models
import schemas
from database import engine, session
from fastapi import FastAPI, HTTPException, Path
from models import Recipe
from sqlalchemy import select

descriptioin = """
Recipes API features:
 ### Browse recipes
 ### Retreive detailed info
 ### Add new recipe
 """

tags_metadata = [{"name": "recipes", "description": "Operations with recipes"}]

app = FastAPI(title="Recipes API", description=descriptioin, openapi_tags=tags_metadata)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)                   #too long line


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get(
    "/recipes/",
    response_model=List[schemas.RecipeList],
    tags=["recipes"],
    summary="Recipies list",
    description="Get list of all recipes",
)
async def get_recipes_list():
    async with session.begin():
        query = select(Recipe).order_by(Recipe.views_count.desc(), Recipe.cook_time)
        res = await session.execute(query)
        return res.scalars().all()


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetail,
    tags=["recipes"],
    summary="Recipe details",
    description="Retrieve a detailed recipe info by ID",
    responses={404: {"description": "Recipe not found"}},
)
async def get_recipe_details(
    recipe_id: int = Path(  # noqa
        ..., title="Recipe ID", description="ID of the recipe to be fetched"
    )
):
    async with session.begin():
        res = await session.execute(select(Recipe).filter(Recipe.id == recipe_id))
        recipe = res.scalar_one_or_none()
        if recipe:
            recipe.views_count += 1
            await session.commit()
            return recipe
        else:
            raise HTTPException(status_code=404, detail="Recipe not found")


@app.post(
    "/recipes/",
    response_model=schemas.RecipeOut,
    tags=["recipes"],
    summary="Add new recipe",
    description="Add new recipe",
)
async def add_recipe(recipe: schemas.RecipeIn) -> Recipe:
    new_recipe = Recipe(**recipe.dict())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe
