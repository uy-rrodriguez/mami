#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowMenu :                                                           #
#        Implémente le menu principal de l'interface.                       #
#        Pour gérer les différentes actions qui peuvent être exécutés       #
#        dans cette fenêtre, on implémente le modèle de programmation       #
#        State. De cette manière on gère les différentes situations de      #
#        simple. Par exemple, on aura un état pour parcourir les menus,     #
#        un autre pour afficher les serveurs, ou pour la configuration.     #
#                                                                           #
#############################################################################

import curses
from lxml import etree as ET

#from os import sys, path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from objets.arraydataobject import ArrayDataObject
from window import *
from config import *
from mail import *



#############################################################################
#    BaseState. Classe de base pour tous les états.                         #
#############################################################################

# Abstraite
import abc
class BaseState():
    # metaclasse pour pouvoir définir une classe abstraite
    __metaclass__ = abc.ABCMeta

    # Fichier contenant les messages à afficher dans les menus
    XML_CONFIG_FILE = "interface/interface.xml"

    # Instance pour gérer le singleton
    inst = None

    # Touches utiles
    KEY_ENTER = 10
    KEY_ESCAPE = 27
    KEY_BACKSPACE = 263

    def __init__(self, context):
        self.context = context

        # Lecture du fichier avec les titres et descriptifs des menus
        f = open(self.XML_CONFIG_FILE, "r")
        self.contents = f.read()
        self.root = ET.fromstring(self.contents)
        f.close()

    # Fonction à exécuter pour changer à un état
    def change_to(self):
        self.context.state = self

    @classmethod
    def instance(cls, context):
        if cls.inst == None:
            cls.inst = cls(context)
        return cls.inst

    @abc.abstractmethod
    def handle_key(self, key):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def render(self):
        pass


#############################################################################
#    BaseMenuState. Classe de base pour les états qui ont des menus.        #
#############################################################################

# Classe représentant un lien vers un autre menu
class Link():
    def __init__(self, name, label):
        self.name = name
        self.label = label

class BaseMenuState(BaseState):
    def __init__(self, context):
        super(BaseMenuState, self).__init__(context)
        self.title = ""
        self.text = ""
        self.links = []
        self.selected = 0

        # Relations entre les options des menus et les états
        self.keys_states = {
            "win_servers":         ServersState,
            "win_config_crises":   ConfigCrisisState,
            "win_config_emails":   ConfigEmailState,
            "win_emails_test":     ConfigEmailTestState
        }

        # Premier menu
        self.load_menu("main")

    def handle_key(self, key):
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1

        elif key == self.KEY_ESCAPE:
            self.load_menu("main")

        elif key == self.KEY_ENTER:
            win_name = self.links[self.selected].name

            # Changement d'état
            if win_name in self.keys_states:
                self.keys_states[win_name].instance(self.context).change_to()
            else:
                self.load_menu(win_name)

    def update(self):
        pass

    def render(self):
        self.context.println(self.title)
        self.context.println("-------------------------------------")
        self.context.print_long(self.text)
        self.context.println()

        # Affichage des options
        for i in range(0, len(self.links)):
            if i == self.selected and self.context.hasFocus:
                self.context.println(self.links[i].label,
                                     self.context.COLOR_SELECTED)
            else:
                self.context.println(self.links[i].label,
                                     self.context.COLOR_NOSELECTED)

        self.context.println()

    # Fonction pour charger l'information d'un menu depuis le fichier XML de configuration
    def load_menu(self, win):
        if win != "main":
            win = "windows/" + win

        self.links = []
        self.selected = 0

        data = self.root.find(win)
        self.title = data.find("title").text
        self.text = data.find("text").text
        for c in list(data.find("links")):
            self.links.append(Link(c.tag, c.text))


#############################################################################
#    ServersState. État pour gérer la liste de serveurs.                    #
#############################################################################

