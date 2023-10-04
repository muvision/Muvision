## Aim
This project aims to create a web application that is able to convert handwritten math text to LaTeX, a document preparation that uses the TeX typesetting format that is widely used in academia for text related to math. Currently, the application can detect basic math symbols (numbers, basic arithmetic operations such as addition, multiplication, division, and subtraction, and some letters (specifically x,y,z). The choice of symbols is due to the complexities and difficulties of detecting more complex math symbols and the data set that was used to train the machine learning models. For future aspirations, see the section on future aspirations.

Over the course of the project, we aimed to incorporate a multitude of different technologies, such as cloud computing (AWS), Machine Learning (Tensorflow) and Computer Vision (OpenCV). 

# Muvision 

![image](https://github.com/muvision/Muvision/assets/113735719/b5b2d8c3-d678-4b8c-806f-7d07d721f211)

Website: [Muvision](https://muvision.netlify.app/).

This repository is made up of many different repositories, which can be found in the following links:
[Backend](https://github.com/muvision/backend)
[Frontend](https://github.com/muvision/front-end)
[ML Model](https://github.com/muvision/CNN)
[OpenCV](https://github.com/muvision/cm-mathvision)

## Future Aspirations
Our aim is to hopefully have the time to add additional symbols to the ML model such as integrals, brackets and other letters. In addition, we hope to add the detection of additional math operations, such as fractions, matrices, and square roots. 

Once the math-vision is completed, we aim to provide students with feedback on their own practice problems, so that they can get actionable feedback on their solutions.

## Project Structure
From the frontend, the user draws some math text on the custom whiteboard. When the user presses "Submit", the frontend sends a POST request to the backend, which uses the OpenCV algorithm that we developed to isolate lines of math text and individual characters. The machine learning model that we developed will then detect the character. 

The frontend is hosted on Netlify, and the backend is hosted on an AWS EC2 instance, launched using Amazon's [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) service. A custom domain set up with an SSL certificate is used as a server. 

## Backend
**Backend created using Django**

Copy in ensemble_model.h5 to the mysite/muvision directory. To find the model, refer to the "ML model" folder.

Run these commands in the terminal.
```console
pip install -r requirements.txt
cd mysite
python manage.py runserver
```

## Frontend
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

### Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

## ML Model
The Model was created in Google Colab, a collaboratory environment where individuals can collaborate together, and uploaded to Google Drive. Running the script in that environment allows you to run a remote, cloud-hosted environment by Google. 

To run the script in Google Drive, create a folder called "Muvision" that contains two folders, "datasets" and "models". The "models" folder is used to store the models that will be created by the script. 

### Dataset
The dataset that we used for this project is found here: [https://www.kaggle.com/datasets/sagyamthapa/handwritten-math-symbols](https://www.kaggle.com/datasets/sagyamthapa/handwritten-math-symbols). Initially we used this dataset: [https://github.com/ThomasLech/CROHME_extractor](https://github.com/ThomasLech/CROHME_extractor) but we found that the letters were too skeletonized and thus leading to inaccurate results.

Inside the "datasets" folder in the Google Drive project, upload the dataset used (link above) and put it in a folder called "handwritten_math_symbols". 

### Running locally
It is possible to run the files locally on Jupyter Notebook or Jupyter Lab, although changes may have to be made to directories. A requirements.txt file is attached to the repository for libraries and dependencies. 

## OpenCV
Similar to the ML Model training, the OpenCV portion was developed using Google Collab as well. The OpenCV uses the library to identify lines of math text and the subsequent individual characters in the lines. The whole process is organized into a pandas dataframe. 
