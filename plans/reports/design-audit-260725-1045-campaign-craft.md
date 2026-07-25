# Design Craft Audit — Galaxy Z Fold8 Campaign

**56/100. KHÔNG đạt ship bar (≥90). Gate cũng FAIL (lỗi wrap chữ "5.5-INCH" bị ngắt giữa cụm, tái hiện ở cả desktop lẫn mobile).** Lý do chính: nền đỏ-vệt-sáng dùng LẶP LẠI y hệt 5-6 lần xuyên suốt page (hero/ratio/decide/system), signature move "hinge line" trong README không thực sự tồn tại trên canvas (`.hero-hinge`/`.hero-word` bị `display:none`), và state "Transition" mới (scale 1.75, neo đáy) crop sản phẩm gần như không nhận diện được.

**Methodology deviation (phải nói rõ):** rubric v2 yêu cầu fresh adversarial judge subagent, tách biệt maker/judge. Tôi KHÔNG spawn judge riêng (single-agent, effort/time budget của task) — điểm số dưới là tự chấm bám sát rubric, KHÔNG phải blind judge score. Coi là chỉ số tham khảo, cần judge riêng trước khi ra quyết định ship thật.

Skills đã nạp thành công: `design-intelligence`, `critique-rubric` (cả hai load OK, không có fallback).

---

## Correctness Gate

| Check | Verdict | Bằng chứng |
|---|---|---|
| G1 — WCAG AA contrast | **PASS** | Đo pixel thật (PIL, công thức luminance WCAG) tại ~10 điểm: text `--paper #f0ece3` trên nền ảnh hero/ratio/system đo được 5.28:1 → 16.79:1 (worst case 5.28:1 tại vùng đỏ giữa hero — vẫn qua ngưỡng vì type cỡ lớn chỉ cần 3:1). Không quét toàn bộ pixel/mọi frame scroll — xem mục "chưa kiểm chứng". |
| G2 — Zero truncation / bad wrap | **FAIL** | `assets/pilots/...` không liên quan; lỗi ở label `.ratio-panel` "FOLDED / 5.5-INCH" wrap thành "FOLDED / 5.5-" xuống dòng "INCH" — tái hiện desktop (`d-06-ratio-00.png`) VÀ mobile (`m-03-ratio.png`). Ngắt giữa số đo, đúng như brief cảnh báo. |
| G3 — Construction lints | **FAIL (nhẹ)** | Dead code: CSS `.hero-hinge{display:none}.hero-word{display:none}` — signature move được khai báo trong README/FABLE-ART-DIRECTION nhưng bị tắt cứng, không render. Không phải lỗi vỡ layout, nhưng là construction defect (tính năng khai báo mà không có trên canvas). |
| G4 — DS/token fidelity | **PASS** | Toàn bộ ảnh chụp chỉ thấy 5 màu hệ thống (`--ink #0a0a0b`, `--paper #f0ece3`, `--lav #b9a9ff`, `--blue #1268ff`, `--coral #ff654f`) — không phát hiện màu lạ. |

Overflow ngang: `scrollWidth - innerWidth = 0` cả desktop 1440 và mobile 390 — **PASS**, không tràn ngang.

---

## 5 chiều Excellence (tự chấm, xem disclaimer trên)

