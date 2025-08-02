import sys
import os
from colorthief import ColorThief
from PIL import Image
from collections import Counter
import webcolors
from sklearn.cluster import KMeans
import numpy as np
import math
from PyQt6.QtWidgets import QApplication, QWidget,QDialog,QTextEdit, QFileDialog, QMessageBox, QHBoxLayout, QScrollArea, QLabel, QGridLayout, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QFrame,QListWidget ,QListWidgetItem
from PyQt6.QtGui import QPixmap, QFont, QIcon, QDesktopServices,QDesktopServices
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.uic import loadUi
from pymongo import MongoClient
from io import BytesIO
import google.generativeai as genai
from functools import partial
import matplotlib.pyplot as plt





genai.configure(api_key="AIzaSyAyGWi5oQnMB6CHK4qvFgeL5oVU-OSwxo8")
class MongoDBHandler:
    def __init__(self, db_name: str, collection_name: str):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print("تم الاتصال بقاعدة البيانات بنجاح!")
        except Exception as e:
            print(f"خطأ في الاتصال بقاعدة البيانات: {e}")

    def insert_artwork(self, filePath, name, category, price):
        artwork = {"filePath": filePath, "name": name, "category": category, "price": price}
        self.collection.insert_one(artwork)
        print("تم إدراج العمل الفني بنجاح:", artwork)

    def get_all_artworks(self):
        return self.collection.find()

    def get_artworks_by_category(self, category):
        return self.collection.find({"category": category})

    def insert_user(self, username: str, password: str):
        user = {"username": username, "password": password}
        result = self.collection.insert_one(user)
        print("تم إدراج المستخدم:", user)
        return result.inserted_id

    def find_user(self, username: str):
        return self.collection.find_one({"username": username})

    def close(self):
        self.client.close()




class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("untitled.ui", self)
        self.db = MongoDBHandler("Arts_system", "Users")
        self.LoginButton.clicked.connect(self.entermyAccount)
        self.SignupButton.clicked.connect(self.createAccount)
        self.InstaButton.clicked.connect(self.gotoInstagram)
        self.FaceButton.clicked.connect(self.gotoFacebook)
        self.TwitButton.clicked.connect(self.gotoTwitter)

    def gotoGalleryWindow(self):

        self.GalleryWindow = GalleryWindow()
        self.GalleryWindow.show()
        self.close()

    def createAccount(self):

        self.createAccountWindow = SignupWindow()
        self.createAccountWindow.show()
        self.close()

    def entermyAccount(self):

        if self.validateFields():
            username = self.Username.text().strip()
            password = self.Password.text().strip()


            user = self.db.find_user(username)
            if user and user["password"] == password:
                self.gotoGalleryWindow()
            else:

                msgBox = QMessageBox(self)
                #msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.setWindowTitle("Alert!")
                msgBox.setText("Password or username does not match!")
                msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)


                msgBox.setStyleSheet("""
                        QMessageBox {
                            background-color: black; 
                        }
                        QMessageBox QLabel {
                            color: white; 
                            font-weight: bold; 
                        }
                        QMessageBox QPushButton {
                            background-color: #600cb9; 
                            color: white;
                        }
                        QMessageBox QPushButton:hover {
                            background-color: #1e0637; 
                        }
                    """)

                msgBox.exec()

    def validateFields(self):

        if self.Username.text().strip() == "" or self.Password.text().strip() == "":
            self.showMessage()
            return False
        return True

    def showMessage(self):

        self.msgBox = MessageBox()
        self.msgBox.show()

    def gotoInstagram(self):

        QDesktopServices.openUrl(QUrl("https://www.instagram.com/"))

    def gotoFacebook(self):

        QDesktopServices.openUrl(QUrl("https://www.facebook.com/"))

    def gotoTwitter(self):

        QDesktopServices.openUrl(QUrl("https://www.twitter.com/"))


