# -*- coding: utf-8 -*

from kivy.config import Config
# ウィンドウサイズの設定
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '720')
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.properties import Clock
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.resources import resource_add_path
from kivy.factory import Factory
from kivy.clock import Clock

import os
import csv
import codecs
import time
import math
import glob
import pygame.mixer
import datetime
import urllib.request
import json
import requests
from dateutil.relativedelta import relativedelta

# ファイルのパス(main.pyがあるフォルダの中にあるファイルの絶対パス)
# file_path = os.path.dirname(os.path.abspath(__file__))

# フォントの設定
resource_add_path('fonts')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')


# 各種データ一時保存用
class Holder():
    
    def getType():
        pass


class PopupList(BoxLayout):
    """結果を表示するためのポップアップウィンドウ"""

    # 現在のカレントディレクトリ。FileChooserIconViewのpathに渡す
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    cancel = ObjectProperty(None)
    popup_text = StringProperty("")

    # ポップアップウィンドウのラベルに引数の文字列をセットするためのクラスメソッド
    @classmethod
    def setText(self, txt):
        self.popup_text = txt

class SearchList(BoxLayout):
    """検索結果を表示するためのポップアップウィンドウ"""

    cancel = ObjectProperty(None)
    popup_text = StringProperty("")
    
    # ポップアップウィンドウのラベルに引数の文字列をセットするためのクラスメソッド
    @classmethod
    def setText(self, txt):
        self.popup_text = txt


