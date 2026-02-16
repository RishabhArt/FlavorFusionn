"""
Smart Recipe Generator - Main Application
==========================================
A Flask web app that matches user ingredients to recipes
using a scoring algorithm. Built with SQLite for storage
and vanilla JS for the frontend.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import json
import os

# ── App Setup ──────────────────────────────────────────────
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Production configuration
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Database configuration - use absolute path for production
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'recipes.db')

# ── Database Initialization ────────────────────────────────
def init_db():
    """Initialize database if it doesn't exist or is empty."""
    try:
        # Check if database exists and has the recipes table
        if not os.path.exists(DATABASE):
            print("Database not found. Creating new database...")
            from database import initialize_database
            initialize_database()
        else:
            # Check if database has the recipes table
            test_db = sqlite3.connect(DATABASE)
            cursor = test_db.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recipes'")
            table_exists = cursor.fetchone() is not None
            test_db.close()
            
            if not table_exists:
                print("Database exists but no recipes table found. Recreating database...")
                from database import initialize_database
                initialize_database()
            else:
                # Check if table has data
                db = get_db()
                count = db.execute('SELECT COUNT(*) FROM recipes').fetchone()[0]
                db.close()
                
                if count == 0:
                    print("Database table exists but is empty. Seeding data...")
                    from database import initialize_database
                    initialize_database()
                else:
                    print(f"Database found with {count} recipes at: {DATABASE}")
                    
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        # Try to create database anyway
        try:
            from database import initialize_database
            initialize_database()
        except Exception as e2:
            print(f"Failed to create database: {str(e2)}")


