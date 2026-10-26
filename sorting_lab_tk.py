"""
Sorting Lab (Tkinter edition) - Bubble, Merge and Quick sort, visualized.
Run:  python sorting_lab_tk.py
No extra packages needed - only Python's built-in tkinter.
"""
import random
import tkinter as tk
from tkinter import ttk

# ------------------------------------------------ colours / fonts
BG = "#F4F6FB"
CARD = "#FFFFFF"
HEADER = "#1F2A44"
ACCENT = "#4F8BF9"
BLUE, YELLOW, GREEN = "#4F8BF9", "#F9A825", "#2E9E5B"
TEXT = "#1F2A44"
MUTED = "#6B7690"
FONT = ("Segoe UI", 10)
FONT_B = ("Segoe UI", 10, "bold")
FONT_H = ("Segoe UI", 18, "bold")
MONO = ("Consolas", 10)


# ------------------------------------------------ sorting generators
# every step yields: (array copy, highlighted indexes, comparisons, swaps/writes)
def bubble(a):
    a, c, s = a[:], 0, 0
    yield a[:], (), c, s
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            c += 1
            yield a[:], (j, j + 1), c, s
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                s += 1
                swapped = True
                yield a[:], (j, j + 1), c, s
        if not swapped:
            break
    yield a[:], (), c, s


def merge_sort(a):
    a, st = a[:], [0, 0]  # [comparisons, writes]

    def ms(lo, hi):
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        yield from ms(lo, mid)
        yield from ms(mid, hi)
        left, right = a[lo:mid], a[mid:hi]
        i = j = 0
        k = lo
        while i < len(left) and j < len(right):
            st[0] += 1
            if left[i] <= right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            st[1] += 1
            yield a[:], (k,), st[0], st[1]
            k += 1
        for rest in (left[i:], right[j:]):
            for v in rest:
                a[k] = v
                st[1] += 1
                yield a[:], (k,), st[0], st[1]
                k += 1

    yield a[:], (), 0, 0
    yield from ms(0, len(a))
    yield a[:], (), st[0], st[1]


def quick_sort(a):
    a, st = a[:], [0, 0]

    def qs(lo, hi):
        if lo >= hi:
            return
        p, i = a[hi], lo
        for j in range(lo, hi):
            st[0] += 1
            yield a[:], (j, hi), st[0], st[1]
            if a[j] < p:
                a[i], a[j] = a[j], a[i]
                st[1] += 1
                i += 1
                yield a[:], (i - 1, j), st[0], st[1]
        a[i], a[hi] = a[hi], a[i]
        st[1] += 1
        yield a[:], (i,), st[0], st[1]
        yield from qs(lo, i - 1)
        yield from qs(i + 1, hi)

    yield a[:], (), 0, 0
    yield from qs(0, len(a) - 1)
    yield a[:], (), st[0], st[1]


SORTS = {"Bubble Sort": bubble, "Merge Sort": merge_sort, "Quick Sort": quick_sort}
ICON = {"Bubble Sort": "🫧", "Merge Sort": "🔀", "Quick Sort": "⚡"}

INFO = {  # best, average, worst, space, stable, idea
    "Bubble Sort": ("O(n)", "O(n²)", "O(n²)", "O(1)", "Yes",
                    "Repeatedly compare neighbours and swap them if they are in the wrong "
                    "order. The largest value 'bubbles' to the end in each pass. Stops early "
                    "if a pass makes no swap."),
    "Merge Sort": ("O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Yes",
                   "Divide the array into halves, sort each half recursively, then merge the "
                   "two sorted halves. Always fast, but needs extra memory."),
    "Quick Sort": ("O(n log n)", "O(n log n)", "O(n²)", "O(log n)", "No",
                   "Pick a pivot, move smaller values to its left and larger to its right, "
                   "then sort both sides recursively. Fastest in practice on average."),
}

