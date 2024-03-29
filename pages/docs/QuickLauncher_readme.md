# Quick Launcher

JSONファイルを元に作成される、Windows専用のランチャーです。
タスクトレイに滞在し、右クリックでメニューが出ます。

EXEファイルを登録し、タスクトレイからアプリケーションを起動出来るようになります。
また、フォルダパスを登録する事でブックマークとして使用できます。

Windows11になると、タスクバーに好きなフォルダを登録できなく困ったので作成。
Windowsに昔からある"Quick Launch"フォルダから名前を取って、"Quick Launcher"と命名してます。

Windows10以降にプリインストールされてるライブラリのみで作成されてるので、追加ランタイム等は不要です。
ファイルサイズが20KBと、極端に小さいのも特徴です。

<img src="https://raw.githubusercontent.com/unitbus/QuickLauncher/main/docs/tasktray_sampleA.png">


## 特徴

- カスタマイズが容易(テキストエディタで編集可能)
- タスクトレイで表示するアイコンが変更可能
- ネットワークに設定ファイルを置く事で共有可能
- 複数起動が可能で、別々の設定ファイルを指定可能
- ファイルサイズが小さい

## License

https://github.com/unitbus/QuickLauncher/blob/main/LICENSE.txt


# 使い方

`QuickLauncher.exe`を実行すると起動し、タスクトレイに滞在します。

## システムメニュー

<img src="https://raw.githubusercontent.com/unitbus/QuickLauncher/main/docs/tasktray_sampleB.png">

左クリックするとシステムメニューが表示されます(v0.1.2から)。
アプリケーションを終了したい場合は`Exit`を押すとタスクトレイから消えます。

`Edit`を押すと、OSに関連付けされたアプリケーションで設定ファイルのJSONを開きます。
`Update`を押すと、JSONファイルを再読み込みし、メニューを更新します。

## ユーザーメニュー

右クリックをすると、JSONファイルから作成したメニューが表示されます。
ダウンロードした状態だと、メニューアイテムにサンプルが登録されています。
好みに合わせて追加、編集してください。


# コマンドラインオプション

```powershell
QuickLauncher.exe -json ".\samples\sample.json" -icon ".\samples\sample.ico"
```

複数起動する事が可能です。目的に応じて利用してください。
例：自分用と、会社共有用など

## -json

設定ファイルを指定します。
指定がない場合は、同じディレクトリにある`QuickLauncher.json`が参照されます。

## -icon

タスクトレイで表示するアイコンが変更されます。
複数起動した際に、見た目で違いが分かるようになります。

## ショートカットの利用

起動用のバッチファイルなど用意してもいいですが、気軽に使いたい場合は、
ウインドウズのショートカット作成し、ここに入力して使うと便利です。
<img src="https://raw.githubusercontent.com/unitbus/QuickLauncher/main/docs/shortcut_property.png">


# 設定ファイル

## JSON

設定ウインドウは容易してません。JSONファイルを直接編集してくだい。
設定ファイルのフォーマットにはJSONを使用してます。

JSONファイルの編集はテキストエディタで行います。
メモ帳でも可能ですが、VSCodeの使用を推奨します。
JSONファイルの不正な記述を指摘してくれます。

## JSONの特徴

- バックスラッシュは、2つ書かないと認識されない(スラッシュに置き換えても可)
- 複数指定する場合、カンマが必要で、最後の一個にカンマ付けるとエラーになる

## サブメニュー

カテゴリ名を入れずに、作成するとメインメニューに追加されます。

```json
[
    {
        "name": "カテゴリ名",  // ここがサブメニュー
        "softwares": [
            // ...
        ]
    }
    {
        "name": "",  // ここがメインメニュー
        "softwares": [
            // ...
        ]
    }
]
```

## ソフトウェア

```json
[
    {
        "name": "カテゴリ名",
        "softwares": [
            {
                "name": "Maya 2024",
                "path": "%ProgramFiles%\\Autodesk\\Maya2024\\bin\\maya.exe",
                "icon": "%ProgramFiles%\\Autodesk\\Maya2024\\bin\\maya.exe",
                "arguments": "",
                "environments": {
                    "AW_JPEG_Q_FACTOR": 90,
                    "MAYA_UI_LANGUAGE": "en_US",
                    "MAYA_MODULE_PATH": [
                        "X:\\inhouse\\packageA",
                        "X:\\inhouse\\packageB",
                        "Y:\\test\\package"
                    ]
                }
            }
        ]
    }
]
```

### name

メニューアイテムに表示する名前です。

### path

EXEのパス、または起動用のバッチファイルを指定してください。
パスの指定には、環境変数が使えます。

### icon

メニューアイテムに使うアイコンを指定します。
EXEに埋め込まれてるアイコンを使いたい場合は、EXEのパスを指定すれば取得できます。
パスの指定には、環境変数が使えます。

### arguments

引数です。EXEを実行する際に必要な引数を追加してください。
例: `-help` `-version`

### environments

環境変数を追加して起動します。辞書型で、左が名前、右が値になります。
辞書型なので、同じ名前(キー)の指定は出来ません。また上から順に処理される保証はありません。
環境変数の設定が複雑になる場合は、`path`にBATファイルを指定して運用してください。

値を配列にすると、文字列をセミコロン(`;`)で結合します。
`PATH`など長い文字列を入れる場合に利用してください。

```json
"MAYA_MODULE_PATH": "X:\\inhouse\\packageA;X:\\inhouse\\packageB;Y:\\test\\package"
```

上と、下は、同じ意味になります。

```json
"MAYA_MODULE_PATH": [
    "X:\\inhouse\\packageA",
    "X:\\inhouse\\packageB",
    "Y:\\test\\package"
]
```

## ブックマーク

`path`にフォルダを指定するとブックマークとして使えます。
エクスプローラーで指定されたパスを開きます。

```json
[
    {
        "name": "ブックマーク",
        "softwares": [
            {
                "name": "インストールディレクトリ",
                "path": "%ProgramFiles%"
            }
        ]
    }
]
```

名前とパス以外のオプションは無効になります。
`icon`でアイコンを変更出来ますが、指定がなければシステムのフォルダアイコンが使われます。

## セパレーター

メニューアイテムの仕切りとして使用出来ます。
`separator`が指定されてる場合、`Visible`以外のアトリビュートはすべて無視されます。
カテゴリと、ソフトウェアの項目で使用可能です。

```json
[
    {
        "name": "カテゴリA",
        "softwares": [
            {
                // Software A
            },
            {
                "separator": true
            },
            {
                // Software B
            }
        ]
    }
    {
        "separator": true
    },
    {
        "name": "カテゴリB",
        "softwares": []
    }
]
```

## 非表示

JSONではコメントアウトが出来ないので、一時的に非表示したい時に使用してください。
カテゴリと、ソフトウェアの項目で使用可能です。

```json
[
    {
        "name": "カテゴリ名",
        "visible": false,
        "softwares": [
            {
                "separator": true
            },
            {
                "name": "インストールディレクトリ",
                "path": "%ProgramFiles%",
                "visible": false
            }
        ]
    }
]
```

# Link

## HomePage

https://unitbus.github.io/index

## QuickLauncher - GitHub

https://github.com/unitbus/QuickLauncher


<div style="text-align: right;">Copyright (C) 2023 Co, UnitBus.</div>
