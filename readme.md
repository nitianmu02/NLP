
## Set and run backend:

- pip install -r requirements.txt

- cd backend/nlp/latent_glat/fairseq

- pip install --editable ./

- cd ../

- git clone https://github.com/moses-smt/mosesdecoder.git

- download the files in https://drive.google.com/drive/folders/1OtNdsomNKxQC_bZMAbk-pt4MkDnK8YAU?usp=sharing into backend/nlp/latent_glat/models

- remember to change the need model file name into checkpoint_best.pt

- cd backend

- python manage.py runserver

---------------------------------

## Set and run frontend:

- cd frontend

- npm install

- npm start