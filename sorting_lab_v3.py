    "Bubble Sort": "🫧",
    "Merge Sort": "🔀",
    "Quick Sort": "⚡",
}

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
