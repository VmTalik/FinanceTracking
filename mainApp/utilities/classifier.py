import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from sklearn.model_selection import train_test_split
import pandas as pd
import random
import os

# pip install spacy
# pip install spacy-lookups-data
# pip install scikit-learn
# pip install pandas
# python -m spacy download ru_core_news_sm

model_path = "mainApp/utilities/text_classifier"  # Путь к модели


def run_classifier():
    """Функция запуска классификатора текста на основе NLP"""
    # Проверка, существует ли сохраненная модель
    if os.path.exists(model_path):
        nlp = spacy.load(model_path)  # Загрузка модели
        print("Модель успешно загружена.")
    else:
        nlp = spacy.load("ru_core_news_sm")  # Загружаем модель для русского языка
        train_model(nlp)
    return nlp


def train_model(nlp):
    """Функция для обучения модели классификации. Используем для категоризации расходов"""
    df = pd.read_csv('mainApp/utilities/data.csv')  # Загружаем данные из CSV-файла

    # Разделяем данные на обучающую и тестовую выборки
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    # Готовим данные для обучения
    train_data = list(zip(train_df["text"], [{"cats": {label: label == train_df["label"].iloc[i]
                                                       for label in set(df["label"])}}
                                             for i in range(len(train_df))]))

    # Добавляем текстовый классификатор в пайплайн
    if "textcat" not in nlp.pipe_names:
        textcat = nlp.add_pipe("textcat", last=True)
    else:
        textcat = nlp.get_pipe("textcat")

    # Добавляем метки категорий
    for label in set(df["label"]):
        textcat.add_label(label)

    # Обучаем модель
    n_iter = 20
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "textcat"]
    with nlp.disable_pipes(*other_pipes):  # Отключаем другие пайплайны во время обучения
        optimizer = nlp.begin_training()
        for i in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                examples = [Example.from_dict(nlp.make_doc(text), annotation) for text, annotation in
                            zip(texts, annotations)]
                nlp.update(examples, sgd=optimizer, drop=0.5, losses=losses)
            print(f"Iteration {i}, Losses: {losses}")

    # Сохраняем модель
    nlp.to_disk(model_path)
    print("Модель успешно обучена и сохранена.")


if __name__ == '__main__':
    # Пример текстов для классификации
    texts = [
        "Купил продуктов в магазине",
        "Купил костюм",
        "Приобрел квартиру",
        "Оплатил интернет",
        "Купил ботинки"
    ]

    nlp = run_classifier()

    # Классификация текстов
    for text in texts:
        doc = nlp(text)
        res = doc.cats
        max_predicted = max(res, key=res.get)
        print(f"Text: {text}, Predicted: {max_predicted, res[max_predicted]}")