class ServersState(BaseState):
    def __init__(self, context):
        super(ServersState, self).__init__(context)
        self.title = self.root.find("./windows/win_servers/title").text
        self.text = self.root.find("./windows/win_servers/text").text
        self.servers = []
        self.links = []
        self.selected = 0

    def change_to(self):
        super(ServersState, self).change_to()

        # Chargement des serveurs (lecture de la BD)
        self.servers = []
        self.links = []
        for elem in self.context.db.get_all("server"):
            s = ArrayDataObject()
            s.name = elem["name"]
            s.ip = elem["ip"]
            s.uptime = elem["uptime"]
            self.servers.append(s)
            self.links.append(Link(s.name, s.name))

        # Option pour aller en arrière
        self.links.append(Link("back", "Retour"))

    def handle_key(self, key):
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1

        elif key == self.KEY_BACKSPACE:
            self.back_to_menu()

        elif key == self.KEY_ENTER:
            # Changement d'état
            if self.links[self.selected].name == "back":
                self.back_to_menu()
            else:
                self.context.select_server(self.servers[self.selected])

        elif key == self.KEY_ESCAPE:
            self.back_to_menu()

    def back_to_menu(self):
        BaseMenuState.instance(self.context).change_to()

    def update(self):
        pass

    def render(self):
        self.context.println(self.title)
        self.context.println("-------------------------------------")
        self.context.print_long(self.text)
        self.context.println()

        # Render options
        for i in range(0, len(self.links)):
            if i == self.selected and self.context.hasFocus:
                self.context.println(self.links[i].label,
                                     self.context.COLOR_SELECTED)
            else:
                self.context.println(self.links[i].label,
                                     self.context.COLOR_NOSELECTED)

        self.context.println()


#############################################################################
#    BaseConfigState. État de base pour la configuration.                   #
#############################################################################

# Classe représentant un paramètre qui peut être configuré
class ParamConfig(object):
    def __init__(self, key, value, description):
        self.key = key
        self.value = value
        self.description = description

    def append(self, c):
        self.value += c

    def suppr(self):
        self.value = self.value[:-1]

class BaseConfigState(BaseState):
    MAX_CLOCK_CURSOR = 10

    def __init__(self, context, title, text):
        super(BaseConfigState, self).__init__(context)
        self.title = title
        self.text = text

        # Chaque fenêtre peut avoir plus d'un paramètre à configurer
        self.params = []
        self.selected = 0

        # Pour imiter le curseur pendant qu'on écrit
        self.reset_cursor()

        # On charge la configuration actuelle
        self.config = Config()

    def reset_cursor(self):
        self.cursor = True
        self.clock_cursor = self.MAX_CLOCK_CURSOR

    def handle_key(self, key):
        # [Entrer] sauvegarde la configuraion et retourne au menu
        # [Backspace] supprime le dernier caractère
        # [Up] et [Down] changent l'élement choisi
        # Les autres touches sont pour écrire dans l'élement choisi
        if key == self.KEY_ENTER:
            self.save_config()
            self.__class__.inst = None
            BaseMenuState.instance(self.context).change_to()

        elif key == self.KEY_ESCAPE:
            self.__class__.inst = None
            BaseMenuState.instance(self.context).change_to()

        elif key == curses.KEY_DOWN and self.selected < len(self.params) - 1:
            self.selected += 1
            self.reset_cursor()
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
            self.reset_cursor()

        elif key == self.KEY_BACKSPACE:
            self.params[self.selected].suppr()
        elif key in range(128):
            self.params[self.selected].append(chr(key))

    def update(self):
        # Pour l'imitation du curseur
        self.clock_cursor -= 1
        if self.clock_cursor == 0:
            self.clock_cursor = self.MAX_CLOCK_CURSOR
            self.cursor = not self.cursor

    def render(self):
        self.context.println(self.title)
        self.context.println("-" * 40)
        self.context.print_long(self.text)
        self.context.println()

        # Affichage de la config actuelle
        # et imitation du curseur
        for i in range(len(self.params)):
            param = self.params[i]
            self.context._print(param.description + " :  ")
            if i == self.selected and self.context.hasFocus:
                self.context._print(param.value, self.context.COLOR_SELECTED)
                self.render_cursor()
            else:
                self.context.println(param.value)

        # Lecture de la nouvelle config
        self.context.println()

    def render_cursor(self):
        if self.cursor:
            self.context.println("|", self.context.COLOR_SELECTED)
        else:
            self.context.println(" ", self.context.COLOR_SELECTED)

    def save_config(self):
        # On stocke dans le xml les valeurs écrites pour les paramètres
        for param in self.params:
            self.config.set(param.key, param.value)
        self.config.save()


