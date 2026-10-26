import random
import time

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

ICON = {"Bubble Sort": "🫧", "Merge Sort": "🔀", "Quick Sort": "⚡"}


def make_data(mode, n, seed):
    rng = random.Random(seed)
    if mode == "Random":
        return [rng.randint(1, 99) for _ in range(n)]
    if mode == "Nearly sorted":
        values = sorted(rng.randint(1, 99) for _ in range(n))
        if n > 2:
            i, j = rng.sample(range(n), 2)
            values[i], values[j] = values[j], values[i]
        return values
    if mode == "Reversed":
        return sorted((rng.randint(1, 99) for _ in range(n)), reverse=True)
    if mode == "Few unique":
        return [rng.choice([10, 20, 30, 40, 50]) for _ in range(n)]
    return [rng.randint(1, 99) for _ in range(n)]


def bubble_sort(values):
    arr = list(values)
    frames = [(arr.copy(), [], 0, 0)]
    comparisons = swaps = 0
    for end in range(len(arr) - 1, 0, -1):
        swapped = False
        for i in range(end):
            comparisons += 1
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swaps += 1
                swapped = True
            frames.append((arr.copy(), [i, i + 1], comparisons, swaps))
        if not swapped:
            break
    frames.append((arr.copy(), [], comparisons, swaps))
    return frames


def merge_sort(values):
    arr = list(values)
    frames = [(arr.copy(), [], 0, 0)]
    comparisons = writes = 0

    def merge(left, right, lo):
        nonlocal comparisons, writes
        i = j = 0
        merged = []
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            writes += 1
        while i < len(left):
            merged.append(left[i])
            i += 1
            writes += 1
        while j < len(right):
            merged.append(right[j])
            j += 1
            writes += 1
        arr[lo:lo + len(merged)] = merged
        frames.append((arr.copy(), list(range(lo, lo + len(merged))), comparisons, writes))

    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        merge(arr[lo:mid], arr[mid:hi], lo)

    sort(0, len(arr))
    frames.append((arr.copy(), [], comparisons, writes))
    return frames


def quick_sort(values):
    arr = list(values)
    frames = [(arr.copy(), [], 0, 0)]
    comparisons = swaps = 0

    def partition(lo, hi):
        nonlocal comparisons, swaps
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            comparisons += 1
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps += 1
                frames.append((arr.copy(), [i, j, hi], comparisons, swaps))
        if i + 1 != hi:
            arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
            swaps += 1
        frames.append((arr.copy(), [i + 1, hi], comparisons, swaps))
        return i + 1

    def sort(lo, hi):
        if lo < hi:
            p = partition(lo, hi)
            sort(lo, p - 1)
            sort(p + 1, hi)

    sort(0, len(arr) - 1)
    frames.append((arr.copy(), [], comparisons, swaps))
    return frames


SORTS = {
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}

INFO = {
    "Bubble Sort": ("O(n)", "O(n²)", "O(n²)", "O(1)", "Yes",
                    "Bubble Sort compares neighboring values and swaps them when they are in the wrong order."),
    "Merge Sort": ("O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Yes",
                   "Merge Sort divides the list into smaller parts, sorts them, and merges the parts."),
    "Quick Sort": ("O(n log n)", "O(n log n)", "O(n²)", "O(log n) average", "Usually no",
                   "Quick Sort chooses a pivot and partitions values around it, then sorts each partition."),
}


def draw(values, highlighted=None, done=False):
    highlighted = set(highlighted or [])
    fig, ax = plt.subplots(figsize=(9, 3.5))
    bars = ax.bar(range(len(values)), values)
    for i, bar in enumerate(bars):
        if i in highlighted:
            bar.set_alpha(0.55)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title("Sorted!" if done else "Sorting in progress")
    ax.set_xticks(range(len(values)))
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    return fig


def play_controls(name, frames):
    step_key = f"step_{name}"
    step = st.slider("Step", 0, len(frames) - 1, 0, key=step_key)
    c1, c2, c3 = st.columns([1, 1, 2])
    play = c1.button("▶ Play", key=f"play_{name}")
    c2.button("↺ Reset", key=f"reset_{name}",
              help="Start this sorting again from step 0",
              on_click=lambda: st.session_state.__setitem__(step_key, 0))
    speed = c3.select_slider("Speed", ["Slow", "Medium", "Fast"],
                             value="Medium", key=f"speed_{name}")
    holder = st.empty()

    def show(s):
        arr, highlighted, comparisons, swaps_writes = frames[s]
        done = s == len(frames) - 1
        with holder.container():
            fig = draw(arr, highlighted, done)
            st.pyplot(fig)
            plt.close(fig)
            if highlighted and not done:
                valid = [i for i in highlighted if 0 <= i < len(arr)]
                st.caption("Working on positions " + " and ".join(
                    f"{i} (value {arr[i]})" for i in valid))
            st.caption(f"Comparisons: {comparisons} | Swaps/Writes: {swaps_writes} | "
                       f"{'✅ Sorted' if done else 'Sorting...'}")

    if play:
        delay = {"Slow": 0.15, "Medium": 0.05, "Fast": 0.01}[speed]
        stride = max(1, len(frames) // 120)
        for s in range(0, len(frames), stride):
            show(s)
            time.sleep(delay)
        show(len(frames) - 1)
    else:
        show(step)


# Sidebar: page and input numbers
st.sidebar.title("📊 Sorting Lab")
if st.sidebar.button("🔄 Reset everything", use_container_width=True):
    st.session_state.clear()
    st.rerun()

pages = ["🏠 Home"] + [f"{ICON[k]} {k}" for k in SORTS] + ["📈 Compare All"]
page = st.sidebar.radio("Go to page", pages, key="page")
st.sidebar.divider()
st.sidebar.subheader("Input numbers")
source = st.sidebar.radio("Data source", ["Generate", "Type my own numbers"], key="source")

if source == "Generate":
    mode = st.sidebar.selectbox("Data type",
                                ["Random", "Nearly sorted", "Reversed", "Few unique"],
                                key="mode")
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
        data = [int(x.strip()) for x in txt.split(",") if x.strip()]
        if not 2 <= len(data) <= 40:
            raise ValueError
    except ValueError:
        st.sidebar.error("Enter 2 to 40 whole numbers separated by commas.")
        st.stop()


# Pages
if page == "🏠 Home":
    st.title("📊 Sorting Lab")
    st.write("Each sorting algorithm has its **own page**. Pick one from the sidebar. "
             "You can change the input numbers in the sidebar at any time - "
             "the change applies to every page.")
    st.write("**Current input:** " + ", ".join(map(str, data)))
    st.table(pd.DataFrame({k: v[:5] for k, v in INFO.items()},
                          index=["Best", "Average", "Worst", "Space", "Stable"]).T)

elif page == "📈 Compare All":
    st.title("📈 Compare All Algorithms")
    st.write("**Input:** " + ", ".join(map(str, data)))
    rows = []
    for name, sort_function in SORTS.items():
        final_frame = sort_function(data)[-1]
        rows.append({"Algorithm": name, "Comparisons": final_frame[2],
                     "Swaps/Writes": final_frame[3]})
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
    metrics = st.columns(4)
    metrics[0].metric("Best case", best)
    metrics[1].metric("Average", avg)
    metrics[2].metric("Worst case", worst)
    metrics[3].metric("Space", space)
    st.write(f"**Stable:** {stable}")
    st.write("**Input:** " + ", ".join(map(str, data)))
    play_controls(name, SORTS[name](data))