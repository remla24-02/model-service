import joblib
import numpy as np

from utils.logging import AppLogger
from models.payload import PhishingPayload
from models.prediction import PhishingPredictionResult

from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# import lib_ml_remla24_team02 as lib_ml


logger = AppLogger.__call__().get_logger()


class PhishingModel:
    RESULT_UNIT_FACTOR = 100

    def __init__(self, path: str) -> None:
        self.path = path
        self._load_local_model()

    def _load_local_model(self) -> None:
        self.model = joblib.load(self.path)

    def _pre_process(self, payload: PhishingPayload) -> np.ndarray:
        logger.debug("Pre-processing payload.")

        tokenizer = Tokenizer(lower=True, char_level=True, oov_token='-n-')
        tokenizer.fit_on_texts([payload.url])
        encoded_url = pad_sequences(
            tokenizer.texts_to_sequences([payload.url]), maxlen=200)

        # encoded_url = lib_ml.preprocess_single(payload.url)  # TODO

        logger.debug(f"Encoded URL: {encoded_url}")

        result = np.asarray([encoded_url]).reshape(1, -1)
        return result

    def _post_process(self, prediction: np.ndarray) -> PhishingPredictionResult:
        logger.debug("Post-processing prediction.")
        result = prediction.tolist()
        encoder = LabelEncoder()
        result = encoder.fit_transform(result)

        human_readable_unit = result[0] * self.RESULT_UNIT_FACTOR
        hpp = PhishingPredictionResult(prediction=human_readable_unit)
        return hpp

    def _predict(self, features: np.ndarray) -> np.ndarray:
        logger.debug("Predicting.")
        prediction_result = self.model.predict(features)
        return prediction_result

    def predict(self, payload: PhishingPayload) -> PhishingPredictionResult:
        pre_processed_payload = self._pre_process(payload)
        prediction = self._predict(pre_processed_payload)
        logger.info(prediction)
        post_processed_result = self._post_process(prediction)

        return post_processed_result
