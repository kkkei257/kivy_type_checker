# kivy_type_checker

## 概要
Kivyでポケモンのタイプ相性チェッカーを作成しました。主な機能として<br>
・攻撃側のわざと防御側のタイプとの相性の確認<br>
・ポケモンの情報の検索<br>
を実装しています。

◯タイプ相性の確認機能<br>
タイル状に並んだタイプのボタンを攻撃側は1つ、防御側は2つまで選ぶことができ、CHECKボタンを押すことで相性を確認することができます。この時、<br>
・攻撃側と防御側両方とも選択した場合：相性を表示<br>
・攻撃側のわざのタイプ又は防御側のポケモンのタイプのみ選択した場合：各タイプとの相性をそれぞれ表示<br>
を表示することができます。ただし効果がふつうのものについては表示されないようになっています。

ボタンの配置：<br>
タイプのボタンの配置にはGridLayoutを用いて6×3ずつボタンを並べています。<br>
~~~
GridLayout:
    size_hint_y: .5
    cols: 6
    rows: 3

    spacing: 2
    padding: 4

    Button: 
        text: "ノーマル"
        background_normal: ''
        background_down: ''
        background_color: 174 / 255, 174  / 255, 174 / 255, root.seld_nor
        on_release: root.select("d", "nor", [174 / 255, 174  / 255, 174 / 255, 1])
        
        ・・・(同様に必要な数だけボタンを記述)・・・
~~~
なおselectメソッドの引数は(<"d"(defender) or "a"(attacker)>, <タイプの英名の略称>, <アイコンのカラー>)となっています。

CHECKボタン：
ウィジェットを中央に配置したい場合にはAnchorLayoutがおすすめです。<br>
~~~
AnchorLayout:
      size_hint_y: .1

      Button:
          size_hint_x: .4
          anchor_x: 'center'
          anchor_y: 'center'
          #pos: self.parent.x / 2 - self.parent.width / 2, self.parent.y
          id: result
          text: "CHECK"
          on_release: root.check()
~~~
<br>
◯ポケモンの情報検索機能<br>
ポケモンの情報検索にはUSUM API(https://usumapi.nelke.jp) を利用させていただきました。テキストボックスに検索したいポケモンの図鑑ナンバー又は名前(日本語名・英名可)を入力することで対象のポケモンの図鑑ナンバー・名前(日本語名と英名)・タイプ・特性を取得することができます。

検索部分：<br>
USUM APIの使用時には検索したいポケモンの図鑑ナンバー(no)と英名(key)を渡す必要があり、このnoとkeyについては別個にリスト(pkmn_data.txt)を作成してそこから検索するようにしています。なおこのデータについては同サイト様のページよりテキストをコピーさせていただきました。
<br>
<img src="Screenshot_1.png" width="24%"> <img src="Screenshot_3.png" width="24%"> <img src="Screenshot_2.png" width="24%"> <img src="Screenshot_4.png" width="24%">
