# Flask-Dash App with User Authentication

This is a web application built using Flask and Dash frameworks. The app allows users to access a Dash table displaying data from the 'data.csv' file. User authentication is implemented, so users need to sign in or sign up with a username and password to access the data.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the app using `python app.py`.
4. Access the app through your web browser.
5. If you are not logged in, you will be redirected to the login page.
6. Sign in or sign up with a username and password to access the Dash table.
7. Use the filter input to refine the table based on Sub-Industry.
8. To log out, navigate to the logout page.

## Requirements

- Python 3.x
- Flask
- Dash
- pandas
- dash_table
- dash_bootstrap_components
- flask_login
- secrets

## File Structure

- `app.py`: The main Python script containing the Flask-Dash app and routes.
- `data.csv`: Sample Excel file containing the data for the Dash table.
- `login.html` and `signup.html`: HTML templates for the login and signup pages.
- `base.html`: Base HTML template containing the layout for the app.

## Author

Created by Adem Ben Abdallah for Nyx Data.

## Contact

For any inquiries or feedback, please email us at adembenabdallah.contact@gmail.com.
