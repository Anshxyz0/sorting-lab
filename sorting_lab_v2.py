"""
Sorting Lab - 5 sorting algorithms, visualized and compared.
Run:  python -m streamlit run sorting_lab.py
"""
import random
import time

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sorting Lab", page_icon="📊", layout="wide")
BLUE, YELLOW, GREEN = "#4F8BF9", "#F9A825", "#2E9E5B"


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


def selection(a):
    a, c, s = a[:], 0, 0
    yield a[:], (), c, s
    for i in range(len(a) - 1):
        m = i
        for j in range(i + 1, len(a)):
            c += 1
            yield a[:], (m, j), c, s
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            s += 1
            yield a[:], (i, m), c, s
    yield a[:], (), c, s


def insertion(a):
    a, c, s = a[:], 0, 0
    yield a[:], (), c, s
    for i in range(1, len(a)):
        j = i
        while j > 0:
            c += 1
            yield a[:], (j - 1, j), c, s
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                s += 1
                j -= 1
                yield a[:], (j, j + 1), c, s
            else:
                break
    yield a[:], (), c, s


def merge_sort(a):
    a, st_ = a[:], [0, 0]  # [comparisons, writes]

    def ms(lo, hi):
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        yield from ms(lo, mid)
        yield from ms(mid, hi)
        L, R = a[lo:mid], a[mid:hi]
        i = j = 0
        k = lo
        while i < len(L) and j < len(R):
            st_[0] += 1
            if L[i] <= R[j]:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            st_[1] += 1
            yield a[:], (k,), st_[0], st_[1]
            k += 1
        for rest in (L[i:], R[j:]):
            for v in rest:
                a[k] = v
                st_[1] += 1
                yield a[:], (k,), st_[0], st_[1]
                k += 1

    yield a[:], (), 0, 0
    yield from ms(0, len(a))
    yield a[:], (), st_[0], st_[1]


def quick_sort(a):
    a, st_ = a[:], [0, 0]

    def qs(lo, hi):
        if lo >= hi:
            return
        p, i = a[hi], lo
        for j in range(lo, hi):
            st_[0] += 1
            yield a[:], (j, hi), st_[0], st_[1]
            if a[j] < p:
                a[i], a[j] = a[j], a[i]
                st_[1] += 1
                i += 1
                yield a[:], (i - 1, j), st_[0], st_[1]
        a[i], a[hi] = a[hi], a[i]
        st_[1] += 1
        yield a[:], (i,), st_[0], st_[1]
        yield from qs(lo, i - 1)
        yield from qs(i + 1, hi)

    yield a[:], (), 0, 0
    yield from qs(0, len(a) - 1)
    yield a[:], (), st_[0], st_[1]


SORTS = {"Bubble Sort": bubble, "Selection Sort": selection,
         "Insertion Sort": insertion, "Merge Sort": merge_sort,
         "Quick Sort": quick_sort}

INFO = {  # best, average, worst, space, stable, idea
    "Bubble Sort": ("O(n)", "O(n²)", "O(n²)", "O(1)", "Yes",
                    "Repeatedly compare neighbours and swap them if they are in the wrong "
                    "order. The largest value 'bubbles' to the end in each pass. Stops early "
                    "if a pass makes no swap."),
    "Selection Sort": ("O(n²)", "O(n²)", "O(n²)", "O(1)", "No",
                       "Find the smallest value in the unsorted part and swap it to the "
                       "front. Very few swaps, but always many comparisons."),
    "Insertion Sort": ("O(n)", "O(n²)", "O(n²)", "O(1)", "Yes",
                       "Take the next element and insert it into its correct place in the "
                       "already-sorted left part. Excellent for nearly sorted data."),
    "Merge Sort": ("O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Yes",
                   "Divide the array into halves, sort each half recursively, then merge the "
                   "two sorted halves. Always fast, but needs extra memory."),
    "Quick Sort": ("O(n log n)", "O(n log n)", "O(n²)", "O(log n)", "No",
                   "Pick a pivot, move smaller values to its left and larger to its right, "
                   "then sort both sides recursively. Fastest in practice on average."),
}


