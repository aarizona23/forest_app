import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forest_app.settings")  # Change to your actual settings module
django.setup()

from api_forest.models import ForestModel, IndicesModel

import datetime
import ee
import json
from api_forest.models import ForestModel, IndicesModel, IndicesTypes
from django.utils.timezone import make_aware

# Authenticate with GEE (Only needed once, then initialize)
ee.Initialize(project='foresthero')

indices = ['NDVI', 'EVI', 'NDWI', 'NBR', 'SAVI', 'GNDVI', 'NDRE', 'SIPI',
           'MGRVI', 'TGI', 'VARI', 'GRVI', 'SR', 'CI', 'MSR', 'OSAVI',
           'NDMI', 'MSAVI', 'NDRI', 'RECI']

def add_indices(image, chosen_indices):
    """
    Adds specified spectral indices as new bands to the Sentinel-2 image.

    Parameters:
      image (ee.Image): A Sentinel-2 image with bands named 'B2', 'B3', 'B4', 'B5', 'B8', 'B11', 'B12', etc.
      chosen_indices (list of str): List of index names to compute. Supported indices include:
        'NDVI', 'EVI', 'NDWI', 'NBR', 'SAVI', 'GNDVI', 'NDRE', 'SIPI', 'MGRVI',
        'TGI', 'VARI', 'GRVI', 'SR', 'CI', 'MSR', 'OSAVI', 'NDMI', 'MSAVI', 'NDRI', 'RECI'

    Returns:
      ee.Image: The input image with new index bands added.
    """

    for index in chosen_indices:
        if index == 'NDVI':
            # NDVI = (B8 - B4) / (B8 + B4)
            ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
            image = image.addBands(ndvi)

        elif index == 'EVI':
            # EVI = 2.5 * ((B8 - B4) / (B8 + 6*B4 - 7.5*B2 + 1))
            evi = image.expression(
                '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
                {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4'),
                    'BLUE': image.select('B2')
                }
            ).rename('EVI')
            image = image.addBands(evi)

        elif index == 'NDWI':
            # NDWI = (B3 - B8) / (B3 + B8)
            ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
            image = image.addBands(ndwi)

        elif index == 'NBR':
            # NBR = (B8 - B12) / (B8 + B12)
            nbr = image.normalizedDifference(['B8', 'B12']).rename('NBR')
            image = image.addBands(nbr)

        elif index == 'SAVI':
            # SAVI = ((B8 - B4) / (B8 + B4 + L)) * (1 + L), with L = 0.5
            savi = image.expression(
                '((NIR - RED) / (NIR + RED + L)) * (1 + L)',
                {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4'),
                    'L': 0.5
                }
            ).rename('SAVI')
            image = image.addBands(savi)

        elif index == 'GNDVI':
            # GNDVI = (B8 - B3) / (B8 + B3)
            gndvi = image.expression(
                '(NIR - GREEN) / (NIR + GREEN)',
                {
                    'NIR': image.select('B8'),
                    'GREEN': image.select('B3')
                }
            ).rename('GNDVI')
            image = image.addBands(gndvi)

        elif index == 'NDRE':
            # NDRE = (B8 - B5) / (B8 + B5)
            ndre = image.expression(
                '(NIR - RED_EDGE) / (NIR + RED_EDGE)',
                {
                    'NIR': image.select('B8'),
                    'RED_EDGE': image.select('B5')
                }
            ).rename('NDRE')
            image = image.addBands(ndre)

        elif index == 'SIPI':
            # SIPI = (B8 - B2) / (B8 - B4)
            sipi = image.expression(
                '(NIR - BLUE) / (NIR - RED)',
                {
                    'NIR': image.select('B8'),
                    'BLUE': image.select('B2'),
                    'RED': image.select('B4')
                }
            ).rename('SIPI')
            image = image.addBands(sipi)

        elif index == 'MGRVI':
            # MGRVI = (B3^2 - B4^2) / (B3^2 + B4^2)
            mgrvi = image.expression(
                '(GREEN * GREEN - RED * RED) / (GREEN * GREEN + RED * RED)',
                {
                    'GREEN': image.select('B3'),
                    'RED': image.select('B4')
                }
            ).rename('MGRVI')
            image = image.addBands(mgrvi)

        elif index == 'TGI':
            # TGI = B3 - 0.39*B4 - 0.61*B2
            tgi = image.expression(
                'GREEN - 0.39 * RED - 0.61 * BLUE',
                {
                    'GREEN': image.select('B3'),
                    'RED': image.select('B4'),
                    'BLUE': image.select('B2')
                }
            ).rename('TGI')
            image = image.addBands(tgi)

        elif index == 'VARI':
            # VARI = (B3 - B4) / (B3 + B4 - B2)
            vari = image.expression(
                '(GREEN - RED) / (GREEN + RED - BLUE)',
                {
                    'GREEN': image.select('B3'),
                    'RED': image.select('B4'),
                    'BLUE': image.select('B2')
                }
            ).rename('VARI')
            image = image.addBands(vari)

        elif index == 'GRVI':
            # GRVI = B3 / B4
            grvi = image.expression(
                'GREEN / RED',
                {
                    'GREEN': image.select('B3'),
                    'RED': image.select('B4')
                }
            ).rename('GRVI')
            image = image.addBands(grvi)

        elif index == 'SR':
            # Simple Ratio = B8 / B4
            sr = image.expression(
                'NIR / RED',
                {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4')
                }
            ).rename('SR')
            image = image.addBands(sr)

        elif index == 'CI':
            # Chlorophyll Index = (B8 / B2) - 1
            ci = image.expression(
                '(NIR / BLUE) - 1',
                {
                    'NIR': image.select('B8'),
                    'BLUE': image.select('B2')
                }
            ).rename('CI')
            image = image.addBands(ci)

        elif index == 'MSR':
            # MSR = ((B8 / B4) - 1) / (sqrt(B8 / B4) + 1)
            msr = image.expression(
                '((NIR / RED) - 1) / (sqrt(NIR / RED) + 1)',
                {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4')
                }
            ).rename('MSR')
            image = image.addBands(msr)

        elif index == 'OSAVI':
            # OSAVI = 1.16 * (B8 - B4) / (B8 + B4 + 0.16)
            osavi = image.expression(
                '1.16 * (NIR - RED) / (NIR + RED + 0.16)',
                {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4')
                }
            ).rename('OSAVI')
            image = image.addBands(osavi)

        elif index == 'NDMI':
            # NDMI = (B8 - B11) / (B8 + B11)
            ndmi = image.normalizedDifference(['B8', 'B11']).rename('NDMI')
            image = image.addBands(ndmi)

        elif index == 'MSAVI':
            # MSAVI = (2 * B8 + 1 - sqrt((2 * B8 + 1)^2 - 8*(B8 - B4)))/2
            msavi = image.expression(
                '(2 * NIR + 1 - sqrt(pow((2 * NIR + 1), 2) - 8 * (NIR - RED)))/2',
                {
                    'NIR': image.select('B8'),
                    'RED': image.select('B4')
                }
            ).rename('MSAVI')
            image = image.addBands(msavi)

        elif index == 'NDRI':
            # NDRI = (B4 - B3) / (B4 + B3)
            ndri = image.expression(
                '(RED - GREEN) / (RED + GREEN)',
                {
                    'RED': image.select('B4'),
                    'GREEN': image.select('B3')
                }
            ).rename('NDRI')
            image = image.addBands(ndri)

        elif index == 'RECI':
            # RECI = (B11 - B2) / (B11 + B2)
            reci = image.expression(
                '(SWIR1 - BLUE) / (SWIR1 + BLUE)',
                {
                    'SWIR1': image.select('B11'),
                    'BLUE': image.select('B2')
                }
            ).rename('RECI')
            image = image.addBands(reci)

        else:
            print('Index ' + index + ' is not recognized or required bands are missing.')

    return image

