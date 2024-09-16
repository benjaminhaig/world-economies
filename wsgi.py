from app import app

app.config['SERVER_NAME'] = 'worldeconomies.info'

if __name__ == '__main__':
    app.run()