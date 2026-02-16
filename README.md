# Smart Recipe Generator

A Flask web application that matches user ingredients to recipes using an intelligent scoring algorithm.

## 🌐 Live Demo

[🚀 Click here to try FlavorFusion](https://flavorfusion-9.onrender.com)


## Project Summary 

The Smart Recipe Generator is a full-stack web application that solves a common kitchen problem: "What can I cook with what I have?" Users enter their available ingredients, and the system matches them against a database of 20 recipes using a percentage-based scoring algorithm. The matching works by comparing each user ingredient against recipe ingredients using substring matching (so "chicken" matches "chicken breast"), then calculating a score as the ratio of matched ingredients to total required ingredients.

The application filters recipes before scoring them, which is more efficient than scoring everything first. Users can filter by dietary preference (vegan, vegetarian, regular), difficulty level, and maximum cooking time. Results show the top 3-5 matches with a visual score bar, missing ingredient list, and nutritional information. The serving adjustment feature scales nutrition values proportionally.

Additional features include a 5-star rating system with running average calculation, localStorage-based favorites, and an ingredient substitution engine. The image upload feature simulates ingredient detection (a real implementation would use a computer vision API). The architecture follows a simple MVC pattern with Flask handling routes, SQLite for persistence, and vanilla JavaScript for the interactive frontend. No unnecessary frameworks were used.

## Features

- **Ingredient Matching**: Enter ingredients and get matched recipes
- **Image Upload**: Upload ingredient photos for AI detection
- **Quick Search**: Real-time recipe search with dropdown
- **Favorites System**: Save and manage favorite recipes
- **Recipe Ratings**: Rate and review recipes
- **Responsive Design**: Works on all devices
- **Mobile Optimized**: Touch-friendly interface

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Vanilla JavaScript
- **Styling**: Custom CSS
- **API**: RESTful endpoints

## How the Matching Algorithm Works

The recipe matching follows a simple 3-step process:

### Step 1: Filter

Before any scoring, we eliminate recipes that don't match the user's constraints:

- **Dietary**: If user selects "vegan", only vegan recipes pass through
- **Difficulty**: If user selects "easy", medium and hard recipes are removed
- **Cook time**: Recipes exceeding the max time are filtered out

This is more efficient than scoring everything and filtering later.

### Step 2: Score

For each remaining recipe, we calculate a match percentage:

```
match_score = (matched_ingredients / total_recipe_ingredients) × 100
```

We use **substring matching** so "tomato" matches "canned tomatoes" and "chicken" matches "chicken breast". This makes the system more forgiving than exact matching.

### Step 3: Rank

Results are sorted by score (highest first) and we return the top 5 matches. Each result includes:

- Match percentage with visual bar
- Count of matched vs. total ingredients
- List of missing ingredients
- Ingredient substitution suggestions

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize database: `python database.py`
4. Run the application: `python app.py`

## Project Structure

```
flask-app/
├── app.py              # Main Flask application
├── database.py          # Database setup script
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css    # Application styles
│   ├── js/
│   │   └── app.js        # Frontend logic
│   └── images/
│       └── logo.png      # Application logo
└── templates/
    └── index.html       # Main HTML template
```

## API Endpoints

- `GET /` - Home page
- `POST /api/search` - Search recipes by ingredients
- `GET /api/recipes` - Get all recipes
- `POST /api/rate` - Rate a recipe
- `GET /api/substitutions` - Get ingredient substitutions

## License

MIT License - feel free to use for personal or commercial projects.