def add_indices_landsat(image, chosen_indices):
    """
    Adds specified spectral indices as new bands to a Landsat 8 T1_L2 image.

    Parameters:
      image (ee.Image): A Landsat 8 T1_L2 image with bands named 'SR_B2' (Blue), 'SR_B3' (Green),
                        'SR_B4' (Red), 'SR_B5' (NIR), 'SR_B6' (SWIR1), and 'SR_B7' (SWIR2).
      chosen_indices (list of str): List of index names to compute. Supported indices include:
        'NDVI', 'EVI', 'NDWI', 'NBR', 'SAVI', 'GNDVI', 'SIPI', 'MGRVI',
        'TGI', 'VARI', 'GRVI', 'SR', 'CI', 'MSR', 'OSAVI', 'NDMI', 'MSAVI',
        'NDRI', 'RECI'. (Note: 'NDRE' is not supported for Landsat 8 due to missing red edge band.)

    Returns:
      ee.Image: The input image with new index bands added.
    """

    for index in chosen_indices:
        if index == 'NDVI':
            # NDVI = (NIR - RED) / (NIR + RED)
            ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
            image = image.addBands(ndvi)

        elif index == 'EVI':
            # EVI = 2.5 * ((NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1))
            evi = image.expression(
                '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
                {
                    'NIR': image.select('SR_B5'),
                    'RED': image.select('SR_B4'),
                    'BLUE': image.select('SR_B2')
                }
            ).rename('EVI')
            image = image.addBands(evi)

        elif index == 'NDWI':
            # NDWI = (GREEN - NIR) / (GREEN + NIR)
            ndwi = image.normalizedDifference(['SR_B3', 'SR_B5']).rename('NDWI')
            image = image.addBands(ndwi)

        elif index == 'NBR':
            # NBR = (NIR - SWIR2) / (NIR + SWIR2)
            nbr = image.normalizedDifference(['SR_B5', 'SR_B7']).rename('NBR')
            image = image.addBands(nbr)

        elif index == 'SAVI':
            # SAVI = ((NIR - RED) / (NIR + RED + L)) * (1 + L) with L = 0.5
            savi = image.expression(
                '((NIR - RED) / (NIR + RED + L)) * (1 + L)',
                {
                    'NIR': image.select('SR_B5'),
                    'RED': image.select('SR_B4'),
                    'L': 0.5
                }
            ).rename('SAVI')
            image = image.addBands(savi)

        elif index == 'GNDVI':
            # GNDVI = (NIR - GREEN) / (NIR + GREEN)
            gndvi = image.expression(
                '(NIR - GREEN) / (NIR + GREEN)',
                {
                    'NIR': image.select('SR_B5'),
                    'GREEN': image.select('SR_B3')
                }
            ).rename('GNDVI')
            image = image.addBands(gndvi)

        elif index == 'NDRE':
            # NDRE is not supported for Landsat 8 because it requires a red edge band.
            print('Index NDRE is not supported for Landsat imagery. Skipping.')

        elif index == 'SIPI':
            # SIPI = (NIR - BLUE) / (NIR - RED)
            sipi = image.expression(
                '(NIR - BLUE) / (NIR - RED)',
                {
                    'NIR': image.select('SR_B5'),
                    'BLUE': image.select('SR_B2'),
                    'RED': image.select('SR_B4')
                }
            ).rename('SIPI')
            image = image.addBands(sipi)

        elif index == 'MGRVI':
            # MGRVI = (GREEN^2 - RED^2) / (GREEN^2 + RED^2)
            mgrvi = image.expression(
                '(GREEN * GREEN - RED * RED) / (GREEN * GREEN + RED * RED)',
                {
                    'GREEN': image.select('SR_B3'),
                    'RED': image.select('SR_B4')
                }
            ).rename('MGRVI')
            image = image.addBands(mgrvi)

        elif index == 'TGI':
            # TGI = GREEN - 0.39*RED - 0.61*BLUE
            tgi = image.expression(
                'GREEN - 0.39 * RED - 0.61 * BLUE',
                {
                    'GREEN': image.select('SR_B3'),
                    'RED': image.select('SR_B4'),
                    'BLUE': image.select('SR_B2')
                }
            ).rename('TGI')
            image = image.addBands(tgi)

        elif index == 'VARI':
            # VARI = (GREEN - RED) / (GREEN + RED - BLUE)
            vari = image.expression(
                '(GREEN - RED) / (GREEN + RED - BLUE)',
                {
                    'GREEN': image.select('SR_B3'),
                    'RED': image.select('SR_B4'),
                    'BLUE': image.select('SR_B2')
                }
            ).rename('VARI')
            image = image.addBands(vari)

        elif index == 'GRVI':
            # GRVI = GREEN / RED
            grvi = image.expression(
                'GREEN / RED',
                {
                    'GREEN': image.select('SR_B3'),
                    'RED': image.select('SR_B4')
                }
            ).rename('GRVI')
            image = image.addBands(grvi)

        elif index == 'SR':
            # Simple Ratio = NIR / RED
            sr = image.expression(
                'NIR / RED',
                {
                    'NIR': image.select('SR_B5'),
                    'RED': image.select('SR_B4')
                }
            ).rename('SR')
            image = image.addBands(sr)

        elif index == 'CI':
            # Chlorophyll Index = (NIR / BLUE) - 1
            ci = image.expression(
                '(NIR / BLUE) - 1',
                {
                    'NIR': image.select('SR_B5'),
                    'BLUE': image.select('SR_B2')
                }
            ).rename('CI')
            image = image.addBands(ci)

        elif index == 'MSR':
            # MSR = ((NIR / RED) - 1) / (sqrt(NIR / RED) + 1)
            msr = image.expression(
                '((NIR / RED) - 1) / (sqrt(NIR / RED) + 1)',
                {
                    'NIR': image.select('SR_B5'),
                    'RED': image.select('SR_B4')
                }
            ).rename('MSR')
            image = image.addBands(msr)

        elif index == 'OSAVI':
            # OSAVI = 1.16 * (NIR - RED) / (NIR + RED + 0.16)
            osavi = image.expression(
                '1.16 * (NIR - RED) / (NIR + RED + 0.16)',
                {
                    'NIR': image.select('SR_B5'),
                    'RED': image.select('SR_B4')
                }
            ).rename('OSAVI')
            image = image.addBands(osavi)

        elif index == 'NDMI':
            # NDMI = (NIR - SWIR1) / (NIR + SWIR1)
            ndmi = image.normalizedDifference(['SR_B5', 'SR_B6']).rename('NDMI')
            image = image.addBands(ndmi)

        elif index == 'MSAVI':
            # MSAVI = (2 * NIR + 1 - sqrt((2 * NIR + 1)^2 - 8*(NIR - RED))) / 2
            msavi = image.expression(
                '(2 * NIR + 1 - sqrt(pow((2 * NIR + 1), 2) - 8 * (NIR - RED))) / 2',
                {
                    'NIR': image.select('SR_B5'),
                    'RED': image.select('SR_B4')
                }
            ).rename('MSAVI')
            image = image.addBands(msavi)

        elif index == 'NDRI':
            # NDRI = (RED - GREEN) / (RED + GREEN)
            ndri = image.expression(
                '(RED - GREEN) / (RED + GREEN)',
                {
                    'RED': image.select('SR_B4'),
                    'GREEN': image.select('SR_B3')
                }
            ).rename('NDRI')
            image = image.addBands(ndri)

        elif index == 'RECI':
            # RECI = (SWIR1 - BLUE) / (SWIR1 + BLUE)
            reci = image.expression(
                '(SWIR1 - BLUE) / (SWIR1 + BLUE)',
                {
                    'SWIR1': image.select('SR_B6'),
                    'BLUE': image.select('SR_B2')
                }
            ).rename('RECI')
            image = image.addBands(reci)

        else:
            print('Index ' + index + ' is not recognized or required bands are missing.')

    return image

