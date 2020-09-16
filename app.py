class App(QtWidgets.QWidget):
    """
    Classe de notre fenetre principale
    QtWidget permet d'avoir acces a plusieurs Widgets
    """
    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()     #nos widgets
        self.setup_css()    #notre style
        self.set_default_values()   #valeur par defaut
        self.setup_connections()    #action lors d'interaction

    def setup_ui(self):
        """methode pour creer les differents element de notre UI"""

        # CREATION DU LAYOUT
        self.layout = QtWidgets.QHBoxLayout(self) #le layout prend la fenetre principal en argument donc notre self

        # CREATION DES WIDGETS
        self.cbb_devisesFrom = QtWidgets.QComboBox() #combobox (liste deroulante) pour choisir la devise From
        self.spn_montant = QtWidgets.QSpinBox() #spinbox (zone affichage) du montant a convertir
        self.cbb_devisesTo = QtWidgets.QComboBox() #cbb pour choisir la devise To
        self.spn_montantConverti = QtWidgets.QSpinBox() #spn du montant converti
        self.btn_inverser = QtWidgets.QPushButton("Inverser devises") #bouton pour inverser les devises

        # AJOUT AU LAYOUT
        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def setup_css(self):
        """methode pour definir le style de notre UI"""
        
        # style de notre interface
        self.setStyleSheet("""
        background-color: rgb(30,30,30);
        color: rgb(240,240,240);
        """)

        # style de nos combobox
        style = """
        QComboBox::down-arrow {
            image: none;
            border-width: 0px;
        }
        QComboBox::drop-down {
            border-width: 0px;
        } 
        """
        self.cbb_devisesFrom.setStyleSheet(style)
        self.cbb_devisesTo.setStyleSheet(style)

        # style de notre bouton
        self.btn_inverser.setStyleSheet("background-color: blue")

    def set_default_values(self):
        """
        methode pour initialiser l'affichage et les valeurs par default de nos widget
        """
        
        # ajout liste de devises a la combobox
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))
        # affichage par defaut cbb
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")

        # choix montant max de la spinbox
        self.spn_montant.setRange(0,1000000)
        self.spn_montantConverti.setRange(0,1000000)
        # affichage par defaut spn
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    def setup_connections(self):
        """
        methode pour connecter les Widget a l'action a effectuer 
        lorsque l'on clique sur les boutons 
        ou lorsque l'on modifie les valeurs des elements des combobox
        """
        # Lorsque l'on choisi une devise dans la cbb
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        # Lorsque l'on change le montant dans la spn
        self.spn_montant.valueChanged.connect(self.compute)
        self.spn_montantConverti.valueChanged.connect(self.compute)
        
        # Lorsque l'on clique sur le bouton 
        self.btn_inverser.clicked.connect(self.inverser_devise) 

    def compute(self):
        """
        methode a executer lorsque l'on change la devise dans les combobox 
        cbb_devisesFrom et cbb_devisesTo 
        """
        montant = self.spn_montant.value() #recuperation de la valeur de la spn
        devise_from = self.cbb_devisesFrom.currentText() #recuperation de la valeur de la cbb
        devise_to = self.cbb_devisesTo.currentText()
        
        # on effectue la conversion grace a currency_converter 
        # on fait une gestion d'erreur pour eviter les conversions non trouvees
        try : 
            """on essaie"""
            resultat = self.c.convert(montant, devise_from, devise_to)

        except currency_converter.currency_converter.RateNotFoundError :
            """si erreur"""
            print("le taux de conversion n'a pas ete trouve")
        
        else : 
            """si pas d'erreur"""
            self.spn_montantConverti.setValue(resultat) #affichage dans la cbb
        
    def inverser_devise(self):
        """methode a executer lorsque l'on clique sur le bouton btn_inverser"""
        
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)
        
        # Une fois inversee on recalcule en appelant compute
        self.compute()

# create an application PySide 
app = QtWidgets.QApplication([])

# create a window on my app
win = App()
win.show()

# execute the app
app.exec_() 