| # | Chiều | Điểm | Ghi chú |
|---|---|---|---|
| 1 | Art direction & distinctiveness | 12/25 | Persona có khai báo rõ (museum black / warm paper / titanium lavender / Samsung blue / coral) nhưng thực thi yếu — 4/5 section chính (`#ratio`, `#decide`, `#system`, hero) dùng CHUNG một file `assets/hero-layers/hero-background-layer.png` (grep xác nhận 5-6 lần), chỉ khác lớp overlay/scrim. "Signature move" (hinge line mở 10:16→4:3) không tồn tại — chỉ còn 1 khung viền 1px scale nhẹ (so `d-01-hero-top.png` vs `d-02-hero-mid.png`: gần như không khác biệt). Đối chiếu Apple product page / Samsung.com: cả hai đều đổi backdrop/ánh sáng rõ rệt theo từng module sản phẩm — page này thì không. |
| 2 | Typographic craft | 13/20 | Type scale tự tin, tracking chặt, mono label làm tốt vai trò kỹ thuật (`d-08-system.png` "4.5mm/201g/4,800mAh"). Bị trừ nặng vì lỗi wrap "5.5-\nINCH" (G2) lặp lại 2 viewport, và tại khung chuyển tiếp ratio (`d-06-ratio-035.png`) cả 2 headline "...on." / "The consequen[ce]" đều bị cắt bởi mép viewport CÙNG LÚC — không đọc được câu nào trọn vẹn ở khoảnh khắc đó. |
| 3 | Composition & space | 12/20 | Views/Ratio section 2 state đầu (Folded, Open — `d-03`, `d-05`) bố cục full-bleed tự tin, cân bằng. Nhưng state **Transition mới** (`d-04-views-transition.png`) crop sản phẩm 3 cạnh (trên/trái/dưới) thành một dải chéo không nhận ra là điện thoại — phá nhịp thị giác vừa thiết lập ở 2 state kia. Đây là hệ quả trực tiếp của thay đổi scale 1.75 + neo đáy vừa deploy. |
| 4 | Color & light | 6/15 | Điểm yếu nhất — xác nhận định lượng: cùng 1 ảnh nền đỏ/vệt-sáng lặp lại xuyên hero → ratio → decide → system (grep `src="assets/hero-layers/hero-background-layer.png"` = 6 lần trong file). 4/8 section nhìn gần như đồng nhất về mood ánh sáng. Điểm sáng duy nhất: finale đổi tông đen gần tuyệt đối (`filter:brightness(.34)`, thấy rõ ở `d-09-finale.png`) — nhưng phải đến cuối trang mới có 1 nhịp nghỉ màu. |
| 5 | Detail density | 13/20 | Chi tiết tốt: mono coordinate "01–08" cố định theo rail, scroll-phase counter động, progress bar `#ratio`, swatch màu thật trong pills (`d-07-decide.png`), microcopy "SELECT A VIEW — THE DOCUMENT STAYS EXACTLY WHERE YOU LEFT IT." Bị trừ vì dead code (mục G3) và lỗi wrap cho thấy chưa polish hết pass cuối. |
| | **TỔNG** | **56/100** | Ship bar 90 — cách xa. |

**Reference duel:** so với Apple Galaxy-class product page (nhịp đổi ánh sáng/backdrop theo từng tính năng) và Samsung.com campaign — cả hai có backdrop RIÊNG cho mỗi khối nội dung; page này dùng 1 ảnh nền tái chế toàn trang → thua ở đúng điểm "mỗi section mang 1 sự thật sản phẩm riêng" mà chính README của project tự đặt ra làm thesis.

---

## Đánh giá 2 thay đổi vừa deploy

1. **Transition scale 1.75 + neo đáy panel:** KHÔNG nâng chất lượng — tạo vấn đề mới. Bằng chứng `d-04-views-transition.png`: bản lề bị crop 3 cạnh, không còn nhận diện được silhouette điện thoại, phá vỡ tính nhất quán với 2 state Folded/Open (đều full-device, cân đối). Đề xuất giảm scale hoặc đổi framing nguồn ảnh.
2. **3 panel #ratio dùng chung 1 backdrop + 1 overlay:** ĐÚNG hướng về mặt kỹ thuật/hiệu năng và giữ được contrast chữ tốt (đo 9.5–16.8:1 tại các điểm mẫu, `d-11-ratio-contrast-check.png`) — không có vụ "chữ đè sản phẩm" hay "2 panel chồng nhau" như lo ngại trong brief (đã kiểm tra `d-06-ratio-035.png`/`065.png`: sản phẩm 2 panel không chồng lấn nhau, chỉ 2 headline cùng bị crop mép — xem mục typographic craft). NHƯNG nó khuếch đại vấn đề monotony vì backdrop này TRÙNG với backdrop của `#decide` và `#system` ngay sau đó — 3 section liên tiếp nhìn giống hệt nhau.

