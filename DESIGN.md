---
name: Project Mastery
description: A clear practice workbench for reading, coding, and interpreting feedback.
colors:
  bg: "#0a0a0a"
  surface: "#121212"
  raised: "#1b1b1b"
  hover: "#272727"
  border: "#383838"
  border-strong: "#7a7a7a"
  text: "#ededed"
  muted: "#b8b8b8"
  subtle: "#9e9e9e"
  accent: "#d4d4d4"
  accent-ink: "#101010"
  accent-hover: "#f0f0f0"
  accent-soft: "#2b2b2b"
  selection: "#4a4a4a"
  code: "#d6d6d6"
  success: "#d4d4d4"
  danger: "#e0e0e0"
  danger-surface: "#242424"
  syntax-keyword: "#e5e5e5"
  syntax-string: "#c3c3c3"
  syntax-number: "#d4d4d4"
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
  working-panel: "12px"
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
    padding: "11px"
    width: "300px"
  problem-card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.container}"
    padding: "25px"
---

# Design System: Project Mastery

## Overview

**Creative North Star: "A clear practice workbench"**

The user-selected dark workspace uses restrained light grey accents to keep reading, editing, and diagnostic feedback central. Black grounds and charcoal surfaces make a compact, familiar tool environment. System UI type is intentional for this code workspace; monospaced code and mathematical notation retain their own functional voices.

The source is the implemented global stylesheet and workspace, shell, learning, experiment, and retrieval-project components. This record captures shipped choices rather than introducing a new identity. Dense controls serve the work, while larger reading regions retain generous line height. Motion is limited to control feedback, expanding results, and running state.

**Key Characteristics:**

- Black and charcoal surfaces with light grey actions, selections, and diagnostic labels.
- Compact controls, readable prose, and real monospaced code.
- Flat bordered panels with feedback adjacent to the editor.
- Connected reading, experiment, and project surfaces with responsive navigation and a mobile description/code switch.

## Colors

The user-selected palette is black and light grey throughout, including syntax, charts, and diagnostics. The frontmatter is the normative primitive source; repeated values represent distinct semantic roles.

### Primary

- **Light grey** (`accent`): actions, selected controls, links, focus outlines, and measured values. `accent-hover` lightens primary action hover and `accent-soft` fills selected states.
- **Black action ink** (`accent-ink`): text on light grey actions.

### Neutral

- **Black ground** (`bg`): page canvas and inset reading regions.
- **Charcoal surface** (`surface`): editor, fields, and workbench.
- **Raised charcoal** (`raised`) and **hover charcoal** (`hover`): distinct working and interactive surfaces.
- **Grey boundaries** (`border`, `border-strong`): panel separation and stronger field/action outlines respectively.
- **Reading white** (`text`), **muted grey** (`muted`), and **subtle grey** (`subtle`): content hierarchy.
- **Selection grey** (`selection`) and **code grey** (`code`): selected text and code reading.

Diagnostic success uses `success`; errors use `danger` and `danger-surface`. These are monochrome semantic roles: explicit wording and icons communicate the outcome. Syntax uses grey tones, bold keywords, and italic comments.

### Named Rules

**The Explicit State Rule.** Use icons and wording to distinguish diagnostic states; light grey emphasis and tonal surfaces support interaction without relying on hue.

## Typography

**Body and heading font:** Segoe UI with system-ui and sans-serif fallbacks.
**Code font:** Consolas with Liberation Mono and monospace fallbacks.
**Formula font:** Georgia with serif fallback.

The hierarchy is functional rather than promotional. UI labels remain compact; prose line height increases in explanation regions. No separate display face is established.

### Hierarchy

- **Headline:** the frontmatter headline role is the default exercise title; it reduces to 24px below 1250px and 23px below 700px. General page headings use 35px and reduce to 29px on mobile. Connected learning headings use 36px, a 24ch maximum width, and 28px on mobile.
- **Title:** the frontmatter title role serves content sections; smaller section headings use 15px at weight 600.
- **Body:** the frontmatter body role is the base. Exercise prose uses 13px with 1.85 line height, growing to 14px on large desktops. Page lead copy uses 15px with 1.8 line height and a 620px maximum width.
- **Label:** compact primary and secondary actions use the frontmatter label role. Supporting controls and navigation commonly use 12–13px.
- **Code:** the editor uses the code role, wrapping long lines. Inline code is 0.92em; reference and diagnostic blocks use smaller monospaced text.

**The Separate Reading Roles Rule.** Use UI type for explanations and controls, monospace for code and filenames, and serif notation only for mathematics.

## Layout

Desktop uses a fixed left sidebar and a flexible main region. The sidebar is 216px by default, 240px from 1600px, 185px at 1250px and below, and a 67px icon rail at 950px and below. At 700px and below it becomes a wrapping header with a horizontally scrollable navigation row above the content.

The workbench uses a description/editor grid with a 7px separator. The initial description width is 44%; pointer and keyboard resizing constrain it to 30–62%. Toolbars align across the two panes at 46px high. The editor, run controls, and results form one vertical working column. Desktop panels scroll internally; focus mode expands the editor across the workbench.

