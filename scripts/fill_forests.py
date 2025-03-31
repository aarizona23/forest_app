import os
import sys
import django
# Get the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project directory to the Python path
sys.path.append(BASE_DIR)

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forest_app.settings")  # Update this with your actual settings module
django.setup()

from api_forest.models import ForestModel

if __name__ == "__main__":
    ForestModel.objects.create(
        name="Semey Ormany",
        unique_id="SemeyOrmany",
        polygon_coors={
            "bbox": [80.5714670950713, 50.3685743211883, 81.0227529049287, 50.6836629049287]
        }
    )
    ForestModel.objects.create(
        name="Semey Ormany 2",
        unique_id="SemeyOrmany2",
        polygon_coors={
            "bbox": [79.424667, 50.763611, 79.852944, 51.101222]
        }
    )
    ForestModel.objects.create(
        name="North KZ",
        unique_id="NorthKZ",
        polygon_coors={
            "bbox": [70.120417, 52.938389, 70.403639, 53.097639]
        }
    )
    ForestModel.objects.create(
        name="East KZ",
        unique_id="EastKZ1",
        polygon_coors={
            "bbox": [82.757861, 50.6734725, 83.174875, 50.910056]
        }
    )