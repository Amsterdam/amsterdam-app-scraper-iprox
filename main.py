import os


if __name__ == '__main__':
    backend_host = os.getenv('BACKEND_HOST', 'api-server')
    for content_type in ['stadsloket']:
        pass