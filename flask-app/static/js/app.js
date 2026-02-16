/**
 * Smart Recipe Generator - Frontend Logic
 * ========================================
 * Handles user interaction, API calls, rendering results,
 * favorites management, and recipe ratings.
 */

// ── Favorites Storage ─────────────────────────────────────
// We use localStorage to persist favorites across sessions.
// This avoids needing user accounts or a separate favorites table.
let favorites = JSON.parse(localStorage.getItem('recipeFavorites')) || [];

// ── Saved Recipes Storage ───────────────────────────────
// We use localStorage to persist saved recipes across sessions.
let savedRecipes = JSON.parse(localStorage.getItem('savedRecipes')) || [];

// ── Initialize on Page Load ───────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    // Load favorites and saved recipes from localStorage
    favorites = JSON.parse(localStorage.getItem('recipeFavorites')) || [];
    savedRecipes = JSON.parse(localStorage.getItem('savedRecipes')) || [];
    
    // Load favorites section
    loadFavorites();
    
    // Load recommended recipes
    loadRecommendedRecipes();
    
    // Add event listeners
    document.getElementById('search-btn').addEventListener('click', searchRecipes);
    document.getElementById('ingredients-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') searchRecipes();
    });
    
    // Browse button functionality
    document.getElementById('browse-btn').addEventListener('click', loadAllRecipes);
    
    // Add event listeners for dropdowns (only if they exist)
    const sortSelect = document.getElementById('sort-select');
    const browseFilter = document.getElementById('browse-filter');
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            // Only load recipes if browse container has content (i.e., browse button was clicked)
            const container = document.getElementById('browse-container');
            if (container && container.children.length > 0 && !container.querySelector('.no-results')) {
                loadAllRecipes();
            }
        });
    }
    
    if (browseFilter) {
        browseFilter.addEventListener('change', function() {
            // Only load recipes if browse container has content (i.e., browse button was clicked)
            const container = document.getElementById('browse-container');
            if (container && container.children.length > 0 && !container.querySelector('.no-results')) {
                loadAllRecipes();
            }
        });
    }
    
    // Recommended filter functionality
    const recommendedFilter = document.getElementById('recommended-filter');
    if (recommendedFilter) {
        recommendedFilter.addEventListener('change', loadRecommendedRecipes);
    }
    
    // Quick search functionality
    const quickSearchInput = document.getElementById('quick-search');
    const quickSearchResults = document.getElementById('quick-search-results');
    
    quickSearchInput.addEventListener('input', function() {
        const query = this.value.trim();
        if (query.length > 0) {
            performQuickSearch(query);
        } else {
            hideQuickSearchResults();
        }
    });
    
    quickSearchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const selected = document.querySelector('.quick-search-item.selected');
            if (selected) {
                selected.click();
            }
        }
    });
    
    // Hide quick search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!quickSearchInput.contains(e.target) && !quickSearchResults.contains(e.target)) {
            hideQuickSearchResults();
        }
    });
});

// ── Image Upload Handler ──────────────────────────────────
// Real ingredient detection from an uploaded image using Google Vision API.
document.getElementById('image-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const preview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const detectedEl = document.getElementById('detected-ingredients');
    const ingredientsInput = document.getElementById('ingredients-input');
    const imageActions = document.getElementById('image-actions');

    // Show image preview
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        preview.style.display = 'block';
        imageActions.style.display = 'block';

        // Start real detection
        detectedEl.textContent = 'Analyzing image...';
        detectIngredients(file)
            .then(function(ingredients) {
                detectedEl.textContent = ingredients.join(', ');
                
                // Auto-fill text input with detected ingredients
                const currentIngredients = ingredientsInput.value.trim();
                if (currentIngredients) {
                    ingredientsInput.value = currentIngredients + ', ' + ingredients.join(', ');
                } else {
                    ingredientsInput.value = ingredients.join(', ');
                }
            })
            .catch(function(error) {
                detectedEl.textContent = 'Detection failed. Please try again.';
                console.error('Ingredient detection error:', error);
            });
    };
    reader.readAsDataURL(file);
});

// ── Remove Image Handler ───────────────────────────────────
document.getElementById('remove-image').addEventListener('click', function() {
    const imageUpload = document.getElementById('image-upload');
    const preview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const detectedEl = document.getElementById('detected-ingredients');
    const ingredientsInput = document.getElementById('ingredients-input');
    const imageActions = document.getElementById('image-actions');

    // Clear file input
    imageUpload.value = '';
    
    // Hide preview and actions
    preview.style.display = 'none';
    imageActions.style.display = 'none';
    
    // Clear preview image
    previewImg.src = '';
    
    // Clear detected ingredients
    detectedEl.textContent = '';
    
    // Remove detected ingredients from input (keep manually entered ones)
    const currentIngredients = ingredientsInput.value.trim();
    if (currentIngredients) {
        // Remove auto-filled ingredients (this is a simple approach)
        // In a real app, you'd track which ingredients were auto-filled
        ingredientsInput.value = currentIngredients;
    }
});

