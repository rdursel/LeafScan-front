import csv
import pandas as pd
result={}

def disease_info(disease_name):
    data_dict = {
        'Apple Apple Scab': 'https://www.planetnatural.com/pest-problem-solver/plant-disease/apple-scab/',
        'Apple Black rot': 'https://extension.umn.edu/plant-diseases/black-rot-apple',
        'Apple Cedar apple rust': 'https://gardenerspath.com/how-to/disease-and-pests/cedar-apple-rust-control/',
        'Apple healthy': '',
        'Background without leaves': '',
        'Blueberry healthy': '',
        'Cherry Powdery mildew': 'https://treefruit.wsu.edu/crop-protection/disease-management/cherry-powdery-mildew/',
        'Cherry healthy': '',
        'Corn Cercospora leaf spot Gray leaf spot': 'https://en.wikipedia.org/wiki/Corn_grey_leaf_spot',
        'Corn Common rust': 'https://extension.umn.edu/corn-pest-management/common-rust-corn#:~:text=Common%20rust%20produces%20rust%2Dcolored,as%20sheaths%2C%20can%20be%20infected.',
        'Corn Northern Leaf Blight': 'https://extension.umn.edu/corn-pest-management/northern-corn-leaf-blight',
        'Grape Black rot': 'https://ohioline.osu.edu/factsheet/plpath-fru-24',
        'Grape Esca (Black Measles)': 'https://ipm.ucanr.edu/agriculture/grape/esca-black-measles/',
        'Grape Leaf blight (Isariopsis Leaf Spot)': 'https://plantvillage.psu.edu/topics/grape/infos',
        'Grape healthy': '',
        'Orange Haunglongbing (Citrus greening)': 'https://en.wikipedia.org/wiki/Citrus_greening_disease',
        'Peach Bacterial spot': 'https://www.canr.msu.edu/news/management_of_bacterial_spot_on_peaches_and_nectarines',
        'Peach healthy': '',
        'Pepper, bell Bacterial spot': 'https://extension.wvu.edu/lawn-gardening-pests/plant-disease/fruit-vegetable-diseases/bacterial-leaf-spot-of-pepper',
        'Pepper, bell healthy': '',
        'Potato Early blight': 'https://www.gardeningknowhow.com/edible/vegetables/potato/potato-early-blight-treatment.htm#:~:text=Early%20blight%20of%20potato%20is,members%20of%20the%20potato%20family.',
        'Potato Late blight': 'https://www.planetnatural.com/pest-problem-solver/plant-disease/late-blight/',
        'Potato healthy': '',
        'Raspberry healthy': '',
        'Soybean healthy': '',
        'Squash Powdery mildew': 'https://www.gardeningknowhow.com/edible/vegetables/squash/powdery-mildew-in-squash.htm',
        'Strawberry Leaf scorch': 'https://www.gardeningknowhow.com/edible/fruits/strawberry/strawberries-with-leaf-scorch.htm',
        'Strawberry healthy': '',
        'Tomato Bacterial spot': 'https://extension.umn.edu/disease-management/bacterial-spot-tomato-and-pepper',
        'Tomato Early blight': 'https://extension.umn.edu/disease-management/early-blight-tomato-and-potato',
        'Tomato Late blight': 'https://www.planetnatural.com/pest-problem-solver/plant-disease/late-blight/',
        'Tomato Leaf Mold': 'https://en.wikipedia.org/wiki/Tomato_leaf_mold',
        'Tomato Septoria leaf spot': 'https://www.thespruce.com/identifying-and-controlling-septoria-leaf-spot-of-tomato-1402974',
        'Tomato Spider mites Two-spotted spider mite': 'https://ag.umass.edu/vegetable/fact-sheets/two-spotted-spider-mite#:~:text=The%20two%2Dspotted%20spider%20mite,most%20important%20pests%20of%20eggplant.',
        'Tomato Target Spot': 'https://www.vegetables.bayer.com/ca/en-ca/resources/agronomic-spotlights/target-spot-of-tomato.html#:~:text=Target%20spot%20of%20tomato%20is,in%20Immokalee%2C%20Florida%20in%201967.',
        'Tomato Tomato Yellow Leaf Curl Virus': 'https://en.wikipedia.org/wiki/Tomato_yellow_leaf_curl_virus',
        'Tomato Tomato mosaic virus': 'https://en.wikipedia.org/wiki/Tomato_mosaic_virus',
        'Tomato healthy': ''
    }
    return data_dict[disease_name]

print(disease_info('Apple Cedar apple rust'))
