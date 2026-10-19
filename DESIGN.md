---
name: Project Mastery
description: A clear practice workbench for reading, coding, and interpreting feedback.
colors:
  bg: "#0c110f"
  surface: "#111715"
  raised: "#17201b"
  hover: "#1e2a23"
  border: "#2a3830"
  text: "#e1e9e4"
  muted: "#9aac9f"
  subtle: "#7d9385"
  accent: "#a1dfb3"
  accent-ink: "#112319"
  danger: "#f1a4a0"
typography:
  headline:
    fontFamily: '"Segoe UI", system-ui, sans-serif'
    fontSize: "27px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.025em"
  title:
    fontFamily: '"Segoe UI", system-ui, sans-serif'
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.015em"
  body:
    fontFamily: '"Segoe UI", system-ui, sans-serif'
    fontSize: "14px"
    lineHeight: 1.6
  label:
    fontFamily: '"Segoe UI", system-ui, sans-serif'
    fontSize: "11px"
    fontWeight: 600
  code:
    fontFamily: 'Consolas, "Liberation Mono", monospace'
    fontSize: "14px"
    lineHeight: "24px"
rounded:
  compact: "4px"
  control: "6px"
  content: "7px"
  standard: "8px"
  container: "10px"
spacing:
  tight: "4px"
  small: "8px"
  control: "12px"
  content: "16px"
  section: "20px"
  roomy: "24px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "8px 12px"
  button-secondary:
    backgroundColor: "{colors.hover}"
    rounded: "{rounded.control}"
    typography: "{typography.label}"
    padding: "8px 12px"
  search-field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.control}"
    padding: "9px 13px"
    width: "300px"
  problem-card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.container}"
    padding: "25px"
---

# Design System: Project Mastery

## Overview

**Creative North Star: "A clear practice workbench"**

The user-selected dark workspace uses restrained green accents to keep reading, editing, and diagnostic feedback central. Deep green-black grounds and subdued forest surfaces make a compact, familiar tool environment. System UI type is intentional for this code workspace; monospaced code and mathematical notation retain their own functional voices.

The source is the implemented global stylesheet and workspace, shell, and catalog components. This record captures shipped choices rather than introducing a new identity. Dense controls serve the work, while larger reading regions retain generous line height. Motion is limited to control feedback, expanding results, and running state.

**Key Characteristics:**

- Dark forest surfaces with pale green actions and selections.
- Compact controls, readable prose, and real monospaced code.
- Flat bordered panels with feedback adjacent to the editor.
- Responsive navigation and a mobile description/code switch.

## Colors

The palette is a near-black forest range with pale green emphasis and a distinct warm error signal; the frontmatter is the normative primitive source.

### Primary

- **Pale green** (`accent`): primary actions, active tabs, focus outlines, and passed results.
- **Deep green ink** (`accent-ink`): readable text on pale green actions.

### Neutral

- **Green-black ground** (`bg`): the page canvas.
- **Forest surface** (`surface`): workbench, editor, search, and catalog cards.
- **Raised forest** (`raised`) and **hover forest** (`hover`): interactive surface changes.
- **Forest boundary** (`border`): thin panel and toolbar separation.
- **Light reading text** (`text`), **muted text** (`muted`), and **subtle text** (`subtle`): the hierarchy of content and supporting labels.

Error feedback uses `danger` with explicit failure labels and icons. Monaco also uses lavender keywords, sage strings, and warm numeric tokens; these are syntax roles, not additional brand accents.

### Named Rules

**The Meaningful Green Rule.** Use pale green for actionable, selected, focused, or successful states; keep the large working surfaces dark.

## Typography

**Body and heading font:** Segoe UI with system-ui and sans-serif fallbacks.
**Code font:** Consolas with Liberation Mono and monospace fallbacks.
**Formula font:** Georgia with serif fallback.

The hierarchy is functional rather than promotional. UI labels remain compact; prose line height increases in explanation regions. No separate display face is established.

### Hierarchy

- **Headline:** the frontmatter headline role is the default exercise title; it reduces to 24px below 1250px and 23px below 700px. General page headings use 35px and reduce to 29px on mobile.
- **Title:** the frontmatter title role serves content sections; smaller section headings use 15px at weight 600.
- **Body:** the frontmatter body role is the base. Exercise prose uses 13px with 1.85 line height, growing to 14px on large desktops. Page lead copy uses 15px with 1.8 line height and a 620px maximum width.
- **Label:** compact primary and secondary actions use the frontmatter label role. Supporting controls and navigation commonly use 12–13px.
- **Code:** the editor uses the code role, wrapping long lines. Inline code is 0.92em; reference and diagnostic blocks use smaller monospaced text.

