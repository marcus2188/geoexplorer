# MAIN ENTRY POINT OF ENTIRE APP
from dashboard import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # run webserver, start flask app, and debug mode auto-update/save
