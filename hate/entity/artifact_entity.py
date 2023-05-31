from dataclasses import dataclass

# Data Ingestion Artifacts
@dataclass
class DataIngestionArtifacts:
    imbalance_data_file_path: str
    raw_data_file_path: str

# Data Transformation Artifacts
@dataclass
class DataTransformationArtifacts:
    transformed_data_path: str

# Model Trainer Artifacts
@dataclass
class ModelTrainerArtifacts:
    trained_model_path: str
    tokenizer_path: str
    x_test_path: str
    y_test_path: str

#Model Evaluation Artifacts
@dataclass
class ModelEvaluationArtifacts:
    is_model_accepted: bool

#Model Pusher Artifacts
@dataclass
class ModelPusherArtifacts:
    bucket_name: str