class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("untitled2.ui", self)
        self.db = MongoDBHandler("Arts_system", "Users")
        self.SignupButton.clicked.connect(self.validateSignup)
        self.BackButton.clicked.connect(self.back)

    def back(self):
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def validateSignup(self):

        username = self.Username.text().strip()
        password = self.Password.text().strip()

        if username == "" or password == "":
            self.showMessage()
            return


        if self.db.find_user(username):
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.setText("User name is already created!")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)


            msgBox.setStyleSheet("""
                QMessageBox {
                    background-color: black;  
                }
                QMessageBox QLabel {
                    color: white;  
                    font-weight: bold;  
                }
                QMessageBox QPushButton {
                    background-color: #600cb9; 
                    color: white;
                }
                QMessageBox QPushButton:hover {
                    background-color: #1e0637;
                }
            """)

            msgBox.exec()

            return


        self.db.insert_user(username, password)


        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setWindowTitle("Created")
        msgBox.setText("Created Successfully!")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)


        msgBox.setStyleSheet("""
            QMessageBox {
                background-color: black;  
            }
            QMessageBox QLabel {
                color: white;  
                font-weight: bold;  
            }
            QMessageBox QPushButton {
                background-color: #600cb9; 
                color: white;
            }
            QMessageBox QPushButton:hover {
                background-color: #1e0637;
            }
        """)
        msgBox.buttonClicked.connect(self.back)
        msgBox.exec()




    def back(self):

        self.login = LoginWindow()
        self.login.show()
        self.close()

    # def openGalleryWindow(self):
    #
    #     self.gotoGalleryWindow()


    def activateCheckBox(self):

        self.PoiliciesCheckBox.setChecked(True)

    def gotoGalleryWindow(self):

        self.GalleryWindow = GalleryWindow()
        self.GalleryWindow.show()
        self.close()

    def showMessage(self):

        self.msgBox = MessageBox()
        self.msgBox.show()


