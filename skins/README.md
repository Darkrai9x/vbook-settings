# Skin trang đọc vBook

Skin là một bộ "trang phục" cho trang đọc chữ: nền, khung giấy, header / footer riêng, ảnh, màu đổi theo giờ trong ngày. Skin không nằm sẵn trong app. Người dùng tải về từ kho (Cài đặt đọc → **Skin**) hoặc nhập file `.zip` từ máy.

Trang này dành cho người muốn tự làm skin. Dùng AI để làm skin: cho nó đọc [`AGENTS.md`](AGENTS.md) (đặc tả đầy đủ), [`skin.schema.json`](skin.schema.json) và bắt đầu từ [`template/`](template/).

- [Cấu trúc gói](#cấu-trúc-gói)
- [Thử skin](#thử-skin)
- [skin.json](#skinjson)
- [Màu: token, timeline, palette](#màu-token-timeline-palette)
- [Layer](#layer)
- [Biểu thức và biến](#biểu-thức-và-biến)
- [Đưa lên kho](#đưa-lên-kho)
- [Mẹo](#mẹo)

---

## Cấu trúc gói

Một skin là một thư mục. Nén thư mục đó (hoặc nội dung của nó) thành `.zip`:

```
my_skin/
├── skin.json        ← bắt buộc
├── preview.jpg      ← ảnh một trang, tỷ lệ 3:4, rộng ~480 px
└── images/…         ← ảnh skin dùng (jpg / png / webp)
```

Giới hạn:
- File zip ≤ 32 MB, giải nén ≤ 128 MB. Nên giữ dưới 1–2 MB vì skin được tải trên điện thoại.
- `id` chỉ gồm `A–Z a–z 0–9 _ -`, tối đa 64 ký tự. Nhập một skin cùng `id` sẽ thay skin cũ.
- Đường dẫn ảnh là đường dẫn tương đối trong gói. `..` và đường dẫn tuyệt đối bị bỏ qua.

## Thử skin

1. Nén thư mục thành `my_skin.zip` và chép sang máy.
2. Trong trang đọc, mở **Cài đặt → Skin**, bấm nút tải lên ở góc trên, rồi chọn file.
3. Sửa rồi nhập lại: cùng `id` thì skin được thay ngay.

Nhấn giữ một skin đã cài để **Xoá** hoặc **Cập nhật** (khi kho có bản mới hơn).

## skin.json

```json
{
  "schema": 1,
  "minApp": 1,
  "id": "my_skin",
  "version": 1,
  "name": { "en": "My skin", "vi": "Skin của tôi" },
  "description": { "en": "One line about it", "vi": "Một dòng giới thiệu" },
  "author": "Tên bạn",
  "preview": "preview.jpg",
  "tokens": { "background": "#efe6d2", "text": "#2b2520", "accent": "#8c2f45" },
  "body": { "top": 96, "bottom": 80, "left": 28, "right": 28 },
  "layers": []
}
```

| Khoá | Ý nghĩa |
|---|---|
| `schema` | Luôn `1`. |
| `minApp` | Mức tính năng skin cần. App hiện ở mức `1`; skin cần mức cao hơn sẽ bị ẩn khỏi kho và không nhập được. |
| `id` | Định danh, cũng là tên thư mục cài. Trong kho, `id` phải trùng tên thư mục nguồn. |
| `version` | Số nguyên. Tăng lên mỗi lần sửa thì người đã cài sẽ thấy nút **Cập nhật**. |
| `name`, `description` | Theo mã ngôn ngữ; thiếu ngôn ngữ của người dùng thì dùng `en`. |
| `author`, `preview` | Tác giả; ảnh xem trước trong gói. |
| `tokens`, `timeline`, `palettes` | Màu, xem [bên dưới](#màu-token-timeline-palette). |
| `body` | Vùng chữ: khoảng cách (dp) từ mép an toàn của trang vào. Khi bật skin, lề của người dùng được thay bằng giá trị này. Thanh tiến độ mặc định cũng bị tắt, vì header / footer nằm trong phần `top` / `bottom` của skin. |
| `imageSets` | Bộ ảnh đánh số, xem layer [`set`](#set). |
| `layers` | Những thứ được vẽ, theo thứ tự. |

Khoá lạ bị bỏ qua, và layer có `type` lạ thì bị bỏ qua chứ không làm hỏng cả skin. Nhờ vậy app cũ vẫn mở được skin mới.

### Kích thước

Mọi số đo đều là **dp**, tức "điểm" không phụ thuộc mật độ điểm ảnh (khoảng 1/160 inch). Một điện thoại rộng khoảng 360–430 dp. Thiết kế phải co giãn được: đừng giả định một khổ màn hình cố định, và nhớ rằng màn ngang / máy gập có thể hiện hai trang cạnh nhau.

## Màu: token, timeline, palette

Màu được đặt tên (**token**). Một giá trị có thể là:
- `#rrggbb` hoặc `#rrggbbaa`,
- tên một token khác (`"muted": "glow"`),
- một trong hai dạng trên kèm độ đục: `"faint": "glow@22%"`.

App đọc hai token:
- `text`: màu chữ truyện,
- `background`: màu nền trang (dưới mọi layer).

Các token còn lại tuỳ bạn đặt tên rồi dùng trong layer (`"color": "accent"`, `"fill": "paper"`).

### timeline: màu theo giờ

```json
"timeline": [
  { "at": "05:30", "tokens": { "background": "#e7dccd", "glow": "#3d2c2a" } },
  { "at": "12:00", "tokens": { "background": "#ebe1cb" } },
  { "at": "19:45", "tokens": { "background": "#e9d2b5" } },
  { "at": "20:00", "tokens": { "background": "#17121a", "text": "#d6cab3" } }
]
```

- Mỗi mốc là một giờ trong ngày. Giữa hai mốc, màu được pha dần (tính theo không gian màu Oklab).
- Màu cập nhật theo bước 15 phút và nối vòng qua nửa đêm.
- Muốn **đổi hẳn** (ví dụ ngày → đêm), đặt hai mốc cách nhau ≤ 15 phút như `19:45` → `20:00` ở trên. Nếu để pha từ từ, sẽ có lúc chữ xám nằm trên nền xám, rất khó đọc.
- Timeline đè lên `tokens`.

### palettes: màu theo điều kiện

```json
"palettes": [
  { "when": { "dark": true }, "tokens": { "background": "#0f0c0d", "text": "#d8cdb7" } }
]
```

Palette đè lên cả timeline. Nhiều palette cùng khớp thì palette viết sau thắng. Điều kiện `when` xem ở [phần layer](#điều-kiện-when).

Trên máy e-ink, mọi màu thành đen / trắng và ảnh không được vẽ. Skin vẫn phải đọc được khi chỉ còn chữ và nét kẻ.

## Layer

Mỗi layer có các khoá chung sau:

| Khoá | Mặc định | Ý nghĩa |
|---|---|---|
| `type` | | `image`, `set`, `text`, `shape`, `texture`. |
| `anchor` | `page` | Vùng đặt layer: `page` (cả trang), `body` (vùng chữ), `top` (dải trên vùng chữ), `bottom` (dải dưới). |
| `rect` | cả vùng | Vị trí trong vùng, xem dưới. |
| `z` | tuỳ loại | `< 0` vẽ **dưới** chữ, `≥ 0` vẽ **trên** chữ. Cùng phía thì vẽ theo thứ tự trong mảng. |
| `opacity` | `1` | 0..1. |
| `when` | luôn | Điều kiện hiện. |

### rect

Đặt vị trí kiểu `position: absolute` của CSS, đơn vị dp, tính từ vùng `anchor`:
- Có `left` thì ghim mép trái, có `right` thì ghim mép phải. Có cả hai thì layer giãn giữa hai mép.
- `width` cho bề rộng. Chỉ có `width` mà không có `left` / `right` thì layer nằm giữa theo chiều ngang. Chiều dọc tương tự với `top` / `bottom` / `height`.
- Không cho gì trên một trục thì layer phủ kín trục đó.
- Số âm thì layer vượt ra ngoài vùng: `"rect": { "left": -14, "right": -14, "top": -12, "bottom": -12 }` là tờ giấy rộng hơn vùng chữ 14 / 12 dp mỗi bên.

### Điều kiện `when`

Mọi điều kiện ghi ra đều phải đúng thì layer mới hiện:
- `pages`: `"first"` (trang mở đầu chương) hoặc `"other"`.
- `dark`: `true` / `false` theo chế độ tối của app.
- `time`: `"HH:mm-HH:mm"` theo giờ máy. Khoảng được phép qua nửa đêm, ví dụ `"20:00-05:30"`.

### image

```json
{ "type": "image", "src": "images/corner.png", "fit": "contain", "anchor": "top", "rect": { "right": 16, "top": 8, "width": 48, "height": 48 }, "z": 1 }
```

`fit` nhận `crop` (mặc định: lấp đầy, cắt phần thừa), `contain` (vừa khít, không cắt) hoặc `fill` (kéo giãn).

### set

Hiện ảnh từ một bộ ảnh đánh số, chọn theo biểu thức. Ví dụ: mỗi chương một lá bài, hoặc một dải ảnh ở footer.

```json
"imageSets": { "cards": { "pattern": "cards/card-{i:2}.jpg", "count": 22 } },
"layers": [
  { "type": "set", "set": "cards", "pick": "chapterSeed % 22", "count": 1, "anchor": "top", "rect": { "right": 24, "top": 12, "width": 40, "height": 67 }, "radius": 3, "z": 1 },
  { "type": "set", "set": "cards", "pick": "chapterSeed + page.index - 4", "count": 7, "highlight": 3, "gap": 4, "anchor": "bottom", "rect": { "top": 16, "width": 164, "height": 33 }, "z": 1 }
]
```

- `pattern`: `{i}` là số thứ tự, `{i:2}` là số thứ tự đệm số 0 đủ 2 chữ số. Bộ ảnh có tối đa 128 ảnh.
- `pick`: chỉ số ảnh đầu tiên (một biểu thức), được tự quay vòng trong bộ ảnh.
- `count`: số ảnh trên một hàng, tối đa 32. Các ảnh cách nhau `gap` dp và có bo góc `radius`.
- `highlight`: vị trí (tính từ 0 trong hàng) của ảnh được vẽ rõ; các ảnh còn lại mờ theo `dim` (mặc định 0.45).

### text

```json
{ "type": "text", "value": "{chapter.title}", "anchor": "top", "rect": { "left": 24, "top": 30, "right": 80, "height": 24 }, "size": 15, "color": "glow", "font": "serif", "weight": 600 }
```

| Khoá | Mặc định | Ý nghĩa |
|---|---|---|
| `value` | | Mẫu chữ. `{…}` là một [biểu thức](#biểu-thức-và-biến). |
| `size` | `12` | Cỡ chữ, sp (4–96). |
| `color` | `text` | Token hoặc mã màu. |
| `font` | font đọc | `serif`, `sans`, `mono`; bỏ trống thì dùng font đọc của người dùng. |
| `weight`, `italic` | `400`, `false` | Độ đậm và nghiêng. |
| `align` | `start` | `start`, `center`, `end`. Tự đảo khi ngôn ngữ viết từ phải sang trái. |
| `letterSpacing` | `0` | sp. |
| `maxLines` | `1` | Số dòng tối đa (đến 8); phần thừa bị cắt bằng dấu "…". |

### shape

```json
{ "type": "shape", "anchor": "page", "fill": "background", "fillEnd": "fog", "z": -3 }
{ "type": "shape", "anchor": "body", "rect": { "left": -14, "right": -14, "top": -12, "bottom": -12 }, "stroke": "rule", "strokeWidth": 1.2, "radius": 4, "z": -2 }
{ "type": "shape", "anchor": "bottom", "rect": { "left": 24, "right": 24, "top": 75, "height": 1.5 }, "fill": "accent", "progress": "chapter.progress", "z": 1 }
```

- `shape`: `rect` (mặc định), `line` (nét ngang giữa hộp, cần `stroke`) hoặc `circle`.
- `fill`: màu nền. Thêm `fillEnd` thì nền thành dải chuyển màu từ trên xuống dưới, tính theo cả trang nên không bị lộ đường nối giữa các layer.
- `stroke`, `strokeWidth`: viền.
- `radius`: bo góc.
- `progress`: một biểu thức cho giá trị 0..1; hộp chỉ được vẽ chừng ấy phần chiều rộng. Dùng để làm thanh tiến độ.

### texture

Vân giấy có sẵn trong app, phủ lên vùng của layer:

```json
{ "type": "texture", "texture": "aged", "anchor": "body", "rect": { "left": -14, "right": -14, "top": -12, "bottom": -12 }, "radius": 4, "opacity": 0.55, "z": -2 }
```

`texture` nhận `paper`, `do` (giấy dó), `linen` hoặc `aged` (giấy cũ). Ban đêm nên giảm `opacity`: tách thành hai layer có `when.time` khác nhau.

## Biểu thức và biến

Mọi thứ trong `{…}` của `text.value`, cùng `set.pick` và `shape.progress`, là một biểu thức nhỏ. Biểu thức hỗ trợ:
- giá trị: số, `'chuỗi'`, `true` / `false`,
- phép toán: `+ - * / %`, so sánh `== != < <= > >=`, logic `&& || !`,
- điều kiện ba ngôi `a ? b : c` và dấu ngoặc.

Biểu thức không có vòng lặp và không gán được. Biểu thức sai cho ra chuỗi rỗng chứ không làm lỗi skin.

| Biến | Ý nghĩa |
|---|---|
| `book.name` | Tên sách |
| `chapter.title` | Tên chương |
| `chapter.index`, `chapter.count` | Chương thứ mấy (đếm từ 1) / tổng số chương |
| `page.index`, `page.count` | Trang thứ mấy trong chương (đếm từ 1) / số trang của chương |
| `chapter.progress`, `book.progress` | Tiến độ 0..1 |
| `chapterSeed` | Số nguyên ổn định cho mỗi chương (băm từ tên sách + tên chương). Dùng để chọn ngẫu nhiên nhưng cố định, ví dụ `chapterSeed % 22` |
| `first` | Đang ở trang mở đầu chương |
| `dark` | Chế độ tối |
| `time.hour`, `time.minute` | Giờ (0–23) / phút tính từ nửa đêm, theo bước 15 phút |
| `dayProgress` | Thời điểm trong ngày, 0..1 |
| `phase` | `'dawn'` 05–08h, `'day'` 08–17h, `'dusk'` 17–20h, `'night'` |

| Hàm | Ví dụ |
|---|---|
| `percent(x)` | `percent(chapter.progress)` → `42.5%` |
| `roman(n)` | `roman(chapter.index)` → `XII` |
| `pad(n, w)` | `pad(page.index, 3)` → `007` |
| `upper(s)` | `upper(chapter.title)` |
| `pick(i, a, b, …)` | `pick(chapterSeed % 3, 'Xuân', 'Hạ', 'Thu')` |
| `if(c, a, b)` | `if(first, 'Mở đầu', '')` |
| `min`, `max`, `clamp(x, lo, hi)`, `lerp(a, b, t)`, `floor`, `round`, `abs`, `sin` | Toán |

## Đưa lên kho

Kho là repo này: nguồn skin nằm trong `skins/src/<id>/`.

1. Thêm thư mục skin vào `skins/src/` (có `skin.json` và `preview`) và tăng `version` nếu là bản sửa.
2. Chạy `python3 skins/build.py`. Script đóng gói `skins/<id>.zip`, chép ảnh xem trước vào `skins/previews/` và viết lại `skins/catalog.json`, danh sách app đọc qua `app_reader_skin_url`.
3. Commit cả nguồn lẫn những gì script sinh ra.

Ảnh dùng trong skin phải là ảnh tự làm, ảnh public domain hoặc CC0. Ghi nguồn trong `SOURCES.md` của skin. Không dùng ảnh hay logo có bản quyền của game, phim, truyện.

## Mẹo

- **Một mặt nền.** Header, footer và trang nên cùng một tông. Một khung tối bọc tờ giấy sáng sẽ trông như hai mảng rời nhau.
- **Tương phản.** Chữ trên nền cần tỷ lệ tương phản ≥ 4.5:1, ở **mọi** mốc giờ.
- **Đổi ngày / đêm dứt khoát**, không pha từ từ (xem [timeline](#timeline-màu-theo-giờ)).
- **Ảnh nhẹ.** Thẻ, góc, hoạ tiết vài chục KB là đủ; ảnh nền toàn trang nên dưới 300 KB (WebP / JPEG).
- **Thử hai trang.** Trên màn ngang hoặc máy gập, mỗi trang được vẽ skin riêng và gáy sách nằm giữa.
- **Cuộn dọc.** Skin đứng yên quanh vùng chữ (header / footer vẫn cập nhật theo chỗ đang đọc), chữ cuộn bên trong `body`.
- Xem các skin trong `src/` để có ví dụ đầy đủ:
  - `gray_fog`: bộ ảnh lá bài, timeline bốn buổi.
  - `co_thu`: chỉ dùng shape, text và một ảnh dấu chỉ hiện ở trang đầu chương.
  - `dem_sao`: skin tối, bộ ảnh tuần trăng, ảnh sao đổi độ đậm theo giờ.
  - `hai_trinh`: biểu thức toạ độ theo `chapterSeed`, hải đồ mờ đi ban đêm.
  - `terminal`: font `mono`, màu chữ đổi xanh / hổ phách theo giờ, vạch quét vẽ trên chữ (`z` dương).
  - `khoi`: bộ ảnh 24 khung trời (`pick: "time.hour"`) và 9 khung hotbar (`pick: "page.index - 1"`): đổi hình theo giờ / theo trang bằng `set`.
  - `dong_bo`, `tap_chi`: header khác nhau giữa trang mở đầu chương và các trang sau (`when.pages`).
  - `thuy_mac`, `anh_dao`, `mua_thu`, `halloween`, `noel`, `xuan`, `ha`, `dong`: một ảnh lớn ở dải `top` làm cảnh, ảnh phủ cả trang (`anchor: page`, `z` âm) làm hoa / lá / tuyết rơi.

Ảnh rộng đặt ở dải `top` nên có tỷ lệ gần với dải đó (rộng gấp 6–7 lần cao): `crop` sẽ cắt hai bên chứ không cắt mất phần trời.