class Type_checker(BoxLayout):

    attack_color = ListProperty()
    attack_list = [] # attackのタイプを格納するリスト(1つだけ)
    defense_color1 = ListProperty()
    defense_color2 = ListProperty()
    defense_index = 0 # defenseの下の2つのラベルのどちらを指すかのインデックス
    defense_list = [] # defenseのタイプを格納するリスト(2つまで格納)

    # タイプ相性の各倍率(18タイプ×18タイプ)
    # ノーマル[0],ほのお[1],みず[2],でんき[3],くさ[4],こおり[5],かくとう[6],どく[7],じめん[8],
    #   ひこう[9],エスパー[10],むし[11],いわ[12],ゴースト[13],ドラゴン[14],あく[15],はがね[16],フェアリー[17] (縦もこの順)
    effect = [
        [1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5,1],
        [1,0.5,0.5,1,2,2,1,1,1,1,1,2,0.5,1,0.5,1,2,1],
        [1,2,0.5,1,0.5,1,1,1,2,1,1,1,2,1,0.5,1,1,1],
        [1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1,1],
        [1,0.5,2,1,0.5,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5,1],
        [1,0.5,0.5,1,2,0.5,1,1,2,2,1,1,1,1,2,1,0.5,1],
        [2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2,0.5],
        [1,1,1,1,2,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0,2],
        [1,2,1,2,0.5,1,1,2,1,0,1,0.5,2,1,1,1,2,1],
        [1,1,1,0.5,2,1,2,1,1,1,1,2,0.5,1,1,1,0.5,1],
        [1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5,1],
        [1,0.5,1,1,2,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5,0.5],
        [1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5,1],
        [0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5,0],
        [1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,1,0.5],
        [1,0.5,0.5,0.5,1,2,1,1,1,1,1,1,2,1,1,1,0.5,2],
        [1,0.5,1,1,1,1,2,0.5,1,1,1,1,1,1,2,2,0.5,1]
    ]

    type_list = ["nor","fir","wat","ele","gra","ice","fig","poi","gro","fly","psy","bug","roc","gho","dra","dar","ste","fai"]

    # ボタンの色の濃さの変更用
    sela_nor = ObjectProperty(int())
    sela_fir = ObjectProperty(int())
    sela_wat = ObjectProperty(int())
    sela_ele = ObjectProperty(int())
    sela_gra = ObjectProperty(int())
    sela_ice = ObjectProperty(int())
    sela_fig = ObjectProperty(int())
    sela_poi = ObjectProperty(int())
    sela_gro = ObjectProperty(int())
    sela_fly = ObjectProperty(int())
    sela_psy = ObjectProperty(int())
    sela_bug = ObjectProperty(int())
    sela_roc = ObjectProperty(int())
    sela_gho = ObjectProperty(int())
    sela_dra = ObjectProperty(int())
    sela_dar = ObjectProperty(int())
    sela_ste = ObjectProperty(int())
    sela_fai = ObjectProperty(int())

    seld_nor = ObjectProperty(int())
    seld_fir = ObjectProperty(int())
    seld_wat = ObjectProperty(int())
    seld_ele = ObjectProperty(int())
    seld_gra = ObjectProperty(int())
    seld_ice = ObjectProperty(int())
    seld_fig = ObjectProperty(int())
    seld_poi = ObjectProperty(int())
    seld_gro = ObjectProperty(int())
    seld_fly = ObjectProperty(int())
    seld_psy = ObjectProperty(int())
    seld_bug = ObjectProperty(int())
    seld_roc = ObjectProperty(int())
    seld_gho = ObjectProperty(int())
    seld_dra = ObjectProperty(int())
    seld_dar = ObjectProperty(int())
    seld_ste = ObjectProperty(int())
    seld_fai = ObjectProperty(int())


    # アプリ実行時の初期化の処理
    def __init__(self, **kwargs):
        super(Type_checker, self).__init__(**kwargs)
        Clock.schedule_once(self.on_start)

        
    def on_start(self, *args):
        self.attack_color = [1, 1, 1, 1]
        self.defense_color1 = [1, 1, 1, 1]
        self.defense_color2 = [1, 1, 1, 1]
        self.defense_index = 0
        self.attack_list = [""] * 1
        self.defense_list = [""] * 2
        self.init_btn()
        

    def init_btn(self):
        """ボタンの濃さを初期化する"""

        self.sela_nor = 0.6
        self.sela_fir = 0.6
        self.sela_wat = 0.6
        self.sela_ele = 0.6
        self.sela_gra = 0.6
        self.sela_ice = 0.6
        self.sela_fig = 0.6
        self.sela_poi = 0.6
        self.sela_gro = 0.6
        self.sela_fly = 0.6
        self.sela_psy = 0.6
        self.sela_bug = 0.6
        self.sela_roc = 0.6
        self.sela_gho = 0.6
        self.sela_dra = 0.6
        self.sela_dar = 0.6
        self.sela_ste = 0.6
        self.sela_fai = 0.6

        self.seld_nor = 0.6
        self.seld_fir = 0.6
        self.seld_wat = 0.6
        self.seld_ele = 0.6
        self.seld_gra = 0.6
        self.seld_ice = 0.6
        self.seld_fig = 0.6
        self.seld_poi = 0.6
        self.seld_gro = 0.6
        self.seld_fly = 0.6
        self.seld_psy = 0.6
        self.seld_bug = 0.6
        self.seld_roc = 0.6
        self.seld_gho = 0.6
        self.seld_dra = 0.6
        self.seld_dar = 0.6
        self.seld_ste = 0.6
        self.seld_fai = 0.6


    # タイプのボタンを押した時の処理
    def select(self, _side, _type, _color):
        # defender
        if _side == "d":
            # すでに選択されているタイプの場合、そこを空白にする
            if _type in self.defense_list:
                self.defense_index = self.defense_list.index(_type)
                self.defense_list[self.defense_index] = ""
                if self.defense_index == 0:
                    self.defense_color1 = [1, 1, 1, 1]
                elif self.defense_index == 1:
                    self.defense_color2 = [1, 1, 1, 1]

            # そうでなければ2つ目のラベルをそのタイプに更新する
            else:
                if self.defense_index == 0:
                    self.defense_color1 = _color
                    self.defense_list[0] = _type
                    self.defense_index = 1
                elif self.defense_index == 1:
                    self.defense_color2 = _color
                    self.defense_list[1] = _type

            # 両方とも空白である/になった場合には1つ目のラベルが更新されるようにする
            if self.defense_list[0] == '' and self.defense_list[1] == '':
                self.defense_index = 0


        # attacker  
        if _side == "a":
            # すでに選択されているタイプの場合そこを空白にする
            if _type in self.attack_list:
                self.attack_list[0] = ""
                self.attack_color = [1, 1, 1, 1]

            # そうでなければ選んだタイプで更新していく
            else:
                self.attack_color = _color
                self.attack_list[0] = _type


        # 選択しているタイプのボタンを濃くする
        self.init_btn()

        self.sel_type("d", self.defense_list[0])
        self.sel_type("d", self.defense_list[1])
        self.sel_type("a", self.attack_list[0])


    def sel_type(self, _side, _type):
        """押したボタンの色を濃くする"""

        if _side == "" or _type == "":
            pass

        else:

            if _side == "d" and _type == "nor":
                self.seld_nor = 1
            if _side == "d" and _type == "fir":
                self.seld_fir = 1
            if _side == "d" and _type == "wat":
                self.seld_wat = 1
            if _side == "d" and _type == "gra":
                self.seld_gra = 1
            if _side == "d" and _type == "ele":
                self.seld_ele = 1
            if _side == "d" and _type == "ice":
                self.seld_ice = 1
            if _side == "d" and _type == "fig":
                self.seld_fig = 1
            if _side == "d" and _type == "poi":
                self.seld_poi = 1
            if _side == "d" and _type == "gro":
                self.seld_gro = 1
            if _side == "d" and _type == "fly":
                self.seld_fly = 1
            if _side == "d" and _type == "psy":
                self.seld_psy = 1
            if _side == "d" and _type == "bug":
                self.seld_bug = 1
            if _side == "d" and _type == "roc":
                self.seld_roc = 1
            if _side == "d" and _type == "gho":
                self.seld_gho = 1
            if _side == "d" and _type == "dra":
                self.seld_dra = 1
            if _side == "d" and _type == "dar":
                self.seld_dar = 1
            if _side == "d" and _type == "ste":
                self.seld_ste = 1
            if _side == "d" and _type == "fai":
                self.seld_fai = 1

            if _side == "a" and _type == "nor":
                self.sela_nor = 1
            if _side == "a" and _type == "fir":
                self.sela_fir = 1
            if _side == "a" and _type == "wat":
                self.sela_wat = 1
            if _side == "a" and _type == "gra":
                self.sela_gra = 1
            if _side == "a" and _type == "ele":
                self.sela_ele = 1
            if _side == "a" and _type == "ice":
                self.sela_ice = 1
            if _side == "a" and _type == "fig":
                self.sela_fig = 1
            if _side == "a" and _type == "poi":
                self.sela_poi = 1
            if _side == "a" and _type == "gro":
                self.sela_gro = 1
            if _side == "a" and _type == "fly":
                self.sela_fly = 1
            if _side == "a" and _type == "psy":
                self.sela_psy = 1
            if _side == "a" and _type == "bug":
                self.sela_bug = 1
            if _side == "a" and _type == "roc":
                self.sela_roc = 1
            if _side == "a" and _type == "gho":
                self.sela_gho = 1
            if _side == "a" and _type == "dra":
                self.sela_dra = 1
            if _side == "a" and _type == "dar":
                self.sela_dar = 1
            if _side == "a" and _type == "ste":
                self.sela_ste = 1
            if _side == "a" and _type == "fai":
                self.sela_fai = 1

            """
            if _side == "d" and _type == "nor":
                if self.seld_nor == 0.6: self.seld_nor = 1
                else: self.seld_nor = 0.6
            if _side == "d" and _type == "fir":
                if self.seld_fir == 0.6: self.seld_fir = 1
                else: self.seld_fir = 0.6
            if _side == "d" and _type == "wat":
                if self.seld_wat == 0.6: self.seld_wat = 1
                else: self.seld_wat = 0.6
            if _side == "d" and _type == "gra":
                if self.seld_gra == 0.6: self.seld_gra = 1
                else: self.seld_gra = 0.6
            if _side == "d" and _type == "ele":
                if self.seld_ele == 0.6: self.seld_ele = 1
                else: self.seld_ele = 0.6
            if _side == "d" and _type == "ice":
                if self.seld_ice == 0.6: self.seld_ice = 1
                else: self.seld_ice = 0.6
            if _side == "d" and _type == "fig":
                if self.seld_fig == 0.6: self.seld_fig = 1
                else: self.seld_fig = 0.6
            if _side == "d" and _type == "poi":
                if self.seld_poi == 0.6: self.seld_poi = 1
                else: self.seld_poi = 0.6
            if _side == "d" and _type == "gro":
                if self.seld_gro == 0.6: self.seld_gro = 1
                else: self.seld_gro = 0.6
            if _side == "d" and _type == "fly":
                if self.seld_fly == 0.6: self.seld_fly = 1
                else: self.seld_fly = 0.6
            if _side == "d" and _type == "psy":
                if self.seld_psy == 0.6: self.seld_psy = 1
                else: self.seld_psy = 0.6
            if _side == "d" and _type == "bug":
                if self.seld_bug == 0.6: self.seld_bug = 1
                else: self.seld_bug = 0.6
            if _side == "d" and _type == "roc":
                if self.seld_roc == 0.6: self.seld_roc = 1
                else: self.seld_roc = 0.6
            if _side == "d" and _type == "gho":
                if self.seld_gho == 0.6: self.seld_gho = 1
                else: self.seld_gho = 0.6
            if _side == "d" and _type == "dra":
                if self.seld_dra == 0.6: self.seld_dra = 1
                else: self.seld_dra = 0.6
            if _side == "d" and _type == "dar":
                if self.seld_dar == 0.6: self.seld_dar = 1
                else: self.seld_dar = 0.6
            if _side == "d" and _type == "ste":
                if self.seld_ste == 0.6: self.seld_ste = 1
                else: self.seld_ste = 0.6
            if _side == "d" and _type == "fai":
                if self.seld_fai == 0.6: self.seld_fai = 1
                else: self.seld_fai = 0.6

            if _side == "a" and _type == "nor":
                if self.sela_nor == 0.6: self.sela_nor = 1
                else: self.sela_nor = 0.6
            if _side == "a" and _type == "fir":
                if self.sela_fir == 0.6: self.sela_fir = 1
                else: self.sela_fir = 0.6
            if _side == "a" and _type == "wat":
                if self.sela_wat == 0.6: self.sela_wat = 1
                else: self.sela_wat = 0.6
            if _side == "a" and _type == "gra":
                if self.sela_gra == 0.6: self.sela_gra = 1
                else: self.sela_gra = 0.6
            if _side == "a" and _type == "ele":
                if self.sela_ele == 0.6: self.sela_ele = 1
                else: self.sela_ele = 0.6
            if _side == "a" and _type == "ice":
                if self.sela_ice == 0.6: self.sela_ice = 1
                else: self.sela_ice = 0.6
            if _side == "a" and _type == "fig":
                if self.sela_fig == 0.6: self.sela_fig = 1
                else: self.sela_fig = 0.6
            if _side == "a" and _type == "poi":
                if self.sela_poi == 0.6: self.sela_poi = 1
                else: self.sela_poi= 0.6
            if _side == "a" and _type == "gro":
                if self.sela_gro == 0.6: self.sela_gro = 1
                else: self.sela_gro = 0.6
            if _side == "a" and _type == "fly":
                if self.sela_fly == 0.6: self.sela_fly = 1
                else: self.sela_fly = 0.6
            if _side == "a" and _type == "psy":
                if self.sela_psy == 0.6: self.sela_psy = 1
                else: self.sela_psy = 0.6
            if _side == "a" and _type == "bug":
                if self.sela_bug == 0.6: self.sela_bug = 1
                else: self.sela_bug = 0.6
            if _side == "a" and _type == "roc":
                if self.sela_roc == 0.6: self.sela_roc = 1
                else: self.sela_roc = 0.6
            if _side == "a" and _type == "gho":
                if self.sela_gho == 0.6: self.sela_gho = 1
                else: self.sela_gho = 0.6
            if _side == "a" and _type == "dra":
                if self.sela_dra == 0.6: self.sela_dra = 1
                else: self.sela_dra = 0.6
            if _side == "a" and _type == "dar":
                if self.sela_dar == 0.6: self.sela_dar = 1
                else: self.sela_dar = 0.6
            if _side == "a" and _type == "ste":
                if self.sela_ste == 0.6: self.sela_ste = 1
                else: self.sela_ste = 0.6
            if _side == "a" and _type == "fai":
                if self.sela_fai == 0.6: self.sela_fai = 1
                else: self.sela_fai = 0.6
            """


    # 選択された相性のチェック
    def result(self):
        """選択されたタイプの相性を各パターン(Attackのみ、defenseのみ、両方ある)ごとに計算"""

        # 効果はばつぐん/ふつう/いまひとつ/無いの判定結果を格納するリスト
        super_e_4 = [] # super effective (×4)
        super_e = [] # super effective (×2)
        normal_e = [] # normal effective (×1)
        not_very_e = [] # not very effective (×0.5)
        not_very_e_q = [] # not very effective (×0.25, quarter)
        no_e = [] # no effective (×0)

        # defenseのみ選択されている時 = 自分のポケモンに対し、相手の技がどのタイプだと相性はどうなるか
        if self.attack_list[0] == "":
            #super_e_4.append("\n    ")
            #super_e.append("\n    ")
            #normal_e.append("\n    ")
            #not_very_e.append("\n    ")
            #not_very_e_q.append("\n    ")
            #no_e.append("\n    ")
            
            for attack_type in self.type_list:
                if self.calculate(attack_type, self.defense_list[0]) * self.calculate(attack_type, self.defense_list[1]) == 4:
                    super_e_4.append(attack_type)

                elif self.calculate(attack_type, self.defense_list[0]) * self.calculate(attack_type, self.defense_list[1]) == 2:
                    super_e.append(attack_type)

                elif self.calculate(attack_type, self.defense_list[0]) * self.calculate(attack_type, self.defense_list[1]) == 1:
                    normal_e.append(attack_type)

                elif self.calculate(attack_type, self.defense_list[0]) * self.calculate(attack_type, self.defense_list[1]) == 0.5:
                    not_very_e.append(attack_type)

                elif self.calculate(attack_type, self.defense_list[0]) * self.calculate(attack_type, self.defense_list[1]) == 0.25:
                    not_very_e_q.append(attack_type)

                elif self.calculate(attack_type, self.defense_list[0]) * self.calculate(attack_type, self.defense_list[1]) == 0:
                    no_e.append(attack_type)

        # attackのみ選択されている時 = 技を使う時、相手のポケモンのタイプがどうであると相性はどうなるか
        elif self.defense_list[0] == "" and self.defense_list[1] == "":
            #super_e.append("\n    ")
            #normal_e.append("\n    ")
            #not_very_e.append("\n    ")
            #no_e.append("\n    ")
            
            for defense_type in self.type_list:
                if self.calculate(self.attack_list[0], defense_type) == 2:
                    super_e.append(defense_type)

                elif self.calculate(self.attack_list[0], defense_type) == 1:
                    normal_e.append(defense_type)

                elif self.calculate(self.attack_list[0], defense_type) == 0.5:
                    not_very_e.append(defense_type)

                elif self.calculate(self.attack_list[0], defense_type) == 0:
                    no_e.append(defense_type)

        # 両方とも選択されている時 = ある技で相手を攻撃した場合の相性の確認
        else:
            if self.calculate(self.attack_list[0], self.defense_list[0]) * self.calculate(self.attack_list[0], self.defense_list[1]) == 4:
                super_e_4.append("◯")

            elif self.calculate(self.attack_list[0], self.defense_list[0]) * self.calculate(self.attack_list[0], self.defense_list[1]) == 2:
                super_e.append("◯")

            elif self.calculate(self.attack_list[0], self.defense_list[0]) * self.calculate(self.attack_list[0], self.defense_list[1]) == 1:
                normal_e.append("◯")

            elif self.calculate(self.attack_list[0], self.defense_list[0]) * self.calculate(self.attack_list[0], self.defense_list[1]) == 0.5:
                not_very_e.append("◯")

            elif self.calculate(self.attack_list[0], self.defense_list[0]) * self.calculate(self.attack_list[0], self.defense_list[1]) == 0.25:
                not_very_e_q.append("◯")

            elif self.calculate(self.attack_list[0], self.defense_list[0]) * self.calculate(self.attack_list[0], self.defense_list[1]) == 0:
                no_e.append("◯")


        """ポップアップウィンドウに表示する結果のテキストの整形"""
        
        result_text = ""
        result_text = result_text + "  Defense :" + self.list_connect(self.defense_list) + "\n"
        result_text += "     ↑\n"
        result_text = result_text + "  Attack    : " + self.list_connect(self.attack_list) + "\n"
        result_text += "\n"
        
        if not self.attack_list[0] == "" and not self.defense_list[0] == "":
            result_text = result_text + "  こうかは ばつぐんだ！(×4) : " + self.list_connect(super_e_4) + "\n"
            result_text = result_text + "  こうかは ばつぐんだ！(×2) : " + self.list_connect(super_e) + "\n"
            result_text = result_text + "  こうかは いまひとつの ようだ(×0.5) : " + self.list_connect(not_very_e) + "\n"
            result_text = result_text + "  こうかは いまひとつの ようだ(×0.25) : " + self.list_connect(not_very_e_q) + "\n"
            result_text = result_text + "  こうかが ない みたいだ.....(×0) : " + self.list_connect(no_e) + "\n"
            
        # 攻撃側と防御側の相性の確認時以外はタイプの頭に改行と空白を加えて読みやすく整形する
        else:
            result_text = result_text + "  こうかは ばつぐんだ！(×4) : " + "\n    " + self.list_connect(super_e_4) + "\n"
            result_text = result_text + "  こうかは ばつぐんだ！(×2) : " + "\n    " + self.list_connect(super_e) + "\n"
            result_text = result_text + "  こうかは いまひとつの ようだ(×0.5) : " + "\n    " + self.list_connect(not_very_e) + "\n"
            result_text = result_text + "  こうかは いまひとつの ようだ(×0.25) : " + "\n    " + self.list_connect(not_very_e_q) + "\n"
            result_text = result_text + "  こうかが ない みたいだ.....(×0) : " + "\n    " + self.list_connect(no_e) + "\n"

        return(result_text)


    # 受け取った配列の要素をカンマ区切りで連結した文字列を返すメソッド
    def list_connect(self, _list):
        text = ""
        for i in _list:
            if not i == "": text = text + "," + str(self.trans_label(i))
        return(text[1:])


    # タイプの英語略称表記を日本語に変換するメソッド
    def trans_label(self, _type):
        if _type == "nor": return("ノーマル")
        elif _type == "fir": return("ほのお")
        elif _type == "wat": return("みず")
        elif _type == "gra": return("くさ")
        elif _type == "ele": return("でんき")
        elif _type == "ice": return("こおり")
        elif _type == "fig": return("かくとう")
        elif _type == "poi": return("どく")
        elif _type == "gro": return("じめん")
        elif _type == "fly": return("ひこう")
        elif _type == "psy": return("エスパー")
        elif _type == "bug": return("むし")
        elif _type == "roc": return("いわ")
        elif _type == "gho": return("ゴースト")
        elif _type == "dra": return("ドラゴン")
        elif _type == "dar": return("あく")
        elif _type == "ste": return("はがね")
        elif _type == "fai": return("フェアリー")
        else: return(_type)


    # 引数の2つのタイプの相性を計算
    def calculate(self, type1, type2):
        """type1(attack)→type2(defense)の相性"""

        # タイプが選択されていない場合は1(等倍)を返す
        if type1 == "" or type2 == "":
            return(1)

        if type1 == "nor":
            if type2 == "nor": return(self.effect[0][0])
            elif type2 == "fir": return(self.effect[0][1])
            elif type2 == "wat": return(self.effect[0][2])
            elif type2 == "ele": return(self.effect[0][3])
            elif type2 == "gra": return(self.effect[0][4])
            elif type2 == "ice": return(self.effect[0][5])
            elif type2 == "fig": return(self.effect[0][6])
            elif type2 == "poi": return(self.effect[0][7])
            elif type2 == "gro": return(self.effect[0][8])
            elif type2 == "fly": return(self.effect[0][9])
            elif type2 == "psy": return(self.effect[0][10])
            elif type2 == "bug": return(self.effect[0][11])
            elif type2 == "roc": return(self.effect[0][12])
            elif type2 == "gho": return(self.effect[0][13])
            elif type2 == "dra": return(self.effect[0][14])
            elif type2 == "dar": return(self.effect[0][15])
            elif type2 == "ste": return(self.effect[0][16])
            elif type2 == "fai": return(self.effect[0][17])
        elif type1 == "fir":
            if type2 == "nor": return(self.effect[1][0])
            elif type2 == "fir": return(self.effect[1][1])
            elif type2 == "wat": return(self.effect[1][2])
            elif type2 == "ele": return(self.effect[1][3])
            elif type2 == "gra": return(self.effect[1][4])
            elif type2 == "ice": return(self.effect[1][5])
            elif type2 == "fig": return(self.effect[1][6])
            elif type2 == "poi": return(self.effect[1][7])
            elif type2 == "gro": return(self.effect[1][8])
            elif type2 == "fly": return(self.effect[1][9])
            elif type2 == "psy": return(self.effect[1][10])
            elif type2 == "bug": return(self.effect[1][11])
            elif type2 == "roc": return(self.effect[1][12])
            elif type2 == "gho": return(self.effect[1][13])
            elif type2 == "dra": return(self.effect[1][14])
            elif type2 == "dar": return(self.effect[1][15])
            elif type2 == "ste": return(self.effect[1][16])
            elif type2 == "fai": return(self.effect[1][17])
        elif type1 == "wat":
            if type2 == "nor": return(self.effect[2][0])
            elif type2 == "fir": return(self.effect[2][1])
            elif type2 == "wat": return(self.effect[2][2])
            elif type2 == "ele": return(self.effect[2][3])
            elif type2 == "gra": return(self.effect[2][4])
            elif type2 == "ice": return(self.effect[2][5])
            elif type2 == "fig": return(self.effect[2][6])
            elif type2 == "poi": return(self.effect[2][7])
            elif type2 == "gro": return(self.effect[2][8])
            elif type2 == "fly": return(self.effect[2][9])
            elif type2 == "psy": return(self.effect[2][10])
            elif type2 == "bug": return(self.effect[2][11])
            elif type2 == "roc": return(self.effect[2][12])
            elif type2 == "gho": return(self.effect[2][13])
            elif type2 == "dra": return(self.effect[2][14])
            elif type2 == "dar": return(self.effect[2][15])
            elif type2 == "ste": return(self.effect[2][16])
            elif type2 == "fai": return(self.effect[2][17])
        elif type1 == "ele":
            if type2 == "nor": return(self.effect[3][0])
            elif type2 == "fir": return(self.effect[3][1])
            elif type2 == "wat": return(self.effect[3][2])
            elif type2 == "ele": return(self.effect[3][3])
            elif type2 == "gra": return(self.effect[3][4])
            elif type2 == "ice": return(self.effect[3][5])
            elif type2 == "fig": return(self.effect[3][6])
            elif type2 == "poi": return(self.effect[3][7])
            elif type2 == "gro": return(self.effect[3][8])
            elif type2 == "fly": return(self.effect[3][9])
            elif type2 == "psy": return(self.effect[3][10])
            elif type2 == "bug": return(self.effect[3][11])
            elif type2 == "roc": return(self.effect[3][12])
            elif type2 == "gho": return(self.effect[3][13])
            elif type2 == "dra": return(self.effect[3][14])
            elif type2 == "dar": return(self.effect[3][15])
            elif type2 == "ste": return(self.effect[3][16])
            elif type2 == "fai": return(self.effect[3][17])
        elif type1 == "gra":
            if type2 == "nor": return(self.effect[4][0])
            elif type2 == "fir": return(self.effect[4][1])
            elif type2 == "wat": return(self.effect[4][2])
            elif type2 == "ele": return(self.effect[4][3])
            elif type2 == "gra": return(self.effect[4][4])
            elif type2 == "ice": return(self.effect[4][5])
            elif type2 == "fig": return(self.effect[4][6])
            elif type2 == "poi": return(self.effect[4][7])
            elif type2 == "gro": return(self.effect[4][8])
            elif type2 == "fly": return(self.effect[4][9])
            elif type2 == "psy": return(self.effect[4][10])
            elif type2 == "bug": return(self.effect[4][11])
            elif type2 == "roc": return(self.effect[4][12])
            elif type2 == "gho": return(self.effect[4][13])
            elif type2 == "dra": return(self.effect[4][14])
            elif type2 == "dar": return(self.effect[4][15])
            elif type2 == "ste": return(self.effect[4][16])
            elif type2 == "fai": return(self.effect[4][17])
        elif type1 == "ice":
            if type2 == "nor": return(self.effect[5][0])
            elif type2 == "fir": return(self.effect[5][1])
            elif type2 == "wat": return(self.effect[5][2])
            elif type2 == "ele": return(self.effect[5][3])
            elif type2 == "gra": return(self.effect[5][4])
            elif type2 == "ice": return(self.effect[5][5])
            elif type2 == "fig": return(self.effect[5][6])
            elif type2 == "poi": return(self.effect[5][7])
            elif type2 == "gro": return(self.effect[5][8])
            elif type2 == "fly": return(self.effect[5][9])
            elif type2 == "psy": return(self.effect[5][10])
            elif type2 == "bug": return(self.effect[5][11])
            elif type2 == "roc": return(self.effect[5][12])
            elif type2 == "gho": return(self.effect[5][13])
            elif type2 == "dra": return(self.effect[5][14])
            elif type2 == "dar": return(self.effect[5][15])
            elif type2 == "ste": return(self.effect[5][16])
            elif type2 == "fai": return(self.effect[5][17])
        elif type1 == "fig":
            if type2 == "nor": return(self.effect[6][0])
            elif type2 == "fir": return(self.effect[6][1])
            elif type2 == "wat": return(self.effect[6][2])
            elif type2 == "ele": return(self.effect[6][3])
            elif type2 == "gra": return(self.effect[6][4])
            elif type2 == "ice": return(self.effect[6][5])
            elif type2 == "fig": return(self.effect[6][6])
            elif type2 == "poi": return(self.effect[6][7])
            elif type2 == "gro": return(self.effect[6][8])
            elif type2 == "fly": return(self.effect[6][9])
            elif type2 == "psy": return(self.effect[6][10])
            elif type2 == "bug": return(self.effect[6][11])
            elif type2 == "roc": return(self.effect[6][12])
            elif type2 == "gho": return(self.effect[6][13])
            elif type2 == "dra": return(self.effect[6][14])
            elif type2 == "dar": return(self.effect[6][15])
            elif type2 == "ste": return(self.effect[6][16])
            elif type2 == "fai": return(self.effect[6][17])
        elif type1 == "poi":
            if type2 == "nor": return(self.effect[7][0])
            elif type2 == "fir": return(self.effect[7][1])
            elif type2 == "wat": return(self.effect[7][2])
            elif type2 == "ele": return(self.effect[7][3])
            elif type2 == "gra": return(self.effect[7][4])
            elif type2 == "ice": return(self.effect[7][5])
            elif type2 == "fig": return(self.effect[7][6])
            elif type2 == "poi": return(self.effect[7][7])
            elif type2 == "gro": return(self.effect[7][8])
            elif type2 == "fly": return(self.effect[7][9])
            elif type2 == "psy": return(self.effect[7][10])
            elif type2 == "bug": return(self.effect[7][11])
            elif type2 == "roc": return(self.effect[7][12])
            elif type2 == "gho": return(self.effect[7][13])
            elif type2 == "dra": return(self.effect[7][14])
            elif type2 == "dar": return(self.effect[7][15])
            elif type2 == "ste": return(self.effect[7][16])
            elif type2 == "fai": return(self.effect[7][17])
        elif type1 == "gro":
            if type2 == "nor": return(self.effect[8][0])
            elif type2 == "fir": return(self.effect[8][1])
            elif type2 == "wat": return(self.effect[8][2])
            elif type2 == "ele": return(self.effect[8][3])
            elif type2 == "gra": return(self.effect[8][4])
            elif type2 == "ice": return(self.effect[8][5])
            elif type2 == "fig": return(self.effect[8][6])
            elif type2 == "poi": return(self.effect[8][7])
            elif type2 == "gro": return(self.effect[8][8])
            elif type2 == "fly": return(self.effect[8][9])
            elif type2 == "psy": return(self.effect[8][10])
            elif type2 == "bug": return(self.effect[8][11])
            elif type2 == "roc": return(self.effect[8][12])
            elif type2 == "gho": return(self.effect[8][13])
            elif type2 == "dra": return(self.effect[8][14])
            elif type2 == "dar": return(self.effect[8][15])
            elif type2 == "ste": return(self.effect[8][16])
            elif type2 == "fai": return(self.effect[8][17])
        elif type1 == "fly":
            if type2 == "nor": return(self.effect[9][0])
            elif type2 == "fir": return(self.effect[9][1])
            elif type2 == "wat": return(self.effect[9][2])
            elif type2 == "ele": return(self.effect[9][3])
            elif type2 == "gra": return(self.effect[9][4])
            elif type2 == "ice": return(self.effect[9][5])
            elif type2 == "fig": return(self.effect[9][6])
            elif type2 == "poi": return(self.effect[9][7])
            elif type2 == "gro": return(self.effect[9][8])
            elif type2 == "fly": return(self.effect[9][9])
            elif type2 == "psy": return(self.effect[9][10])
            elif type2 == "bug": return(self.effect[9][11])
            elif type2 == "roc": return(self.effect[9][12])
            elif type2 == "gho": return(self.effect[9][13])
            elif type2 == "dra": return(self.effect[9][14])
            elif type2 == "dar": return(self.effect[9][15])
            elif type2 == "ste": return(self.effect[9][16])
            elif type2 == "fai": return(self.effect[9][17])
        elif type1 == "psy":
            if type2 == "nor": return(self.effect[10][0])
            elif type2 == "fir": return(self.effect[10][1])
            elif type2 == "wat": return(self.effect[10][2])
            elif type2 == "ele": return(self.effect[10][3])
            elif type2 == "gra": return(self.effect[10][4])
            elif type2 == "ice": return(self.effect[10][5])
            elif type2 == "fig": return(self.effect[10][6])
            elif type2 == "poi": return(self.effect[10][7])
            elif type2 == "gro": return(self.effect[10][8])
            elif type2 == "fly": return(self.effect[10][9])
            elif type2 == "psy": return(self.effect[10][10])
            elif type2 == "bug": return(self.effect[10][11])
            elif type2 == "roc": return(self.effect[10][12])
            elif type2 == "gho": return(self.effect[10][13])
            elif type2 == "dra": return(self.effect[10][14])
            elif type2 == "dar": return(self.effect[10][15])
            elif type2 == "ste": return(self.effect[10][16])
            elif type2 == "fai": return(self.effect[10][17])
        elif type1 == "bug":
            if type2 == "nor": return(self.effect[11][0])
            elif type2 == "fir": return(self.effect[11][1])
            elif type2 == "wat": return(self.effect[11][2])
            elif type2 == "ele": return(self.effect[11][3])
            elif type2 == "gra": return(self.effect[11][4])
            elif type2 == "ice": return(self.effect[11][5])
            elif type2 == "fig": return(self.effect[11][6])
            elif type2 == "poi": return(self.effect[11][7])
            elif type2 == "gro": return(self.effect[11][8])
            elif type2 == "fly": return(self.effect[11][9])
            elif type2 == "psy": return(self.effect[11][10])
            elif type2 == "bug": return(self.effect[11][11])
            elif type2 == "roc": return(self.effect[11][12])
            elif type2 == "gho": return(self.effect[11][13])
            elif type2 == "dra": return(self.effect[11][14])
            elif type2 == "dar": return(self.effect[11][15])
            elif type2 == "ste": return(self.effect[11][16])
            elif type2 == "fai": return(self.effect[11][17])
        elif type1 == "roc":
            if type2 == "nor": return(self.effect[12][0])
            elif type2 == "fir": return(self.effect[12][1])
            elif type2 == "wat": return(self.effect[12][2])
            elif type2 == "ele": return(self.effect[12][3])
            elif type2 == "gra": return(self.effect[12][4])
            elif type2 == "ice": return(self.effect[12][5])
            elif type2 == "fig": return(self.effect[12][6])
            elif type2 == "poi": return(self.effect[12][7])
            elif type2 == "gro": return(self.effect[12][8])
            elif type2 == "fly": return(self.effect[12][9])
            elif type2 == "psy": return(self.effect[12][10])
            elif type2 == "bug": return(self.effect[12][11])
            elif type2 == "roc": return(self.effect[12][12])
            elif type2 == "gho": return(self.effect[12][13])
            elif type2 == "dra": return(self.effect[12][14])
            elif type2 == "dar": return(self.effect[12][15])
            elif type2 == "ste": return(self.effect[12][16])
            elif type2 == "fai": return(self.effect[12][17])
        elif type1 == "gho":
            if type2 == "nor": return(self.effect[13][0])
            elif type2 == "fir": return(self.effect[13][1])
            elif type2 == "wat": return(self.effect[13][2])
            elif type2 == "ele": return(self.effect[13][3])
            elif type2 == "gra": return(self.effect[13][4])
            elif type2 == "ice": return(self.effect[13][5])
            elif type2 == "fig": return(self.effect[13][6])
            elif type2 == "poi": return(self.effect[13][7])
            elif type2 == "gro": return(self.effect[13][8])
            elif type2 == "fly": return(self.effect[13][9])
            elif type2 == "psy": return(self.effect[13][10])
            elif type2 == "bug": return(self.effect[13][11])
            elif type2 == "roc": return(self.effect[13][12])
            elif type2 == "gho": return(self.effect[13][13])
            elif type2 == "dra": return(self.effect[13][14])
            elif type2 == "dar": return(self.effect[13][15])
            elif type2 == "ste": return(self.effect[13][16])
            elif type2 == "fai": return(self.effect[13][17])
        elif type1 == "dra":
            if type2 == "nor": return(self.effect[14][0])
            elif type2 == "fir": return(self.effect[14][1])
            elif type2 == "wat": return(self.effect[14][2])
            elif type2 == "ele": return(self.effect[14][3])
            elif type2 == "gra": return(self.effect[14][4])
            elif type2 == "ice": return(self.effect[14][5])
            elif type2 == "fig": return(self.effect[14][6])
            elif type2 == "poi": return(self.effect[14][7])
            elif type2 == "gro": return(self.effect[14][8])
            elif type2 == "fly": return(self.effect[14][9])
            elif type2 == "psy": return(self.effect[14][10])
            elif type2 == "bug": return(self.effect[14][11])
            elif type2 == "roc": return(self.effect[14][12])
            elif type2 == "gho": return(self.effect[14][13])
            elif type2 == "dra": return(self.effect[14][14])
            elif type2 == "dar": return(self.effect[14][15])
            elif type2 == "ste": return(self.effect[14][16])
            elif type2 == "fai": return(self.effect[14][17])
        elif type1 == "dar":
            if type2 == "nor": return(self.effect[15][0])
            elif type2 == "fir": return(self.effect[15][1])
            elif type2 == "wat": return(self.effect[15][2])
            elif type2 == "ele": return(self.effect[15][3])
            elif type2 == "gra": return(self.effect[15][4])
            elif type2 == "ice": return(self.effect[15][5])
            elif type2 == "fig": return(self.effect[15][6])
            elif type2 == "poi": return(self.effect[15][7])
            elif type2 == "gro": return(self.effect[15][8])
            elif type2 == "fly": return(self.effect[15][9])
            elif type2 == "psy": return(self.effect[15][10])
            elif type2 == "bug": return(self.effect[15][11])
            elif type2 == "roc": return(self.effect[15][12])
            elif type2 == "gho": return(self.effect[15][13])
            elif type2 == "dra": return(self.effect[15][14])
            elif type2 == "dar": return(self.effect[15][15])
            elif type2 == "ste": return(self.effect[15][16])
            elif type2 == "fai": return(self.effect[15][17])
        elif type1 == "ste":
            if type2 == "nor": return(self.effect[16][0])
            elif type2 == "fir": return(self.effect[16][1])
            elif type2 == "wat": return(self.effect[16][2])
            elif type2 == "ele": return(self.effect[16][3])
            elif type2 == "gra": return(self.effect[16][4])
            elif type2 == "ice": return(self.effect[16][5])
            elif type2 == "fig": return(self.effect[16][6])
            elif type2 == "poi": return(self.effect[16][7])
            elif type2 == "gro": return(self.effect[16][8])
            elif type2 == "fly": return(self.effect[16][9])
            elif type2 == "psy": return(self.effect[16][10])
            elif type2 == "bug": return(self.effect[16][11])
            elif type2 == "roc": return(self.effect[16][12])
            elif type2 == "gho": return(self.effect[16][13])
            elif type2 == "dra": return(self.effect[16][14])
            elif type2 == "dar": return(self.effect[16][15])
            elif type2 == "ste": return(self.effect[16][16])
            elif type2 == "fai": return(self.effect[16][17])
        elif type1 == "fai":
            if type2 == "nor": return(self.effect[17][0])
            elif type2 == "fir": return(self.effect[17][1])
            elif type2 == "wat": return(self.effect[17][2])
            elif type2 == "ele": return(self.effect[17][3])
            elif type2 == "gra": return(self.effect[17][4])
            elif type2 == "ice": return(self.effect[17][5])
            elif type2 == "fig": return(self.effect[17][6])
            elif type2 == "poi": return(self.effect[17][7])
            elif type2 == "gro": return(self.effect[17][8])
            elif type2 == "fly": return(self.effect[17][9])
            elif type2 == "psy": return(self.effect[17][10])
            elif type2 == "bug": return(self.effect[17][11])
            elif type2 == "roc": return(self.effect[17][12])
            elif type2 == "gho": return(self.effect[17][13])
            elif type2 == "dra": return(self.effect[17][14])
            elif type2 == "dar": return(self.effect[17][15])
            elif type2 == "ste": return(self.effect[17][16])
            elif type2 == "fai": return(self.effect[17][17])



    # CHECKボタンを押した時の処理
    def check(self):
        """CHECKボタンを押すとポップアップウィンドウを開く"""
        # 何も選択されていない時は押しても何も起きない
        if self.attack_list[0] == "" and self.defense_list[0] == "" and self.defense_list[1] == "":
            pass

        else:
            PopupList.setText(self.result())
            content = PopupList(cancel=self.cancel)
            self.popup = Popup(title="Result", content=content, size_hint=(.8, .7))
            self.popup.open()


    # ポップアップウィンドウのcancelボタンを押した時の処理
    def cancel(self):
        """　ポップアップ画面でキャンセル"""
        self.popup.dismiss()

        
    # 検索結果を表示するポップアップウィンドウの表示
    def search(self):
        """検索ボタンを押すとポケモンの情報を検索してポップアップウィンドウに表示"""
        
        if not self.ids.search.text == '':
            SearchList.setText(self.search_pkmn(self.ids.search.text))
            content = SearchList(cancel=self.cancel)
            self.popup = Popup(title="Search Result", content=content, size_hint=(.8, .7))
            self.popup.open()
        
    
    # ポケモンの情報を検索して表示するメソッド
    def search_pkmn(self, pkmn):
        """入力されたポケモンの名前について図鑑番号と英名をpkmn_data.txtから取得し、pokeAPIを用いてデータを検索"""
        
        # 入力された文字列に改行が含まれていたら削除
        inp = []
        inp.append(pkmn)
        inp_name = inp[0].split()
        pkmn = inp_name[0]
        
        try:
            # テキストデータ(pkmn_data.txt)を配列に格納
            with open('pkmn_data.txt') as f:
                lines = f.readlines()
                data = [line.strip() for line in lines]
                
            # データ中の\tを,に変換
            for i in range(len(data)):
                data[i] = data[i].replace('\t',',')

            # データ中から入力されたポケモンを検索し該当するものがあればそのポケモンの番号と英名を取得
            for i in data:
                poke = i.split(',')
                if pkmn == poke[1] or pkmn == poke[2]:
                    no = poke[0]
                    pkmn = poke[1]
                    
            """図鑑ナンバーと名前を用いてpokeAPIでポケモンのデータを検索"""
            params = {
                "no": no,
                "key": pkmn,
            }
            p = urllib.parse.urlencode(params)
            url = 'https://usumapi.nelke.jp/v1/pokemon/?' + p
                    
                    
        except:
            pass
        
        
        """図鑑ナンバーと名前を用いてpokeAPIでポケモンのデータを検索"""
        
        _no = ""
        _name = ""
        _type = ""
        _ability = ""
        
        try:
            with urllib.request.urlopen(url) as res:
                html = res.read().decode("utf-8")
                jsn = json.loads(html) # json形式を辞書型に変換
                                
                _no = str(jsn['results'][0]['no'])
                _name = jsn['results'][0]['names'][0]['name'] + " / " + jsn['results'][0]['names'][1]['name']
                _type = jsn['results'][0]['types'][0]['type']['names'][1]['name']
                try:
                    _type = _type + ", " + jsn['results'][0]['types'][1]['type']['names'][1]['name']
                except:
                    pass
                _ability = jsn['results'][0]['abilities'][0]['ability']['names'][0]['name']
                try:
                    _ability = _ability + "," + jsn['results'][0]['abilities'][1]['ability']['names'][0]['name']
                except:
                    pass
        
        except:
            return("Error.")
        
        
        """検索結果を整形してポップアップウィンドウに表示"""
        text = ""
        text = text + "  No. " + _no + "\n"
        text = text + "  Name : " + _name + "\n"
        text = text + "  Type : " + _type + "\n"
        text = text + "  Ability : " + _ability + "\n"
        
        return(text)



class Type_checkerApp(App):
    
    # kivy launcherでのリスト表示時におけるタイトルとアイコンの設定
    title = 'type_checker'
    icon = 'icon.png'

    def build(self):
        return Type_checker()

    # アプリをポーズした時
    def on_pause(self):
        return True
    
    # アプリ終了時
    #def on_stop(self):

if __name__ == '__main__':
    Type_checkerApp().run()