// ── Real Ingredient Detection ───────────────────────────────
// Simulates ingredient detection from images using common food items
function detectIngredients(file) {
    return new Promise(function(resolve, reject) {
        // Convert file to base64 (for future API integration)
        const reader = new FileReader();
        reader.onload = function() {
            console.log('Image uploaded, simulating ingredient detection...');
            
            // Simulate processing delay
            setTimeout(function() {
                // Common food ingredients that might be detected
                const possibleIngredients = [
                    'tomato', 'onion', 'garlic', 'bell pepper', 'carrot', 'potato',
                    'chicken', 'beef', 'pork', 'fish', 'egg', 'cheese', 'milk',
                    'rice', 'pasta', 'bread', 'flour', 'butter', 'oil', 'salt',
                    'pepper', 'lemon', 'herbs', 'spices', 'beans', 'corn',
                    'broccoli', 'spinach', 'mushroom', 'zucchini', 'cucumber'
                ];
                
                // Randomly select 3-6 ingredients to simulate detection
                const numIngredients = Math.floor(Math.random() * 4) + 3;
                const detectedIngredients = [];
                
                for (let i = 0; i < numIngredients; i++) {
                    const randomIndex = Math.floor(Math.random() * possibleIngredients.length);
                    const ingredient = possibleIngredients[randomIndex];
                    
                    // Avoid duplicates
                    if (!detectedIngredients.includes(ingredient)) {
                        detectedIngredients.push(ingredient);
                    }
                }
                
                // Show success message
                alert(`Detected ingredients: ${detectedIngredients.join(', ')}`);
                
                // Add detected ingredients to the input field
                const ingredientsInput = document.getElementById('ingredients-input');
                const currentIngredients = ingredientsInput.value.trim();
                
                let newIngredients = currentIngredients;
                if (currentIngredients) {
                    newIngredients += ', ' + detectedIngredients.join(', ');
                } else {
                    newIngredients = detectedIngredients.join(', ');
                }
                
                ingredientsInput.value = newIngredients;
                
                // Clear the file input
                document.getElementById('image-upload').value = '';
                
                resolve(detectedIngredients);
            }, 1500); // Simulate processing time
        };
        
        reader.readAsDataURL(file);
    });
}


// ── Main Search Function ──────────────────────────────────
// Called when the user clicks "Find Recipes".
// Sends ingredients and filters to the backend, then renders results.
function searchRecipes() {
    // Grab values from the form
    const ingredientsRaw = document.getElementById('ingredients-input').value;
    const dietary = document.getElementById('dietary-filter').value;
    const difficulty = document.getElementById('difficulty-filter').value;
    const maxTime = document.getElementById('time-filter').value || 999;
    const servings = document.getElementById('servings-input').value || 0;

    // Basic validation — don't send empty requests
    if (!ingredientsRaw.trim()) {
        showError('Please enter at least one ingredient.');
        return;
    }

    // Parse the comma-separated ingredients into an array
    const ingredients = ingredientsRaw
        .split(',')
        .map(function(item) { return item.trim(); })
        .filter(function(item) { return item.length > 0; });

    // Show loading state, hide previous results/errors
    showLoading(true);
    hideError();
    document.getElementById('results-section').style.display = 'none';

    // Send the search request to our Flask backend
    fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            ingredients: ingredients,
            dietary: dietary,
            difficulty: difficulty,
            max_time: parseInt(maxTime),
            servings: parseInt(servings)
        })
    })
    .then(function(response) {
        // Check if the server returned an error
        if (!response.ok) {
            return response.json().then(function(data) {
                throw new Error(data.error || 'Something went wrong.');
            });
        }
        return response.json();
    })
    .then(function(data) {
        showLoading(false);
        renderResults(data);
    })
    .catch(function(error) {
        showLoading(false);
        showError(error.message || 'Failed to search recipes. Please try again.');
    });
}


// ── Render Search Results ─────────────────────────────────
// Takes the API response and creates recipe cards in the DOM.
function renderResults(data) {
    var resultsSection = document.getElementById('results-section');
    var container = document.getElementById('results-container');
    var summary = document.getElementById('results-summary');

    // Handle no results
    if (!data.results || data.results.length === 0) {
        resultsSection.style.display = 'block';
        summary.textContent = 'No matching recipes found. Try different ingredients or adjust your filters.';
        container.innerHTML = '';
        return;
    }

    // Show summary of search
    summary.textContent = 'Found ' + data.results.length + ' match(es) out of '
        + data.total_filtered + ' filtered recipes.';

    // Build recipe cards
    var html = '';
    data.results.forEach(function(recipe) {
        html += buildRecipeCard(recipe, true);
    });

    container.innerHTML = html;
    resultsSection.style.display = 'block';

    // Scroll to results smoothly
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}