**The Separate Reading Roles Rule.** Use UI type for explanations and controls, monospace for code and filenames, and serif notation only for mathematics.

## Layout

Desktop uses a fixed left sidebar and a flexible main region. The sidebar is 216px by default, 240px from 1600px, 185px at 1250px and below, and a 67px icon rail at 950px and below. At 700px and below it becomes a horizontal 62px navigation bar above the content.

The workbench uses a description/editor grid with a 7px separator. The initial description width is 44%; pointer and keyboard resizing constrain it to 30–62%. Toolbars align across the two panes at 46px high. The editor, run controls, and results form one vertical working column. Desktop panels scroll internally; focus mode expands the editor across the workbench.

At 700px and below, a two-option switch presents description or code in a single column. The separator disappears, content flows vertically, and run buttons share the available width. Inline replacement confirmations wrap above the editor. General content pages use a centered 1070px maximum width, with 54px/44px desktop vertical/horizontal entry padding and 32px/20px mobile padding.

Spacing favors compact 4–12px control gaps and 16–28px content insets. Preserve room for explanatory prose rather than applying the toolbar density to every region.

## Elevation & Depth

The application stylesheet defines no box shadows. Depth comes from tonal surface differences and thin forest borders. The workbench is one enclosing container with internal dividers, not a pile of independently elevated cards. Monaco owns its editor overlays.

**The Flat Workbench Rule.** Separate adjacent working regions with tone and borders; retain the existing flat surface treatment.

## Shapes

Corners are restrained: compact badges and icon controls use the compact radius; ordinary actions, navigation, and search use the control radius; examples, hints, and reference code use the content radius; major workbench and catalog containers use the container radius. Borders are generally 1px. Icons are stroke SVGs, not textual glyph substitutes.

## Components

### Buttons

Compact and legible. Primary actions use pale green with dark ink; secondary actions use a dark forest fill and subdued border. Both use the frontmatter control shape and padding, with a 35px minimum height and a 7px icon gap. Hover lightens the fill over 0.16 seconds. Disabled buttons reduce opacity to 0.48 and use a not-allowed cursor. Keyboard focus uses a 2px accent outline offset by 4px. Icon buttons are 29px squares with compact corners and a forest hover fill.

### Chips

The difficulty badge is a passive label: a dark green fill, light green text, compact corners, and 2px/8px vertical/horizontal padding. Do not imply filter behavior for this noninteractive badge.

### Cards / Containers

Catalog cards use the frontmatter container style, a thin boundary, and a horizontal content/action arrangement. Mobile cards wrap with 20px padding and place the action after the description. Hints use disclosure controls; examples and code references use darker inset surfaces. Containers do not gain hover elevation.

### Inputs / Fields

Search uses a bordered forest field with an icon, transparent input, and muted placeholder. Its width becomes fluid on mobile. A 2px accent outline with a 2px offset surrounds the whole field on focus-within. No error variant for general text fields is established.

### Navigation

Navigation links have compact corners, muted text, and SVG icons. Hover uses a raised forest surface; the current page has a brighter forest fill and pale text. The rail becomes icon-only at the medium breakpoint and moves above content on mobile. Resource tabs use text emphasis and a 2px accent underline, with keyboard arrow navigation. The mobile workspace switch uses filled selection rather than an underline.

### Editor and feedback

The Monaco theme shares the forest surface with its surrounding workbench. Line numbers, indentation, current line, and selection use distinct subdued tones; syntax retains semantic color. Minimap, folding, and glyph margin are disabled, with 20px editor top/bottom padding and 4-space tabs.

Run controls sit directly above diagnostic results. Individual test rows are expandable and pair passed/failed wording with icons and color. Result chevrons rotate over 0.18 seconds. A spinner indicates running work. Reduced-motion preference disables CSS transitions and animations. Confirmation prompts for replacing code remain inline and wrap rather than becoming a modal.

## Do's and Don'ts

### Do:

- **Do** retain dark forest working surfaces and meaningful pale green emphasis.
- **Do** preserve distinct UI, code, and mathematics type roles.
- **Do** keep keyboard focus visible and pair result color with explicit status text.
- **Do** adapt navigation and workspace panels to the available width.

### Don't:

- **Don't** turn restrained accents into large bright decorative panels.
- **Don't** replace the flat workbench with shadow-heavy floating cards.
- **Don't** encode success or failure through color alone.
- **Don't** apply dense toolbar typography to long instructional paragraphs.
