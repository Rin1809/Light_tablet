# Bảng Hắt Sáng (Light Table) ᓚᘏᗢ

# Example
![image](https://github.com/user-attachments/assets/5f2798d2-1d1d-440e-a0b0-95d6bb35a3d3)


<!-- Vietnamese -->
<details>
  <summary>🇻🇳 Tiếng Việt</summary>

## Giới thiệu

**Bảng Hắt Sáng (LightTableApp)** là một ứng dụng Python đơn giản, mô phỏng bảng hắt sáng kỹ thuật số (digital light table/tracing board).  Nó cho phép bạn hiển thị, sắp xếp và thao tác nhiều hình ảnh cùng lúc trên một canvas trong suốt. Ứng dụng này rất hữu ích cho việc vẽ đồ họa, so sánh ảnh, hoặc bất kỳ tác vụ nào yêu cầu chồng nhiều lớp ảnh lên nhau. Ứng dụng được xây dựng bằng `customtkinter` và `Pillow`.

## Tính năng

*   **Hiển thị nhiều ảnh:** Tải và hiển thị đồng thời nhiều hình ảnh (PNG, JPG, JPEG, GIF, BMP, ICO) trên cùng một bảng vẽ.
*   **Phóng to/Thu nhỏ:** Phóng to hoặc thu nhỏ từng ảnh riêng biệt bằng cách sử dụng con lăn chuột.
*   **Xoay:** Xoay ảnh theo bất kỳ góc độ nào bằng thanh trượt hoặc nhập giá trị cụ thể.
*   **Lật ảnh:** Lật ảnh theo chiều ngang.
*   **Điều chỉnh độ trong suốt (Opacity):** Thay đổi độ mờ của toàn bộ bảng vẽ, giúp bạn nhìn xuyên qua các lớp ảnh dễ dàng hơn.
*   **Chế độ "Click-through" (Xuyên thấu):** Cho phép thao tác với các ứng dụng khác *bên dưới* bảng vẽ, ngay cả khi bảng vẽ đang hiển thị.  (Chỉ hỗ trợ trên Windows).
*   **Ghim cửa sổ (Always on Top):** Giữ cho cửa sổ bảng vẽ luôn hiển thị trên cùng, không bị che khuất bởi các cửa sổ khác.
*   **Sắp xếp thứ tự ảnh:** Kéo và thả các ảnh trong danh sách để thay đổi thứ tự hiển thị của chúng (ảnh nào ở trên trong danh sách sẽ hiển thị ở trên cùng trên bảng vẽ).
*   **Lưu và tải trạng thái:** Lưu lại toàn bộ trạng thái làm việc hiện tại (bao gồm ảnh, vị trí, góc xoay, độ phóng đại, cài đặt) vào một file `.lts` và tải lại sau đó để tiếp tục công việc.
*   **Xóa ảnh:** Xóa các ảnh đã chọn khỏi bảng vẽ.
* **Thông tin ảnh:** Hiển thị tên tệp, kích thước, định dạng của ảnh đang được chọn.
*   **Phím tắt:**
    *   `Ctrl + O`: Mở/Đóng bảng vẽ.
    *   `Ctrl + Q`: Bật/Tắt chế độ Click-through.
    *   `Ctrl + E`: Bật/Tắt chế độ Ghim cửa sổ.
* Kéo thả ảnh để di chuyển.

## Cài đặt

1.  **Yêu cầu hệ thống:**
    *   Python 3.6 trở lên.
    *   Các thư viện Python: `customtkinter`, `Pillow`, `keyboard`, `pywin32` (chỉ cần thiết trên Windows cho tính năng Click-through).

2.  **Các bước cài đặt (Sử dụng `run.bat` - Khuyến nghị):**

    *   Tải repository này về máy (Clone hoặc tải ZIP).
    *   Mở thư mục vừa tải về.
    *   Chạy file `run.bat`. File này sẽ tự động tạo môi trường ảo (virtual environment) `moitruongao`, cài đặt các thư viện cần thiết, và chạy ứng dụng.

3.  **Các bước cài đặt (Thủ công):**
    Mở terminal (command prompt hoặc PowerShell trên Windows):

    ```bash
    # Clone repository (nếu chưa tải về)
    git clone https://github.com/Rin1809/Bang-Hat-Sang.git
    cd Bang-Hat-Sang

    # Tạo môi trường ảo (tùy chọn nhưng rất khuyến khích)
    python -m venv moitruongao

    # Kích hoạt môi trường ảo
    # Trên Windows:
    moitruongao\Scripts\activate
    # Trên Linux/macOS:
    source moitruongao/bin/activate

    # Cài đặt các thư viện
    pip install -r requirements.txt
    ```

4.  **Chạy ứng dụng:**

    ```bash
    # Đảm bảo môi trường ảo đã được kích hoạt (nếu bạn dùng môi trường ảo)
    python Bang_Hat_Sang/main.py
    ```

## Hướng dẫn sử dụng chi tiết

1.  **Mở Bảng Vẽ:** Nhấn nút "Mở Bảng Vẽ" trên giao diện chính, hoặc nhấn tổ hợp phím `Ctrl + O`.

2.  **Thêm Ảnh:**
    *   Nhấn nút "Chọn Ảnh" trên giao diện chính.  Một cửa sổ chọn file sẽ hiện ra, cho phép bạn chọn một hoặc nhiều ảnh cùng lúc.
    *   Sau khi chọn ảnh, chúng sẽ xuất hiện trong danh sách ảnh ở bên trái và trên bảng vẽ.

3.  **Chọn Ảnh:**
    *   **Click chuột trái** vào ảnh trên bảng vẽ để chọn.
    *   **Click chuột trái** vào ảnh trong danh sách.
    *   **Giữ phím `Ctrl` và click** vào nhiều ảnh trong danh sách để chọn nhiều ảnh cùng lúc.
    *   Ảnh được chọn sẽ được đánh dấu trong danh sách.

4.  **Thao tác với Ảnh trên Bảng Vẽ:**

    *   **Di chuyển:** Click chuột trái và kéo ảnh được chọn đến vị trí mong muốn.
    *   **Phóng to/Thu nhỏ:** Đặt con trỏ chuột lên ảnh *được chọn*, sau đó *cuộn con lăn chuột* lên để phóng to, cuộn xuống để thu nhỏ.
    *   **Xoay:**
        *   Kéo thanh trượt "Xoay" trên giao diện.
        *   Hoặc, chọn ảnh, sau đó nhập giá trị góc xoay (độ) mong muốn.
    *   **Lật ngang:** Chọn ảnh và nhấn nút "Lật Ngang".

5.  **Sắp xếp thứ tự Ảnh (trong danh sách):**
    * Click chuột trái vào thumbnail của ảnh, kéo lên hoặc xuống trong danh sách ảnh, và thả vào vị trí mong muốn

6.  **Xóa Ảnh:**
    *   Chọn một hoặc nhiều ảnh.
    *   Nhấn nút "Xóa Ảnh".

7.  **Thay đổi độ trong suốt (Opacity):** Kéo thanh trượt "Độ mờ" để thay đổi độ trong suốt của *toàn bộ bảng vẽ*.

8.  **Chế độ Ghim cửa sổ (Always on Top):** Bật công tắc "Ghim" để giữ cho cửa sổ bảng vẽ luôn hiển thị trên cùng.

9.  **Chế độ Click-through (Xuyên thấu):**
    *   Bật công tắc "Click-through".
    *   Hoặc nhấn tổ hợp phím `Ctrl + Q`.
    *   Khi chế độ này được bật, bạn có thể click chuột *xuyên qua* bảng vẽ để thao tác với các cửa sổ/ứng dụng nằm bên dưới.

10. **Lưu Trạng Thái:** Nhấn nút "Lưu" để lưu trạng thái hiện tại (danh sách ảnh, vị trí, kích thước, góc xoay,...) vào một file `.lts`.

11. **Tải Trạng Thái:** Nhấn nút "Tải lại" để mở một file `.lts` đã lưu trước đó và khôi phục lại trạng thái làm việc.

12. **Thông tin ảnh:** Thông tin chi tiết của ảnh được chọn (tên, kích thước, định dạng) sẽ được hiển thị trong phần "Thông tin ảnh".

</details>

<!-- English -->
<details>
  <summary>🇬🇧 English</summary>

## Introduction

**Light Table (Bảng Hắt Sáng)** is a simple Python application that simulates a digital light table (also known as a tracing board).  It allows you to display, arrange, and manipulate multiple images simultaneously on a transparent canvas. This application is useful for drawing, comparing images, or any task that requires overlaying multiple image layers.  It is built using `customtkinter` and `Pillow`.

## Features

*   **Display Multiple Images:** Load and display multiple images (PNG, JPG, JPEG, GIF, BMP, ICO) simultaneously on a single canvas.
*   **Zoom In/Out:** Zoom in or out of individual images using the mouse scroll wheel.
*   **Rotate:** Rotate images to any angle using the slider or by entering a specific value.
*   **Flip:** Flip images horizontally.
*   **Adjust Opacity:** Change the transparency of the entire canvas, allowing you to see through the image layers more easily.
*   **Click-through Mode:**  Allows interaction with applications *beneath* the light table, even while it's displayed (Windows only).
*   **Always on Top:** Keep the light table window always visible on top of other windows.
*   **Reorder Images:** Drag and drop images in the list to change their display order (the image on top of the list will be displayed on top of the canvas).
*   **Save and Load State:** Save the entire current working state (including images, positions, rotation, zoom, settings) to an `.lts` file and reload it later to continue your work.
*   **Delete Image:** Remove selected image from the canvas.
* **Image Info**: Show file name, size, format of selected image.
*   **Keyboard Shortcuts:**
    *   `Ctrl + O`: Open/Close the light table.
    *   `Ctrl + Q`: Toggle Click-through mode.
    *   `Ctrl + E`: Toggle Always on Top mode.
* Drag and drop images to move them.

## Installation

1.  **System Requirements:**
    *   Python 3.6 or higher.
    *   Python libraries: `customtkinter`, `Pillow`, `keyboard`, `pywin32` (only required on Windows for Click-through functionality).

2.  **Installation Steps (Using `run.bat` - Recommended):**

    *   Download this repository (Clone or download ZIP).
    *   Open the downloaded folder.
    *   Run the `run.bat` file.  This will automatically create a virtual environment (`moitruongao`), install the necessary libraries, and run the application.

3.  **Installation Steps (Manual):**
    Open a terminal (command prompt or PowerShell on Windows):

    ```bash
    # Clone the repository (if not already downloaded)
    git clone https://github.com/Rin1809/Bang-Hat-Sang.git
    cd Bang-Hat-Sang

    # Create a virtual environment (optional but highly recommended)
    python -m venv moitruongao

    # Activate the virtual environment
    # On Windows:
    moitruongao\Scripts\activate
    # On Linux/macOS:
    source moitruongao/bin/activate

    # Install the libraries
    pip install -r requirements.txt
    ```

4.  **Run the Application:**

    ```bash
    # Make sure the virtual environment is activated (if you are using one)
    python Bang_Hat_Sang/main.py
    ```

## Detailed Usage Instructions

1.  **Open the Light Table:** Click the "Open Light Table" button on the main interface, or press `Ctrl + O`.

2.  **Add Images:**
    *   Click the "Select Images" button on the main interface. A file selection window will appear, allowing you to choose one or more images.
    *   After selecting images, they will appear in the image list on the left and on the canvas.

3.  **Select Images:**
    *   **Left-click** an image on the canvas to select it.
    *   **Left-click** an image in the list.
    *   **Hold `Ctrl` and click** multiple images in the list to select multiple images at once.
    *   The selected image(s) will be highlighted in the list.

4.  **Manipulate Images on the Canvas:**

    *   **Move:** Left-click and drag the selected image to the desired position.
    *   **Zoom In/Out:** Place the mouse cursor over the *selected* image, then *scroll the mouse wheel* up to zoom in, scroll down to zoom out.
    *   **Rotate:**
        *   Drag the "Rotate" slider on the interface.
        *   Or, select the image, then enter the desired rotation angle (in degrees).
    *   **Flip Horizontally:** Select the image and click the "Flip Horizontal" button.

5.  **Reorder Images (in the list):**
      Click the image thumbnail, drag and drop to the desired position in the list

6.  **Delete Images:**
    *   Select one or more images.
    *   Click the "Delete Image" button.

7.  **Change Opacity:** Drag the "Opacity" slider to change the transparency of the *entire canvas*.

8.  **Always on Top Mode:** Toggle the "Always on Top" switch to keep the light table window always visible.

9.  **Click-through Mode:**
    *   Toggle the "Click-through" switch.
    *   Or press `Ctrl + Q`.
    *   When this mode is enabled, you can click *through* the canvas to interact with windows/applications beneath it.

10. **Save State:** Click the "Save" button to save the current state (image list, positions, sizes, rotation, etc.) to an `.lts` file.

11. **Load State:** Click the "Load" button to open a previously saved `.lts` file and restore the working state.
12. **Image Info:** Details of the currently selected images will be displayed in the "Image Info" section.

</details>

<!-- Japanese -->
<details>
  <summary>🇯🇵 日本語</summary>

## 概要

**ライトテーブル (Bảng Hắt Sáng)** は、デジタルのライトテーブル（トレーシングボードとも呼ばれます）をシミュレートするシンプルな Python アプリケーションです。透明なキャンバス上に複数の画像を同時に表示、配置、操作できます。このアプリケーションは、画像の描画、比較、または複数の画像レイヤーを重ねる必要があるタスクに役立ちます。`customtkinter` と `Pillow` を使用して構築されています。

## 機能

*   **複数画像の表示:** 複数の画像 (PNG, JPG, JPEG, GIF, BMP, ICO) を1つのキャンバスに同時に読み込んで表示します。
*   **ズームイン/アウト:** マウスのスクロールホイールを使用して、個々の画像をズームインまたはズームアウトします。
*   **回転:** スライダーを使用するか、特定の値を入力して、画像を任意の角度に回転させます。
*   **反転:** 画像を水平方向に反転します。
*   **不透明度の調整:** キャンバス全体の透明度を変更して、画像レイヤーをより簡単に見やすくします。
*   **クリックスルーモード:** ライトテーブルが表示されている状態でも、その下にあるアプリケーションを操作できます (Windows のみ)。
*   **常に最前面:** ライトテーブルウィンドウを常に他のウィンドウの上に表示したままにします。
*   **画像の並べ替え:** リスト内の画像をドラッグアンドドロップして、表示順序を変更します (リストの一番上にある画像がキャンバスの一番上に表示されます)。
*   **状態の保存と読み込み:** 現在の作業状態全体 (画像、位置、回転、ズーム、設定を含む) を `.lts` ファイルに保存し、後で読み込んで作業を続行できます。
*   **画像の削除:** 選択した画像をキャンバスから削除します。
*　**画像情報**: 選択されている画像のファイル名・サイズ・形式を表示します。
*   **キーボードショートカット:**
    *   `Ctrl + O`: ライトテーブルを開く/閉じる。
    *   `Ctrl + Q`: クリックスルーモードの切り替え。
    *   `Ctrl + E`: 常に最前面モードの切り替え。
* 画像をドラッグ＆ドロップして移動。

## インストール

1.  **システム要件:**
    *   Python 3.6 以上。
    *   Python ライブラリ: `customtkinter`, `Pillow`, `keyboard`, `pywin32` (クリックスルー機能のために Windows でのみ必要)。

2.  **インストール手順 (`run.bat` の使用 - 推奨):**

    *   このリポジトリをダウンロードします (クローンまたは ZIP ダウンロード)。
    *   ダウンロードしたフォルダを開きます。
    *   `run.bat` ファイルを実行します。これにより、仮想環境 (`moitruongao`) が自動的に作成され、必要なライブラリがインストールされ、アプリケーションが実行されます。

3.  **インストール手順 (手動):**
    ターミナル (Windows ではコマンドプロンプトまたは PowerShell) を開きます。

    ```bash
    # リポジトリをクローンします (まだダウンロードしていない場合)
    git clone https://github.com/Rin1809/Bang-Hat-Sang.git
    cd Bang-Hat-Sang

    # 仮想環境を作成します (オプションですが、強く推奨します)
    python -m venv moitruongao

    # 仮想環境をアクティブ化します
    # Windows の場合:
    moitruongao\Scripts\activate
    # Linux/macOS の場合:
    source moitruongao/bin/activate

    # ライブラリをインストールします
    pip install -r requirements.txt
    ```

4.  **アプリケーションの実行:**

    ```bash
    # 仮想環境がアクティブ化されていることを確認してください (使用している場合)
    python Bang_Hat_Sang/main.py
    ```

## 詳細な使用方法

1.  **ライトテーブルを開く:** メインインターフェイスの「ライトテーブルを開く」ボタンをクリックするか、`Ctrl + O` を押します。

2.  **画像の追加:**
    *   メインインターフェイスの「画像を選択」ボタンをクリックします。ファイル選択ウィンドウが表示され、1つまたは複数の画像を選択できます。
    *   画像を選択すると、左側の画像リストとキャンバスに表示されます。

3.  **画像の選択:**
    *   キャンバス上の画像を**左クリック**して選択します。
    *   リスト内の画像を**左クリック**します。
    *   リスト内の複数の画像を **`Ctrl` キーを押しながらクリック**すると、複数の画像を一度に選択できます。
    *   選択した画像はリスト内で強調表示されます。

4.  **キャンバス上の画像の操作:**

    *   **移動:** 選択した画像を左クリックしてドラッグし、目的の位置に移動します。
    *   **ズームイン/アウト:** *選択した*画像の上にマウスカーソルを置き、*マウスホイールを上にスクロール*してズームイン、下にスクロールしてズームアウトします。
    *   **回転:**
        *   インターフェイスの「回転」スライダーをドラッグします。
        *   または、画像を選択し、目的の回転角度 (度単位) を入力します。
    *   **水平方向に反転:** 画像を選択し、「水平方向に反転」ボタンをクリックします。

5.  **画像の並べ替え (リスト内):**
    画像のサムネイルをクリックしてリスト内でドラッグ＆ドロップ

6.  **画像の削除:**
    *   1つまたは複数の画像を選択します。
    *   「画像を削除」ボタンをクリックします。

7.  **不透明度の変更:** 「不透明度」スライダーをドラッグして、*キャンバス全体*の透明度を変更します。

8.  **常に最前面モード:** 「常に最前面」スイッチを切り替えて、ライトテーブルウィンドウを常に表示したままにします。

9.  **クリックスルーモード:**
    *   「クリックスルー」スイッチを切り替えます。
    *   または、`Ctrl + Q` を押します。
    *   このモードが有効になっていると、キャンバスを*クリックして*、その下にあるウィンドウ/アプリケーションを操作できます。

10. **状態の保存:** 「保存」ボタンをクリックして、現在の状態 (画像リスト、位置、サイズ、回転など) を `.lts` ファイルに保存します。

11. **状態の読み込み:** 「読み込み」ボタンをクリックして、以前に保存した `.lts` ファイルを開き、作業状態を復元します。
12. **画像情報:** 選択している画像の詳細は[画像情報] セクションに表示されます。
</details>
