# kivy_type_checker（2019年）

## 概要
<br>スクリーンショット：<br>
<img src="Screenshot_1.png" width="24%"> <img src="Screenshot_3.png" width="24%"> <img src="Screenshot_2.png" width="24%"> <img src="Screenshot_4.png" width="24%">

Kivyでポケモンのタイプ相性チェッカーを作成しました。主な機能として<br>
・攻撃側のわざと防御側のタイプとの相性の確認<br>
・ポケモンの情報の検索<br>
を実装しています。

◯タイプ相性の確認機能<br>
タイル状に並んだタイプのボタンを攻撃側は1つ、防御側は2つまで選ぶことができ、CHECKボタンを押すことで相性を確認することができます。この時、<br>
・攻撃側と防御側両方とも選択した場合：相性を表示<br>
・攻撃側のわざのタイプ又は防御側のポケモンのタイプのみ選択した場合：各タイプとの相性をそれぞれ表示<br>
することができます。ただし効果がふつうのものについては表示されないようになっています。

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
なおselectメソッドの引数は(<"d"(defender) or "a"(attacker)>, <タイプの英名の略称>, <アイコンのカラー>)となっています（これにより押されたボタンをメソッド内で識別することができます。色情報は押されたボタンと同色のラベルを下部に表示するために使用しています）。<br>

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
ポケモンの情報検索にはUSUM API(https://usumapi.nelke.jp) を利用させていただきました。テキストボックスに検索したいポケモンの図鑑ナンバー又は名前(日本語名・英名可)を入力することで対象のポケモンの図鑑ナンバー・名前(日本語名と英名)・タイプ・特性を取得できるようにしています。

検索部分：<br>
USUM APIの使用時には検索したいポケモンの図鑑ナンバー(no)と英名(key)を渡す必要があり、このnoとkeyについては別個にリスト(pkmn_data.txt)を作成してそこから検索するようにしています。なおこのデータについては同サイト様のページよりテキストをコピーさせていただきました。<br>
~~~
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
~~~

リクエストによりポケモンに関する情報がjson形式で返されます。それを辞書型に変換し、配列で指定して必要なデータを取り出しています。
~~~
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
~~~