CODE = {
"Bubble Sort": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:      # already sorted, stop early
            break
    return arr""",
"Merge Sort": """def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]""",
"Quick Sort": """def quick_sort(arr, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        pivot, i = arr[hi], lo
        for j in range(lo, hi):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        quick_sort(arr, lo, i - 1)
        quick_sort(arr, i + 1, hi)
    return arr""",
}

SPEEDS = {"Slow": 150, "Medium": 50, "Fast": 10}


# ------------------------------------------------ data helper
def make_data(mode, n, rng):
    if mode == "Random":
        return rng.sample(range(1, 100), n)
    if mode == "Nearly sorted":
        a = sorted(rng.sample(range(1, 100), n))
        for _ in range(max(1, n // 10)):
            i, j = rng.randrange(n), rng.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    if mode == "Reversed":
        return sorted(rng.sample(range(1, 100), n), reverse=True)
    return [rng.choice([10, 30, 50, 70, 90]) for _ in range(n)]  # Few unique


# ------------------------------------------------ one page per algorithm
class SortPage(tk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent, bg=BG)
        self.name = name
        self.frames = []
        self.idx = 0
        self.playing = False
        self.job = None

        best, avg, worst, space, _stable, idea = INFO[name]

        # title + explanation
        tk.Label(self, text=f"{ICON[name]}  {name}", font=FONT_H, bg=BG,
                 fg=TEXT).pack(anchor="w", padx=20, pady=(16, 2))
        tk.Label(self, text=idea, font=FONT, bg=BG, fg=MUTED, wraplength=760,
                 justify="left").pack(anchor="w", padx=20, pady=(0, 10))

        # complexity cards
        cards = tk.Frame(self, bg=BG)
        cards.pack(fill="x", padx=20)
        for i, (label, val) in enumerate([("Best case", best), ("Average", avg),
                                          ("Worst case", worst), ("Extra space", space)]):
            cards.columnconfigure(i, weight=1, uniform="c")
            card = tk.Frame(cards, bg=CARD, highlightbackground="#E1E6F0",
                            highlightthickness=1)
            card.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0))
            tk.Label(card, text=label, font=("Segoe UI", 9), bg=CARD,
                     fg=MUTED).pack(anchor="w", padx=12, pady=(8, 0))
            tk.Label(card, text=val, font=("Segoe UI", 13, "bold"), bg=CARD,
                     fg=ACCENT).pack(anchor="w", padx=12, pady=(0, 8))

        # input / output text
        self.input_lbl = tk.Label(self, bg=BG, fg=TEXT, font=FONT, anchor="w",
                                  justify="left", wraplength=760)
        self.input_lbl.pack(fill="x", padx=20, pady=(10, 0))

        # chart
        chart = tk.Frame(self, bg=CARD, highlightbackground="#E1E6F0",
                         highlightthickness=1)
        chart.pack(fill="both", expand=True, padx=20, pady=10)
        self.canvas = tk.Canvas(chart, bg=CARD, highlightthickness=0, height=240)
        self.canvas.pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas.bind("<Configure>", lambda e: self.draw())
        self.status = tk.Label(chart, bg=CARD, fg=MUTED, font=FONT, anchor="w")
        self.status.pack(fill="x", padx=12, pady=(0, 8))

        # controls
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=20)
        self.play_btn = ttk.Button(ctrl, text="▶  Play", style="Accent.TButton",
                                   command=self.toggle_play)
        self.play_btn.pack(side="left")
        ttk.Button(ctrl, text="↺  Reset", command=self.reset).pack(side="left", padx=6)
        ttk.Button(ctrl, text="◀", width=3, command=lambda: self.step(-1)).pack(side="left")
        ttk.Button(ctrl, text="▶", width=3, command=lambda: self.step(1)).pack(side="left", padx=(2, 12))
        tk.Label(ctrl, text="Speed", bg=BG, fg=MUTED, font=FONT).pack(side="left")
        self.speed = tk.StringVar(value="Medium")
        ttk.Combobox(ctrl, textvariable=self.speed, values=list(SPEEDS), width=8,
                     state="readonly").pack(side="left", padx=6)

        self.scale = tk.Scale(self, from_=0, to=1, orient="horizontal", showvalue=False,
                              bg=BG, troughcolor="#DDE3F0", highlightthickness=0,
                              activebackground=ACCENT, command=self.on_scale)
        self.scale.pack(fill="x", padx=20, pady=(8, 0))

        self.out_lbl = tk.Label(self, bg=BG, fg=TEXT, font=FONT, anchor="w",
                                justify="left", wraplength=760)
        self.out_lbl.pack(fill="x", padx=20, pady=(6, 0))

        # code
        code_box = tk.LabelFrame(self, text=" 📜 Python code ", bg=BG, fg=TEXT, font=FONT_B)
        code_box.pack(fill="x", padx=20, pady=12)
        txt = tk.Text(code_box, height=min(12, CODE[name].count("\n") + 1), font=MONO,
                      bg="#101828", fg="#E6EDF7", relief="flat", padx=10, pady=8)
        txt.insert("1.0", CODE[name])
        txt.config(state="disabled")
        txt.pack(fill="x", padx=6, pady=6)

    # ---- data
    def load(self, data):
        self.stop()
        self.frames = list(SORTS[self.name](data))
        self.idx = 0
        self.scale.config(to=len(self.frames) - 1)
        self.scale.set(0)
        self.input_lbl.config(text="Input:  " + ", ".join(map(str, data)))
        self.out_lbl.config(text="Sorted output:  " + ", ".join(map(str, self.frames[-1][0])))
        self.draw()

    # ---- drawing
    def draw(self):
        if not self.frames:
            return
        arr, hl, c, sw = self.frames[self.idx]
        done = self.idx == len(self.frames) - 1
        cv = self.canvas
        cv.delete("all")
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 20 or h < 20:
            return
        n = len(arr)
        top = max(arr) or 1
        slot = (w - 20) / n
        bar_w = slot * 0.78
        for i, v in enumerate(arr):
            x0 = 10 + i * slot + (slot - bar_w) / 2
            bar_h = (h - 36) * v / top
            colour = GREEN if done else YELLOW if i in hl else BLUE
            cv.create_rectangle(x0, h - 10 - bar_h, x0 + bar_w, h - 10, fill=colour, outline="")
            if n <= 20:
                cv.create_text(x0 + bar_w / 2, h - 16 - bar_h, text=str(v),
                               font=("Segoe UI", 8), fill=TEXT)
        msg = f"Step {self.idx}/{len(self.frames) - 1}   |   Comparisons: {c}   |   Swaps/Writes: {sw}   |   "
        msg += "✅ Sorted" if done else "Sorting..."
        if hl and not done:
            msg += "   |   Working on " + " and ".join(f"position {i} (value {arr[i]})" for i in hl)
        self.status.config(text=msg)

    # ---- controls
    def on_scale(self, value):
        self.idx = int(float(value))
        self.draw()

    def step(self, d):
        self.stop()
        self.scale.set(max(0, min(len(self.frames) - 1, self.idx + d)))

    def reset(self):
        self.stop()
        self.scale.set(0)

    def toggle_play(self):
        if self.playing:
            self.stop()
            return
        if self.idx >= len(self.frames) - 1:
            self.scale.set(0)
        self.playing = True
        self.play_btn.config(text="⏸  Pause")
        self.tick()

    def stop(self):
        self.playing = False
        if self.job:
            self.after_cancel(self.job)
            self.job = None
        self.play_btn.config(text="▶  Play")

    def tick(self):
        if not self.playing:
            return
        last = len(self.frames) - 1
        stride = max(1, len(self.frames) // 300)
        self.scale.set(min(last, self.idx + stride))
        if self.idx >= last:
            self.stop()
            return
        self.job = self.after(SPEEDS[self.speed.get()], self.tick)


# ------------------------------------------------ home page
class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="📊  Sorting Lab", font=FONT_H, bg=BG,
                 fg=TEXT).pack(anchor="w", padx=20, pady=(16, 2))
        tk.Label(self, text="Pick an algorithm tab above, press Play and watch it work. "
                            "Change the input numbers on the left any time - every tab updates.",
                 font=FONT, bg=BG, fg=MUTED, wraplength=760,
                 justify="left").pack(anchor="w", padx=20, pady=(0, 10))
        self.input_lbl = tk.Label(self, bg=BG, fg=TEXT, font=FONT, anchor="w",
                                  justify="left", wraplength=760)
        self.input_lbl.pack(fill="x", padx=20, pady=(0, 12))

        cols = ("Algorithm", "Best", "Average", "Worst", "Space", "Stable")
        tree = ttk.Treeview(self, columns=cols, show="headings", height=len(INFO))
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=110)
        tree.column("Algorithm", anchor="w", width=160)
        for k, v in INFO.items():
            tree.insert("", "end", values=(f"{ICON[k]} {k}", *v[:5]))
        tree.pack(fill="x", padx=20)

    def load(self, data):
        self.input_lbl.config(text="Current input:  " + ", ".join(map(str, data)))


# ------------------------------------------------ main app
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sorting Lab")
        self.geometry("1100x860")
        self.minsize(900, 700)
        self.configure(bg=BG)
        self.rng = random.Random(1)
        self.setup_style()

        header = tk.Frame(self, bg=HEADER)
        header.pack(fill="x")
        tk.Label(header, text="📊  Sorting Lab", font=("Segoe UI", 15, "bold"),
                 bg=HEADER, fg="white").pack(side="left", padx=20, pady=12)
        tk.Label(header, text="Learn sorting algorithms by watching them work",
                 font=FONT, bg=HEADER, fg="#AEB9D3").pack(side="left")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        self.build_sidebar(body)

        self.tabs = ttk.Notebook(body)
        self.tabs.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        self.home = HomePage(self.tabs)
        self.tabs.add(self.home, text="  🏠 Home  ")
        self.pages = {}
        for name in SORTS:
            page = SortPage(self.tabs, name)
            self.pages[name] = page
            self.tabs.add(page, text=f"  {ICON[name]} {name}  ")
        self.tabs.bind("<<NotebookTabChanged>>", lambda e: self.stop_all(except_current=True))

        self.generate()

    def setup_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TButton", font=FONT, padding=6)
        s.configure("Accent.TButton", font=FONT_B, background=ACCENT, foreground="white")
        s.map("Accent.TButton", background=[("active", "#3A74E0")])
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", font=FONT_B, padding=(10, 6))
        s.configure("Treeview", font=FONT, rowheight=30)
        s.configure("Treeview.Heading", font=FONT_B)

    def build_sidebar(self, parent):
        side = tk.Frame(parent, bg=CARD, width=250, highlightbackground="#E1E6F0",
                        highlightthickness=1)
        side.pack(side="left", fill="y", padx=10, pady=10)
        side.pack_propagate(False)

        tk.Label(side, text="Input numbers", font=("Segoe UI", 12, "bold"), bg=CARD,
                 fg=TEXT).pack(anchor="w", padx=14, pady=(14, 8))

        # generate
        tk.Label(side, text="Data type", bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", padx=14)
        self.mode = tk.StringVar(value="Random")
        cb = ttk.Combobox(side, textvariable=self.mode, state="readonly",
                          values=["Random", "Nearly sorted", "Reversed", "Few unique"])
        cb.pack(fill="x", padx=14, pady=(2, 10))
        cb.bind("<<ComboboxSelected>>", lambda e: self.generate())

        tk.Label(side, text="Number of elements", bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", padx=14)
        self.n = tk.IntVar(value=12)
        tk.Scale(side, from_=5, to=40, orient="horizontal", variable=self.n, bg=CARD,
                 highlightthickness=0, troughcolor="#DDE3F0", activebackground=ACCENT,
                 command=lambda v: self.generate(keep_seed=True)).pack(fill="x", padx=14)

        ttk.Button(side, text="🎲  New data", style="Accent.TButton",
                   command=lambda: self.generate()).pack(fill="x", padx=14, pady=(8, 14))

        ttk.Separator(side).pack(fill="x", padx=14)

        # custom
        tk.Label(side, text="Or type your own numbers", bg=CARD, fg=MUTED,
                 font=FONT).pack(anchor="w", padx=14, pady=(12, 0))
        self.entry = tk.Entry(side, font=FONT, relief="solid", bd=1)
        self.entry.insert(0, "42, 7, 19, 3, 88, 25, 61, 11")
        self.entry.pack(fill="x", padx=14, pady=(2, 6))
        self.entry.bind("<Return>", lambda e: self.use_custom())
        ttk.Button(side, text="Use these numbers", command=self.use_custom).pack(fill="x", padx=14)
        self.error = tk.Label(side, text="", bg=CARD, fg="#D93025", font=("Segoe UI", 9),
                              wraplength=220, justify="left")
        self.error.pack(anchor="w", padx=14, pady=6)

        # legend
        ttk.Separator(side).pack(fill="x", padx=14, pady=(6, 0))
        tk.Label(side, text="Colour guide", font=FONT_B, bg=CARD, fg=TEXT).pack(anchor="w", padx=14, pady=(10, 4))
        for colour, text in [(BLUE, "Waiting"), (YELLOW, "Being compared / moved"), (GREEN, "Sorted")]:
            row = tk.Frame(side, bg=CARD)
            row.pack(anchor="w", padx=14, pady=2)
            tk.Frame(row, bg=colour, width=14, height=14).pack(side="left")
            tk.Label(row, text=text, bg=CARD, fg=MUTED, font=FONT).pack(side="left", padx=8)

    # ---- data handling
    def generate(self, keep_seed=False):
        if not keep_seed:
            self.seed = self.rng.randrange(1_000_000)
        data = make_data(self.mode.get(), self.n.get(), random.Random(self.seed))
        self.error.config(text="")
        self.apply(data)

    def use_custom(self):
        try:
            data = [int(x) for x in self.entry.get().split(",") if x.strip()]
            if not 2 <= len(data) <= 40:
                raise ValueError
            if any(v < 0 for v in data):
                raise ValueError
        except ValueError:
            self.error.config(text="Enter 2 to 40 whole numbers (0 or more) separated by commas.")
            return
        self.error.config(text="")
        self.apply(data)

    def apply(self, data):
        self.data = data
        self.home.load(data)
        for page in self.pages.values():
            page.load(data)

    def stop_all(self, except_current=False):
        for page in self.pages.values():
            page.stop()


if __name__ == "__main__":
    App().mainloop()