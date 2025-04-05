# Bug Detection and Fixing

A machine learning project that aims to automatically detect bugs in source code and suggest potential fixes using intelligent models. This tool helps developers identify issues early and potentially save time in the debugging process.

## Features

- Automatic bug detection in code snippets
- Suggests fixes using trained models
- Machine Learning-based approach (includes custom datasets and models)
- Analysis using Jupyter notebooks
- Easy to extend for different programming languages

## Project Structure

Bug-Detection-And-Fixing/
├── data/                               
│   ├── bugs.csv
│   ├── bugs.json
│   ├── cleaned_bugs.csv
│   ├── cleaned_sstubs.csv
│   ├── sstubs.csv
│   └── sstubs.json
│
├── pretrained_model/                  
│   └── codet5-base.ipynb               
│
├── bug_detection.py                    
├── bug_fixer.py                        
├── fine_ture_model.py                  
├── load_dataset.py                    
├── test_model.py                     
├── train.json                          
│
├── README.md                          
├── requirements.txt                    
└── .gitignore                         




## Technologies Used

- Python
- Scikit-learn
- TensorFlow / Keras (if applicable)
- Pandas, NumPy
- Jupyter Notebooks
- GitHub for version control

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/chevy-67/Bug-Detection-And-Fixing.git
cd Bug-Detection-And-Fixing
