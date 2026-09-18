from src.pipeline.predict_pipeline import CustomData, PredictPipeline


def test_prediction_pipeline():
    data = CustomData(
        2,
        120,
        70,
        25,
        100,
        30.5,
        0.5,
        35
    )

    prediction = PredictPipeline().predict(
        data.get_data_as_data_frame()
    )

    assert prediction[0] in [0, 1]