# Code audit — Galaxy Z Fold8 campaign implementation (260725-1045)

Phạm vi: chỉ implementation quality (không thẩm mỹ). Read-only, không sửa code. Mọi số đo lấy từ lệnh thật trên `/Users/jang/Products/galaxy-z-fold8-campaign` (darwin, HEAD `d2003dd`).

## 3 vấn đề nghiêm trọng nhất

1. **QA gate luôn fail giả** — `scripts/verify-page.py:12-16` còn 5 asset đã bị xoá khỏi working tree (`hero-open.png`, `view-folded.png`, `commerce-ghost.png`, `system-lab.jpg`, `finale-macro.png`), không file nào được `index.html` tham chiếu → `python3 scripts/verify-page.py` thoát mã 1, verifier "deterministic" của dự án vô dụng ngay bây giờ.
2. **18.59MB ảnh tải eager, không lazy/srcset** — `index.html` tham chiếu 15 file ảnh phân biệt tổng 18.59MB (đo bằng script, không ước tính), không img nào có `loading`/`decoding`/`srcset` (0 kết quả grep) → toàn bộ tải ngay khi mở trang, kể cả ảnh full-res 1672×941 dùng làm thumbnail hover 430px (`index.html:79`).
3. **CSS/JS nén 1 dòng, vi phạm rule >200 dòng phải modular hoá** — khối `<style>` (index.html:11-38) là 28 dòng vật lý nhưng 18,881 ký tự (dòng dài nhất 2011 ký tự, index.html:23); JS (index.html:85-98) là 14 dòng / 6,488 ký tự. Không thể diff/test/lint theo dòng. **Nhưng đây là xung đột với chính constraint của dự án**: `AGENTS.md:17` bắt buộc "No runtime dependencies or build step. Inline CSS and JavaScript in `index.html`" — tách file sẽ vi phạm hard rule của dự án. Xem mục Kiến trúc bên dưới.

---

## 1. Kiến trúc & khả năng bảo trì

| # | Phát hiện | Bằng chứng | Mức độ | Cách sửa ngắn nhất |
|---|---|---|---|---|
| 1.1 | CSS/JS minify-tay, không format | `sed -n '11,38p' index.html \| wc -c` = 18881 ký tự / 28 dòng; dòng 23 dài 2011 ký tự | major | **Xung đột constraint**: `AGENTS.md` cấm build step/tách file. Fix an toàn = reformat tại chỗ (thêm newline/indent thủ công, vẫn 1 file, 0 dependency) chứ không tách file. ~20 phút CSS + 15 phút JS. |
| 1.2 | `data-reveal`/`.reveal`/`initReveals()` là dead code | `grep -c '\.reveal{'` = 1, rule đó **chỉ tồn tại trong `@media(prefers-reduced-motion:reduce)`** (index.html:38: `.js .reveal{opacity:1;transform:none;clip-path:none}`) — không có rule base nào khác. Playwright đo `getComputedStyle(document.querySelector('.reveal')).opacity` = `"1"` ngay từ đầu (không cần scroll). `IntersectionObserver` ở index.html:94 toggle class `.is-visible` nhưng `grep -c '\.is-visible'` (không tính JS) = 0 — class không có CSS nào định nghĩa. | major | Toàn bộ hệ thống "entrance reveal" (5 elements: index.html:63,75,77,79) không có hiệu ứng, chỉ tốn 1 `IntersectionObserver` vô nghĩa. Xoá `data-reveal`/`.reveal`/`initReveals()` (10 phút) HOẶC viết lại CSS state thật cho `[data-reveal]` (30-45 phút nếu muốn hiệu ứng thật). |
| 1.3 | `.section-bg` lặp markup 10 lần | `grep -c section-bg index.html` = 10 occurrences, cùng 1 src `assets/hero-layers/hero-background-layer.png` mỗi lần. Đã xác nhận **không phải performance issue** (browser cache 1 request duy nhất — nằm trong 15 file distinct, không tính trùng ở tổng 18.59MB) — chỉ là duplication markup thuần. | minor | Không bắt buộc sửa do ràng buộc 1-file. Nếu muốn giảm lặp: JS render `<img class="section-bg">` từ 1 template lúc init (~20 phút), không thêm dependency. |
| 1.4 | Repo gốc lẫn lộn file rác/scratch chưa dọn | `ls` root: 9 file `CODEX-*.md`/`.codex-*.txt` chưa track, `.brv/`, `references/` (12M), `assets/pilots/` (9.0M) untracked; 10 file working-tree bị xoá (`git status --porcelain`) chưa commit. Không ảnh hưởng runtime nhưng gây nhiễu khi Grep/Glob tìm file theo rule kebab-case self-documenting. | minor | `git add`/`git rm` dọn theo lô một lần khi có chủ đích (không thuộc phạm vi audit này — cần approval trước khi động vào git state). ~15 phút review + commit. |