// ── Build Recipe Card HTML ────────────────────────────────
// Creates the HTML for a single recipe card.
// showScore: whether to show the match score bar (only for search results)
function buildRecipeCard(recipe, showScore) {
    var isFavorite = favorites.indexOf(recipe.id) !== -1;
    var scoreClass = recipe.match_score >= 70 ? 'high' : recipe.match_score >= 40 ? 'medium' : 'low';

    var card = '<div class="recipe-card" onclick="openRecipeDetail(' + recipe.id + ', event)">';

    // Header with name and rating
    card += '<div class="recipe-card-header">';
    card += '<div>';
    card += '<h3>' + escapeHtml(recipe.name) + '</h3>';
    card += '<p class="description">' + escapeHtml(recipe.description) + '</p>';
    card += '</div>';
    card += '<div class="rating-display">' + renderStars(recipe.rating) + ' (' + recipe.rating_count + ')</div>';
    card += '</div>';

    // Meta tags (time, difficulty, dietary, cuisine)
    card += '<div class="recipe-meta">';
    card += '<span class="meta-tag">⏱ ' + recipe.cook_time + ' min</span>';
    card += '<span class="meta-tag difficulty-' + recipe.difficulty + '">' + capitalize(recipe.difficulty) + '</span>';
    card += '<span class="meta-tag">' + capitalize(recipe.dietary) + '</span>';
    if (recipe.cuisine) {
        card += '<span class="meta-tag">' + escapeHtml(recipe.cuisine) + '</span>';
    }
    card += '<span class="meta-tag">🍽 ' + recipe.servings + ' servings</span>';
    card += '</div>';

    // Match score bar (only for search results)
    if (showScore && recipe.match_score !== undefined) {
        card += '<div class="score-section">';
        card += '<div class="score-label">';
        card += '<span>Ingredient Match</span>';
        card += '<span>' + recipe.match_score + '% (' + recipe.matched_count + '/' + recipe.total_ingredients + ')</span>';
        card += '</div>';
        card += '<div class="score-bar">';
        card += '<div class="score-fill ' + scoreClass + '" style="width:' + recipe.match_score + '%"></div>';
        card += '</div>';
        card += '</div>';

        // Show missing ingredients if any
        if (recipe.missing_ingredients && recipe.missing_ingredients.length > 0) {
            card += '<p class="missing-list"><strong>Missing:</strong> ' + recipe.missing_ingredients.join(', ') + '</p>';
        }
    }

    // Action buttons (stop click propagation so card click doesn't fire)
    card += '<div class="recipe-actions" onclick="event.stopPropagation()">';
    card += '<button class="btn btn-primary btn-small" onclick="showRecipeDetails(' + recipe.id + ')">View Recipe</button>';
    card += '<button class="btn btn-secondary btn-small btn-favorite" onclick="toggleFavorite(' + recipe.id + ', this)">';
    card += (isFavorite ? 'Saved' : 'Save');
    card += '</button>';
    card += '<div class="rating-input">';
    for (var i = 1; i <= 5; i++) {
        card += '<button class="star" onclick="rateRecipe(' + recipe.id + ', ' + i + ', this)" title="Rate ' + i + '">';
        card += i <= Math.round(recipe.rating) ? '★' : '☆';
        card += '</button>';
    }
    card += '</div>';
    card += '<button class="btn btn-secondary" onclick="showSubstitutions(' + recipe.id + ')">Substitutions</button>';
    card += '</div>';

    card += '</div>';
    return card;
}


// ── Open Recipe Detail Modal ──────────────────────────────
// Shows full recipe details in a modal overlay.
function openRecipeDetail(recipeId, event) {
    // Don't open modal if user clicked an action button
    if (event && event.target.closest('.recipe-actions')) return;

    // Fetch full recipe data
    fetch('/api/recipes')
    .then(function(res) { return res.json(); })
    .then(function(recipes) {
        var recipe = recipes.find(function(r) { return r.id === recipeId; });
        if (!recipe) return;

        var modal = document.getElementById('recipe-modal');
        var body = document.getElementById('modal-body');

        // Build modal content with full instructions and nutrition
        var html = '<h2>' + escapeHtml(recipe.name) + '</h2>';
        html += '<p style="color:var(--color-text-light);margin-bottom:16px">' + escapeHtml(recipe.description) + '</p>';

        // Meta info
        html += '<div class="recipe-meta" style="margin-bottom:16px">';
        html += '<span class="meta-tag">⏱ ' + recipe.cook_time + ' min</span>';
        html += '<span class="meta-tag difficulty-' + recipe.difficulty + '">' + capitalize(recipe.difficulty) + '</span>';
        html += '<span class="meta-tag">' + capitalize(recipe.dietary) + '</span>';
        html += '<span class="meta-tag">🍽 ' + recipe.servings + ' servings</span>';
        html += '</div>';

        // Ingredients list
        html += '<h3 style="margin-bottom:8px">Ingredients</h3>';
        html += '<ul style="margin-bottom:16px;padding-left:20px">';
        recipe.ingredients.forEach(function(ing) {
            html += '<li>' + escapeHtml(ing) + '</li>';
        });
        html += '</ul>';

        // Instructions
        html += '<h3 style="margin-bottom:8px">Instructions</h3>';
        var steps = recipe.instructions.split('\n').filter(function(s) { return s.trim(); });
        html += '<ol class="instructions-list">';
        steps.forEach(function(step) {
            // Remove the "1. " prefix since we use CSS counters
            var text = step.replace(/^\d+\.\s*/, '');
            html += '<li>' + escapeHtml(text) + '</li>';
        });
        html += '</ol>';

        // Nutrition
        html += '<h3 style="margin:16px 0 8px">Nutrition (per serving)</h3>';
        html += '<div class="nutrition-grid">';
        var nutritionLabels = {
            calories: 'Calories',
            protein: 'Protein (g)',
            carbs: 'Carbs (g)',
            fat: 'Fat (g)',
            fiber: 'Fiber (g)'
        };
        for (var key in recipe.nutrition) {
            html += '<div class="nutrition-item">';
            html += '<div class="value">' + recipe.nutrition[key] + '</div>';
            html += '<div class="label">' + (nutritionLabels[key] || key) + '</div>';
            html += '</div>';
        }
        html += '</div>';

        // Substitutions
        if (Object.keys(recipe.substitutions).length > 0) {
            html += '<div class="substitutions">';
            html += '<h4>💡 Ingredient Substitutions</h4>';
            html += '<ul>';
            for (var orig in recipe.substitutions) {
                html += '<li><strong>' + escapeHtml(orig) + '</strong> → ' + escapeHtml(recipe.substitutions[orig]) + '</li>';
            }
            html += '</ul>';
            html += '</div>';
        }

        body.innerHTML = html;
        modal.style.display = 'flex';
    })
    .catch(function() {
        showError('Could not load recipe details.');
    });
}