---

## Top 5 việc cần làm (xếp theo tác động)

1. **Phân biệt backdrop mỗi section** (Art direction + Color&Light, tác động lớn nhất) — `#system` nên đổi sang nền tối/museum-black đúng persona đã khai báo thay vì tái dùng ảnh đỏ của hero; `#decide` cần tông riêng. ~30 phút (CSS filter/hue-rotate nhanh) đến nửa ngày (ảnh riêng thật).
2. **Sửa lỗi wrap "5.5-INCH"** — `white-space:nowrap` hoặc non-breaking hyphen trên label `.ratio-panel`, test lại 3 breakpoint. ~15 phút.
3. **Giảm crop state Transition** — scale 1.75 hiện tại quá gắt, đưa về ~1.1–1.3 hoặc đổi vùng crop nguồn để giữ bản lề trong khung nhìn. ~1 giờ (chỉnh + so lại với Folded/Open).
4. **Quyết định số phận `.hero-hinge`/`.hero-word`** — đang là dead code mâu thuẫn với tài liệu định hướng (README, FABLE-ART-DIRECTION.md tuyên bố đây là signature move). Hoặc dựng lại animation hinge thật (~2 giờ), hoặc xoá khỏi tài liệu định hướng cho khớp thực tế (~10 phút).
5. **Làm mượt khung chuyển tiếp ratio** — tại frac ~0.3–0.4 hai headline cùng bị crop mép cùng lúc, không đọc được câu nào; stagger fade opacity để chỉ 1 headline rõ tại 1 thời điểm. ~1 giờ.

---

## Ledger

- FACT: đã đọc README.md, index.html (đủ 101 dòng), CSS inline, JS inline.
- FACT: đã chụp + Read lại toàn bộ 19 ảnh (10 desktop + 4 mobile + 1 contrast-check + gate/overflow checks) trước khi chấm — không chấm mù.
- FACT: `git status --porcelain` tại thời điểm viết báo cáo chỉ còn thay đổi từ trước phiên (ASSET-CONTRACT.md, assets xoá, các file .md brief mới, .brv/, plans/, references/) — không có `index.html` hay bất kỳ file code nào bị tôi sửa.
- INFERENCE: monotony màu là do tái sử dụng 1 asset (không phải chủ đích nghệ thuật) — dựa trên grep tìm thấy đúng 1 filename lặp lại; chưa hỏi được ý đồ thật của người thiết kế.
- ASSUMPTION: coi ngắt dòng giữa cụm số đo là lỗi gate (G2), không phải chọn lọc có chủ đích — hợp lý vì brief đã liệt kê đúng ví dụ này là điều cần kiểm tra.

## Chưa kiểm chứng

- Không quét contrast từng pixel/mọi khung hình scroll — chỉ mẫu ~10 điểm đại diện.
- Không chụp tablet 768px (README liệt kê là mốc verify nhưng brief chỉ yêu cầu desktop 1440 + mobile 390).
- Không test pointer-parallax (mousemove tilt hero/ratio/system) — Playwright scroll-based, không simulate hover delta thật.
- Không chụp prefers-reduced-motion path.
- Điểm 5-chiều là tự chấm (single-agent), CHƯA qua judge riêng biệt/blind theo đúng yêu cầu rubric v2 — cần re-run với judge subagent trước khi dùng số này để quyết định ship.

## Câu hỏi chưa giải đáp

1. Việc dùng chung 1 ảnh nền cho 4 section có phải chủ đích (giảm asset debt, xem `ASSET-DEBT.md`) hay là thiếu sót chưa kịp làm ảnh riêng?
2. `.hero-hinge`/`.hero-word` bị tắt có chủ đích (đổi hướng thiết kế) hay là dở dang?
3. Có cần tôi spawn judge subagent riêng để chấm lại theo đúng chuẩn "blind judge" của rubric v2 không, hay điểm tự chấm này đã đủ dùng cho mục đích hiện tại?
