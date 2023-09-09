from gensim.models import FastText
from modules.product.classStructure import ProductClass
import logging


logging.basicConfig(level=logging.DEBUG)


def trainProductModelDescription(userId):
    allProductsUser = ProductClass.getData(**{"user_id": userId})
    sentences = list()
    for product in range(len(allProductsUser)):
        sentences.append(allProductsUser[product]["name"].split())

    # Entrenar un modelo FastText
    model = FastText(sentences, vector_size=100, window=3, min_count=1, sg=1, epochs=50)

    # Guardar el modelo entrenado
    model.save("/app/config/modelsFastText/products_{}.model".format(userId))
