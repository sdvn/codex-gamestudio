<p align="center">
  <h1 align="center">Codex Game Studio</h1>
  <p align="center">
    Biến một phiên Codex thành một game studio có workflow rõ ràng.
    <br />
    39 workflow. 48 role brief. Một bộ kit production theo hướng Codex-first.
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="plugins/codex-game-studio/skills"><img src="https://img.shields.io/badge/workflows-39-1f7a1f" alt="39 workflows"></a>
  <a href="plugins/codex-game-studio/references/roles"><img src="https://img.shields.io/badge/roles-48-0f766e" alt="48 roles"></a>
  <a href="plugins/codex-game-studio/references/templates"><img src="https://img.shields.io/badge/templates-26-9a3412" alt="26 templates"></a>
  <a href="docs/engine-reference"><img src="https://img.shields.io/badge/engine%20refs-46-334155" alt="46 engine references"></a>
  <a href="plugins/codex-game-studio/.codex-plugin/plugin.json"><img src="https://img.shields.io/badge/runtime-Codex-111827" alt="Codex runtime"></a>
</p>

<p align="center">
  <a href="README.md">English</a> · <strong>Tiếng Việt</strong>
</p>

> Đây là bản port Codex-native từ repo gốc
> [`Donchitos/Claude-Code-Game-Studios`](https://github.com/Donchitos/Claude-Code-Game-Studios),
> đã được dọn lại và tổ chức lại để dùng tự nhiên hơn trong Codex.

## Repo Này Để Làm Gì

Làm game cần cấu trúc rõ ràng, nhưng một phiên chat thuần thường không tạo ra
được các lane riêng cho thiết kế, triển khai, review, production planning và
release. Repo này biến cách làm việc đó thành một mô hình studio kỷ luật hơn
cho Codex.

Bạn vẫn là người ra quyết định. Repo chỉ cung cấp cho Codex một shape làm việc
tốt hơn: workflow có tên, role brief có thể tái sử dụng, template tài liệu và
reference note theo engine.

## Có Gì Trong Repo

| Hạng mục | Số lượng | Mô tả |
|----------|----------|-------|
| **Workflow** | 39 | Điểm vào skill cho planning, review, production, implementation và release |
| **Role Brief** | 48 | Brief chuyên môn cho design, programming, art, QA, production và engine work |
| **Template** | 26 | Mẫu tài liệu cho GDD, ADR, milestone, retrospective, release và reverse-documentation |
| **Engine Reference** | 46 | Ghi chú theo phiên bản cho Godot, Unity và Unreal |

## Cấu Trúc Studio

Thư viện role giữ nguyên mô hình studio 3 tầng:

| Tầng | Trọng tâm | Ví dụ |
|------|-----------|-------|
| **Leadership** | Định hướng và xử lý xung đột | `creative-director`, `technical-director`, `producer` |
| **Department Leads** | Sở hữu theo domain | `game-designer`, `lead-programmer`, `art-director`, `qa-lead` |
| **Specialists** | Thực thi trực tiếp | `gameplay-programmer`, `ui-programmer`, `writer`, `technical-artist`, `qa-tester` |

Các role này nằm trong `plugins/codex-game-studio/references/roles/` và được
dùng như role brief cho Codex, không phải custom subagent type của một sản phẩm khác.

## Workflow Chính

**Khởi tạo dự án**

`game-studio` `start` `setup-engine` `bootstrap-engine` `project-stage-detect`

**Thiết kế và lập kế hoạch**

`brainstorm` `map-systems` `design-system` `design-review` `architecture-decision` `estimate`

**Nhóm triển khai**

`team-combat` `team-ui` `team-level` `team-narrative` `team-audio` `team-polish` `team-release`

**Review và vận hành**

`code-review` `perf-profile` `balance-check` `asset-audit` `scope-check` `tech-debt` `release-checklist` `launch-checklist` `hotfix`

## Preview

<p align="center">
  <img src="plugins/codex-game-studio/assets/preview-studio-overview.png" alt="Ảnh preview tổng quan Codex Game Studio" width="100%" />
</p>

<table>
  <tr>
    <td width="50%">
      <img src="plugins/codex-game-studio/assets/preview-workflow-router.png" alt="Ảnh preview luồng workflow" />
    </td>
    <td width="50%">
      <img src="plugins/codex-game-studio/assets/preview-reference-stack.png" alt="Ảnh preview reference và validation" />
    </td>
  </tr>
  <tr>
    <td>Các lane workflow rõ ràng cho onboarding, design, implementation và release control.</td>
    <td>Hệ tài liệu chung, engine reference và validation rule giúp Codex bám đúng repo.</td>
  </tr>
</table>

## Bắt Đầu Nhanh

1. Mở repo này trong Codex và để Codex load local marketplace từ `.agents/plugins/marketplace.json`.
2. Xác nhận plugin `codex-game-studio` đã xuất hiện. Nếu danh sách plugin chưa cập nhật, mở lại workspace để Codex reload plugin local.
3. Bắt đầu bằng một trong các prompt sau:

   ```text
   Use game-studio to route this repo
   Run start and onboard me from scratch
   Use setup-engine for a Godot project, then run bootstrap-engine
   ```

4. Giữ các quyết định chung của studio trong `docs/CODEX-STUDIO.md`.
5. Giữ quy ước theo engine trong `docs/studio/technical-preferences.md`.
6. Chạy `bootstrap-engine` sau khi pin engine xong nếu bạn cần bộ file runtime thật.
7. Khi dự án đã vào guồng, gọi trực tiếp workflow phù hợp với phần việc đang làm.

## Bố Cục Repo

```text
.
├── .agents/plugins/marketplace.json
├── docs/
│   ├── CODEX-STUDIO.md
│   ├── studio/technical-preferences.md
│   └── engine-reference/
├── plugins/
│   └── codex-game-studio/
│       ├── .codex-plugin/plugin.json
│       ├── skills/
│       ├── references/roles/
│       ├── references/templates/
│       └── references/studio/
└── production/session-state/
```

## Luồng Làm Việc Điển Hình

1. Bắt đầu bằng `game-studio` nếu muốn route tổng quát, hoặc `start` nếu repo vẫn đang là template trắng.
2. Chạy `setup-engine` một lần để chốt engine, ngôn ngữ và đường dẫn reference đang dùng.
3. Chạy `bootstrap-engine` để tạo runtime scaffold thật cho Godot, Unity hoặc Unreal.
4. Dùng các skill planning như `brainstorm`, `map-systems`, `design-system` và `architecture-decision`.
5. Chuyển sang triển khai với các workflow `team-*` phù hợp với lát cắt công việc hiện tại.
6. Dùng `gate-check`, `release-checklist`, `launch-checklist` và `hotfix` để kiểm soát giai đoạn sau.

## File Quan Trọng

- `plugins/codex-game-studio/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `docs/CODEX-STUDIO.md`
- `docs/studio/technical-preferences.md`
- `plugins/codex-game-studio/references/roles/`
- `plugins/codex-game-studio/references/templates/`