# ── Database Helper ────────────────────────────────────────
# We use a helper function to get a fresh connection each time.
# This avoids issues with SQLite's thread-safety limitations.
def get_db():
    """Open a new database connection for each request."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # So we can access columns by name
    return conn


# ── Routes ─────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main single-page application."""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Return favicon to avoid 404 errors."""
    from flask import send_from_directory
    import os
    
    # Try to serve a favicon file if it exists, otherwise return a simple one
    favicon_path = os.path.join(app.static_folder, 'favicon.ico')
    if os.path.exists(favicon_path):
        return send_from_directory(app.static_folder, 'favicon.ico')
    else:
        # Return a simple 1x1 pixel PNG as fallback
        import base64
        favicon_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
        from flask import Response
        return Response(favicon_data, mimetype='image/x-icon')


@app.route('/api/recipes', methods=['GET'])
def get_all_recipes():
    """
    Return all recipes from the database.
    Used to populate the browse section.
    """
    try:
        # Ensure database is initialized
        init_db()
        
        db = get_db()
        recipes = db.execute('SELECT * FROM recipes').fetchall()
        db.close()
        
        print(f"Found {len(recipes)} recipes in database")

        # Convert Row objects to dictionaries so we can serialize them
        result = []
        for r in recipes:
            recipe = dict(r)
            
            # Safe JSON parsing with fallbacks
            try:
                recipe['ingredients'] = json.loads(recipe['ingredients']) if recipe['ingredients'] else []
            except (json.JSONDecodeError, TypeError):
                recipe['ingredients'] = []
                
            try:
                recipe['nutrition'] = json.loads(recipe['nutrition']) if recipe['nutrition'] else {}
            except (json.JSONDecodeError, TypeError):
                recipe['nutrition'] = {}
                
            try:
                recipe['substitutions'] = json.loads(recipe['substitutions']) if recipe['substitutions'] else {}
            except (json.JSONDecodeError, TypeError):
                recipe['substitutions'] = {}
                
            result.append(recipe)

        print(f"Successfully processed {len(result)} recipes")
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in get_all_recipes: {str(e)}")
        return jsonify({'error': 'Failed to load recipes', 'details': str(e)}), 500


@app.route('/api/debug', methods=['GET'])
def debug_info():
    """Debug endpoint to check database status."""
    try:
        db = get_db()
        count = db.execute('SELECT COUNT(*) FROM recipes').fetchone()[0]
        db.close()
        return jsonify({
            'database_path': DATABASE,
            'database_exists': os.path.exists(DATABASE),
            'recipe_count': count,
            'working_directory': os.getcwd()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search_recipes():
    """
    Main search endpoint.
    Accepts user ingredients and filters, then returns
    the top matching recipes ranked by a matching score.

    Algorithm overview:
    1. Parse user input (ingredients list + filters)
    2. Filter recipes by dietary, difficulty, and time constraints
    3. Score remaining recipes by ingredient overlap
    4. Sort by score descending, return top 3-5 matches
    """
    try:
        # Ensure database is initialized
        init_db()
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        # Extract user inputs with sensible defaults
        user_ingredients = data.get('ingredients', [])
        dietary = data.get('dietary', '')          # e.g. "vegetarian", "vegan"
        max_difficulty = data.get('difficulty', '')  # "easy", "medium", "hard"
        max_time = data.get('max_time', 999)        # in minutes
        servings = data.get('servings', 0)          # 0 means "no preference"

        # Normalize user ingredients to lowercase for fair comparison
        user_ingredients = [ing.strip().lower() for ing in user_ingredients if ing.strip()]

        if not user_ingredients:
            return jsonify({'error': 'Please enter at least one ingredient.'}), 400

        # Fetch all recipes from the database
        db = get_db()
        recipes = db.execute('SELECT * FROM recipes').fetchall()
        db.close()

        # ── Step 1: Filter ─────────────────────────────────────
        # We eliminate recipes that don't match the user's constraints
        # BEFORE scoring. This is more efficient than scoring everything
        # and filtering afterwards.
        filtered = []
        for r in recipes:
            recipe = dict(r)
            
            # Safe JSON parsing with fallbacks
            try:
                recipe['ingredients'] = json.loads(recipe['ingredients']) if recipe['ingredients'] else []
            except (json.JSONDecodeError, TypeError):
                recipe['ingredients'] = []
                
            try:
                recipe['nutrition'] = json.loads(recipe['nutrition']) if recipe['nutrition'] else {}
            except (json.JSONDecodeError, TypeError):
                recipe['nutrition'] = {}
                
            try:
                recipe['substitutions'] = json.loads(recipe['substitutions']) if recipe['substitutions'] else {}
            except (json.JSONDecodeError, TypeError):
                recipe['substitutions'] = {}

            # Dietary filter: skip if recipe doesn't match
            if dietary and recipe['dietary'] != dietary:
                continue

            # Difficulty filter: map to numeric for comparison
            difficulty_map = {'easy': 1, 'medium': 2, 'hard': 3}
            if max_difficulty:
                recipe_diff = difficulty_map.get(recipe['difficulty'], 2)
                filter_diff = difficulty_map.get(max_difficulty, 3)
                if recipe_diff > filter_diff:
                    continue

            # Time filter: skip if recipe takes too long
            if recipe['cook_time'] > int(max_time):
                continue

            filtered.append(recipe)

    # ── Step 2: Score ──────────────────────────────────────
        # For each filtered recipe, calculate how well user's
        # ingredients match what the recipe needs.
        #
        # Score formula:
        #   match_score = matched_count / total_recipe_ingredients
        #
        # This gives a value between 0.0 and 1.0.
        # A score of 1.0 means the user has ALL ingredients.
        # We also track which ingredients are missing.
        scored = []
        for recipe in filtered:
            recipe_ingredients = [ing.lower() for ing in recipe['ingredients']]
            total = len(recipe_ingredients)

            # Count how many of user's ingredients appear in this recipe.
            # We use substring matching so "tomato" matches "tomatoes" etc.
            matched = 0
            missing = []
            for r_ing in recipe_ingredients:
                found = False
                for u_ing in user_ingredients:
                    # Check if user ingredient is part of recipe ingredient
                    # e.g., "chicken" matches "chicken breast"
                    if u_ing in r_ing or r_ing in u_ing:
                        found = True
                        break
                if found:
                    matched += 1
                else:
                    missing.append(r_ing)

            # Calculate score as a percentage
            score = round((matched / total) * 100, 1) if total > 0 else 0

            # Only include recipes where at least one ingredient matched
            if matched > 0:
                recipe['match_score'] = score
                recipe['matched_count'] = matched
                recipe['total_ingredients'] = total
                recipe['missing_ingredients'] = missing
                scored.append(recipe)
        
        
        # ── Step 3: Rank and Return ────────────────────────────
        # Sort by score (highest first) and return top 5
        scored.sort(key=lambda x: x['match_score'], reverse=True)
        top_results = scored[:5]

        # Adjust servings if requested
        if servings and servings > 0:
            for recipe in top_results:
                ratio = servings / recipe['servings']
                # Scale nutrition values
                for key in recipe['nutrition']:
                    recipe['nutrition'][key] = round(recipe['nutrition'][key] * ratio, 1)
                recipe['servings'] = servings
                recipe['serving_ratio'] = ratio  # Frontend uses this to show adjusted amounts

        return jsonify({
            'results': top_results,
            'total_filtered': len(filtered),
            'total_scored': len(scored)
        })
        
    except Exception as e:
        print(f"Error in search_recipes: {str(e)}")
        return jsonify({'error': 'Failed to search recipes', 'details': str(e)}), 500


@app.route('/api/rate', methods=['POST'])
def rate_recipe():
    """
    Save a user's rating for a recipe.
    Updates the average rating using a simple running average.
    """
    data = request.get_json()
    recipe_id = data.get('recipe_id')
    rating = data.get('rating')

    if not recipe_id or not rating:
        return jsonify({'error': 'Missing recipe_id or rating'}), 400

    if not (1 <= int(rating) <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    db = get_db()

    # Get current rating info
    recipe = db.execute(
        'SELECT rating, rating_count FROM recipes WHERE id = ?',
        (recipe_id,)
    ).fetchone()

    if not recipe:
        db.close()
        return jsonify({'error': 'Recipe not found'}), 404

    # Calculate new average rating
    # Formula: new_avg = (old_avg * count + new_rating) / (count + 1)
    old_avg = recipe['rating']
    old_count = recipe['rating_count']
    new_count = old_count + 1
    new_avg = round((old_avg * old_count + int(rating)) / new_count, 1)

    db.execute(
        'UPDATE recipes SET rating = ?, rating_count = ? WHERE id = ?',
        (new_avg, new_count, recipe_id)
    )
    db.commit()
    db.close()

    return jsonify({'new_rating': new_avg, 'rating_count': new_count})


@app.route('/api/substitutions/<int:recipe_id>', methods=['GET'])
def get_substitutions(recipe_id):
    """
    Return ingredient substitutions for a specific recipe.
    Useful when a user is missing some ingredients.
    """
    db = get_db()
    recipe = db.execute(
        'SELECT substitutions FROM recipes WHERE id = ?',
        (recipe_id,)
    ).fetchone()
    db.close()

    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    subs = json.loads(recipe['substitutions'])
    return jsonify(subs)


# ── Error Handlers ─────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors - serve main app for client-side routing."""
    return render_template('index.html')


@app.errorhandler(500)
def server_error(e):
    """Handle server errors gracefully."""
    return jsonify({'error': 'Something went wrong on our end. Please try again.'}), 500


# ── Catch-all Route for Client-Side Routing ───────────────
@app.route('/<path:path>')
def catch_all(path):
    """Serve static files or main app for client-side routing."""
    # Try to serve as static file first
    if '.' in path:
        try:
            return send_from_directory(app.static_folder, path)
        except:
            pass
    # Fall back to main app
    return render_template('index.html')


# ── Entry Point ────────────────────────────────────────────
if __name__ == '__main__':
    # Initialize database before starting the app
    init_db()
    # Use environment variables for production
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = app.config['DEBUG']
    app.run(host=host, port=port, debug=debug)
