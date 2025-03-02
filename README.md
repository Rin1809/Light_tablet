# LightTableApp

<!-- Vietnamese -->
<details>
  <summary>🇻🇳 Tiếng Việt</summary>

## Giới thiệu

LightTableApp là một ứng dụng bảng vẽ kỹ thuật số (light table) đơn giản, cho phép hiển thị và thao tác nhiều hình ảnh trên một canvas trong suốt. Ứng dụng được xây dựng bằng Python và CustomTkinter.

## Tính năng

*   Hiển thị nhiều hình ảnh.
*   Phóng to/thu nhỏ, xoay, lật ảnh.
*   Thay đổi độ trong suốt.
*   Chế độ "click-through" (xuyên qua).
*   Ghim cửa sổ lên trên cùng.
*   Sắp xếp thứ tự các ảnh.
*   Lưu và tải lại trạng thái.

## Cài đặt

1.  **Yêu cầu:**
    *   Python 3.6 trở lên.
    *   Các thư viện: `customtkinter`, `Pillow`, `keyboard`, `pywin32` (chỉ trên Windows).
2.  **Các bước cài đặt:**

    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    python -m venv moitruongao
    moitruongao\Scripts\activate  # Hoặc  source moitruongao/bin/activate  trên Linux/macOS
    pip install -r requirements.txt
    ```
    * Thay `your-username` và `your-repository-name` bằng link repo github của bạn.
3. **Chạy ứng dụng**

    ```
    python Bang_Hat_Sang\main.py
    ```
     Hoặc:
    ```
    run.bat
    ```

## Hướng dẫn sử dụng

*   **Mở bảng vẽ:** Ctrl + O
*   **Chọn ảnh:** Ctrl + Click vào ảnh trên danh sách, hoặc click chuột vào ảnh trên bảng vẽ.
*   **Phóng to/thu nhỏ:** Cuộn chuột khi con trỏ ở trên ảnh được chọn.
*   **Xoay:** Chỉnh thanh trượt "Xoay" hoặc nhập giá trị góc.
*   **Lật ngang:** Nhấn nút "Lật ngang".
*   **Xóa ảnh:** Nhấn nút "Xóa ảnh".
*   **Sắp xếp ảnh:** Kéo thả trong danh sách ảnh.
*   **Ghim cửa sổ:** Bật/tắt công tắc "Ghim".
*   **Chế độ click-through:** Bật/tắt công tắc "Click-through" hoặc Ctrl + Q.
*   **Lưu trạng thái:** Nhấn nút Lưu.
*   **Tải trạng thái:** Nhấn nút Tải lại.
*   **Thay đổi độ trong suốt:** Chỉnh thanh trượt "Độ mờ".



</details>

<!-- English -->
<details>
  <summary>🇬🇧 English</summary>

## Introduction

LightTableApp is a simple digital light table application that allows you to display and manipulate multiple images on a transparent canvas. The application is built using Python and CustomTkinter.

## Features

*   Display multiple images.
*   Zoom in/out, rotate, flip images.
*   Change opacity.
*   "Click-through" mode.
*   Always on top.
*   Reorder images.
*   Save and load state.

## Installation

1.  **Requirements:**
    *   Python 3.6 or higher.
    *   Libraries: `customtkinter`, `Pillow`, `keyboard`, `pywin32` (Windows only).
2.  **Installation steps:**

    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    python -m venv virtual_environment_name
    virtual_environment_name\Scripts\activate  # Or  source virtual_environment_name/bin/activate  on Linux/macOS
    pip install -r requirements.txt
    ```
    *  Replace `your-username` and `your-repository-name` with your github repo link.
3. **Run application**
    ```
    python Bang_Hat_Sang\main.py
    ```
    Or
    ```
    run.bat
    ```

## Usage

*   **Open light table:** Ctrl + O
*   **Select image:** Ctrl + Click on the image in the list, or click on the image on the canvas.
*   **Zoom in/out:** Scroll the mouse wheel when the cursor is over the selected image.
*   **Rotate:** Adjust the "Rotate" slider or enter the angle value.
*   **Flip horizontally:** Press the "Flip Horizontal" button.
*   **Delete image:** Press the "Delete Image" button.
*   **Reorder images:** Drag and drop in the image list.
*   **Always on top:** Toggle the "Always on Top" switch.
*   **Click-through mode:** Toggle the "Click-through" switch or Ctrl + Q.
*   **Save state:** Click the Save button.
*   **Load state:** Click the Load button.
*   **Change opacity:** Adjust the "Opacity" slider.

</details>

<!-- Japanese -->
<details>
  <summary>🇯🇵 日本語</summary>

## 概要

LightTableAppは、透明なキャンバス上に複数の画像を表示および操作できるシンプルなデジタルライトテーブルアプリケーションです。このアプリケーションは、PythonとCustomTkinterを使用して構築されています。

## 機能

*   複数画像の表示
*   画像の拡大/縮小、回転、反転
*   不透明度の変更
*   「クリックスルー」モード
*   常に最前面表示
*   画像の並べ替え
*   状態の保存と読み込み

## インストール

1.  **必要条件:**
    *   Python 3.6 以上
    *   ライブラリ: `customtkinter`, `Pillow`, `keyboard`, `pywin32` (Windowsのみ)
2.  **インストール手順:**

    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    python -m venv virtual_environment_name
    virtual_environment_name\Scripts\activate  # または Linux/macOS では  source virtual_environment_name/bin/activate
    pip install -r requirements.txt
    ```
    *  `your-username` と `your-repository-name` をあなたのGithubリポジトリのリンクに置き換えて下さい
3. **アプリケーションの実行**
     ```
      python Bang_Hat_Sang\main.py
      ```
      または
      ```
      run.bat
      ```

## 使用方法

*   **ライトテーブルを開く:** Ctrl + O
*   **画像の選択:** リスト内の画像をCtrl + クリック、またはキャンバス上の画像をクリック
*   **拡大/縮小:** 選択した画像の上にカーソルを置いてマウスホイールをスクロール
*   **回転:** 「回転」スライダーを調整するか、角度の値を入力
*   **水平方向に反転:** 「水平方向に反転」ボタンを押す
*   **画像の削除:** 「画像を削除」ボタンを押す
*   **画像の並べ替え:** 画像リスト内でドラッグアンドドロップ
*   **常に最前面:** 「常に最前面」スイッチを切り替え
*   **クリックスルーモード:** 「クリックスルー」スイッチを切り替えるか、Ctrl + Q
*   **状態の保存:** 保存ボタンをクリック
*   **状態の読み込み:** 読み込みボタンをクリック
*   **不透明度の変更:** 「不透明度」スライダーを調整
*   
</details>
