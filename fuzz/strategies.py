from hypothesis import strategies as st

def get_chaotic_payload_strategy():
    """
    Returns a hypothesis strategy that generates structurally chaotic JSON payloads:
    empty strings, unicode edge cases, boundary integers, null values, and nested structures.
    """
    # A recursive strategy to build nested, chaotic JSON data
    json_strategy = st.recursive(
        st.one_of(
            st.none(),
            st.booleans(),
            st.integers(min_value=-999999, max_value=999999),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(alphabet=st.characters(blacklist_categories=('Cs',)), min_size=0, max_size=50)
        ),
        lambda children: st.one_of(
            st.lists(children, max_size=5),
            st.dictionaries(st.text(min_size=1, max_size=10), children, max_size=5)
        ),
        max_leaves=10  # <-- Changed from max_depth=3 to max_leaves=10
    )
    return json_strategy

def generate_fuzzed_payloads(count: int) -> list:
    """
    Draws 'count' number of randomized, chaotic payloads from our strategy.
    """
    strategy = get_chaotic_payload_strategy()
    return [strategy.example() for _ in range(count)]