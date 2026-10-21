"""
Study sheet: Project 01, steps 1-2 (The First Call & Memory).

Render (from the ai-engineering folder):
    notes/.venv/Scripts/manim -s --disable_caching --media_dir notes/media notes/p01_steps1_2.py Sheet
"""

from manim import *

# A4 landscape at 300 dpi.
config.pixel_width = 3508
config.pixel_height = 2480
config.frame_width = 16
config.frame_height = 16 * 2480 / 3508

BG = "#0E1116"
PANEL = "#161B22"
CODEBG = "#0A0D12"
FG = "#E6EDF3"
DIM = "#8B949E"
BLUE = "#58C4DD"
GOLD = "#F0AC5F"
GREEN = "#83C167"
RED = "#FC6255"
TEAL = "#5CD0B3"
PURPLE = "#A98BDB"
PINK = "#E87BD0"
YELLOW = "#FFD95A"
config.background_color = BG

SANS = "Segoe UI"
MONO = "Consolas"
BODY = 15
SMALL = 12.5
CODE = 12.5
TITLE = 16


# ---------- markup helpers (Pango markup; never put raw < > & in text) ----------

def c(s, col):
    return f'<span foreground="{col}">{s}</span>'


def b(s):
    return f"<b>{s}</b>"


def m(s, col=None):
    """Inline monospace, optionally colored."""
    color = f' foreground="{col}"' if col else ""
    return f'<span font_family="{MONO}"{color}>{s}</span>'


# code syntax colors
def kw(s): return c(s, PURPLE)
def st(s): return c(s, GREEN)
def ty(s): return c(s, TEAL)
def fn(s): return c(s, BLUE)
def nm(s): return c(s, GOLD)
def cm(s): return c(s, DIM)


def T(s, size=BODY, color=FG, bold=False, font=SANS):
    return Text(s, font=font, font_size=size, color=color, weight=BOLD if bold else NORMAL)


def mk(markup, size=BODY, color=FG, font=SANS):
    return MarkupText(markup, font=font, font_size=size, color=color)


def para(lines, size=BODY, buff=0.07, color=FG):
    return VGroup(*[mk(line, size, color) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def chip(label, col, size=CODE, font=MONO, fill_op=0.16, text_col=FG, bold=False):
    t = T(label, size, text_col, bold=bold, font=font)
    h = T("Mg", size, font=font).height + 0.16
    r = RoundedRectangle(corner_radius=0.07, width=t.width + 0.26, height=h,
                         stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=fill_op)
    t.move_to(r)
    return VGroup(r, t)


def code_block(lines, size=CODE, width=None):
    """lines: list of (indent_chars, markup). Leading spaces have no glyph, so indent by hand."""
    char_w = 0.12181 * size / 16
    rows = VGroup()
    for indent, markup in lines:
        row = mk(markup, size, FG, font=MONO)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    for (indent, _), row in zip(lines, rows):
        row.shift(RIGHT * indent * char_w)
    w = width if width else rows.width + 0.32
    bg = RoundedRectangle(corner_radius=0.08, width=w, height=rows.height + 0.26,
                          fill_color=CODEBG, fill_opacity=1, stroke_color="#2A313C", stroke_width=1.5)
    rows.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.16)
    return VGroup(bg, rows)


def warn_icon(col=YELLOW):
    tri = Triangle(fill_color=col, fill_opacity=1, stroke_width=0).scale(0.14)
    ex = T("!", 12, BG, bold=True).move_to(tri.get_center() + DOWN * 0.015)
    return VGroup(tri, ex)


def panel(x_left, top, w, h, accent, num, title, xp):
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=accent,
                           stroke_width=3, fill_color=PANEL, fill_opacity=1)
    box.move_to([x_left + w / 2, top - h / 2, 0])
    tt = T(f"{num}  {title}", TITLE, BG, bold=True)
    tab = RoundedRectangle(corner_radius=0.08, width=tt.width + 0.34, height=0.42,
                           fill_color=accent, fill_opacity=1, stroke_width=0)
    tab.move_to(box.get_corner(UL) + RIGHT * (0.22 + tab.width / 2))
    tt.move_to(tab)
    xpt = T(f"+{xp} XP", SMALL, accent, bold=True)
    xpb = RoundedRectangle(corner_radius=0.08, width=xpt.width + 0.24, height=0.32,
                           fill_color=PANEL, fill_opacity=1, stroke_color=accent, stroke_width=2)
    xpb.move_to(box.get_corner(DR) + LEFT * (0.22 + xpb.width / 2))
    xpt.move_to(xpb)
    return box, VGroup(box, tab, tt, xpb, xpt)


