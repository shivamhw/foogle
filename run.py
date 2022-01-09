from app.main import create_app


if __name__ == "__main__":
    create_app().run()
else:
    gunicorn = create_app()