#############################################################################
#    Classes spécifiques pour les différentes options de configuration.     #
#############################################################################

class ConfigCrisisState(BaseConfigState):
    def __init__(self, context):
        super(ConfigCrisisState, self).__init__(context,
            "Configuration des situations de crise",
            "Ici, vous pouvez configurer vos situations de crise. Chaque valeur correspond au pourcentage maximal tolere.")
        self.params = [ParamConfig("crisis/max_cpu", self.config.get("crisis/max_cpu"), "Max. CPU"),
                       ParamConfig("crisis/max_ram", self.config.get("crisis/max_ram"), "Max. RAM"),
                       ParamConfig("crisis/max_swap", self.config.get("crisis/max_swap"), "Max. swap"),
                       ParamConfig("crisis/max_disk", self.config.get("crisis/max_disk"), "Max. disque")]

class ConfigEmailState(BaseConfigState):
    def __init__(self, context):
        super(ConfigEmailState, self).__init__(context,
            "Configuration d'adresses email",
            "Ici, vous pouvez configurer l'adresse email de l'administrateur et le fichier à utiliser comme template.")
        self.params = [ParamConfig("email/address", self.config.get("email/address"), "Adresse email"),
                       ParamConfig("email/subject", self.config.get("email/subject"), "Sujet du message"),
                       ParamConfig("email/template_html", self.config.get("email/template_html"), "Fichier template HTML"),
                       ParamConfig("email/template_txt", self.config.get("email/template_txt"), "Fichier template texte")]

class ConfigEmailTestState(BaseConfigState):
    def __init__(self, context):
        super(ConfigEmailTestState, self).__init__(context,
                                                "Test d'envoie d'un email en cas de crise",
                                                "Tapez [Entrer] pour envoyer un email de test. \n Tapez [Esc] pour retourner au menu.")
        self.msg = ""

    def change_to(self):
        super(ConfigEmailTestState, self).change_to()
        self.msg = ""

    def handle_key(self, key):
        # [Entrer] envoie un email de test et retourne au menu
        # [Backspace] annule l'envoi et retourne au menu
        if key == self.KEY_ENTER:
            self.msg = ""
            try:
                m = Mail()
                m.send(self.config.get("email/address"),
                       self.config.get("email/subject"),
                       self.config.get("email/template_html"),
                       self.config.get("email/template_txt"))

                #BaseMenuState.instance(self.context).change_to()
                self.msg = "Mail de test envoye"

            except Exception as e:
                self.msg = e

        elif key == self.KEY_ESCAPE:
            BaseMenuState.instance(self.context).change_to()

    def render(self):
        super(ConfigEmailTestState, self).render()
        self.context.println(self.msg, self.context.COLOR_SELECTED)


#############################################################################
#    WindowMenu.                                                            #
#############################################################################

class WindowMenu(Window):
    def __init__(self, parent, stdscr, height, width, y, x, dataBaseInstance):
        super(WindowMenu, self).__init__(parent, stdscr, height, width, y, x)
        self.db = dataBaseInstance
        self.state = BaseMenuState.instance(self)

    def set_servers(self, servers):
        self.servers = servers

    def action_change_menu(self, attribs):
        if attribs[0] == ACTION_MAIN:
            self.load_menu(WINDOW_MAIN)
        else:
            self.load_menu(BASE_WINDOWS + attribs[0])


    # Quand on choisit un serveur dans le menu, il faut envoyer un message à
    # la fenêtre qui affiche les stats, pour qu'elle puisse afficher les
    # données qui correspondent
    def select_server(self, server):
        self.interface.change_server(server)


    def handle_key(self, key):
        if not self.hasFocus:
            return
        self.state.handle_key(key)

    def update(self):
        self.state.update()

    def render(self):
        self.clear()
        self.state.render()