## 2. Đúng đắn / robustness

| # | Phát hiện | Bằng chứng | Mức độ | Cách sửa |
|---|---|---|---|---|
| 2.1 | Scroll handler **đã** đúng pattern rAF + passive | index.html:97: `addEventListener('scroll',requestRender,{passive:true})`, có biến `ticking` gate qua `requestAnimationFrame`. **Đây là điểm làm tốt**, không phải bug. | — | Không cần sửa. Ghi nhận để không bị hiểu nhầm là thiếu throttle. |
| 2.2 | `initSectionScrollDepth()` gọi `getBoundingClientRect()` cho 8 layer mỗi rAF tick khi scroll | Đếm attribute thật (không tính CSS var): `grep -oE '<[a-z]+ class="[^"]*"[^>]*data-depth[^>]*>' index.html` → 8 phần tử. Code index.html:92 loop `layers.forEach` đọc `rect` rồi ghi `style.setProperty` ngay trong cùng vòng lặp cho từng layer. | minor | Rủi ro forced-reflow thấp vì chỉ ghi `transform` (không kích layout), nhưng vẫn 8 lần đọc layout/tick. Có thể cache `rect` 1 lần/tick bằng `ResizeObserver` thay vì đọc lại mỗi frame nếu muốn tối ưu — ~30 phút, không bắt buộc. |
| 2.3 | `prefers-reduced-motion` + `pointer:coarse` fallback có thật và hoạt động | index.html:37 (`@media(hover:none),(pointer:coarse)`) và :38 (`prefers-reduced-motion:reduce`) tắt `will-change`, tắt parallax; JS `initDepth()` (index.html:96) check `coarse.matches\|\|reduced.matches` trước khi gắn `pointermove`. Verified bằng Playwright: không lỗi console ở 3 viewport, `scrollWidth-innerWidth`=0 cả 3. | — | Không cần sửa — đúng theo README §Verification target #5. |
| 2.4 | **Robustness khi ảnh fail load**: text rơi xuống 2.46:1 contrast ở vùng không có gradient overlay | Test thật: block toàn bộ `*.png`/`*.jpg` qua Playwright route interception → `getComputedStyle('.hero-sticky').backgroundColor` = `rgb(255,101,79)` = `--coral` (index.html:13). Contrast paper `#f0ece3` / coral `#ff654f` = **2.46:1** (tính bằng công thức WCAG relative luminance, không ước lượng) — dưới ngưỡng AA large-text (3:1). Vùng bị lộ: `.hero-phase` (bottom-right, không nằm trong gradient `.hero-grid::after` chỉ phủ tới 72% từ trái, index.html:19), `.commerce-product .mono` (index.html:25). Screenshot xác nhận `/tmp/fold8-noimg.png`: label "Scroll phase / Intro / 00" mờ trên nền coral. | major | Thêm `background:var(--ink)` (hoặc darken) cho `.hero-sticky`/`.commerce-product`/`.laboratory` thay vì `--coral` làm màu nền chờ ảnh — 1 dòng CSS mỗi selector, ~15 phút, không đổi visual khi ảnh load bình thường (ảnh phủ kín nền). |
| 2.5 | JS không có `noscript`, nhưng nội dung chính vẫn đọc được nếu JS tắt | `grep -c noscript` = 0. Kiểm tra tay: heading/copy/CTA đều là HTML tĩnh (không render bằng JS), chỉ animation/switcher/parallax mất. Đúng với rule AGENTS.md:19 "readable if JavaScript fails". | — | Không có action — xác nhận đạt yêu cầu, không phải thiếu sót. |

## 3. Hiệu năng

