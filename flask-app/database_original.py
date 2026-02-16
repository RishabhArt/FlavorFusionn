"""
Database Initialization Script
==============================
Creates the SQLite database and seeds it with 20 sample recipes.
Run this once before starting the Flask app.

Usage:
    python database.py
"""

import sqlite3
import json
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'recipes.db')


def create_tables(cursor):
    """
    Create the recipes table.
    We store ingredients, nutrition, and substitutions as JSON strings
    because SQLite doesn't have native array/object types.
    This keeps things simple — no need for junction tables.
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            ingredients TEXT NOT NULL,       -- JSON array of ingredient strings
            instructions TEXT NOT NULL,
            cook_time INTEGER NOT NULL,      -- in minutes
            difficulty TEXT NOT NULL,         -- "easy", "medium", "hard"
            dietary TEXT NOT NULL,            -- "regular", "vegetarian", "vegan"
            servings INTEGER NOT NULL,
            cuisine TEXT,
            image_url TEXT,
            nutrition TEXT NOT NULL,          -- JSON object with nutritional info
            substitutions TEXT NOT NULL,      -- JSON object: ingredient -> substitute
            rating REAL DEFAULT 0.0,
            rating_count INTEGER DEFAULT 0
        )
    ''')


def seed_recipes(cursor):
    """
    Insert 20 sample recipes into the database.
    Each recipe has realistic ingredients, nutrition, and substitution info.
    """
    recipes = [
        # ── Recipe 1: Classic Spaghetti Bolognese ──────────
        {
            "name": "Classic Spaghetti Bolognese",
            "description": "A hearty Italian meat sauce served over spaghetti. Perfect comfort food for any night of the week.",
            "ingredients": ["spaghetti", "ground beef", "onion", "garlic", "canned tomatoes", "tomato paste", "olive oil", "salt", "pepper", "basil"],
            "instructions": "1. Cook spaghetti according to package directions.\n2. Heat olive oil in a large pan over medium heat.\n3. Sauté diced onion until soft, about 5 minutes.\n4. Add minced garlic, cook 1 minute.\n5. Add ground beef, break apart, cook until browned.\n6. Stir in canned tomatoes and tomato paste.\n7. Season with salt, pepper, and basil.\n8. Simmer for 20 minutes, stirring occasionally.\n9. Serve sauce over spaghetti.",
            "cook_time": 40,
            "difficulty": "easy",
            "dietary": "regular",
            "servings": 4,
            "cuisine": "Italian",
            "image_url": "https://tse3.mm.bing.net/th/id/OIP.OxTBVlTLtzxBfxHSwBLvuAHaEw?pid=Api&P=0&h=220",
            "nutrition": {"calories": 520, "protein": 28, "carbs": 62, "fat": 16, "fiber": 4},
            "substitutions": {"ground beef": "ground turkey or mushrooms", "spaghetti": "penne or gluten-free pasta", "basil": "oregano"}
        },
        # ── Recipe 2: Chicken Stir Fry ─────────────────────
        {
            "name": "Chicken Stir Fry",
            "description": "Quick and colorful stir fry with tender chicken and crispy vegetables in a savory sauce.",
            "ingredients": ["chicken breast", "broccoli", "bell pepper", "soy sauce", "garlic", "ginger", "sesame oil", "rice", "cornstarch", "green onion"],
            "instructions": "1. Cook rice according to package directions.\n2. Slice chicken into thin strips, toss with cornstarch.\n3. Heat sesame oil in a wok over high heat.\n4. Cook chicken strips until golden, about 5 minutes. Set aside.\n5. Add chopped broccoli and bell pepper, stir fry 3 minutes.\n6. Add minced garlic and grated ginger, cook 30 seconds.\n7. Return chicken to wok.\n8. Pour in soy sauce, toss everything together.\n9. Serve over rice, garnish with sliced green onion.",
            "cook_time": 25,
            "difficulty": "easy",
            "dietary": "regular",
            "servings": 3,
            "cuisine": "Asian",
            "image_url": "https://tse1.mm.bing.net/th/id/OIP.BIgnyScngaRIZWvPHzSQXQHaHa?pid=Api&P=0&h=220",
            "nutrition": {"calories": 450, "protein": 35, "carbs": 48, "fat": 12, "fiber": 5},
            "substitutions": {"chicken breast": "tofu or shrimp", "soy sauce": "tamari (gluten-free)", "sesame oil": "vegetable oil"}
        },
        # ── Recipe 3: Vegetable Curry ──────────────────────
        {
            "name": "Vegetable Curry",
            "description": "Creamy coconut curry loaded with vegetables. Warming, aromatic, and naturally vegan.",
            "ingredients": ["chickpeas", "coconut milk", "sweet potato", "spinach", "onion", "garlic", "curry powder", "cumin", "olive oil", "rice"],
            "instructions": "1. Cook rice according to package directions.\n2. Dice sweet potato into small cubes.\n3. Heat olive oil in a pot, sauté diced onion 5 minutes.\n4. Add garlic, curry powder, and cumin, cook 1 minute.\n5. Add sweet potato cubes and coconut milk.\n6. Simmer 15 minutes until sweet potato is tender.\n7. Stir in drained chickpeas and spinach.\n8. Cook 5 more minutes until spinach wilts.\n9. Serve over rice.",
            "cook_time": 35,
            "difficulty": "easy",
            "dietary": "vegan",
            "servings": 4,
            "cuisine": "Indian",
            "image_url": "https://tse3.mm.bing.net/th/id/OIP.ITwj7vz9WZTT49eNpJVXxwHaE8?pid=Api&P=0&h=220",
            "nutrition": {"calories": 380, "protein": 12, "carbs": 52, "fat": 14, "fiber": 9},
            "substitutions": {"chickpeas": "lentils or white beans", "sweet potato": "butternut squash", "coconut milk": "cashew cream"}
        },
        # ── Recipe 4: Caesar Salad ─────────────────────────
        {
            "name": "Caesar Salad",
            "description": "Crisp romaine lettuce with creamy Caesar dressing, croutons, and parmesan.",
            "ingredients": ["romaine lettuce", "parmesan cheese", "croutons", "lemon juice", "garlic", "olive oil", "egg yolk", "dijon mustard", "anchovy paste", "salt"],
            "instructions": "1. Wash and chop romaine lettuce into bite-size pieces.\n2. Make dressing: whisk egg yolk, minced garlic, lemon juice, dijon mustard, and anchovy paste.\n3. Slowly drizzle in olive oil while whisking to emulsify.\n4. Season dressing with salt.\n5. Toss lettuce with dressing.\n6. Top with grated parmesan and croutons.\n7. Serve immediately.",
            "cook_time": 15,
            "difficulty": "easy",
            "dietary": "regular",
            "servings": 2,
            "cuisine": "American",
            "image_url": "https://tse3.mm.bing.net/th/id/OIP.8UagT3WWGxruvIOqJTCPeQHaE8?pid=Api&P=0&h=220",
            "nutrition": {"calories": 320, "protein": 12, "carbs": 18, "fat": 24, "fiber": 3},
            "substitutions": {"anchovy paste": "Worcestershire sauce", "egg yolk": "mayonnaise", "croutons": "toasted bread cubes"}
        },
        # ── Recipe 5: Black Bean Tacos ─────────────────────
        {
            "name": "Black Bean Tacos",
            "description": "Flavorful black bean tacos topped with fresh salsa, avocado, and lime.",
            "ingredients": ["black beans", "tortillas", "avocado", "tomato", "onion", "cilantro", "lime", "cumin", "chili powder", "salt"],
            "instructions": "1. Drain and rinse black beans.\n2. Heat beans in a pan with cumin and chili powder.\n3. Mash slightly with a fork for texture.\n4. Dice tomato and onion for fresh salsa.\n5. Mix tomato, onion, chopped cilantro, and lime juice.\n6. Warm tortillas in a dry pan.\n7. Fill tortillas with seasoned beans.\n8. Top with salsa and sliced avocado.\n9. Squeeze extra lime on top.",
            "cook_time": 15,
            "difficulty": "easy",
            "dietary": "vegan",
            "servings": 3,
            "cuisine": "Mexican",
            "image_url": "https://tse1.mm.bing.net/th/id/OIP.m43hLXXcCuwzp9Nl90oZYwHaFF?pid=Api&P=0&h=220",
            "nutrition": {"calories": 340, "protein": 14, "carbs": 48, "fat": 12, "fiber": 12},
            "substitutions": {"black beans": "pinto beans or lentils", "tortillas": "lettuce wraps", "avocado": "sour cream"}
        },
        # ── Recipe 6: Mushroom Risotto ─────────────────────
        {
            "name": "Mushroom Risotto",
            "description": "Creamy Italian risotto with earthy mushrooms and parmesan cheese.",
            "ingredients": ["arborio rice", "mushrooms", "onion", "garlic", "vegetable broth", "parmesan cheese", "butter", "white wine", "olive oil", "thyme"],
            "instructions": "1. Heat vegetable broth in a separate pot, keep warm.\n2. Sauté sliced mushrooms in butter until golden. Set aside.\n3. In the same pan, heat olive oil, cook diced onion 5 minutes.\n4. Add garlic, cook 30 seconds.\n5. Add arborio rice, stir to coat in oil for 2 minutes.\n6. Pour in white wine, stir until absorbed.\n7. Add warm broth one ladle at a time, stirring after each addition.\n8. Continue for 18-20 minutes until rice is creamy.\n9. Fold in mushrooms, parmesan, and thyme.\n10. Serve immediately.",
            "cook_time": 40,
            "difficulty": "medium",
            "dietary": "vegetarian",
            "servings": 4,
            "cuisine": "Italian",
            "image_url": "https://tse4.mm.bing.net/th/id/OIP.U9rWj6YKHR8C8XYj4ISKxgHaHa?pid=Api&P=0&h=220",
            "nutrition": {"calories": 420, "protein": 14, "carbs": 58, "fat": 16, "fiber": 3},
            "substitutions": {"white wine": "extra broth with lemon juice", "parmesan cheese": "nutritional yeast (for vegan)", "butter": "olive oil"}
        },
        # ── Recipe 7: Grilled Salmon ───────────────────────
        {
            "name": "Grilled Salmon with Lemon Dill",
            "description": "Perfectly grilled salmon fillet with a bright lemon and dill sauce.",
            "ingredients": ["salmon fillet", "lemon", "dill", "garlic", "olive oil", "salt", "pepper", "asparagus", "butter"],
            "instructions": "1. Preheat grill to medium-high heat.\n2. Pat salmon dry, brush with olive oil.\n3. Season with salt, pepper, and minced garlic.\n4. Grill salmon skin-side down 4-5 minutes per side.\n5. Meanwhile, toss asparagus with olive oil and salt.\n6. Grill asparagus alongside the salmon.\n7. Make sauce: melt butter, add lemon juice and chopped dill.\n8. Plate salmon with asparagus.\n9. Drizzle lemon dill sauce on top.",
            "cook_time": 20,
            "difficulty": "medium",
            "dietary": "regular",
            "servings": 2,
            "cuisine": "American",
            "image_url": "https://tse4.mm.bing.net/th/id/OIP.jeC0mIQc5chFBuGT4AHI4AHaHa?pid=Api&P=0&h=220",
            "nutrition": {"calories": 480, "protein": 42, "carbs": 8, "fat": 32, "fiber": 3},
            "substitutions": {"salmon fillet": "trout or cod", "asparagus": "green beans or broccoli", "dill": "parsley"}
        },
        # ── Recipe 8: Veggie Buddha Bowl ───────────────────
        {
            "name": "Veggie Buddha Bowl",
            "description": "A colorful nourishing bowl with roasted vegetables, quinoa, and tahini dressing.",
            "ingredients": ["quinoa", "sweet potato", "chickpeas", "kale", "avocado", "red cabbage", "tahini", "lemon", "garlic", "olive oil"],
            "instructions": "1. Preheat oven to 400°F (200°C).\n2. Cook quinoa according to package directions.\n3. Cube sweet potato, toss with olive oil, roast 25 minutes.\n4. Drain chickpeas, toss with olive oil and spices, roast 20 minutes.\n5. Massage chopped kale with a drizzle of olive oil.\n6. Make dressing: whisk tahini, lemon juice, minced garlic, and water.\n7. Shred red cabbage.\n8. Assemble bowls: quinoa base, top with sweet potato, chickpeas, kale, cabbage.\n9. Slice avocado on top.\n10. Drizzle with tahini dressing.",
            "cook_time": 35,
            "difficulty": "easy",
            "dietary": "vegan",
            "servings": 2,
            "cuisine": "American",
            "image_url": "https://tse1.mm.bing.net/th/id/OIP.YWrNd8GmR4yKHhJWjtkNNwHaFl?pid=Api&P=0&h=220",
            "nutrition": {"calories": 520, "protein": 18, "carbs": 64, "fat": 22, "fiber": 14},
            "substitutions": {"quinoa": "brown rice or couscous", "tahini": "peanut butter", "kale": "spinach"}
        },
        # ── Recipe 9: Beef Tacos ───────────────────────────
        {
            "name": "Beef Tacos",
            "description": "Classic seasoned ground beef tacos with all the fixings.",
            "ingredients": ["ground beef", "tortillas", "lettuce", "tomato", "cheddar cheese", "sour cream", "onion", "cumin", "chili powder", "garlic"],
            "instructions": "1. Heat a skillet over medium-high heat.\n2. Cook ground beef, breaking it apart, until browned.\n3. Drain excess fat.\n4. Add diced onion, minced garlic, cumin, and chili powder.\n5. Cook 3 more minutes.\n6. Warm tortillas in a dry pan or microwave.\n7. Shred lettuce, dice tomato, grate cheese.\n8. Fill tortillas with beef mixture.\n9. Top with lettuce, tomato, cheese, and sour cream.",
            "cook_time": 20,
            "difficulty": "easy",
            "dietary": "regular",
            "servings": 4,
            "cuisine": "Mexican",
            "image_url": "https://tse2.mm.bing.net/th/id/OIP.r26FdOfa27arX9DQE7hSOQHaHa?pid=Api&P=0&h=220",
            "nutrition": {"calories": 440, "protein": 26, "carbs": 32, "fat": 24, "fiber": 3},
            "substitutions": {"ground beef": "ground turkey or black beans", "sour cream": "Greek yogurt", "cheddar cheese": "pepper jack"}
        },
        # ── Recipe 10: Tomato Soup ─────────────────────────
        {
            "name": "Creamy Tomato Soup",
            "description": "Velvety smooth tomato soup made from scratch. Best served with grilled cheese.",
            "ingredients": ["canned tomatoes", "onion", "garlic", "vegetable broth", "heavy cream", "butter", "basil", "salt", "pepper", "sugar"],
            "instructions": "1. Melt butter in a large pot over medium heat.\n2. Sauté diced onion until translucent, about 5 minutes.\n3. Add minced garlic, cook 1 minute.\n4. Pour in canned tomatoes and vegetable broth.\n5. Add a pinch of sugar to balance acidity.\n6. Simmer for 20 minutes.\n7. Blend soup until smooth using an immersion blender.\n8. Stir in heavy cream, season with salt, pepper, and basil.\n9. Serve hot with fresh basil on top.",
            "cook_time": 30,
            "difficulty": "easy",
            "dietary": "vegetarian",
            "servings": 4,
            "cuisine": "American",
            "image_url": "https://tse2.mm.bing.net/th/id/OIP.HSe3AH_sXo6LjiofL2gRBwHaIH?pid=Api&P=0&h=220",
            "nutrition": {"calories": 220, "protein": 4, "carbs": 18, "fat": 16, "fiber": 3},
            "substitutions": {"heavy cream": "coconut cream (for vegan)", "butter": "olive oil", "vegetable broth": "water with bouillon"}
        },
        # ── Recipe 11: Pad Thai ────────────────────────────
        {
            "name": "Pad Thai",
            "description": "Sweet, sour, and savory Thai noodles with shrimp, peanuts, and bean sprouts.",
            "ingredients": ["rice noodles", "shrimp", "egg", "bean sprouts", "green onion", "peanuts", "lime", "fish sauce", "brown sugar", "garlic"],
            "instructions": "1. Soak rice noodles in warm water 30 minutes, drain.\n2. Make sauce: mix fish sauce, brown sugar, and lime juice.\n3. Heat oil in a wok over high heat.\n4. Cook shrimp 2 minutes per side, set aside.\n5. Scramble egg in the wok, break into pieces.\n6. Add noodles and sauce, toss 2 minutes.\n7. Add shrimp back, toss with bean sprouts and green onion.\n8. Plate and top with crushed peanuts.\n9. Serve with lime wedges.",
            "cook_time": 30,
            "difficulty": "medium",
            "dietary": "regular",
            "servings": 3,
            "cuisine": "Thai",
            "image_url": "https://tse2.mm.bing.net/th/id/OIP.DAzHt9oUhHFUmQe8be5hfQHaE8?pid=Api&P=0&h=220",
            "nutrition": {"calories": 480, "protein": 24, "carbs": 58, "fat": 18, "fiber": 3},
            "substitutions": {"shrimp": "tofu or chicken", "fish sauce": "soy sauce", "peanuts": "cashews"}
        },
        # ── Recipe 12: Caprese Salad ───────────────────────
        {
            "name": "Caprese Salad",
            "description": "Simple and elegant Italian salad with fresh mozzarella, tomatoes, and basil.",
            "ingredients": ["fresh mozzarella", "tomato", "basil", "olive oil", "balsamic vinegar", "salt", "pepper"],
            "instructions": "1. Slice fresh mozzarella into 1/4-inch rounds.\n2. Slice tomatoes into similar-sized rounds.\n3. Arrange alternating slices of mozzarella and tomato on a plate.\n4. Tuck fresh basil leaves between slices.\n5. Drizzle generously with olive oil.\n6. Add a drizzle of balsamic vinegar.\n7. Season with salt and pepper.\n8. Serve at room temperature for best flavor.",
            "cook_time": 10,
            "difficulty": "easy",
            "dietary": "vegetarian",
            "servings": 2,
            "cuisine": "Italian",
            "image_url": "https://tse1.mm.bing.net/th/id/OIP.Oso72QbeIuTm5kQy9TsMAQHaHa?pid=Api&P=0&h=220",
            "nutrition": {"calories": 280, "protein": 16, "carbs": 8, "fat": 22, "fiber": 1},
            "substitutions": {"fresh mozzarella": "burrata or vegan mozzarella", "balsamic vinegar": "balsamic glaze", "basil": "arugula"}
        },
        # ── Recipe 13: Chicken Alfredo ─────────────────────
        {
            "name": "Chicken Alfredo",
            "description": "Rich and creamy fettuccine alfredo topped with seasoned grilled chicken.",
            "ingredients": ["fettuccine", "chicken breast", "heavy cream", "parmesan cheese", "butter", "garlic", "salt", "pepper", "olive oil"],
            "instructions": "1. Cook fettuccine according to package directions.\n2. Season chicken breast with salt and pepper.\n3. Heat olive oil in a pan, cook chicken 6-7 minutes per side.\n4. Let chicken rest, then slice.\n5. In the same pan, melt butter over medium heat.\n6. Add minced garlic, cook 30 seconds.\n7. Pour in heavy cream, bring to a gentle simmer.\n8. Stir in grated parmesan until melted and smooth.\n9. Toss cooked fettuccine in the sauce.\n10. Top with sliced chicken.",
            "cook_time": 30,
            "difficulty": "medium",
            "dietary": "regular",
            "servings": 3,
            "cuisine": "Italian",
            "image_url": "https://tse4.mm.bing.net/th/id/OIP.p8hEmGfxqsIVDOnL8-2NlQHaHa?pid=Api&P=0&h=220",
            "nutrition": {"calories": 680, "protein": 38, "carbs": 52, "fat": 36, "fiber": 2},
            "substitutions": {"heavy cream": "half-and-half or cashew cream", "fettuccine": "any pasta shape", "chicken breast": "shrimp"}
        },
        # ── Recipe 14: Lentil Soup ─────────────────────────
        {
            "name": "Lentil Soup",
            "description": "Hearty and nutritious lentil soup with vegetables and warm spices.",
            "ingredients": ["red lentils", "carrot", "celery", "onion", "garlic", "cumin", "turmeric", "vegetable broth", "olive oil", "lemon"],
            "instructions": "1. Rinse red lentils under cold water.\n2. Heat olive oil in a pot, sauté diced onion, carrot, and celery.\n3. Cook 5 minutes until softened.\n4. Add minced garlic, cumin, and turmeric, cook 1 minute.\n5. Add lentils and vegetable broth.\n6. Bring to a boil, then reduce heat and simmer 25 minutes.\n7. Lentils should be very soft and breaking apart.\n8. Season with salt and a squeeze of lemon.\n9. Serve with crusty bread.",
            "cook_time": 35,
            "difficulty": "easy",
            "dietary": "vegan",
            "servings": 4,
            "cuisine": "Middle Eastern",
            "image_url": "https://tse2.mm.bing.net/th/id/OIP.4TDX5Gev0jrLAySY1NrpNAHaHa?pid=Api&P=0&h=220",
            "nutrition": {"calories": 280, "protein": 18, "carbs": 42, "fat": 6, "fiber": 16},
            "substitutions": {"red lentils": "green lentils (longer cook time)", "vegetable broth": "chicken broth", "cumin": "coriander"}
        },
        # ── Recipe 15: Omelette ────────────────────────────
        {
            "name": "Garden Vegetable Omelette",
            "description": "Fluffy three-egg omelette stuffed with fresh vegetables and cheese.",
            "ingredients": ["eggs", "bell pepper", "mushrooms", "spinach", "cheddar cheese", "butter", "salt", "pepper", "milk"],
            "instructions": "1. Dice bell pepper and slice mushrooms.\n2. Whisk 3 eggs with a splash of milk, salt, and pepper.\n3. Melt butter in a non-stick pan over medium heat.\n4. Sauté bell pepper and mushrooms 3 minutes.\n5. Add spinach, cook until wilted. Remove veggies.\n6. Add more butter to the pan.\n7. Pour in egg mixture, swirl to cover pan.\n8. Cook until edges set, about 2 minutes.\n9. Add veggies and grated cheese to one half.\n10. Fold omelette over, cook 1 more minute.",
            "cook_time": 15,
            "difficulty": "easy",
            "dietary": "vegetarian",
            "servings": 1,
            "cuisine": "French",
            "image_url": "https://tse2.mm.bing.net/th/id/OIP.UoNkatEVpC-oE1aRHbF9EwHaEK?pid=Api&P=0&h=220",
            "nutrition": {"calories": 380, "protein": 26, "carbs": 8, "fat": 28, "fiber": 2},
            "substitutions": {"cheddar cheese": "feta or goat cheese", "butter": "olive oil", "milk": "water"}
        },
        # ── Recipe 16: Fish and Chips ──────────────────────
        {
            "name": "Fish and Chips",
            "description": "Crispy beer-battered cod with golden chips. A British classic.",
            "ingredients": ["cod fillet", "potatoes", "flour", "beer", "egg", "salt", "pepper", "vegetable oil", "lemon", "tartar sauce"],
            "instructions": "1. Cut potatoes into thick chips, soak in cold water 30 minutes.\n2. Pat chips dry, fry at 325°F until soft but not browned. Set aside.\n3. Make batter: whisk flour, beer, egg, salt, and pepper.\n4. Pat cod fillets dry, dust with flour.\n5. Dip cod in batter, let excess drip off.\n6. Fry battered cod at 375°F for 5-6 minutes until golden.\n7. Increase oil temp, fry chips again until crispy and golden.\n8. Drain on paper towels, season with salt.\n9. Serve with lemon wedges and tartar sauce.",
            "cook_time": 45,
            "difficulty": "hard",
            "dietary": "regular",
            "servings": 2,
            "cuisine": "British",
            "image_url": "https://tse3.mm.bing.net/th/id/OIP.85Kh8NkHbgoTXVBFakKfBwHaEK?pid=Api&P=0&h=220",
            "nutrition": {"calories": 620, "protein": 32, "carbs": 58, "fat": 28, "fiber": 4},
            "substitutions": {"cod fillet": "haddock or halibut", "beer": "sparkling water", "tartar sauce": "malt vinegar"}
        },
        # ── Recipe 17: Greek Salad ─────────────────────────
        {
            "name": "Greek Salad",
            "description": "Refreshing Mediterranean salad with cucumber, olives, and feta cheese.",
            "ingredients": ["cucumber", "tomato", "red onion", "feta cheese", "kalamata olives", "olive oil", "red wine vinegar", "oregano", "salt", "pepper"],
            "instructions": "1. Chop cucumber into half-moons.\n2. Cut tomatoes into wedges.\n3. Thinly slice red onion.\n4. Combine vegetables in a large bowl.\n5. Add kalamata olives.\n6. Crumble feta cheese on top.\n7. Drizzle with olive oil and red wine vinegar.\n8. Sprinkle with dried oregano, salt, and pepper.\n9. Toss gently and serve.",
            "cook_time": 10,
            "difficulty": "easy",
            "dietary": "vegetarian",
            "servings": 3,
            "cuisine": "Greek",
            "image_url": "https://tse3.mm.bing.net/th/id/OIP.h36c3mDusD0RJyXYbS06QgHaGC?pid=Api&P=0&h=220",
            "nutrition": {"calories": 240, "protein": 8, "carbs": 12, "fat": 18, "fiber": 3},
            "substitutions": {"feta cheese": "goat cheese or vegan feta", "kalamata olives": "green olives", "red wine vinegar": "lemon juice"}
        },
        # ── Recipe 18: Fried Rice ──────────────────────────
        {
            "name": "Vegetable Fried Rice",
            "description": "Quick and satisfying fried rice loaded with vegetables and scrambled egg.",
            "ingredients": ["rice", "egg", "carrot", "peas", "soy sauce", "sesame oil", "garlic", "ginger", "green onion", "vegetable oil"],
            "instructions": "1. Use day-old cold rice for best results (or cook and cool).\n2. Heat vegetable oil in a wok over high heat.\n3. Scramble eggs, break into small pieces. Set aside.\n4. Add more oil, stir fry diced carrot 2 minutes.\n5. Add peas, minced garlic, and grated ginger. Cook 1 minute.\n6. Add cold rice, press flat against wok to get crispy.\n7. Pour soy sauce and sesame oil over rice.\n8. Toss everything together with scrambled egg.\n9. Garnish with sliced green onion.",
            "cook_time": 15,
            "difficulty": "easy",
            "dietary": "vegetarian",
            "servings": 3,
            "cuisine": "Chinese",
            "image_url": "https://tse4.mm.bing.net/th/id/OIP.X95ashIyAoaJM6FX0YsyvgHaFj?pid=Api&P=0&h=220",
            "nutrition": {"calories": 360, "protein": 12, "carbs": 54, "fat": 10, "fiber": 4},
            "substitutions": {"egg": "extra tofu (for vegan)", "soy sauce": "tamari", "peas": "edamame or corn"}
        },
        # ── Recipe 19: Banana Pancakes ─────────────────────
        {
            "name": "Banana Pancakes",
            "description": "Fluffy pancakes naturally sweetened with ripe bananas. A weekend breakfast favorite.",
            "ingredients": ["banana", "flour", "egg", "milk", "baking powder", "butter", "vanilla extract", "cinnamon", "maple syrup"],
            "instructions": "1. Mash ripe banana in a bowl.\n2. Whisk in egg, milk, and vanilla extract.\n3. In another bowl, mix flour, baking powder, and cinnamon.\n4. Combine wet and dry ingredients, stir until just mixed.\n5. Don't overmix — some lumps are fine.\n6. Heat butter in a pan over medium-low heat.\n7. Pour 1/4 cup batter per pancake.\n8. Cook until bubbles form on surface, about 2 minutes.\n9. Flip and cook 1-2 more minutes.\n10. Serve with maple syrup and extra banana slices.",
            "cook_time": 20,
            "difficulty": "easy",
            "dietary": "vegetarian",
            "servings": 2,
            "cuisine": "American",
            "image_url": "https://tse1.mm.bing.net/th/id/OIP.ezhXOt2zDmTkLrIihDO_3QHaHa?pid=Api&P=0&h=220",
            "nutrition": {"calories": 340, "protein": 10, "carbs": 56, "fat": 10, "fiber": 3},
            "substitutions": {"milk": "oat milk or almond milk", "egg": "flax egg (1 tbsp ground flax + 3 tbsp water)", "butter": "coconut oil"}
        },
        # ── Recipe 20: Beef Stew ───────────────────────────
        {
            "name": "Hearty Beef Stew",
            "description": "Slow-cooked beef stew with tender vegetables in a rich savory broth.",
            "ingredients": ["beef chuck", "potatoes", "carrot", "celery", "onion", "garlic", "beef broth", "tomato paste", "flour", "thyme", "bay leaf", "olive oil"],
            "instructions": "1. Cut beef into 1-inch cubes, toss with flour, salt, and pepper.\n2. Heat olive oil in a Dutch oven over medium-high heat.\n3. Brown beef on all sides in batches. Set aside.\n4. Sauté diced onion, carrot, and celery 5 minutes.\n5. Add minced garlic and tomato paste, cook 1 minute.\n6. Return beef to pot.\n7. Pour in beef broth, add thyme and bay leaf.\n8. Bring to a boil, then reduce heat to low.\n9. Cover and simmer 1.5 hours.\n10. Add diced potatoes, cook 30 more minutes until tender.\n11. Remove bay leaf before serving.",
            "cook_time": 120,
            "difficulty": "hard",
            "dietary": "regular",
            "servings": 6,
            "cuisine": "American",
            "image_url": "https://tse2.mm.bing.net/th/id/OIP.yRjMDDAiVKpENizpbJoXjgHaHM?pid=Api&P=0&h=220",
            "nutrition": {"calories": 480, "protein": 36, "carbs": 32, "fat": 22, "fiber": 5},
            "substitutions": {"beef chuck": "lamb or chickpeas (vegetarian)", "beef broth": "vegetable broth", "potatoes": "sweet potatoes"}
        }
    ]

    # Insert each recipe into the database
    for recipe in recipes:
        cursor.execute('''
            INSERT INTO recipes (name, description, ingredients, instructions, cook_time,
                               difficulty, dietary, servings, cuisine, image_url,
                               nutrition, substitutions, rating, rating_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe['name'],
            recipe['description'],
            json.dumps(recipe['ingredients']),
            recipe['instructions'],
            recipe['cook_time'],
            recipe['difficulty'],
            recipe['dietary'],
            recipe['servings'],
            recipe['cuisine'],
            recipe['image_url'],
            json.dumps(recipe['nutrition']),
            json.dumps(recipe['substitutions']),
            0.0,  # Starting rating
            0     # No ratings yet
        ))


def initialize_database():
    """Main function to create and populate the database."""
    # Remove old database if it exists (fresh start)
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print("Removed old database.")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    print("Creating tables...")
    create_tables(cursor)

    print("Seeding 20 sample recipes...")
    seed_recipes(cursor)

    conn.commit()
    conn.close()
    print(f"Database created successfully at: {DATABASE}")
    print("You can now run the app with: python app.py")


# Run this script directly to initialize the database
if __name__ == '__main__':
    initialize_database()