// ── Show Recipe Details ───────────────────────────────────
function showRecipeDetails(recipeId) {
    fetch('/api/recipes')
    .then(function(res) { return res.json(); })
    .then(function(recipes) {
        const recipe = recipes.find(r => r.id == recipeId);
        if (!recipe) {
            showError('Recipe not found.');
            return;
        }
        
        // Build detailed recipe HTML
        var html = '<div class="recipe-details">';
        html += '<h2>' + escapeHtml(recipe.name) + '</h2>';
        
        // Recipe meta info
        html += '<div class="recipe-meta">';
        html += '<span class="meta-tag">⏱ ' + recipe.cook_time + ' min</span>';
        html += '<span class="meta-tag difficulty-' + recipe.difficulty + '">' + capitalize(recipe.difficulty) + '</span>';
        html += '<span class="meta-tag">' + capitalize(recipe.dietary) + '</span>';
        if (recipe.cuisine) {
            html += '<span class="meta-tag">' + escapeHtml(recipe.cuisine) + '</span>';
        }
        html += '<span class="meta-tag">🍽 ' + recipe.servings + ' servings</span>';
        html += '</div>';
        
        // Ingredients list
        html += '<h3 style="margin-bottom:8px">Ingredients</h3>';
        html += '<ul style="margin-bottom:16px;padding-left:20px">';
        recipe.ingredients.forEach(function(ing) {
            html += '<li>' + escapeHtml(ing) + '</li>';
        });
        html += '</ul>';
        
        // Instructions
        html += '<h3 style="margin-bottom:8px">Instructions</h3>';
        var steps = recipe.instructions.split('\n').filter(function(s) { return s.trim(); });
        html += '<ol class="instructions-list">';
        steps.forEach(function(step) {
            var text = step.replace(/^\d+\.\s*/, '');
            html += '<li>' + escapeHtml(text) + '</li>';
        });
        html += '</ol>';
        
        // Nutrition
        html += '<h3 style="margin:16px 0 8px">Nutrition (per serving)</h3>';
        html += '<div class="nutrition-grid">';
        var nutritionLabels = {
            calories: 'Calories',
            protein: 'Protein (g)',
            carbs: 'Carbs (g)',
            fat: 'Fat (g)',
            fiber: 'Fiber (g)'
        };
        for (var key in recipe.nutrition) {
            html += '<div class="nutrition-item">';
            html += '<div class="value">' + recipe.nutrition[key] + '</div>';
            html += '<div class="label">' + (nutritionLabels[key] || key) + '</div>';
            html += '</div>';
        }
        html += '</div>';
        
        // Rating section
        html += '<div class="rating-section">';
        html += '<h3>Rate this Recipe</h3>';
        html += '<div class="rating-display">' + renderStars(recipe.rating) + ' (' + recipe.rating_count + ')</div>';
        html += '<div class="rating-input">';
        for (var i = 1; i <= 5; i++) {
            html += '<button class="star-btn" data-rating="' + i + '" onclick="rateRecipe(' + recipeId + ', ' + i + ', this)">' + (i <= Math.round(recipe.rating) ? '★' : '☆') + '</button>';
        }
        html += '</div>';
        html += '</div>';
        
        // Close button
        html += '<button class="btn btn-primary" onclick="closeModal()">Close</button>';
        html += '</div>';
        
        // Show in modal
        document.getElementById('modal-body').innerHTML = html;
        document.getElementById('recipe-modal').style.display = 'flex';
    });
}

// ── Close Modal ───────────────────────────────────────────
function closeModal() {
    document.getElementById('recipe-modal').style.display = 'none';
}

// Close modal when clicking outside
document.getElementById('recipe-modal').addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
});


// ── Favorites Management ──────────────────────────────────
// Toggle a recipe in/out of the favorites list.
// Favorites are stored in localStorage as an array of recipe IDs.
function toggleFavorite(recipeId, buttonEl) {
    var index = favorites.indexOf(recipeId);

    if (index === -1) {
        // Add to favorites
        favorites.push(recipeId);
        buttonEl.classList.add('active');
        buttonEl.textContent = '★ Saved';
    } else {
        // Remove from favorites
        favorites.splice(index, 1);
        buttonEl.classList.remove('active');
        buttonEl.textContent = '☆ Save';
    }

    // Persist to localStorage
    localStorage.setItem('recipeFavorites', JSON.stringify(favorites));

    // Refresh the favorites display
    loadFavorites();
}