class MessageBox(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("message.ui", self)
        self.OkButton.clicked.connect(self.close)


class MessageBox2(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("message2.ui",self)
        self.OkButton.clicked.connect(self.close)
    def showMessage(self, message):

        if hasattr(self, 'MessageLabel'):
            self.MessageLabel.setText(message)
        else:
            print("MessageLabel not found")


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()


        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["art_chatbot_db"]
        self.collection = self.db["conversations"]

        self.setWindowTitle("AI Art Chat")
        self.setGeometry(100, 100, 400, 300)


        self.setStyleSheet("""
            QWidget {

                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
            QTextEdit, QLineEdit, QPushButton {
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #fffbea;  
                color: #333;
                font-family: Arial;
            }
            QLineEdit {
                background-color: #fffbea;  
                color: #333;
            }
            QPushButton {
                background-color: #600cb9 ;
                color: white;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1e0637 ;
            }
        """)

        self.layout = QVBoxLayout(self)


        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.layout.addWidget(self.chat_history)


        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ask something about art...")git push -f origin master

        self.layout.addWidget(self.user_input)


        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_user_input)
        self.layout.addWidget(self.send_button)

    def handle_user_input(self):
        user_text = self.user_input.text().strip()
        if not user_text:
            return

        self.chat_history.append(f"You: {user_text}")
        self.user_input.clear()


        self.chat_history.append('<span style="line-height: 1.5;"> </span>')  # فاصل بمقدار خط واحد


        bot_response = self.get_gpt_response(user_text)
        self.chat_history.append(f"Bot: {bot_response}")


        self.chat_history.append('<span style="line-height: 1.5;"> </span>')  # فاصل بمقدار خط واحد


        self.save_conversation(user_text, bot_response)

    def save_conversation(self, user_input, bot_response):
        conversation = {"user_input": user_input, "bot_response": bot_response}
        self.collection.insert_one(conversation)

    def get_gpt_response(self, prompt):
        try:
            model = genai.GenerativeModel(model_name='gemini-pro')
            prompt_ = f'''
            You are an art assistant bot. You can only answer questions related to art, including painting, sculpture, photography, art history, and design.
            If the user asks anything outside of art, politely tell them you cannot answer that.

            User's question: {prompt}
            '''
            response = model.generate_content(prompt_)
            return response.text if response else "No response from the bot."
        except Exception as e:
            return f"Error: {e}"


class ColorAnalysisWindow(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Color Analysis")
        self.setStyleSheet("background-color: #fef9e7 ;")
        self.setFont(QFont("Segoe UI", 12))
        self.image_path = image_path
        self.setGeometry(300, 200, 400, 300)

        layout = QVBoxLayout(self)

        label = QLabel("Color Analysis of the Selected Image")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(image_label)


        self.analyze_colors(image_path)

        self.setLayout(layout)

    def analyze_colors(self, image_path):

        image = Image.open(image_path)
        image = image.convert("RGB")

        image = image.resize((image.width // 5, image.height // 5))

        pixels = np.array(image).reshape(-1, 3)


        kmeans = KMeans(n_clusters=15, random_state=0)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_
        labels = kmeans.labels_


        color_info = []
        for color in colors:

            color_name = self.get_closest_color_name(tuple(int(c) for c in color))
            color_info.append(f"Color: {color_name}, RGB: {tuple(int(c) for c in color)}")


        color_label = QLabel("\n".join(color_info))
        color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(color_label)


        unique, counts = np.unique(labels, return_counts=True)
        percentages = counts / counts.sum()

        colors_for_pie = [tuple(colors[i] / 255) for i in unique]


        plt.figure(figsize=(4, 4))
        plt.pie(percentages,
                labels=[f"{int(perc * 100)}%" for perc in percentages],
                colors=colors_for_pie,
                startangle=90,
                wedgeprops={'edgecolor': 'black'})
        plt.axis("equal")
        chart_path = "color_distribution.png"
        plt.savefig(chart_path)
        plt.close()


        chart_label = QLabel(self)
        chart_label.setPixmap(QPixmap(chart_path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(chart_label)

    def get_closest_color_name(self, rgb):

        color_names = {
            "Red": (255, 0, 0),
            "Green": (0, 255, 0),
            "Blue": (0, 0, 255),
            "Yellow": (255, 255, 0),
            "White": (255, 255, 255),
            "Gray": (128, 128, 128),
            "Orange": (255, 165, 0),
            "Purple": (128, 0, 128),
            "Brown": (139, 69, 19),
            "LightGray": (211, 211, 211),
            "DarkGray": (169, 169, 169),
            "LightBlue": (173, 216, 230),
            "DarkBlue": (0, 0, 139),
            "LightGreen": (144, 238, 144),
            "Olive": (128, 128, 0),
            "Pink": (255, 192, 203),
            "LightPink": (255, 182, 193),
            "Lavender": (230, 230, 250),
            "SkyBlue": (135, 206, 235),
            "Beige": (245, 245, 220),
            "Lime": (0, 255, 0),
            "LimeGreen": (50, 205, 50),
            "YellowGreen": (154, 205, 50),
            "Aquamarine": (127, 255, 212),
            "Turquoise": (64, 224, 208),
            "Teal": (0, 128, 128),
            "OliveDrab": (107, 142, 35),
            "Coral": (255, 127, 80),
            "PeachPuff": (255, 218, 185),
            "PapayaWhip": (255, 239, 184),
            "LightSalmon": (255, 160, 122),
            "Gold": (255, 215, 0),
            "Khaki": (240, 230, 140),
            "Chartreuse": (127, 255, 0),
            "MediumPurple": (147, 112, 219),
            "DarkOrange": (255, 140, 0),
            "MediumAquamarine": (102, 205, 170),
            "SlateBlue": (106, 90, 205),
            "DarkKhaki": (189, 183, 107),
            "Periwinkle": (204, 204, 255)
        }
        closest_color = None
        min_distance = float('inf')
        for name, value in color_names.items():
            distance = np.linalg.norm(np.array(rgb) - np.array(value))
            if distance < min_distance:
                min_distance = distance
                closest_color = name
        return closest_color

class GalleryWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("GALLERY.ui", self)
        self.db = MongoDBHandler("Arts_system", "Artworks")
        self.cart_items = []
        self.all_artworks = []
        self.prefer = []


        self.detailsWindow = None
        self.basketWindow = None
        self.analysisWindow = None
        self.chatWindow = None
        self.preferencesWindow = None

        self.Search.textChanged.connect(self.searchCategories)

        self.Share.clicked.connect(self.ShareArtWindow)
        self.ShowStuff.clicked.connect(self.showBasketWindow)
        self.chat_button.clicked.connect(self.openChatWindow)
        self.preferencesButton.clicked.connect(self.showPreferencesWindow)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.imageContainer = QWidget()
        self.gridLayout = QGridLayout(self.imageContainer)
        self.gridLayout.setVerticalSpacing(95)
        self.scrollArea.setWidget(self.imageContainer)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.Share)
        self.mainLayout.addWidget(self.scrollArea)


        self.scrollArea.setMinimumHeight(int(self.height() * 0.6))
        self.scrollArea.setMaximumHeight(int(self.height() * 0.6))


        self.Share.setFixedSize(120, 50)

        self.mainLayout.setAlignment(self.Share, Qt.AlignmentFlag.AlignCenter)

        self.columns = 3
        self.imageCount = 0

        self.loadImagesFromDatabase()

    def loadImagesFromDatabase(self):
        artworks = self.db.get_all_artworks()
        self.all_artworks = list(artworks)
        self.displayImages(self.all_artworks)

    def displayImages(self, artworks):
        self.clearImages()
        for artwork in artworks:
            filePath = artwork["filePath"]
            name = artwork["name"]
            category = artwork["category"]
            price = artwork["price"]
            self.addImage(filePath, name, category, price)

    def clearImages(self):

        for i in reversed(range(self.gridLayout.count())):
            widget = self.gridLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.imageCount = 0

    def searchCategories(self):

        category = self.Search.text().lower()
        filtered_artworks = [artwork for artwork in self.all_artworks if category in artwork["category"].lower()]
        self.displayImages(filtered_artworks)


    def showBasketWindow(self):

        if not self.basketWindow or not self.basketWindow.isVisible():
            self.basketWindow = BasketWindow(self.cart_items)
            self.basketWindow.show()
        else:
            self.basketWindow.raise_()
            self.basketWindow.activateWindow()

    def showPreferencesWindow(self):

        if not self.preferencesWindow or not self.preferencesWindow.isVisible():
            self.preferencesWindow = PreferencesWindow(self.prefer)
            self.preferencesWindow.show()
        else:
            self.preferencesWindow.raise_()
            self.preferencesWindow.activateWindow()


    def addImage(self, filePath, name, category, price):

        if filePath:

            container = QWidget()
            layout = QFormLayout(container)


            image_label = QLabel(self)
            pixmap = QPixmap(filePath)
            image_label.setPixmap(pixmap.scaled(300, 400))
            image_label.mousePressEvent = lambda event: self.showAnalysisWindow(filePath)
            layout.addRow(image_label)


            name_label = QLabel(f"Name: {name}")
            name_label.setFont(QFont("Times New Roman", 12))
            layout.addRow(name_label)


            category_label = QLabel(f"Category: {category}")
            category_label.setFont(QFont("Times New Roman", 12))
            layout.addRow(category_label)


            price_label = QLabel(f"Price: {price} $")
            price_label.setFont(QFont("Times New Roman", 12))
            layout.addRow(price_label)


            cart_button = QPushButton()
            cart_button.setIcon(QIcon("C:\\Users\\DELL\\Desktop\\Icons\\cart.png"))
            cart_button.setIconSize(QSize(20, 20))
            cart_button.setStyleSheet("border: none;")
            layout.addRow(cart_button)


            like_button = QPushButton()
            like_button.setIcon(QIcon("C:\\Users\\DELL\\Desktop\\Icons\\like.png"))
            like_button.setIconSize(QSize(20, 20))
            like_button.setStyleSheet("border: none;")
            layout.addRow(like_button)

            cart_button.clicked.connect(lambda: self.addToCart(filePath, name, category, price))
            like_button.clicked.connect(lambda: self.addToPrefer(filePath, name, category, price))


            self.gridLayout.addWidget(container, self.imageCount // self.columns, self.imageCount % self.columns)
            self.imageCount += 1



    def showAnalysisWindow(self, image_path):



        if not os.path.exists(image_path):
            print(f"❌ الملف غير موجود: {image_path}")
            return

        if self.analysisWindow is None or not self.analysisWindow.isVisible():
            self.analysisWindow = ColorAnalysisWindow(image_path)
            self.analysisWindow.show()
        else:
            self.analysisWindow.raise_()
            self.analysisWindow.activateWindow()


    def openChatWindow(self):

        if not self.chatWindow or not self.chatWindow.isVisible():
            self.chatWindow = ChatWindow()
            self.chatWindow.show()
        else:
            self.chatWindow.raise_()
            self.chatWindow.activateWindow()


    def addToCart(self, filePath, name, category, price):

        self.cart_items.append((filePath, name, category, price))

        msg = QMessageBox(self)
        msg.setWindowTitle("Added to Cart")
        msg.setText(f"{name} has been added to the cart!")
        msg.setStyleSheet("""
                    QMessageBox {
                        background-color: #fdf9e9  ;
                        border: 2px double #410668  ;
                    }
                    QLabel {
                        color: #410668  ;
                        font-size: 14px;
                    }
                """)

        msg.exec()

    def addToPrefer(self,filePath, name, category, price):
        self.prefer.append((filePath, name, category, price))
        msg = QMessageBox(self)
        msg.setWindowTitle("Added to your preferences page !")
        msg.setText(f"{name} has been added!")
        msg.setStyleSheet("""
                            QMessageBox {
                                background-color: #fdf9e9  ;
                                border: 2px double #410668  ;
                            }
                            QLabel {
                                color: #410668  ;
                                font-size: 14px;
                            }
                        """)

        msg.exec()

    def ShareArtWindow(self):

        if not self.detailsWindow or not self.detailsWindow.isVisible():
            self.detailsWindow = DetailsWindow(self)
            self.detailsWindow.show()
        else:

            self.detailsWindow.raise_()
            self.detailsWindow.activateWindow()




class PreferencesWindow(QWidget):
    def __init__(self, prefer_items):
        super().__init__()

        self.setWindowTitle("Your Preferences")
        self.setStyleSheet("background-color:#fffbea ;")
        self.setGeometry(200, 200, 400, 400)

        self.prefer_items = prefer_items
        layout = QVBoxLayout(self)

        if not prefer_items:
            empty_image = QLabel(self)
            pixmap = QPixmap("C:\\Users\\DELL\\Desktop\\Icons\\feedback.png")
            empty_image.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(empty_image, alignment=Qt.AlignmentFlag.AlignCenter)

            empty_label = QLabel("No items in your preferences yet!")
            empty_label.setStyleSheet("color: purple; font-size: 16px; font-weight: bold;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty_label)

        else:
            for item in prefer_items:
                filePath, name, category, price = item


                item_widget = QWidget()
                item_layout = QHBoxLayout(item_widget)


                image_label = QLabel()
                pixmap = QPixmap(filePath).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
                image_label.setPixmap(pixmap)
                item_layout.addWidget(image_label)


                details_label = QLabel(f"{name} - {category} - {price} $")
                details_label.setStyleSheet("color: green; font-size: 13px;")
                item_layout.addWidget(details_label)


                # delete_button = QPushButton()
                # delete_button.setIcon(QIcon("C:\\Users\\DELL\\Desktop\\Icons\\trash.png"))
                # delete_button.setIconSize(QSize(20, 20))
                # delete_button.setStyleSheet("background-color: transparent; border: none;")
                # delete_button.clicked.connect(partial(self.removeFromPreferences, item))
                # item_layout.addWidget(delete_button)
                #
                layout.addWidget(item_widget)

                separator = QFrame(self)
                separator.setFrameShape(QFrame.Shape.HLine)
                separator.setFrameShadow(QFrame.Shadow.Sunken)
                separator.setStyleSheet("background-color: #37045a ; height: 2px;")
                layout.addWidget(separator)

        self.setLayout(layout)

    # def removeFromPreferences(self, item):
    #
    #     self.prefer_items.remove(item)
    #     self.refreshPreferencesWindow()

    def refreshPreferencesWindow(self):

        self.setLayout(QVBoxLayout())
        self.__init__(self.prefer_items)
        self.show()





class BasketWindow(QWidget):
    def __init__(self, cart_items):
        super().__init__()

        self.setWindowTitle("Shopping Cart")
        self.setStyleSheet("background-color:#fffbea ;")
        self.setGeometry(200, 200, 400, 400)

        self.cart_items = cart_items
        layout = QVBoxLayout(self)

        total_price = 0

        if not cart_items:

            empty_image = QLabel(self)
            pixmap = QPixmap("C:\\Users\\DELL\\Desktop\\Icons\\shopping.png")
            empty_image.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(empty_image , alignment=Qt.AlignmentFlag.AlignCenter)


            empty_label = QLabel("Your cart is empty! \n Please add some items.")
            empty_label.setStyleSheet("color: purple; font-size: 16px; font-weight: bold;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty_label)



        else:
            for item in cart_items:
                filePath, name, category, price = item
                total_price += float(price)


                item_widget = QWidget()
                item_layout = QHBoxLayout(item_widget)


                image_label = QLabel()
                pixmap = QPixmap(filePath).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
                image_label.setPixmap(pixmap)
                item_layout.addWidget(image_label)


                details_label = QLabel(f"{name} - {category} - {price} $")
                details_label.setStyleSheet("color: green; font-size: 13px;")
                item_layout.addWidget(details_label)


                delete_button = QPushButton()
                delete_button.setIcon(QIcon("C:\\Users\\DELL\\Desktop\\Icons\\trash.png"))
                delete_button.setIconSize(QSize(20, 20))
                delete_button.setStyleSheet("background-color: transparent; border: none;")
                delete_button.clicked.connect(partial(self.removeFromCart, item))
                item_layout.addWidget(delete_button)

                layout.addWidget(item_widget)

                separator = QFrame(self)
                separator.setFrameShape(QFrame.Shape.HLine)
                separator.setFrameShadow(QFrame.Shadow.Sunken)
                separator.setStyleSheet("background-color: blue; height: 2px;")
                layout.addWidget(separator)


            total_label = QLabel(f"Total Price: {total_price:.2f} $")
            total_label.setStyleSheet("color: blue; font-size: 14px; font-weight: bold; margin-top: 10px;")
            layout.addWidget(total_label)

        self.setLayout(layout)

    def removeFromCart(self, item):

        self.cart_items.remove(item)
        self.updateBasketWindow()

    def updateBasketWindow(self):

        self.close()
        self.__init__(self.cart_items)
        self.show()

class DetailsWindow(QWidget):
    def __init__(self, galleryWindow):
        super().__init__()
        loadUi("Details.ui", self)
        self.db = MongoDBHandler("Arts_system", "Artworks")
        self.galleryWindow = galleryWindow
        self.ChoosePhoto.clicked.connect(self.showDialog)

    def showDialog(self):
        if not self.Price.text().strip() or not self.ArtName.text().strip() or not self.ComboCategory.currentText():
            self.showMessage("Alert!")
            return

        fileName, _ = QFileDialog.getOpenFileName(self, "اختر صورة", "", "Image Files (*.png *.jpg *.bmp)")
        if fileName:
            self.galleryWindow.addImage(fileName, self.ArtName.text().strip(), self.ComboCategory.currentText(),
                                        self.Price.text().strip())

            self.db.insert_artwork(fileName, self.ArtName.text().strip(), self.ComboCategory.currentText(),
                                   self.Price.text().strip())

            self.close()

    def showMessage(self, message):

        self.msgBox = MessageBox2()
        self.msgBox.showMessage(message)
        self.msgBox.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