| # | Phát hiện | Bằng chứng | Mức độ | Cách sửa |
|---|---|---|---|---|
| 3.1 | Tổng 18.59MB ảnh cho 1 trang, tải hết ngay | Script Python đo thật tổng `os.path.getsize()` của 15 file distinct mà `index.html` tham chiếu (src/data-src/data-preview) = **18.59 MB**. Riêng viewport đầu (`hero-bg`+`hero-product`) đã 3.1MB (`du -ch`). | blocker (cho mobile/3G) | Thêm `loading="lazy" decoding="async"` cho mọi `<img>` ngoài hero (13/15 ảnh) — ~15 phút, 0 risk vì không đổi asset. |
| 3.2 | Ảnh preview hover (430px hiển thị) nhưng serve full-res 1672×941 PNG ~1.5-1.8MB/file | `index.html:79` data-preview trỏ 5 file trong `assets/campaign-series-v3/` (`du -h` mỗi file 1.5M-1.8M), hiển thị qua `.index-preview{width:min(30vw,430px)...}` (index.html:29). | major | Tạo bản resize/nén riêng (không phải regenerate — không vi phạm ASSET-CONTRACT "do not modify source imagery" vì là derivative cho delivery) bằng `sips`/`magick` xuống ~480px + convert PNG→WebP: ~30 phút cho 5 file + đo dung lượng thật sau khi làm. |
| 3.3 | Font tự host `.ttf`, không có `.woff2` | `du -h assets/fonts/*` = 6 file TTF, tổng 532K (đo bằng `du -h`, không WOFF2 nào tồn tại trong repo — `find assets/fonts -name '*.woff2'` không kiểm tra nhưng listing đầy đủ ở trên chỉ có .ttf). `font-display:swap` đã có (index.html:11) — tốt, tránh FOIT. | minor | Convert bằng `fonttools varLib.instancer`/`woff2_compress` CLI — nén thường 30-50% nhưng **chưa đo thật trên font này**, cần đo sau khi convert. ~20 phút. |
| 3.4 | Không CLS rõ ràng vì `width`/`height` đã có trên mọi `<img>` | `grep -c '<img'` = 15, tất cả có `width="1672" height="941"` (đọc trực tiếp source) → trình duyệt reserve đúng tỷ lệ khung hình trước khi ảnh load. Đây là điểm làm đúng. | — | Không cần sửa. |
| 3.5 | `will-change:transform` trên 12 vị trí CSS, tắt đúng lúc qua coarse/reduced media query | `grep -c will-change` = 12; index.html:37 set `will-change:auto` khi `hover:none,pointer:coarse`; index.html:38 set lại `auto` khi reduced-motion. Không phát hiện leak will-change vĩnh viễn. | — | Không cần sửa. |

## 4. Accessibility

| # | Phát hiện | Bằng chứng | Mức độ | Cách sửa |
|---|---|---|---|---|
| 4.1 | Switcher `role="tab"` thiếu `tabpanel`/`aria-controls` | index.html:63-64: 3 `<button role="tab">` trong `role="tablist"`, ảnh kết quả (`.views-stage`) không có `role="tabpanel"`/`id`. Playwright đo thật: `document.querySelector('[role=tabpanel]')` = `null`, `aria-controls` trên tab đầu = `null`. Vi phạm APG Tabs pattern — AT không biết panel nào liên kết với tab nào. | major | Thêm `id="views-stage"` cho `.views-stage`, `role="tabpanel"` + `aria-controls="views-stage"` trên mỗi button. ~15 phút. |
| 4.2 | Roving tabindex không đúng chuẩn APG (nhưng vẫn dùng được) | JS `initSwitcher()` (index.html:93) xử lý ArrowUp/Down/Left/Right để `.focus()` nhưng không set `tabindex="-1"` cho tab không active — cả 3 button vẫn nằm trong Tab order mặc định của trình duyệt (không phải bug chức năng, chỉ lệch APG spec). | minor | Thêm roving `tabindex` (`0` active / `-1` inactive) — ~15 phút, tuỳ chọn. |
| 4.3 | Contrast fallback coral/paper dưới AA khi ảnh fail | Xem mục 2.4 — cùng 1 root cause, liệt lại ở đây vì là accessibility issue thật sự (2.46:1 < 3:1 AA large-text). | major (trùng 2.4) | Xem fix ở 2.4. |
| 4.4 | Heading order hợp lệ | `grep -o '<h[1-6]'` cho thứ tự: 1×h1 → 8×h2 → 1×h3 (đúng vị trí lồng trong h2 ratio-story, không nhảy cấp). `verify-page.py` cũng check `h1` count = 1 — pass được phần này độc lập với 5 lỗi asset. | — | Không cần sửa. |
| 4.5 | `:focus-visible` global tồn tại, hoạt động | index.html:14: `:focus-visible{outline:2px solid var(--coral);outline-offset:4px}` áp dụng toàn trang, không override riêng lẻ làm mất outline ở component nào (grep không thấy `outline:none` nào khác trong file). | — | Không cần sửa. |

## 5. Nợ kỹ thuật đã biết (xác nhận bằng lệnh thật)

