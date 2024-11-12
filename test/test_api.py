from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient


class MockModel:
    def predict_entities(
        text: str, labels: list[str], threshold: float, multi_label: bool
    ) -> list[dict]:
        return [
            {
                "start": 0,
                "end": 16,
                "text": "Willem Alexander",
                "label": "person",
                "score": 0.6,
            },
            {
                "start": 34,
                "end": 43,
                "text": "Nederland",
                "label": "country",
                "score": 0.9,
            },
            {
                "start": 59,
                "end": 71,
                "text": "sinaasappels",
                "label": "food",
                "score": 0.94,
            },
            {
                "start": 79,
                "end": 94,
                "text": "Armin van Buren",
                "label": "person",
                "score": 0.6,
            },
            {
                "start": 79,
                "end": 94,
                "text": "Armin van Buren",
                "label": "dj",
                "score": 0.6,
            },
        ]


class TestAPI:
    """
    Test the API by mocking the gliner package and the model
    """

    @staticmethod
    @patch.dict("sys.modules", {"gliner": MagicMock()})
    @patch("api.api.GLiNER.from_pretrained", return_value=MockModel)
    def test_predict(mock_gliner_object):
        # assign
        input_data = {
            "text": (
                "Willem Alexander is de koning van Nederland. Hij houdt"
                " van sinaasappels en van Armin van Buren (een wereldberoemde DJ)"
            ),
            "labels": ["person", "country", "food", "dj"],
            "threshold": 0.5,
        }

        # act
        from api.api import app

        with TestClient(app) as client:
            response = client.post("/predict", json=input_data)

        # assert
        assert response.status_code == 200
        output = response.json()
        assert len(output["entities"]) == 5
        expected_keys = ["start", "end", "text", "label", "score"]
        assert all([key in expected_keys for key in output["entities"][0].keys()])

    @staticmethod
    @patch.dict("sys.modules", {"gliner": MagicMock()})
    def test_corrupt_input():
        # assign
        input_data = "random text not following predictions body base model"

        # act
        from api.api import app

        with TestClient(app) as client:
            response = client.post("/predict", json=input_data)

        # assert
        assert response.status_code == 422