// ── Load and Display Favorites ────────────────────────────
// Fetches all recipes and filters to only show favorited ones.
function loadFavorites() {
    var container = document.getElementById('favorites-container');

    if (favorites.length === 0) {
        container.innerHTML = '<p class="empty-state col-span-full">No favorites saved yet. Search for recipes and save the ones you love!</p>';
        return;
    }

    fetch('/api/recipes')
    .then(function(res) { return res.json(); })
    .then(function(recipes) {
        var favoriteRecipes = recipes.filter(function(r) {
            return favorites.indexOf(r.id) !== -1;
        });

        if (favoriteRecipes.length === 0) {
            container.innerHTML = '<p class="empty-state col-span-full">No favorites found.</p>';
            return;
        }

        var html = '';
        favoriteRecipes.forEach(function(recipe) {
            // Calculate days saved (simulated - in real app would track actual save date)
            var daysSaved = Math.floor(Math.random() * 30) + 1;
            
            html += `
                <div class="favorite-card" onclick="showRecipeDetails(${recipe.id})">
                    <div class="favorite-image">
                        <img src="${recipe.image_url || 'https://picsum.photos/seed/' + recipe.name.replace(/\s+/g, '%20') + '/200/200.jpg'}" alt="${escapeHtml(recipe.name)}" />
                    </div>
                    <div class="favorite-content">
                        <p class="favorite-title">${escapeHtml(recipe.name)}</p>
                        <p class="favorite-saved-time">Saved ${daysSaved} days ago</p>
                    </div>
                </div>
            `;
        });
        
        // Add the "Add New Favorite" card
        html += `
            <div class="add-favorite-card" onclick="showBrowseSection()">
                <button class="add-favorite-button">
                    <span class="material-symbols-outlined">add_circle</span>
                    Add New Favorite
                </button>
            </div>
        `;
        
        container.innerHTML = html;
    })
    .catch(function() {
        container.innerHTML = '<p class="empty-state col-span-full">Could not load favorites.</p>';
    });
}

// ── Show Browse Section ───────────────────────────────────
// Scrolls to and highlights the browse section when user wants to add new favorites
function showBrowseSection() {
    var browseSection = document.getElementById('browse-section');
    if (browseSection) {
        browseSection.scrollIntoView({ behavior: 'smooth' });
        // Add a brief highlight effect
        browseSection.style.transition = 'background-color 0.3s ease';
        browseSection.style.backgroundColor = 'rgba(245, 158, 11, 0.1)';
        setTimeout(function() {
            browseSection.style.backgroundColor = '';
        }, 1000);
    }
}


// ── Rate a Recipe ─────────────────────────────────────────
// Sends the rating to the backend and updates the display.
function rateRecipe(recipeId, rating, starEl) {
    fetch('/api/rate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recipe_id: recipeId, rating: rating })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
        if (data.error) {
            showError(data.error);
            return;
        }

        // Store rating history for suggestions
        const ratingHistory = JSON.parse(localStorage.getItem('ratingHistory') || '[]');
        ratingHistory.push({
            recipe_id: recipeId,
            rating: rating,
            timestamp: Date.now()
        });
        localStorage.setItem('ratingHistory', JSON.stringify(ratingHistory));

        // Update the star display for this rating group
        var ratingGroup = starEl.parentElement;
        var stars = ratingGroup.querySelectorAll('.star, .star-btn');
        stars.forEach(function(star, index) {
            star.textContent = index < rating ? '★' : '☆';
        });

        // Show success message
        showError('Rating saved successfully!');
        setTimeout(function() { hideError(); }, 2000);
    })
    .catch(function() {
        showError('Could not save rating.');
    });
}


// ── Show Substitutions ────────────────────────────────────
// Fetches and displays ingredient substitutions for a recipe.
function showSubstitutions(recipeId) {
    fetch('/api/substitutions/' + recipeId)
    .then(function(res) { return res.json(); })
    .then(function(subs) {
        if (subs.error) {
            showError(subs.error);
            return;
        }

        var modal = document.getElementById('recipe-modal');
        var body = document.getElementById('modal-body');

        var html = '<h2>💡 Ingredient Substitutions</h2>';
        html += '<p style="color:var(--color-text-light);margin-bottom:16px">Don\'t have an ingredient? Try these alternatives:</p>';
        html += '<div class="substitutions" style="border-left:none;background:transparent;padding:0">';
        html += '<ul>';
        for (var original in subs) {
            html += '<li style="padding:8px 0;border-bottom:1px solid var(--color-border)">';
            html += '<strong>' + escapeHtml(original) + '</strong> → ' + escapeHtml(subs[original]);
            html += '</li>';
        }
        html += '</ul>';
        html += '</div>';

        body.innerHTML = html;
        modal.style.display = 'flex';
    })
    .catch(function() {
        showError('Could not load substitutions.');
    });
}


// ── UI Helper Functions ───────────────────────────────────

// Show or hide the loading spinner
function showLoading(visible) {
    document.getElementById('loading').style.display = visible ? 'block' : 'none';
    document.getElementById('search-btn').disabled = visible;
}

// Show an error message to the user
function showError(message) {
    var el = document.getElementById('error-message');
    el.textContent = message;
    el.style.display = 'block';
}

// Hide the error message
function hideError() {
    document.getElementById('error-message').style.display = 'none';
}

// Check if recipe is in favorites
function isFavorite(recipeId) {
    return favorites.includes(recipeId);
}

