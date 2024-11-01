# Advanced Recommendation System

## Overview

This project implements an advanced recommendation system for an e-commerce platform. The system recommends products to users based on their browsing and purchase history, the browsing/purchase history of similar users, and contextual signals such as time of day, seasonality, and user device type.

The recommendation system is designed to handle a large product catalog with multiple categories, ensuring scalability, relevance, and diversity in recommendations.

## Features

- **Hybrid Recommendation Approach:**
  - **Content-Based Filtering:** Recommends products similar to those a user has interacted with, using product metadata.
  - **Collaborative Filtering:** Identifies similar users based on interaction history and recommends products they've engaged with.
  - **Clustering:** Groups users and products to improve recommendation efficiency.
  - **Matrix Factorization:** Uses latent factors to predict user-product affinity scores.
- **Context-Aware Recommendations:** Adjusts suggestions based on contextual signals like time of day, day of the week, seasonality, and device type.
- **Cold Start Handling:** Provides recommendations for new users and new products with limited interaction history.
- **Diversity Assurance:** Ensures recommendations cover a range of product categories to expose users to new items.
- **Performance Optimization:**
  - **Caching with Redis:** Speeds up recommendation retrieval for active users.
  - **Parallel Processing:** Utilizes multiple cores for computations to handle large datasets.
  - **Pre-computation:** Computes similarities and clusters offline to reduce online load.
- **Model Explainability:** Offers insights into why each product was recommended (e.g., "Recommended because users similar to you purchased this").


## Setup Instructions

1. **Clone the Repository**

   ```sh
   git clone https://github.com/ghazalbn/recommendation_system.git
   cd recommendation_system
   ```

2. **Create a Virtual Environment and Install Dependencies**

```sh
python -m venv venv
```

Activate the virtual environment:

On Windows:

```sh
venv\Scripts\activate
```

On macOS/Linux:

```sh
source venv/bin/activate
```

Install required packages:

```sh
pip install -r requirements.txt
```

3. **Install and Start Redis**

### Install Redis:

- **macOS:**  
  ```bash
  brew install redis
  ```
- **Ubuntu:**  
  ```bash
  sudo apt-get install redis-server
  ```
- **Windows:**  
  Download from [Redis for Windows](https://github.com/microsoftarchive/redis/releases)


Start Redis Server:

```sh
redis-server
```

4. **Run the Application**

```sh
python main.py
```

5. **Run Tests**

```sh
python -m unittest discover tests
```



## Algorithm Components

### Content-Based Filtering

- Utilizes product metadata (tags, categories, descriptions) to recommend products similar to those a user has interacted with.
- Handles new products by using their metadata, allowing them to be recommended without prior interaction data.

### Collaborative Filtering

- **User-Based Collaborative Filtering:** Finds users similar to the target user based on interaction history and recommends products they've engaged with.
- Computes user similarity using interaction weights for events like views, clicks, add-to-cart actions, and purchases.

### Clustering

- **User Clustering:** Groups users into clusters based on interaction patterns to enhance recommendation scalability.
- **Product Clustering:** Groups products into clusters based on features to improve recommendation diversity.

### Matrix Factorization

- Uses latent factors to model user-product interactions.
- Implements Singular Value Decomposition (SVD) to predict user preferences for products.

### Context-Aware Recommendations

- Adjusts recommendations based on contextual signals:
  - **Time of Day and Day of Week:** Recommends products popular during specific times or days.
  - **Seasonality:** Incorporates seasonal trends into recommendations.
  - **Device Type:** Personalizes recommendations based on whether the user is on mobile or desktop.

### Diversity Assurance

- Ensures recommended products cover a range of categories.
- Implements a diversity metric to avoid recommendation monotony.

### Cold Start Handling

- **New Users:** Recommends popular products adjusted for context.
- **New Products:** Includes them in content-based recommendations using metadata.

### Performance Optimization

- **Caching:** Uses Redis to cache recommendations and reduce computation time.
- **Parallel Processing:** Employs joblib for parallel computations to handle large datasets efficiently.
- **Pre-computation:** Calculates similarity matrices and clusters offline.

### Model Explainability

- Provides reasons for recommendations, such as:
  - "Recommended because users similar to you purchased this."
  - "Because you showed interest in fitness products."


## Code Structure

### `data/`

- **`load_data.py`**: Functions to load user data, product data, browsing history, purchase history, and contextual signals.
- **`preprocess.py`**: Functions to preprocess timestamps, encode product tags, and prepare data for modeling.

### `models/`

- **`content_based.py`**: Implements content-based filtering using product metadata.
- **`collaborative_filtering.py`**: Implements user-based collaborative filtering.
- **`clustering.py`**: Clusters users and products to improve scalability.
- **`context_aware.py`**: Adjusts recommendations based on contextual signals.
- **`hybrid.py`**: Combines all recommendation strategies into a hybrid system.
- **`matrix_factorization.py`**: Implements matrix factorization using SVD.

### `utils/`

- **`caching.py`**: Manages caching of recommendations using Redis.
- **`explainability.py`**: Provides explanations for recommendations.
- **`helpers.py`**: Contains utility functions for assigning interaction weights and other helper methods.

### `tests/`

- **`test_data.py`**: Tests for data loading and preprocessing functions.
- **`test_models.py`**: Tests for individual recommendation models.
- **`test_recommendations.py`**: Integration tests for the recommendation system.

### `main.py`

- Entry point of the application that ties all components together.

### `README.md`

- Provides an overview of the project, setup instructions, and documentation of components.

### `requirements.txt`

- Lists all Python dependencies required to run the project.
