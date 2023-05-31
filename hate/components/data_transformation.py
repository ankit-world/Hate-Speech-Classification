import os
import re
import sys
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from sklearn.model_selection import train_test_split
from hate.logger import logging 
from hate.exception import CustomException
from hate.entity.config_entity import DataTransformationConfig
from hate.entity.artifact_entity import DataIngestionArtifacts, DataTransformationArtifacts


class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_ingestion_artifacts: DataIngestionArtifacts):

        """
        :param data_transformation_config: Configuration for data transformation
        """
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifacts = data_ingestion_artifacts
        
    def imbalanced_data_cleaning(self):

        try:
            logging.info("Entered into the imbalance_data_cleaning function")
            imbalance_data = pd.read_csv(self.data_ingestion_artifacts.imbalance_data_file_path)
            imbalance_data.drop(self.data_transformation_config.ID, axis=self.data_transformation_config.AXIS, inplace=self.data_transformation_config.INPLACE)
            logging.info(f"Exited the imbalance data_cleaning function and returned imbalance data {imbalance_data}")
            return imbalance_data
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def raw_data_cleaning(self):

        try:
            logging.info("Entered into the raw_data_cleaning function")
            raw_data = pd.read_csv(self.data_ingestion_artifacts.raw_data_file_path)
            raw_data.drop(self.data_transformation_config.DROP_COLUMNS, axis=self.data_transformation_config.AXIS, inplace=self.data_transformation_config.INPLACE)
            
            raw_data[raw_data[self.data_transformation_config.CLASS]==0][self.data_transformation_config.CLASS]=1

            # replace the value of 0 to 1
            raw_data[self.data_transformation_config.CLASS].replace({0:1}, inplace=self.data_transformation_config.INPLACE)

            # Let's replace the value of 2 to 0.
            raw_data[self.data_transformation_config.CLASS].replace({2:0}, inplace=self.data_transformation_config.INPLACE)

            # Let's change the name of the 'class' to label
            raw_data.rename(columns={'class':'label'}, inplace=True)
            raw_data.rename(columns = {self.data_transformation_config.CLASS:self.data_transformation_config.LABEL}, inplace=self.data_transformation_config.INPLACE)
            logging.info(f"Exited the raw_data_cleaning function and returned the raw_data {raw_data}")
            return raw_data
        
        except Exception as e:
            raise CustomException(e, sys)
        

    def concat_dataframe(self):

        try:
            logging.info("Entered into the concat_dataframe function")


            df = pd.concat([self.raw_data_cleaning(), self.imbalanced_data_cleaning()])
            print(df.head())

            logging.info(f"returned the concatinated dataframe {df}")

            return df
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def concat_data_cleaning(self, words):
        try:
            logging.info("Entered into the concat_data_cleaning function")
            stemmer = nltk.SnowballStemmer("english")
            stopword = set(stopwords.words('english'))
            words = str(words).lower()
            words = re.sub('\[.*?\]', '', words)
            words = re.sub('https?://\S+|www\.\S+', '', words)
            words = re.sub('<.*?>+', '', words)
            words = re.sub('[%s]' % re.escape(string.punctuation), '', words)
            words = re.sub('\n', '', words)
            words = re.sub('\w*\d\w*', '', words)
            words = [word for word in words.split(' ') if words not in stopword]
            words=" ".join(words)
            words = [stemmer.stem(words) for word in words.split(' ')]
            words=" ".join(words)
            logging.info("Exited the concat_data_cleaning function")
            return words
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def initiate_data_transformation(self) -> DataTransformationArtifacts:

        """
        Method Name :   initiate_data_transformation
        Description :   This function initiates a data transformation steps
        Output      :   Returns data return artifact
        On Failure  :   Write an exception log and then raise an exception
        """

        logging.info("Entered the initiate_data_transformation method of Data transformation class")
        try:
            logging.info("Entered the initiate_data_transformation method of Data transformation class")
            self.imbalanced_data_cleaning()
            self.raw_data_cleaning()
            df = self.concat_dataframe()
            df[self.data_transformation_config.TWEET] = df[self.data_transformation_config.TWEET].apply(self.concat_data_cleaning)

            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACTS_DIR, exist_ok=True)
            df.to_csv(self.data_transformation_config.TRANSFORMED_FILE_PATH, index=False, header=True)


            data_transformation_artifacts = DataTransformationArtifacts(transformed_data_path=self.data_transformation_config.TRANSFORMED_FILE_PATH)

            logging.info("Exited the initiate_data_transformation method of Data transformation class")

            logging.info(f"Data transformation artifact: {data_transformation_artifacts}")
            return data_transformation_artifacts
        
        except Exception as e:
            raise CustomException(e, sys) from e