def place(content, box, name, top_pad=0.45, side=0.22, bottom=0.2, align_left=False):
    maxw = box.width - 2 * side
    maxh = box.height - top_pad - bottom
    if content.width > maxw:
        print(f"[fit] {name}: width {content.width:.2f} > {maxw:.2f}, scaling")
        content.scale_to_fit_width(maxw)
    if content.height > maxh:
        print(f"[fit] {name}: height {content.height:.2f} > {maxh:.2f}, scaling")
        content.scale_to_fit_height(maxh)
    content.move_to(box.get_center())
    content.align_to(box.get_top() + DOWN * top_pad, UP)
    if align_left:
        content.align_to(box.get_left() + RIGHT * side, LEFT)
    return content


def arrow(a, b_, col=DIM):
    return Arrow(a, b_, buff=0.06, stroke_width=3, color=col, max_tip_length_to_length_ratio=0.22)


# ---------- grid ----------
X = [-7.8, -3.85, 0.1, 4.05]
W1 = 3.75
ROW1_TOP, ROW1_H = 4.45, 4.75
ROW2_TOP, ROW2_H = -0.75, 4.2


class Sheet(Scene):
    def construct(self):
        self.add(self.header(), self.footer())
        self.add(*self.panel_call())
        self.add(*self.panel_types())
        self.add(*self.panel_tokens())
        self.add(*self.panel_boss())
        self.add(*self.panel_stop())
        self.add(*self.panel_memory())
        self.add(*self.panel_traps())

    # ----- header / footer -----
    def header(self):
        lvl = chip("LEVEL 01", GOLD, size=17, font=SANS, fill_op=1, text_col=BG, bold=True)
        title = T("LLM API FUNDAMENTALS", 32, FG, bold=True)
        top = VGroup(lvl, title).arrange(RIGHT, buff=0.3)
        sub = mk(f"Project 01  ·  Steps 1–2  ·  {c('The First Call', BLUE)} &amp; {c('Memory', GREEN)}"
                 f"  ·  {c('115 XP available', GOLD)}", 15, DIM)
        left = VGroup(top, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        left.to_corner(UL, buff=0).shift(RIGHT * 0.2 + DOWN * 0.12)

        card_lines = VGroup(
            T("EQUIPPED MODEL", 11, DIM, bold=True),
            T("claude-haiku-5-5", 15, TEAL, font=MONO),
            mk(f"{c('$0.10', BLUE)} in  ·  {c('$0.50', GOLD)} out  per 1M tokens", 11, DIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        card = RoundedRectangle(corner_radius=0.12, width=card_lines.width + 0.4, height=card_lines.height + 0.2,
                                fill_color=PANEL, fill_opacity=1, stroke_color=TEAL, stroke_width=2.5)
        card_lines.move_to(card)
        card_g = VGroup(card, card_lines).to_corner(UR, buff=0).shift(LEFT * 0.2 + DOWN * 0.1)
        return VGroup(left, card_g)

    def footer(self):
        y = -5.36
        label = T("PROJECT 01", SMALL, GOLD, bold=True)
        cells = VGroup()
        for i in range(6):
            done = i < 2
            r = RoundedRectangle(corner_radius=0.06, width=0.48, height=0.32, stroke_color=GOLD if done else DIM,
                                 stroke_width=2, fill_color=GOLD, fill_opacity=1 if done else 0)
            t = T(f"S{i + 1}", SMALL, BG if done else DIM, bold=True).move_to(r)
            cells.add(VGroup(r, t))
        cells.arrange(RIGHT, buff=0.07)
        prog = VGroup(label, cells).arrange(RIGHT, buff=0.2)
        prog.move_to([0, y, 0]).align_to([-7.8, 0, 0], LEFT)

        star = c("★", GOLD)
        ach = mk(f"{b('UNLOCKED')}  {star} First Call  {star} Read the Response  {star} Priced a Call"
                 f"  {star} Beat the Boss  {star} Gave Claude Memory", 12)
        nxt = mk(f"{b(c('NEXT QUEST ▶', TEAL))}  Step 3: Streaming", 13)
        nxt.move_to([0, y, 0]).align_to([7.8, 0, 0], RIGHT)
        # center the achievements in the gap between progress and next quest
        gap_mid = (prog.get_right()[0] + nxt.get_left()[0]) / 2
        ach.move_to([gap_mid, y, 0])
        if ach.width > nxt.get_left()[0] - prog.get_right()[0] - 0.4:
            print("[fit] footer: achievements too wide")
        return VGroup(prog, ach, nxt)

    # ----- ① the call -----
    def panel_call(self):
        box, frame = panel(X[0], ROW1_TOP, W1, ROW1_H, BLUE, "①", "THE CALL", 10)

        chips = VGroup(chip("model", BLUE), chip("max_tokens", GOLD), chip("messages", GREEN)).arrange(RIGHT, buff=0.15)
        api = chip("POST /v1/messages", DIM, fill_op=0.06).next_to(chips, DOWN, buff=0.55)
        arrows = VGroup(*[
            arrow(ch.get_bottom(), api.get_top() + RIGHT * (ch.get_x() - api.get_x()) * 0.45) for ch in chips
        ])
        resp = chip("Message", TEAL, fill_op=0.28).next_to(api, DOWN, buff=0.45)
        resp_lbl = T("an SDK object, not a dict", SMALL, TEAL).next_to(resp, DOWN, buff=0.08)
        diagram = VGroup(chips, api, arrows, resp, resp_lbl, arrow(api.get_bottom(), resp.get_top()))

        mnem = para([
            f"{b('3 required M’s:')}",
            f"{c(b('M'), BLUE)}odel · {c(b('M'), GOLD)}ax_tokens · {c(b('M'), GREEN)}essages",
            f"One call = one HTTP request.",
            f"Every call starts from {b('zero')}: no memory.",
        ])
        code = code_block([
            (0, f"response = client.messages.{fn('create')}("),
            (4, f"model={nm('MODEL')},"),
            (4, f"max_tokens={nm('4000')},"),
            (4, "messages=messages,"),
            (0, ")"),
        ], size=11.5)
        content = VGroup(diagram, mnem, code).arrange(DOWN, buff=0.3)
        place(content, box, "call")
        return frame, content

    # ----- ② types -----
    def panel_types(self):
        box, frame = panel(X[1], ROW1_TOP, 2 * W1 + 0.2, ROW1_H, TEAL, "②", "TYPES: YOU SEND DICTS, YOU GET OBJECTS", 25)

        # left: what you send
        lh = VGroup(mk(f"{b('YOU SEND')}  ▶", 16), chip("dict", GREEN, fill_op=0.25),
                    T("plain Python", SMALL, DIM)).arrange(RIGHT, buff=0.15)
        lcode = code_block([
            (0, "messages = ["),
            (2, f"{{{st(chr(34) + 'role' + chr(34))}: {st(chr(34) + 'user' + chr(34))},"),
            (3, f"{st(chr(34) + 'content' + chr(34))}: {st(chr(34) + 'My name is Sam' + chr(34))}}},"),
            (2, f"{{{st(chr(34) + 'role' + chr(34))}: {st(chr(34) + 'assistant' + chr(34))},"),
            (3, f"{st(chr(34) + 'content' + chr(34))}: response.content}},"),
            (0, "]"),
        ], width=3.45)
        lnotes = para([
            f"You build these. Read with {b('brackets')}:",
            f"{m('msg[' + chr(34) + 'role' + chr(34) + ']', GREEN)}",
            f"{m('MessageParam', TEAL)} is only a type hint;",
            "at runtime it is a plain dict.",
        ], size=SMALL)
        left = VGroup(lh, lcode, lnotes).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        # right: what you get
        rh = VGroup(mk(f"◀  {b('YOU GET')}", 16), chip("Message", TEAL, fill_op=0.28),
                    T("pydantic object", SMALL, DIM)).arrange(RIGHT, buff=0.15)
        rcode = code_block([
            (0, f"response: {ty('Message')}"),
            (0, f"├─ .content: {ty('list[ContentBlock]')}"),
            (0, f"│  ├─ {c('ThinkingBlock', PURPLE)} .thinking"),
            (0, f"│  └─ {c('TextBlock', GREEN)} .text  {cm('← answer')}"),
            (0, f"├─ .stop_reason: {ty('str')}  {st(chr(34) + 'end_turn' + chr(34))}"),
            (0, f"└─ .usage: {ty('Usage')}"),
            (3, f"├─ .input_tokens: {ty('int')}"),
            (3, f"└─ .output_tokens: {ty('int')}"),
        ], width=3.75)
        rnotes = para([
            f"Read with {b('dots')}: {m('block.text', GREEN)}",
            f"{m('ContentBlock', TEAL)} is a union of block types:",
            f"check {m('block.type')} before reading {m('.text')}.",
        ], size=SMALL)
        right = VGroup(rh, rcode, rnotes).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        cols = VGroup(left, right).arrange(RIGHT, buff=0.3, aligned_edge=UP)

        ok, no = c("✓", GREEN), c("✗", RED)
        q = chr(34)
        rules = para([
            f"{ok} {m('block.text')}          {no} {m('block[' + q + 'text' + q + ']')}  → {c('TypeError: not subscriptable', RED)}",
            f"{ok} {m('json.dumps([b.model_dump() for b in response.content])')}  → JSON-safe dicts",
            f"{no} {m('json.dumps(response.content)')}  → {c('TypeError: not JSON serializable', RED)}",
            f"{ok} {m('{' + q + 'role' + q + ': ' + q + 'assistant' + q + ', ' + q + 'content' + q + ': response.content}')}"
            f"  → {cm('the SDK takes its objects back')}",
        ], size=SMALL, buff=0.1)
        rules_t = T("RULES OF THE GAME", SMALL, TEAL, bold=True)
        rules_g = VGroup(rules_t, rules).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rules_bg = RoundedRectangle(corner_radius=0.1, width=rules_g.width + 0.3, height=rules_g.height + 0.24,
                                    fill_color=TEAL, fill_opacity=0.07, stroke_color=TEAL, stroke_width=1.5)
        rules_g.move_to(rules_bg)
        content = VGroup(cols, VGroup(rules_bg, rules_g)).arrange(DOWN, buff=0.25)
        place(content, box, "types")
        return frame, content

    # ----- ③ tokens = money -----
    def panel_tokens(self):
        box, frame = panel(X[3], ROW1_TOP, W1, ROW1_H, GOLD, "③", "TOKENS = MONEY", 15)

        toks = VGroup(chip("un", BLUE, size=17), chip("believ", GOLD, size=17), chip("able", GREEN, size=17)).arrange(RIGHT, buff=0)
        brk_y = toks.get_bottom()[1] - 0.1
        brk = VGroup(
            Line([toks.get_left()[0], brk_y, 0], [toks.get_right()[0], brk_y, 0], color=DIM, stroke_width=2),
            Line([toks.get_left()[0], brk_y, 0], [toks.get_left()[0], brk_y + 0.08, 0], color=DIM, stroke_width=2),
            Line([toks.get_right()[0], brk_y, 0], [toks.get_right()[0], brk_y + 0.08, 0], color=DIM, stroke_width=2),
        )
        tok_lbl = T("1 word → 3 tokens", SMALL, DIM).next_to(brk, DOWN, buff=0.08)
        tok_g = VGroup(toks, brk, tok_lbl)

        facts = para([
            f"≈ ¾ word per token · billed {b('in')} and {b('out')}",
            f"8-word prompt → {c(b('22'), BLUE)} input tokens {c('(overhead)', DIM)}",
        ], size=SMALL)

        formula = para([
            f"{b('cost')} = {c('in', BLUE)} ÷ 1M × {c('in price', BLUE)}",
            f"        + {c('out', GOLD)} ÷ 1M × {c('out price', GOLD)}",
        ], size=BODY)
        f_bg = RoundedRectangle(corner_radius=0.1, width=formula.width + 0.3, height=formula.height + 0.22,
                                fill_color=GOLD, fill_opacity=0.08, stroke_color=GOLD, stroke_width=1.5)
        formula.move_to(f_bg)

        bar_full = 2.0
        opus_bar = Rectangle(width=bar_full, height=0.16, fill_color=RED, fill_opacity=1, stroke_width=0)
        haiku_bar = Rectangle(width=bar_full / 40, height=0.16, fill_color=GREEN, fill_opacity=1, stroke_width=0)
        price = VGroup(
            T("OUTPUT PRICE PER 1M", SMALL, DIM, bold=True),
            VGroup(T("Opus 5.5 ", SMALL, FG, font=MONO), opus_bar, T("$20.00", SMALL, RED)).arrange(RIGHT, buff=0.1),
            VGroup(T("Haiku 5.5", SMALL, FG, font=MONO), haiku_bar, T("$0.50  (40× less)", SMALL, GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        runs = para([
            b("SAME QUESTION, REAL RUNS"),
            f"{m('Opus ')}  142 out → {c(m('$0.002928'), RED)}",
            f"{m('Haiku')}   73 out → {c(m('$0.000039'), GREEN)}",
            f"{c(b('75× cheaper'), GOLD)}: price + Haiku skipped thinking",
            f"Output costs {b('5×')} input per token.",
        ], size=SMALL)

        content = VGroup(tok_g, facts, VGroup(f_bg, formula), price, runs).arrange(DOWN, buff=0.2)
        place(content, box, "tokens")
        return frame, content

    # ----- ④ boss: max_tokens -----
    def panel_boss(self):
        box, frame = panel(X[0], ROW2_TOP, W1, ROW2_H, RED, "④", "BOSS: max_tokens", 20)

        def seg(w, col, label, dashed=False, lab_col=None):
            r = Rectangle(width=w, height=0.34, stroke_width=0 if not dashed else 2, stroke_color=col,
                          fill_color=col, fill_opacity=0 if dashed else 1)
            if dashed:
                r = DashedVMobject(Rectangle(width=w, height=0.34, stroke_color=col, stroke_width=2), num_dashes=24)
            t = T(label, 11.5, lab_col or (BG if not dashed else col), bold=True).move_to(r)
            return VGroup(r, t)

        bar1 = VGroup(seg(0.75, PURPLE, "think"), seg(1.0, GREEN, "text"), seg(1.45, DIM, "unused = free", True)).arrange(RIGHT, buff=0)
        lab1 = mk(f"{m('max_tokens = 1000')}", SMALL)
        res1 = mk(f"{c('✓', GREEN)} {m('end_turn', GREEN)}", SMALL)
        g1 = VGroup(lab1, bar1, res1).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        think2 = seg(1.25, PURPLE, "thinking")
        wall = Line(UP * 0.28, DOWN * 0.28, color=RED, stroke_width=7)
        ghost = seg(0.95, GREEN, "text?", True)
        bar2 = VGroup(think2, wall, ghost).arrange(RIGHT, buff=0)
        cap = T("CAP", 11, RED, bold=True).next_to(wall, DOWN, buff=0.04)
        lab2 = mk(f"{m('max_tokens = 20')}", SMALL)
        res2 = mk(f"{c('✗', RED)} {m('max_tokens', RED)} · 0 words · still billed 20", SMALL)
        g2 = VGroup(lab2, VGroup(bar2, cap), res2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        lessons = para([
            f"{m('max_tokens')} caps thinking {b('+')} text together.",
            "A ceiling, not a target: unused is free.",
            f"{c(b('Strategy:'), RED)} set it high (4000) and",
            f"always check {m('stop_reason')}.",
        ], size=SMALL)
        content = VGroup(g1, g2, lessons).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        place(content, box, "boss", top_pad=0.5)
        return frame, content

    # ----- ⑤ stop_reason -----
    def panel_stop(self):
        box, frame = panel(X[1], ROW2_TOP, W1, ROW2_H, PURPLE, "⑤", "STATUS: stop_reason", 10)
        rows = [
            ("end_turn", GREEN, "finished normally → safe to use"),
            ("max_tokens", RED, "hit your cap → answer incomplete"),
            ("tool_use", GOLD, "wants YOU to run a tool (Project 06)"),
            ("refusal", DIM, "the model declined the request"),
            ("model_context_window_exceeded", PINK, "history too big for the model (step 5)"),
        ]
        items = VGroup(*[
            VGroup(chip(v, col, fill_op=0.22), T(d, SMALL, FG)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            for v, col, d in rows
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        rule = para([
            f"{c(b('Rule:'), PURPLE)} check it {b('before')} trusting {m('content')}.",
            f"Type: a plain {m('str', TEAL)} → compare with {m('==')}",
        ], size=SMALL)
        content = VGroup(items, rule).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        place(content, box, "stop", align_left=True)
        return frame, content

    # ----- ⑥ memory -----
    def panel_memory(self):
        box, frame = panel(X[2], ROW2_TOP, W1, ROW2_H, GREEN, "⑥", "MEMORY = A LIST", 20)

        rows = VGroup()
        tok_labels = ["28 in", "59 in", "", ""]
        for t in range(1, 5):
            lbl = T(f"turn {t}", SMALL, DIM)
            sq = VGroup(*[
                Square(0.17, fill_color=BLUE if i % 2 == 0 else GREEN, fill_opacity=1, stroke_width=0)
                for i in range(2 * t - 1)
            ]).arrange(RIGHT, buff=0.04)
            row = VGroup(lbl, sq).arrange(RIGHT, buff=0.15)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        stairs_extra = VGroup(*[
            T(tl, SMALL, GOLD, font=MONO).next_to(row, RIGHT, buff=0.15) for row, tl in zip(rows, tok_labels) if tl
        ])
        gx = rows.get_right()[0] + 0.22
        grow = Arrow([gx, rows[0].get_y(), 0], [gx, rows[3].get_y(), 0],
                     buff=0, color=GOLD, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        grow_lbl = para([c("input", GOLD), c("grows", GOLD)], size=SMALL, buff=0.03).next_to(grow, RIGHT, buff=0.08)
        legend = mk(f"{c('■', BLUE)} you   {c('■', GREEN)} Claude   (all re-sent)", SMALL)
        stairs = VGroup(rows, stairs_extra, grow, grow_lbl, legend)
        legend.next_to(rows, DOWN, buff=0.12).align_to(rows, LEFT)

        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=1.55, y_length=1.0, tips=False,
                  axis_config={"color": DIM, "include_ticks": False, "stroke_width": 2})
        lin = ax.plot(lambda x: x, color=GOLD, stroke_width=3)
        quad = ax.plot(lambda x: x * x / 10, color=RED, stroke_width=3)
        chart_lbls = para([
            c("per turn: linear", GOLD),
            c("session total: quadratic", RED),
            c("(x = turns)", DIM),
        ], size=SMALL, buff=0.05)
        chart = VGroup(VGroup(ax, lin, quad), chart_lbls).arrange(RIGHT, buff=0.15)

        notes = para([
            f"{b('1 run = 1 session = 1 list.')}",
            f"{m('quit')} → list gone. The API stores nothing.",
            f"Keep it: save {m('model_dump()')} output to JSON.",
        ], size=SMALL)
        content = VGroup(stairs, chart, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        place(content, box, "memory", align_left=True)
        return frame, content

    # ----- ⑦ trap cards -----
    def panel_traps(self):
        box, frame = panel(X[3], ROW2_TOP, W1, ROW2_H, YELLOW, "⑦", "TRAP CARDS", 15)
        q = chr(34)
        traps = [
            (f"{m('content[0]')} isn’t always text", "Opus thought first; Haiku skipped it."),
            (f"{m('output_tokens')} includes thinking", "You pay for words you never see."),
            (f"{m('temperature')} → 400 error", "Current models use effort (step 3)."),
            (f"{m(q + chr(92) + '$' + q)} in a Python string", f"SyntaxWarning. Just write {m('$')}."),
            ("Same prompt ≠ same output", "142 vs 168 tokens: measure many runs."),
        ]
        cards = VGroup()
        for head, sub in traps:
            txt = VGroup(mk(b(head), SMALL), mk(sub, SMALL, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
            card = VGroup(warn_icon(), txt).arrange(RIGHT, buff=0.15, aligned_edge=UP)
            cards.add(card)
        cards.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        place(cards, box, "traps", top_pad=0.55, align_left=True)
        return frame, cards