# ------------------------------------------------ helpers
def make_data(mode, n, seed):
    r = random.Random(seed)
    if mode == "Random":
        return r.sample(range(1, 100), n)
    if mode == "Nearly sorted":
        a = sorted(r.sample(range(1, 100), n))
        for _ in range(max(1, n // 10)):
            i, j = r.randrange(n), r.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    if mode == "Reversed":
        return sorted(r.sample(range(1, 100), n), reverse=True)
    return [r.choice([10, 30, 50, 70, 90]) for _ in range(n)]  # Few unique


def draw(arr, hl, done):
    fig, ax = plt.subplots(figsize=(4.5, 2.8))
    colors = [GREEN if done else YELLOW if i in hl else BLUE for i in range(len(arr))]
    bars = ax.bar(range(len(arr)), arr, color=colors)
    if len(arr) <= 20:
        for b, v in zip(bars, arr):
            ax.text(b.get_x() + b.get_width() / 2, v + 1, str(v),
                    ha="center", fontsize=7)
    ax.axis("off")
    fig.tight_layout()
    return fig


# ------------------------------------------------ clean code shown to the student
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
"Selection Sort": """def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        m = i                        # index of the smallest value
        for j in range(i + 1, n):
            if arr[j] < arr[m]:
                m = j
        arr[i], arr[m] = arr[m], arr[i]
    return arr""",
"Insertion Sort": """def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]      # shift bigger values right
            j -= 1
        arr[j + 1] = key
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
ICON = {"Bubble Sort": "🫧", "Selection Sort": "🎯", "Insertion Sort": "🃏",
        "Merge Sort": "🔀", "Quick Sort": "⚡"}

# ------------------------------------------------ sidebar: page + input numbers
st.sidebar.title("📊 Sorting Lab")
if st.sidebar.button("🔄 Reset everything", use_container_width=True):
    st.session_state.clear()   # back to the starting state
    st.rerun()
pages = ["🏠 Home"] + [f"{ICON[k]} {k}" for k in SORTS] + ["📈 Compare All"]
page = st.sidebar.radio("Go to page", pages, key="page")

st.sidebar.divider()
st.sidebar.subheader("Input numbers")
source = st.sidebar.radio("Data source", ["Generate", "Type my own numbers"], key="source")
if source == "Generate":
    mode = st.sidebar.selectbox("Data type", ["Random", "Nearly sorted",
                                              "Reversed", "Few unique"], key="mode")
    n = st.sidebar.slider("Number of elements", 5, 40, 12, key="n")
    if "seed" not in st.session_state:
        st.session_state.seed = 1
    if st.sidebar.button("🎲 New data"):
        st.session_state.seed += 1
    data = make_data(mode, n, st.session_state.seed)
else:
    txt = st.sidebar.text_input("Numbers (comma separated)",
                                "42, 7, 19, 3, 88, 25, 61, 11", key="txt")
    try:
        data = [int(x) for x in txt.split(",") if x.strip()]
        assert 2 <= len(data) <= 40
    except Exception:
        st.sidebar.error("Enter 2 to 40 whole numbers separated by commas.")
        st.stop()


def play_controls(name, frames):
    """step slider + play button + animated chart for one algorithm"""
    step = st.slider("Step", 0, len(frames) - 1, 0, key=f"step_{name}")
    c1, c2, c3 = st.columns([1, 1, 2])
    play = c1.button("▶ Play", key=f"play_{name}")
    c2.button("↺ Reset", key=f"reset_{name}",
              help="Start this sorting again from step 0",
              on_click=lambda: st.session_state.__setitem__(f"step_{name}", 0))
    speed = c3.select_slider("Speed", ["Slow", "Medium", "Fast"], "Medium",
                             key=f"speed_{name}")
    holder = st.empty()

    def show(s):
        arr, hl, c, sw = frames[s]
        done = s == len(frames) - 1
        with holder.container():
            fig = draw(arr, hl, done)
            st.pyplot(fig)
            plt.close(fig)
            if hl and not done:
                st.caption("Working on positions " + " and ".join(
                    f"{i} (value {arr[i]})" for i in hl))
            st.caption(f"Comparisons: {c}  |  Swaps/Writes: {sw}  |  "
                       f"{'✅ Sorted' if done else 'Sorting...'}")

    if play:
        delay = {"Slow": 0.15, "Medium": 0.05, "Fast": 0.01}[speed]
        for s in range(0, len(frames), max(1, len(frames) // 120)):
            show(s)
            time.sleep(delay)
        show(len(frames) - 1)
    else:
        show(step)


# ------------------------------------------------ pages
if page == "🏠 Home":
    st.title("📊 Sorting Lab")
    st.write("Each sorting algorithm has its **own page**. Pick one from the sidebar. "
             "You can change the input numbers in the sidebar at any time - "
             "the change applies to every page.")
    st.write("**Current input:** " + ", ".join(map(str, data)))
    st.table(pd.DataFrame(
        {k: v[:5] for k, v in INFO.items()},
        index=["Best", "Average", "Worst", "Space", "Stable"]).T)

elif page == "📈 Compare All":
    st.title("📈 Compare All Algorithms")
    st.write("**Input:** " + ", ".join(map(str, data)))
    rows = []
    for k in SORTS:
        f = list(SORTS[k](data))
        rows.append({"Algorithm": k, "Comparisons": f[-1][2],
                     "Swaps/Writes": f[-1][3]})
    df = pd.DataFrame(rows).set_index("Algorithm")
    st.dataframe(df, use_container_width=True)
    st.subheader("Comparisons")
    st.bar_chart(df["Comparisons"])
    st.subheader("Swaps / Writes")
    st.bar_chart(df["Swaps/Writes"])
    st.success(f"Fewest comparisons on this data: {df['Comparisons'].idxmin()}")

else:
    name = page.split(" ", 1)[1]
    st.title(f"{ICON[name]} {name}")
    best, avg, worst, space, stable, idea = INFO[name]
    st.info(idea)
    m = st.columns(4)
    m[0].metric("Best case", best)
    m[1].metric("Average", avg)
    m[2].metric("Worst case", worst)
    m[3].metric("Extra space", space)
    st.write("**Input:** " + ", ".join(map(str, data)))
    frames = list(SORTS[name](data))
    play_controls(name, frames)
    st.write("**Sorted output:** " + ", ".join(map(str, frames[-1][0])))
    with st.expander("📜 Python code"):
        st.code(CODE[name], language="python")