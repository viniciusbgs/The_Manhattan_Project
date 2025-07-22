# The Manhattan Project - Real Estate Heatmap and Price Prediction Game

## Overview

This project is a web application built using Flask that visualizes the heatmap of the most expensive properties in Manhattan from 2003 to 2023. Additionally, the application includes a mini-game where users are shown an image of a property and must guess its price.

---

## Features

- **Heatmap Visualization**: Interactive heatmap showing the distribution of the most expensive properties in Manhattan over the years (2003-2023).
- **Price Guessing Game**: A fun mini-game where users are presented with an image of a property and must guess its price. The game includes multiple levels of difficulty.
- **Future Predictions**: Planned integration of a machine learning model to predict future property values based on historical data.

---

## Technologies Used

- **Flask**: A lightweight web framework for Python used to build the web application.
- **Pandas**: Used for data manipulation and preprocessing.
- **NumPy**: Used for numerical computations.
- **Matplotlib & Seaborn**: Libraries used for data visualization and creating the heatmap.
- **Scikit-learn**: Used for data preprocessing and future machine learning model development.

---

## Installation

To run this project locally, follow these steps:

1.  **Clone the repository**:

   ```bash
    git clone https://github.com/viniciusbgs/The_Manhattan_Project.git
    cd The_Manhattan_Project
   ```
2.  **Create a virtual environment**:


   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3.  **Install the required dependencies**:

   ```bash
    pip install -r requirements.txt
   ```

3.  **Run the Flask application**:

   ```bash
    flask run
   ```

5.  **Access the application**:\
    Open your web browser and go to `http://127.0.0.1:5000/`.
    

* * * * *

Data Sources
------------

The data used in this project was obtained from the NYC government. The raw data was cleaned and preprocessed using Pandas to ensure it was suitable for visualization and analysis.

* * * * *

Future Work
-----------

-   **Machine Learning Model**: Develop a predictive model to forecast property prices in Manhattan for the next few years.

-   **Game Enhancements**: Add more levels to the price guessing game and introduce a scoring system to track user performance.

* * * * *

Contributing
------------

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes.


* * * * *

Acknowledgments
---------------

-   NYC Government for providing the real estate data.

-   Flask and Pandas communities for their excellent documentation and support.

* * * * *

Feel free to explore the project and contribute to its development! If you have any questions or suggestions, please open an issue on the GitHub repository.
