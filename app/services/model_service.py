import joblib
import numpy as np

from utils.logging import AppLogger
from models.payload import PhishingPayload
from models.prediction import PhishingPredictionResult

from lib_ml_remla24_team02 import data_preprocessing


logger = AppLogger.__call__().get_logger()


class PhishingModel:
    def __init__(self, path: str) -> None:
        self.path = path
        self._load_local_model()

    def _load_local_model(self) -> None:
        self.model = joblib.load(self.path)

    def _pre_process(self, payload: PhishingPayload) -> np.ndarray:
        logger.debug("Pre-processing payload.")

        encoded_url = data_preprocessing.preprocess_single(payload.url)

        result = np.asarray(encoded_url).reshape(1, -1)
        return result

    def _post_process(self, prediction: np.ndarray) -> PhishingPredictionResult:
        logger.debug("Post-processing prediction.")
        result = (prediction > 0.5).astype(int)

        hpp = PhishingPredictionResult(prediction=result)
        return hpp

    def _predict(self, features: np.ndarray) -> np.ndarray:
        logger.debug("Predicting.")
        prediction_result = self.model.predict(features)
        return prediction_result

    def predict(self, payload: PhishingPayload) -> PhishingPredictionResult:
        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        post_processed_result = self._post_process(prediction)

        return post_processed_result