def get_preprocessed_image(date_str, end_date_str, bbox):
    collection = ee.ImageCollection('COPERNICUS/S2_SR') \
                    .filterBounds(bbox) \
                    .filterDate(date_str, end_date_str)

    composite = collection.mean().clip(bbox)
    composite = add_indices(composite, indices)  # Your existing function

    return composite.select(indices)

def get_preprocessed_image_landsat(date_str, end_date_str, bbox):
    collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
                .filterBounds(bbox) \
                .filterDate(date_str, end_date_str)

    composite = collection.first().clip(bbox)
    composite = add_indices_landsat(composite, indices)  # Your existing function

    return composite.select(indices)

def calculate_mean_indices(image_with_indices, bbox):
    index_bands = image_with_indices.select(indices)

    index_means = index_bands.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=bbox,
        scale=10,
        maxPixels=1e9
    )

    return index_means.getInfo()


def process_forest_indices():
    forests = ForestModel.objects.all()  # Get all forests

    for forest in forests:
        bbox_coords = forest.polygon_coors.get('bbox', [])  # Get bounding box from `polygon_coors`
        bbox = ee.Geometry.Rectangle(bbox_coords)

        # Example date range, you can modify it
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 12, 31)

        while start_date <= end_date:
            date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

            image_with_indices = get_preprocessed_image(date_str, end_date_str, bbox)
            mean_values = calculate_mean_indices(image_with_indices, bbox)

            # Store results in IndicesModel
            for index_name, value in mean_values.items():
                in_name = IndicesTypes(index_name).label
                IndicesModel.objects.create(
                    name=in_name,
                    value=value,
                    forest=forest,
                    timestamp=make_aware(datetime.datetime.strptime(date_str, "%Y-%m-%d"))
                )

            print(f"Saved indices for {forest.name} on {date_str}")
            start_date += datetime.timedelta(days=7)  # Process weekly

if __name__ == "__main__":
    process_forest_indices()
