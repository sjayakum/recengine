# recengine

Societe Generale Global Solution Centre (SG GSC) hosted the second edition of its annual hackathon, Brainwaves 2015, on September 12 and 13. The event aimed at bringing together college students, working professionals and SG GSC employees together for a 30-hour build session which saw 165 participants across 45 teams showcase their coding abilities to create applications.

**This application was awarded first place**

## Index
- [Introduction](#introduction)
- [Architecture](#architecture)
- [Backed](#backend)
- [Pitch](#pitch)
- [Sample Screenshots](#sample-screenshots)
- [References](#references)


## Introduction
An app that analyses stock portfolio, recommends securities based on the user profile and also verifies recommendations using sentiment analysis from social media.

## Architecture
A python microframework called **Flask** was used to build a RESTful connection between Client (Front-end) and Server (Back-end).

Back-end was deployed using **Apache Spark** for big data munging with the help of *pyspark and mllib*.

## Backend

**Collaborative Filtering** is a method of making automatic predictions (filtering) about the interests of a user by collecting preferences or taste information from many users (collaborating).
It is been vastly used by "e-commerce gaints" in order to provide its clients a highly personalized recommendations based on thier past transactions and common interests with other people with similar purchases.

![alt tag](https://upload.wikimedia.org/wikipedia/commons/5/52/Collaborative_filtering.gif)

A sample collaborative filtering dataset by [Jester](https://github.com/sjayakum/recengine/blob/master/recengine/back-end/Datasets/jester-data-1.xls) was used to train the model.

**Accuracy of the model**

![alt tag](https://github.com/sjayakum/recengine/blob/master/recengine/samples/pic2.png)

Here,
- **Green** indicates the "Predicted" metric of a all the stocks for a given user.
- **Blue** indiciates the "Actual" pre-calculated metric of all stock for a given user.
- **x-axis** List of all stocks index from 0 to 40 [which are in our consideration]
- **y-axis** Represents the likeliness that the given person would go for that stock. More positive the value, more likely he is to buy that stock.



This prediction was further verified using **Sentiment Analysis** of public data (twitter/facebook/articles) on that stock (Opinion Mining) to help user make an **INFORMED** decision.


## Pitch
[Click here for more details](https://github.com/sjayakum/recengine/blob/master/recengine/socgen.pptx)

## Sample Screenshots
[Click here for more details](https://github.com/sjayakum/recengine/tree/master/recengine/samples)

## References

- [Redefining banking in a digital world](https://github.com/sjayakum/recengine/blob/master/recengine/references/96a32ed5-137c-0010-82c7-eda71af511fa.pdf)
- [Digital Banking Point of View](https://github.com/sjayakum/recengine/blob/master/recengine/references/Digital_Banking_PoV_2015_04_08_final_EN.pdf)
