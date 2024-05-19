# Titanic Survival Prediction

This project explores the process of building and validating classification models to predict the survival of passengers on the Titanic. The project is divided into two parts: one without data scaling and one with data scaling using StandardScaler. The goal is to compare the performance of the models before and after scaling.

## Project Structure

Titanic_Prediction_unscaled_data.ipynb: This notebook contains the steps to build and evaluate classification models on the Titanic dataset without scaling the data.
Titanic_Prediction_scaled_data.ipynb: This notebook includes the steps to build and evaluate classification models on the Titanic dataset with scaled data using StandardScaler.

## Key Steps in the Workflow
1. **Load and Clean the Dataset**
**Objective:** Ensure the dataset is ready for model building and evaluation.
**Steps:** Handle missing values, encode categorical variables, and perform necessary data cleaning.

2. **Scale the Data Using StandardScaler (in Titanic_Prediction_scaled_data.ipynb)**
**Objective:** Standardize the features to have a mean of 0 and a standard deviation of 1.
**Impact:** Improve the performance of machine learning models.

3. **Model Building**
**Models Used:** Support Vector Machine (SVM), Random Forest Classifier, and Feedforward Neural Network.
**Libraries:** scikit-learn, keras.

**4. Initial Evaluation of Models (before and after scaling)**
**Objective:** Evaluate the performance of models on the training and testing sets.
**Metrics:** Accuracy, Precision, Recall, F1-score.

5. **Hyperparameter Tuning with Cross-Validation**
**Objective:** Optimize model performance by selecting the best hyperparameters.
**Method:** Grid Search with Cross-Validation.

6. **Final Evaluation**
## Objective: 
To Assess the models' performance and generalizability using cross-validation on the training set with the best hyperparameters.

## Result Summary

**Initial Evaluation(Before Scaling)**

**Support Vector Machine:**
Accuracy: 67.04%
Precision: 77.78%
Recall: 28.38%
F1-score: 41.58%

**Random Forest**
Accuracy: 83.24%
Precision: 79.73%
Recall: 79.73%
F1-score: 79.73%

**Feedforward Neural Network:**
Accuracy: 79.89%
Precision: 79.69%
Recall: 68.92%
F1-score: 73.91%

**Model Evaluation After Scaling**

**Support Vector Machine:**
Accuracy: 82.68%
Precision: 81.16%
Recall: 75.68%
F1-score: 78.32%

**Random Forest:**
Accuracy: 83.80%
Precision: 80.82%
Recall: 79.73%
F1-score: 80.27%

**Feedforward Neural Network:**
Accuracy: 82.68%
Precision: 84.13%
Recall: 71.62%
F1-score: 77.37%

**Final Evaluation Using Cross-Validation**

**Support Vector Machine:**
Accuracy: 83.00%
Precision: 82.29%
Recall: 81.11%
F1-score: 81.57%

**Random Forest:**
Accuracy: 83.71%
Precision: 83.55%
Recall: 80.98%
F1-score: 81.25%

**Feedforward Neural Network:**
Accuracy: 83.28%
Precision: 82.38%
Recall: 79.74%
F1-score: 80.92%

## Conclusion

The project successfully demonstrates the process of building and validating classification models using the Titanic dataset. The results show that scaling the data using StandardScaler significantly improves the performance of the models. The Random Forest Classifier achieved the highest accuracy and F1-score after scaling and hyperparameter tuning, making it the most effective model for predicting passenger survival in this study.