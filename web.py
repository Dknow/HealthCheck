from Views.view import app

if __name__ == '__main__':
    # app.debug = True
    app.run(threaded=True, debug=True, port=8000, host='0.0.0.0')