| # | Phát hiện | Bằng chứng | Mức độ | Cách sửa |
|---|---|---|---|---|
| 5.1 | `verify-page.py` `REQUIRED_ASSETS` trỏ asset đã xoá | Chạy `python3 scripts/verify-page.py` → `VERIFY FAILED`, liệt đúng 5 file: `hero-open.png, view-folded.png, commerce-ghost.png, system-lab.jpg, finale-macro.png`. `grep -c` từng tên trong `index.html` = 0 cho cả 5 → không file nào còn được dùng, xoá khỏi `REQUIRED_ASSETS` là an toàn. | blocker (cho CI/QA) | Sửa `scripts/verify-page.py:12-16`, xoá 5 dòng đó (hoặc thay bằng danh sách asset thật đang dùng: 15 file đã liệt ở mục 3.1). ~5-10 phút + chạy lại verify để confirm PASS. |
| 5.2 | Working tree lẫn tracked-deleted + untracked mới, chưa reconcile | `git status --porcelain` (baseline đầu phiên = cuối phiên, không đổi): 10 dòng ` D`/`??` hỗn hợp. Không phải bug code nhưng là rủi ro thao tác (dễ commit nhầm/sót). | minor | Review + `git add -A`/`git rm` có chủ đích 1 lần, ngoài phạm vi audit này (cần chủ động approval, không tự ý xử lý). |

---

## Ước lượng tổng thời gian nếu fix theo thứ tự ưu tiên

1. Sửa `verify-page.py` REQUIRED_ASSETS (5.1) — **5-10 phút** — mở blocker CI trước tiên.
2. Thêm `loading="lazy"`/`decoding="async"` (3.1) — **15 phút**.
3. Fix fallback background color thay coral (2.4/4.3) — **15 phút**.
4. Thêm `tabpanel`/`aria-controls` cho switcher (4.1) — **15 phút**.
5. Xoá hoặc implement thật `data-reveal` system (1.2) — **10-45 phút** tuỳ chọn xoá hay làm thật.
6. Resize+nén ảnh preview hover (3.2) — **30 phút** + đo lại dung lượng thật.
7. Convert font TTF→WOFF2 (3.3) — **20 phút** + đo lại dung lượng thật.
8. Reformat CSS/JS tại chỗ, không tách file (1.1) — **35 phút**.

Tổng nếu làm hết mục blocker+major: **~2-2.5 giờ**. Mục minor (1.3, 1.4, 2.2, 4.2, 5.2): thêm **~1.5 giờ** nếu muốn dọn triệt để.

---

## Ledger

- FACT: mọi số đo trong bảng trên lấy từ lệnh thật (`du`, `wc`, `grep -c`, `sips`, Playwright DOM/contrast/screenshot) chạy trong phiên này trên HEAD `d2003dd`.
- FACT: `git status --porcelain` trước và sau audit giống hệt nhau (không file code nào bị đổi, chỉ báo cáo này được tạo mới).
- INFERENCE: nguyên nhân gốc của 1.1 (monolith) là **constraint có chủ đích** từ `AGENTS.md`, không phải sơ suất — đã surface xung đột với global rule >200 dòng thay vì đề xuất tách file.
- ASSUMPTION: `campaign-series-v3/` (không transparent) tồn tại chỉ để phục vụ index-preview hover — chưa grep hết tất cả cách dùng khác ngoài `data-preview`, có thể còn dùng ở nơi khác chưa audit kỹ (OG tags, sitemap...).
- NOT VERIFIED: screen-reader thật (VoiceOver/NVDA), test trên thiết bị di động vật lý, hành vi khi `assets/fonts/*.ttf` fail load (không test riêng), độ chính xác contrast trên các cặp màu khác ngoài 5 cặp đã tính.

## Câu hỏi chưa giải đáp

1. `AGENTS.md` cấm build step/tách file — team có chấp nhận derivative asset (resize/WebP cho preview, WOFF2 cho font) như một ngoại lệ ngoài "no build step", hay coi đó cũng là vi phạm cần né?
2. `campaign-series-v3/` (15MB, non-transparent) và `section-cutouts/` (7.2MB, transparent) trùng nội dung ảnh — có phải giữ cả 2 bộ vĩnh viễn, hay `campaign-series-v3` chỉ nên giữ 5 file thực sự được `data-preview` dùng (giảm ngay ~6MB rác)?
3. Việc dọn `git status` (10 file D/??, xoá deleted 10 file cũ + track file mới) có nằm trong scope của ai — team lead hay agent khác — và khi nào?
