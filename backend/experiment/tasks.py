import warnings
from datetime import datetime

import numpy as np
import pandas as pd
from celery.utils.log import get_task_logger
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from backend.celery import app

celery_logger = get_task_logger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


@app.task(bind=True)
def wine_quality(self, alpha, l1_ratio, **kwargs):
    celery_logger.info("kwargs: %s", kwargs)
    if alpha is None:
        alpha = 0.5
    else:
        alpha = float(alpha)
    if l1_ratio is None:
        l1_ratio = 0.5
    else:
        l1_ratio = float(l1_ratio)
    celery_logger.info("alpha: %s", alpha)
    celery_logger.info("l1_ratio: %s", l1_ratio)
    request_id = self.request.id
    started_at = str(datetime.now())
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url = "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/data/winequality-red.csv"
    try:
        data = pd.read_csv(csv_url, sep=";")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s",
            e,
        )

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    predicted_qualities = lr.predict(test_x)

    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    print("Elasticnet model (alpha={:f}, l1_ratio={:f}):".format(alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    celery_logger.info("alpha: %s", alpha)
    celery_logger.info("l1_ratio: %s", l1_ratio)
    celery_logger.info("rmse: %s", rmse)
    celery_logger.info("r2: %s", r2)
    celery_logger.info("mae: %s", mae)

    celery_logger.info(
        "model: %s", {"lr": lr, "registered_model_name": "ElasticnetWineModel"}
    )
    return {
        "date": started_at,
        "request_id": request_id,
        "alpha": alpha,
        "l1_ratio": l1_ratio,
        "rmse": rmse,
        "r2": r2,
        "mae": mae,
    }