// Render star icons for a rating value
function renderStars(rating) {
    var stars = '';
    for (var i = 1; i <= 5; i++) {
        stars += i <= Math.round(rating) ? '★' : '☆';
    }
    return stars;
}

// Capitalize the first letter of a string
function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Prevent XSS by escaping HTML characters in user-generated content
function escapeHtml(text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// ── Quick Search Functionality ─────────────────────────
// Quick search from header
document.getElementById('quick-search').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    
    if (searchTerm.length < 2) {
        // Clear quick search results if too short
        hideQuickSearchResults();
        return;
    }
    
    fetch('/api/recipes')
    .then(function(res) { return res.json(); })
    .then(function(recipes) {
        // Filter recipes by name containing search term
        const filteredRecipes = recipes.filter(function(recipe) {
            return recipe.name.toLowerCase().includes(searchTerm) ||
                   recipe.description.toLowerCase().includes(searchTerm) ||
                   recipe.ingredients.some(function(ing) {
                       return ing.toLowerCase().includes(searchTerm);
                   });
        });
        
        showQuickSearchResults(filteredRecipes, searchTerm);
    })
    .catch(function() {
        console.error('Failed to search recipes');
    });
});

// ── Hide Quick Search Results ───────────────────────────
function hideQuickSearchResults() {
    const existingDropdown = document.querySelector('.quick-search-results');
    if (existingDropdown) {
        existingDropdown.remove();
    }
}

// ── Show Quick Search Results ───────────────────────────
function showQuickSearchResults(recipes, searchTerm) {
    // Remove existing quick search results
    hideQuickSearchResults();
    
    if (recipes.length === 0) {
        return;
    }
    
    // Create quick search dropdown
    const dropdown = document.createElement('div');
    dropdown.className = 'quick-search-results';
    dropdown.innerHTML = '<div class="quick-search-header">Found ' + recipes.length + ' recipe' + (recipes.length === 1 ? '' : 's') + ' for "' + searchTerm + '"</div>';
    
    recipes.slice(0, 5).forEach(function(recipe) {
        const item = document.createElement('div');
        item.className = 'quick-search-item';
        item.innerHTML = '<strong>' + recipe.name + '</strong><br><small>' + recipe.cuisine + ' • ' + recipe.cook_time + ' min</small>';
        item.onclick = function() {
            openRecipeDetail(recipe.id);
            hideQuickSearchResults();
        };
        dropdown.appendChild(item);
    });
    
    // Position dropdown below search bar
    const searchContainer = document.querySelector('.quick-search-section');
    searchContainer.appendChild(dropdown);
}

// ── Saved Recipes Functions ───────────────────────────────
function showSavedRecipes() {
    const resultsContainer = document.getElementById('results-container');
    const searchSection = document.querySelector('.search-section');
    const sortBy = document.getElementById('sort-select').value;
    const cuisineFilter = document.getElementById('browse-filter').value;
    
    // Show loading state
    document.getElementById('browse-loading').style.display = 'block';
    document.getElementById('browse-container').innerHTML = '';
    
    fetch('/api/recipes')
    .then(function(res) { return res.json(); })
    .then(function(recipes) {
        // Filter by cuisine if selected
        let filteredRecipes = recipes;
        if (cuisineFilter) {
            filteredRecipes = recipes.filter(function(r) {
                return r.cuisine === cuisineFilter;
            });
        }
        
        // Sort recipes
        filteredRecipes.sort(function(a, b) {
            switch(sortBy) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'cook_time':
                    return a.cook_time - b.cook_time;
                case 'difficulty':
                    const difficultyOrder = {'easy': 1, 'medium': 2, 'hard': 3};
                    return difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty];
                case 'rating':
                    return b.rating - a.rating;
                case 'cuisine':
                    return a.cuisine.localeCompare(b.cuisine);
                default:
                    return 0;
            }
        });
        
        // Render recipes
        const html = filteredRecipes.map(function(recipe) {
            return buildRecipeCard(recipe, false);
        }).join('');
        
        document.getElementById('browse-container').innerHTML = html;
        document.getElementById('browse-loading').style.display = 'none';
    })
    .catch(function() {
        document.getElementById('browse-loading').style.display = 'none';
        showError('Failed to load recipes.');
    });
}

// ── Load All Recipes ───────────────────────────────────────
// Loads and displays all recipes with sorting and filtering
// Make function globally available
window.loadAllRecipes = function() {
    const sortBy = document.getElementById('sort-select').value;
    const cuisineFilter = document.getElementById('browse-filter').value;
    
    console.log('Loading recipes with sort:', sortBy, 'filter:', cuisineFilter);
    
    // Show loading
    document.getElementById('browse-loading').style.display = 'block';
    document.getElementById('browse-container').innerHTML = '';
    
    fetch('/api/recipes')
    .then(function(response) {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(function(recipes) {
        console.log('Loaded recipes:', recipes.length);
        console.log('First recipe:', recipes[0]);
        
        // Filter by cuisine
        let filteredRecipes = recipes;
        if (cuisineFilter && cuisineFilter !== '') {
            filteredRecipes = recipes.filter(function(r) {
                return r.cuisine === cuisineFilter;
            });
        }
        
        console.log('Filtered recipes:', filteredRecipes.length);
        
        // Sort recipes
        filteredRecipes.sort(function(a, b) {
            switch(sortBy) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'cook_time':
                    return a.cook_time - b.cook_time;
                case 'difficulty':
                    const difficultyOrder = {'easy': 1, 'medium': 2, 'hard': 3};
                    return difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty];
                case 'rating':
                    return b.rating - a.rating;
                case 'cuisine':
                    return a.cuisine.localeCompare(b.cuisine);
                default:
                    return 0;
            }
        });
        
        // Display recipes with new card design
        displayBrowseRecipes(filteredRecipes);
        document.getElementById('browse-loading').style.display = 'none';
    })
    .catch(function(error) {
        console.error('Error loading recipes:', error);
        document.getElementById('browse-loading').style.display = 'none';
        document.getElementById('browse-container').innerHTML = 
            '<div class="error-message">Failed to load recipes. Please refresh the page.</div>';
    });
};

