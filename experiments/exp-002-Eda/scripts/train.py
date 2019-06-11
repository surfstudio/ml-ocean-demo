# import your model from somewhere
from sklearn.dummy import DummyClassifier

# import some metrics
from sklearn.metrics import accuracy_score

from crimes.alarmbot import notify

import janus
import mlflow
import pickle
import yaml


def train(config_path: str, data_path: str, save_path: str, usernames: str = None):
    # Telegram token to send notifications

    with open(config_path) as f:
        model_config = yaml.load(f)

    with open(data_path, 'rb') as f:
        data = pickle.load(f)
        X = data['X']
        y = data['y']

    with mlflow.start_run():

        clf = DummyClassifier()
        mlflow.log_param('param_name', 4)

        clf.fit(X, y)
        y_hat = clf.predict(X)

        acc = accuracy_score(y, y_hat)
        
        # Log to MLFlow
        mlflow.log_metric('accuracy', acc)
        
        # Send Telegram message 
        if usernames is not None:
            notify(usernames=usernames, message="The accuracy is {}".format(acc))


if __name__ == '__main__':
    p = janus.ArgParser()
    p.new_str('c config')
    p.new_str('d data')
    p.new_str('s save')
    p.new_str('u usernames')
    p.parse()
    train(config_path=p['c'],
          data_path=p['d'],
          save_path=p['s'],
          usernames=p['u'])
