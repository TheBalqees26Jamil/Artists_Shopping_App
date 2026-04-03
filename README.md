# 🎨 Art Gallery Management System with AI

## 📌 Overview

This project is a **complete Art Gallery Management System** built with Python and PyQt6.

It allows users to explore artworks, analyze image colors, chat with an AI assistant about art, and manage their personal gallery experience (cart & preferences).

---

## 🎯 Objective

The goal of this project is to combine:

* GUI development
* Database management
* AI integration
* Image processing

into one interactive system for art exploration.

---

## 🛠️ Technologies Used

* Python
* PyQt6 (GUI)
* MongoDB (Database)
* Scikit-learn (KMeans for color analysis)
* Pillow (Image processing)
* Matplotlib (Visualization)
* Google Generative AI (Gemini API)

---

## 🚀 Features

### 🔐 User System

* Login & Signup
* User authentication with MongoDB

### 🎨 Gallery System

* Display artworks from database
* Search by category
* Add new artworks

### 🛒 User Interaction

* Add to cart
* Add to favorites (preferences)
* View cart with total price

### 🎨 Color Analysis

* Extract dominant colors using KMeans
* Display color names + RGB values
* Generate color distribution chart

### 🤖 AI Chatbot

* Ask questions about art
* AI responds using Gemini API
* Stores conversations in database

---

## 🖥️ How It Works

1. User logs in or creates an account
2. Enters the gallery
3. Can:

   * View artworks
   * Add items to cart or favorites
   * Click image → analyze colors
   * Open chatbot → ask about art
4. Data is stored in MongoDB

---

## 🖥️ Installation & Usage

### 1. Install dependencies

```
pip install PyQt6 pymongo pillow scikit-learn matplotlib colorthief google-generativeai
```

### 2. Run MongoDB locally

Make sure MongoDB is running


### 3. Run the application

```
python main.py
```

---

## 💡 Key Concepts

* GUI Design with PyQt6
* Database integration (MongoDB)
* Image processing & clustering
* AI chatbot integration
* Event-driven programming

---


## ⚠️ Notes

* Requires MongoDB running locally
* Requires valid Gemini API key
* This project is for educational and portfolio purposes

---

## 🚀 Future Improvements

* Add payment system
* Improve recommendation system using ML
* Add user profiles
* Deploy as desktop app or web app