At 700px and below, a two-option switch presents description or code in a single column. The separator disappears, content flows vertically, and run buttons share the available width. Inline replacement confirmations wrap above the editor. General content pages use a centered 1070px maximum width, with 54px/44px desktop vertical/horizontal entry padding and 32px/20px mobile padding.

Connected learning pages extend to a 1160px maximum width, keep prose within 72ch, and use divider-led lesson rows. Learning entry sections use a 1.2fr/1fr grid; open experiments use a 210px topic column beside the working surface. Comparison controls use two columns and rankings three. At 1100px, continuation/project introductions stack and search spans the filter grid; at 700px, learning, experiment, and comparison layouts become single-column, with horizontally scrolling experiment topics. Tables retain horizontal overflow within their container.

Spacing favors compact 4–12px control gaps and 16–28px content insets. Preserve room for explanatory prose rather than applying the toolbar density to every region.

## Elevation & Depth

The application stylesheet defines no box shadows. Depth comes from tonal surface differences and thin grey boundaries. The workbench is one enclosing container with internal dividers, not a pile of independently elevated cards. Monaco owns its editor overlays.

**The Flat Workbench Rule.** Separate adjacent working regions with tone and borders; retain the existing flat surface treatment.

## Shapes

Corners are restrained: compact badges and icon controls use the compact radius; ordinary actions, navigation, and search use the control radius; examples, hints, and reference code use the content radius; major workbench and catalog containers use the container radius. Continuation, project entry, and experiment panels use the working-panel radius. Borders are generally 1px. Icons are stroke SVGs, not textual glyph substitutes.

## Components

### Buttons

Compact and legible. Primary actions use light grey with dark ink; secondary actions use a dark charcoal fill and subdued border. Both use the frontmatter control shape and padding, with a 35px minimum height and a 7px icon gap. Primary hover lightens the fill over 0.16 seconds; secondary actions retain their fill and use the stronger boundary. Disabled buttons reduce opacity to 0.48 and use a not-allowed cursor. Keyboard focus uses a 2px accent outline offset by 4px. Icon buttons are 29px squares with compact corners and a charcoal hover fill.

### Chips

The difficulty badge is a passive label: a soft charcoal fill, light grey text, compact corners, and 2px/8px vertical/horizontal padding. Do not imply filter behavior for this noninteractive badge.

### Cards / Containers

Catalog cards use the frontmatter container style, a thin boundary, and a horizontal content/action arrangement. Mobile cards wrap with 20px padding and place the action after the description. Hints use disclosure controls; examples and code references use darker inset surfaces. Containers do not gain hover elevation.

### Inputs / Fields

Search uses a bordered charcoal field with an icon, transparent input, and muted placeholder. Its width becomes fluid on mobile. A 2px accent outline with a 2px offset surrounds the whole field on focus-within. No error variant for general text fields is established.

### Navigation

Navigation links have compact corners, muted text, and SVG icons. Hover uses a raised charcoal surface; the current page has a soft charcoal fill and pale text. The rail becomes icon-only at the medium breakpoint; mobile restores text labels and horizontal scrolling above content. Resource tabs use text emphasis and a 2px accent underline, with keyboard arrow navigation. The mobile workspace switch uses filled selection rather than an underline.

### Connected learning and experiment surfaces

Lesson rows use a bottom divider, compact metadata, a clear title, and a trailing continuation or completion indicator; hover changes the background to the raised surface. Continuation and project entry panels use a raised fill, thin border, and larger working-panel corners.

Experiments place native range controls beside visible outputs, explanatory prose, and SVG or CSS diagrams. Measurements use tabular figures; definition-list values and table cells use Consolas. Reading pages use underlined light grey text links to connect lessons, experiments, and projects. Project evidence uses native disclosure rows, comparison tables, rankings, and a resizable reflection textarea. Selects and textareas use charcoal surfaces, stronger boundaries, control corners, 10px/12px padding, and visible focus outlines.

### Editor and feedback

The Monaco theme shares the charcoal surface with its surrounding workbench. Line numbers, indentation, current line, and selection use distinct subdued tones; syntax uses monochrome tokens with bold keywords and italic comments. Theme inheritance is disabled and the default token uses the neutral text color; editor overlays, selection, cursor, and diagnostics also use the shared grey roles. Minimap, folding, and glyph margin are disabled, with 20px editor top/bottom padding and 4-space tabs.

Run controls sit directly above diagnostic results. Individual test rows are expandable and pair passed/failed wording with icons and color. Result chevrons rotate over 0.18 seconds. A spinner indicates running work. Reduced-motion preference disables CSS transitions and animations. Confirmation prompts for replacing code remain inline and wrap rather than becoming a modal.

## Do's and Don'ts

### Do:

- **Do** retain dark charcoal working surfaces and light grey interaction emphasis with explicitly labelled diagnostic states.
- **Do** preserve distinct UI, code, and mathematics type roles.
- **Do** keep keyboard focus visible and pair result color with explicit status text.
- **Do** adapt navigation and workspace panels to the available width.

### Don't:

- **Don't** turn restrained accents into large bright decorative panels.
- **Don't** replace the flat workbench with shadow-heavy floating cards.
- **Don't** encode success or failure through color alone.
- **Don't** apply dense toolbar typography to long instructional paragraphs.
