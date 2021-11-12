from bd_project import create_app
from bd_project.models import create_db

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