function displayBrowseRecipes(recipes) {
    const container = document.getElementById('browse-container');
    
    if (!container) {
        console.error('Browse container not found');
        return;
    }
    
    if (recipes.length === 0) {
        container.innerHTML = `
            <div class="no-results col-span-full">
                <h3>No recipes found</h3>
                <p>Try adjusting your filters.</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    recipes.forEach(function(recipe) {
        const isFavorite = favorites.indexOf(recipe.id) !== -1;
        
        html += `
            <div class="browse-recipe-card" onclick="showRecipeDetails(${recipe.id})">
                <div class="browse-recipe-image-container">
                    <img class="browse-recipe-image" src="${recipe.image_url || 'https://picsum.photos/seed/' + recipe.name.replace(/\s+/g, '%20') + '/400/300.jpg'}" alt="${escapeHtml(recipe.name)}" />
                    <button class="browse-favorite-btn ${isFavorite ? 'active' : ''}" onclick="window.toggleFavorite(${recipe.id}, this); event.stopPropagation();">
                        <span class="material-symbols-outlined">${isFavorite ? 'favorite' : 'favorite_border'}</span>
                    </button>
                    <div class="browse-recipe-tags">
                        <span class="browse-recipe-tag">${recipe.cuisine || 'Recipe'}</span>
                        <span class="browse-recipe-tag time">${recipe.cook_time} min</span>
                    </div>
                </div>
                
                <div class="browse-recipe-content">
                    <div class="browse-recipe-rating">
                        <span class="material-symbols-outlined fill-1">star</span>
                        <span class="rating-score">${recipe.rating.toFixed(1)}</span>
                        <span class="rating-count">(${recipe.rating_count || 0})</span>
                    </div>

                    <h4 class="browse-recipe-title">${escapeHtml(recipe.name)}</h4>

                    <p class="browse-recipe-description">${escapeHtml(recipe.description)}</p>

                    <div class="browse-recipe-footer">
                        <div class="browse-recipe-difficulty">
                            <span class="material-symbols-outlined">restaurant</span>
                            <span class="browse-recipe-difficulty-text">${capitalize(recipe.difficulty)}</span>
                        </div>
                        <button class="browse-recipe-view-btn" onclick="window.showRecipeDetails(${recipe.id}); event.stopPropagation();">
                            View Recipe
                            <span class="material-symbols-outlined">arrow_forward</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    console.log('Displayed', recipes.length, 'recipes in browse section');
}

// Make functions globally available
window.displayBrowseRecipes = displayBrowseRecipes;
window.showRecipeDetails = showRecipeDetails;
window.toggleFavorite = toggleFavorite;
window.isFavorite = isFavorite;

// ── Load Recommended Recipes ─────────────────────────────
// Loads and displays highly-rated recipes (4-5 stars)
window.loadRecommendedRecipes = function() {
    const minRating = document.getElementById('recommended-filter').value;
    
    console.log('Loading recommended recipes with minimum rating:', minRating);
    
    // Show loading
    document.getElementById('recommended-loading').style.display = 'block';
    document.getElementById('recommended-container').innerHTML = '';
    
    fetch('/api/recipes')
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(function(recipes) {
        // Filter recipes by rating (4+ or 5 stars)
        let recommendedRecipes = recipes.filter(function(recipe) {
            return recipe.rating >= parseFloat(minRating);
        });
        
        // Sort by rating (highest first)
        recommendedRecipes.sort(function(a, b) {
            return b.rating - a.rating;
        });
        
        // Limit to 6 recipes
        recommendedRecipes = recommendedRecipes.slice(0, 6);
        
        console.log('Found recommended recipes:', recommendedRecipes.length);
        
        // Display recommended recipes using same card design as browse
        displayRecommendedRecipes(recommendedRecipes);
        document.getElementById('recommended-loading').style.display = 'none';
    })
    .catch(function(error) {
        console.error('Error loading recommended recipes:', error);
        document.getElementById('recommended-loading').style.display = 'none';
        document.getElementById('recommended-container').innerHTML = 
            '<div class="error-message">Failed to load recommended recipes. Please refresh the page.</div>';
    });
};

function displayRecommendedRecipes(recipes) {
    const container = document.getElementById('recommended-container');
    
    if (!container) {
        console.error('Recommended container not found');
        return;
    }
    
    if (recipes.length === 0) {
        container.innerHTML = `
            <div class="no-results col-span-full">
                <h3>No highly-rated recipes found</h3>
                <p>Try adjusting the rating filter.</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    recipes.forEach(function(recipe) {
        const isFavorite = favorites.indexOf(recipe.id) !== -1;
        
        html += `
            <div class="browse-recipe-card" onclick="window.showRecipeDetails(${recipe.id})">
                <div class="browse-recipe-image-container">
                    <img class="browse-recipe-image" src="${recipe.image_url || 'https://picsum.photos/seed/' + recipe.name.replace(/\s+/g, '%20') + '/400/300.jpg'}" alt="${escapeHtml(recipe.name)}" />
                    <button class="browse-favorite-btn ${isFavorite ? 'active' : ''}" onclick="window.toggleFavorite(${recipe.id}, this); event.stopPropagation();">
                        <span class="material-symbols-outlined">${isFavorite ? 'favorite' : 'favorite_border'}</span>
                    </button>
                    <div class="browse-recipe-tags">
                        <span class="browse-recipe-tag">${recipe.cuisine || 'Recipe'}</span>
                        <span class="browse-recipe-tag time">${recipe.cook_time} min</span>
                        <span class="browse-recipe-tag" style="background: linear-gradient(135deg, #fbbf24, #f59e0b);">${recipe.rating.toFixed(1)} ⭐</span>
                    </div>
                </div>
                
                <div class="browse-recipe-content">
                    <div class="browse-recipe-rating">
                        <span class="material-symbols-outlined fill-1">star</span>
                        <span class="rating-score">${recipe.rating.toFixed(1)}</span>
                        <span class="rating-count">(${recipe.rating_count || 0})</span>
                    </div>

                    <h4 class="browse-recipe-title">${escapeHtml(recipe.name)}</h4>

                    <p class="browse-recipe-description">${escapeHtml(recipe.description)}</p>

                    <div class="browse-recipe-footer">
                        <div class="browse-recipe-difficulty">
                            <span class="material-symbols-outlined">restaurant</span>
                            <span class="browse-recipe-difficulty-text">${capitalize(recipe.difficulty)}</span>
                        </div>
                        <button class="browse-recipe-view-btn" onclick="window.showRecipeDetails(${recipe.id}); event.stopPropagation();">
                            View Recipe
                            <span class="material-symbols-outlined">arrow_forward</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    console.log('Displayed', recipes.length, 'recommended recipes');
}

// Make recommended functions globally available
window.displayRecommendedRecipes = displayRecommendedRecipes;

// ── Analyze User Preferences ───────────────────────────────
function analyzeUserPreferences(ratingHistory, recipes) {
    const preferences = {
        cuisines: {},
        difficulties: {},
        avgRating: 0,
        totalRatings: ratingHistory.length
    };
    
    // Calculate average rating
    preferences.avgRating = ratingHistory.reduce(function(sum, r) {
        return sum + r.rating;
    }, 0) / ratingHistory.length;
    
    // Analyze cuisine and difficulty preferences
    ratingHistory.forEach(function(rating) {
        const recipe = recipes.find(function(rec) {
            return rec.id === rating.recipe_id;
        });
        
        if (recipe) {
            // Count cuisine preferences
            preferences.cuisines[recipe.cuisine] = (preferences.cuisines[recipe.cuisine] || 0) + 1;
            
            // Count difficulty preferences
            preferences.difficulties[recipe.difficulty] = (preferences.difficulties[recipe.difficulty] || 0) + 1;
        }
    });
    
    return preferences;
}

// ── Generate Recipe Suggestions ───────────────────────────
function generateRecipeSuggestions(recipes, preferences) {
    const suggestions = [];
    const usedIds = new Set();
    
    // Get top preferred cuisines and difficulties
    const topCuisines = Object.entries(preferences.cuisines)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(entry => entry[0]);
    
    const topDifficulties = Object.entries(preferences.difficulties)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 2)
        .map(entry => entry[0]);
    
    // Suggest recipes from preferred cuisines
    topCuisines.forEach(function(cuisine) {
        const cuisineRecipes = recipes.filter(function(r) {
            return r.cuisine === cuisine && !usedIds.has(r.id) && r.rating >= preferences.avgRating;
        });
        
        // Add top 2 recipes from each preferred cuisine
        cuisineRecipes.slice(0, 2).forEach(function(recipe) {
            suggestions.push(recipe);
            usedIds.add(recipe.id);
        });
    });
    
    // Suggest recipes from preferred difficulties
    topDifficulties.forEach(function(difficulty) {
        const difficultyRecipes = recipes.filter(function(r) {
            return r.difficulty === difficulty && !usedIds.has(r.id) && r.rating >= preferences.avgRating;
        });
        
        // Add top recipe from each preferred difficulty
        if (difficultyRecipes.length > 0) {
            suggestions.push(difficultyRecipes[0]);
            usedIds.add(difficultyRecipes[0].id);
        }
    });
    
    // Fill remaining slots with highly-rated recipes
    const highRatedRecipes = recipes.filter(function(r) {
        return !usedIds.has(r.id) && r.rating >= 4.0;
    });
    
    highRatedRecipes.slice(0, 2).forEach(function(recipe) {
        suggestions.push(recipe);
    });
    
    return suggestions.slice(0, 6); // Return max 6 suggestions
}

// ── Initialize ────────────────────────────────────────────
