import os

repository_dir = os.path.dirname(os.path.dirname(__file__))
model_save_path = 'Webpage\Classifier\RNN_model'
web_dir = os.path.join(repository_dir, model_save_path)

print(web_dir)