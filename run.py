# This is the main entry point to run the application.
from my_app import create_app

def main():
    # Create the Flask app instance using the factory
    app = create_app()
    # Run the development server
    # The host='0.0.0.0' makes it accessible from your network
    app.run(debug=True, host='0.0.0.0', port=5000)


# This block runs only when the script is executed directly.
if __name__ == '__main__':
    main()
