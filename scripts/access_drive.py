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

from api_forest.models import ForestModel, ForestMaskModel

if __name__ == "__main__":
    forestmask1 = ForestMaskModel.objects.filter(forest__id=1).count()
    print(forestmask1)
    forestmask2 = ForestMaskModel.objects.filter(forest__id=2).count()
    print(forestmask2)
    forestmask3 = ForestMaskModel.objects.filter(forest__id=3).count()
    print(forestmask3)
    forestmask4 = ForestMaskModel.objects.filter(forest__id=4).count()
    print(forestmask4)