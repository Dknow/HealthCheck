from Views.view import app

if __name__ == '__main__':
    app.run(threaded=True, debug=True, port=8008, host='0.0.0.0')
